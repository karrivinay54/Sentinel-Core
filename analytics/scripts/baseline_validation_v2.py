from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "cpp_engine" / "data" / "sensor_data_v2.csv"


# --------------------------------------------------
# Configuration
# --------------------------------------------------

FEATURES = [
    "Temperature",
    "Vibration",
    "Current",
    "Voltage",
    "RPM"
]

TARGET = "FaultType"

TEST_SIZE = 0.20
MODEL_DEPTH = 4

RANDOM_SEEDS = range(1, 31)


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

df = pd.read_csv(DATASET_PATH)

X = df[FEATURES]
y = df[TARGET]


# --------------------------------------------------
# Repeated evaluation
# --------------------------------------------------

results = []

for seed in RANDOM_SEEDS:

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=seed,
        stratify=y
    )

    model = DecisionTreeClassifier(
        max_depth=MODEL_DEPTH,
        random_state=seed
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    results.append({
        "seed": seed,
        "accuracy": accuracy
    })


# --------------------------------------------------
# Results
# --------------------------------------------------

results_df = pd.DataFrame(results)

print("=" * 60)
print("SENTINEL-CORE REPEATED BASELINE VALIDATION")
print("=" * 60)

print(f"\nDataset samples: {len(df)}")
print(f"Test size: {TEST_SIZE:.0%}")
print(f"Decision tree max depth: {MODEL_DEPTH}")
print(f"Number of splits: {len(results_df)}")

print("\nAccuracy by split:")

for _, row in results_df.iterrows():
    print(
        f"  Seed {int(row['seed']):2d}: "
        f"{row['accuracy']:.4f}"
    )


# --------------------------------------------------
# Summary statistics
# --------------------------------------------------

mean_accuracy = results_df["accuracy"].mean()
std_accuracy = results_df["accuracy"].std()
min_accuracy = results_df["accuracy"].min()
max_accuracy = results_df["accuracy"].max()


print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print(f"\nMean accuracy:       {mean_accuracy:.4f}")
print(f"Standard deviation:  {std_accuracy:.4f}")
print(f"Minimum accuracy:    {min_accuracy:.4f}")
print(f"Maximum accuracy:    {max_accuracy:.4f}")


print("\nPercentage form:")

print(f"Mean:       {mean_accuracy * 100:.2f}%")
print(f"Std. dev.:  {std_accuracy * 100:.2f}%")
print(f"Minimum:    {min_accuracy * 100:.2f}%")
print(f"Maximum:    {max_accuracy * 100:.2f}%")


print("\n" + "=" * 60)
print("Repeated validation complete.")
print("=" * 60)