
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import StratifiedShuffleSplit


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT
    / "cpp_engine"
    / "data"
    / "sensor_data_v5.csv"
)

MODEL_DIR = PROJECT_ROOT / "analytics" / "models"
MODEL_PATH = MODEL_DIR / "sentinel_fault_classifier_v5.pkl"


# --------------------------------------------------
# Configuration
# --------------------------------------------------

FEATURES = [
    "Temperature",
    "Vibration",
    "Current",
    "Voltage",
    "RPM",
]

TARGET = "FaultType"
GROUP = "MachineID"

FAULT_CLASSES = [
    "BEARING_WEAR",
    "COOLING_FAILURE",
    "MISALIGNMENT",
    "NONE",
    "OVERLOAD",
]


def main():
    # Load and validate dataset
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH)

    required = FEATURES + [TARGET, GROUP]
    missing = [column for column in required if column not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    if df[required].isnull().any().any():
        raise ValueError("Required columns contain missing values.")

    if set(df[TARGET].unique()) != set(FAULT_CLASSES):
        raise ValueError("Unexpected fault classes in dataset.")

    # Verify that each machine has one fault label
    machine_table = df[[GROUP, TARGET]].drop_duplicates()

    if machine_table[GROUP].duplicated().any():
        raise ValueError(
            "A machine has multiple fault labels."
        )

    class_counts = machine_table[TARGET].value_counts()

    if any(class_counts.get(c, 0) < 2 for c in FAULT_CLASSES):
        raise ValueError(
            "Each class needs at least two machines."
        )

    # Stratify MACHINE IDs, not individual readings
    splitter = StratifiedShuffleSplit(
        n_splits=1,
        test_size=0.20,
        random_state=42,
    )

    train_idx, test_idx = next(
        splitter.split(machine_table[GROUP], machine_table[TARGET])
    )

    train_machines = set(
        machine_table.iloc[train_idx][GROUP]
    )
    test_machines = set(
        machine_table.iloc[test_idx][GROUP]
    )

    assert train_machines.isdisjoint(test_machines)

    train_df = df[df[GROUP].isin(train_machines)].copy()
    test_df = df[df[GROUP].isin(test_machines)].copy()

    if set(train_df[TARGET]) != set(FAULT_CLASSES):
        raise ValueError("Training split is missing a fault class.")

    if set(test_df[TARGET]) != set(FAULT_CLASSES):
        raise ValueError("Testing split is missing a fault class.")

    X_train = train_df[FEATURES]
    y_train = train_df[TARGET]

    X_test = test_df[FEATURES]
    y_test = test_df[TARGET]

    print("=" * 60)
    print("SENTINEL-CORE V5 TRAINING")
    print("=" * 60)
    print(f"Dataset: {DATASET_PATH.name}")
    print(f"Total readings: {len(df)}")
    print(f"Total machines: {df[GROUP].nunique()}")
    print(f"Training readings: {len(train_df)}")
    print(f"Testing readings: {len(test_df)}")
    print(f"Training machines: {len(train_machines)}")
    print(f"Testing machines: {len(test_machines)}")
    print("Machine overlap: 0")

    print("\nTraining machines per class:")
    print(
        machine_table[
            machine_table[GROUP].isin(train_machines)
        ][TARGET].value_counts().sort_index().to_string()
    )

    print("\nTesting machines per class:")
    print(
        machine_table[
            machine_table[GROUP].isin(test_machines)
        ][TARGET].value_counts().sort_index().to_string()
    )

    # Train model
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    # Evaluate on held-out machines
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print("\n=== HELD-OUT MACHINE EVALUATION ===")
    print(f"Accuracy: {accuracy * 100:.2f}%")

    print("\n=== CLASSIFICATION REPORT ===")
    print(
        classification_report(
            y_test,
            predictions,
            labels=FAULT_CLASSES,
            zero_division=0,
        )
    )

    # Save V5 model separately
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    model_package = {
        "model": model,
        "features": FEATURES,
        "target": TARGET,
        "dataset": DATASET_PATH.name,
        "dataset_records": len(df),
        "machine_count": int(df[GROUP].nunique()),
        "evaluation_method": (
            "StratifiedShuffleSplit on machine IDs"
        ),
        "random_state": 42,
        "test_accuracy": float(accuracy),
        "train_machines": sorted(train_machines),
        "test_machines": sorted(test_machines),
        "fault_classes": FAULT_CLASSES,
    }

    joblib.dump(model_package, MODEL_PATH)

    print("\n=== V5 MODEL SAVED ===")
    print(f"Path: {MODEL_PATH}")


if __name__ == "__main__":
    main()
