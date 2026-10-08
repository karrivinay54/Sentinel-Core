from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT
    / "cpp_engine"
    / "data"
    / "sensor_data_v2.csv"
)

MODEL_DIR = PROJECT_ROOT / "analytics" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "sentinel_fault_classifier.pkl"


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


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

df = pd.read_csv(DATASET_PATH)

X = df[FEATURES]
y = df[TARGET]


# --------------------------------------------------
# Train / test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=42,
)


# --------------------------------------------------
# Train Random Forest
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    random_state=42,
)

model.fit(X_train, y_train)


# --------------------------------------------------
# Evaluate model
# --------------------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("=== SENTINEL-CORE FAULT CLASSIFIER ===")
print(f"Dataset size:      {len(df)}")
print(f"Training samples:  {len(X_train)}")
print(f"Testing samples:   {len(X_test)}")
print()
print(f"Accuracy: {accuracy * 100:.2f}%")
print()
print("=== CLASSIFICATION REPORT ===")
print(classification_report(y_test, predictions))


# --------------------------------------------------
# Save model
# --------------------------------------------------

model_package = {
    "model": model,
    "features": FEATURES,
    "target": TARGET,
}

joblib.dump(model_package, MODEL_PATH)

print("=== MODEL SAVED ===")
print(f"Path: {MODEL_PATH}")