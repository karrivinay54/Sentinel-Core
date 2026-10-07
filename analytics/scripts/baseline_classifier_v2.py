from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


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


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

df = pd.read_csv(DATASET_PATH)

print("=" * 60)
print("SENTINEL-CORE BASELINE CLASSIFIER")
print("=" * 60)

print(f"\nDataset: {DATASET_PATH}")
print(f"Dataset shape: {df.shape}")


# --------------------------------------------------
# Select features and target
# --------------------------------------------------

X = df[FEATURES]
y = df[TARGET]

print("\nFeatures:")
for feature in FEATURES:
    print(f"  - {feature}")

print(f"\nTarget:")
print(f"  - {TARGET}")


# --------------------------------------------------
# Class distribution
# --------------------------------------------------

print("\nClass distribution:")
print(y.value_counts())


# --------------------------------------------------
# Train/test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTrain/test split:")
print(f"  Training samples: {len(X_train)}")
print(f"  Testing samples:  {len(X_test)}")


# --------------------------------------------------
# Train baseline model
# --------------------------------------------------

model = DecisionTreeClassifier(
    max_depth=4,
    random_state=42
)

model.fit(X_train, y_train)


# --------------------------------------------------
# Predictions
# --------------------------------------------------

y_pred = model.predict(X_test)


# --------------------------------------------------
# Evaluation
# --------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 60)
print("RESULTS")
print("=" * 60)

print(f"\nAccuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)

print("Confusion Matrix:")

labels = sorted(y.unique())

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)

print("\nLabels:")
print(labels)

print("\nMatrix:")
print(cm)


# --------------------------------------------------
# Feature importance
# --------------------------------------------------

print("\nFeature importance:")

importance = pd.Series(
    model.feature_importances_,
    index=FEATURES
).sort_values(ascending=False)

for feature, value in importance.items():
    print(f"  {feature:<15} {value:.4f}")


print("\n" + "=" * 60)
print("Baseline classification complete.")
print("=" * 60)