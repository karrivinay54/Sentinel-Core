
from pathlib import Path
import math

import joblib
import pandas as pd


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    PROJECT_ROOT
    / "analytics"
    / "models"
    / "sentinel_fault_classifier.pkl"
)


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

model_package = joblib.load(MODEL_PATH)

model = model_package["model"]
FEATURES = model_package["features"]
TARGET = model_package["target"]


# --------------------------------------------------
# Fault prediction function
# --------------------------------------------------

def predict_fault(sensor_readings):
    """
    Predict a machine fault from five sensor readings.

    Parameters:
        sensor_readings (dict): Dictionary containing the
        five sensor features expected by the trained model.

    Returns:
        dict: Predicted fault, confidence, and class probabilities.
    """

    # Validate required features
    missing_features = [
        feature
        for feature in FEATURES
        if feature not in sensor_readings
    ]

    if missing_features:
        raise ValueError(
            f"Missing sensor features: {missing_features}"
        )

    # Validate numeric and finite sensor values
    validated_readings = {}

    for feature in FEATURES:
        value = sensor_readings[feature]

        if isinstance(value, bool):
            raise ValueError(
                f"{feature} must be a finite numeric value."
            )

        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError(
                f"{feature} must be a finite numeric value."
            ) from None

        if not math.isfinite(value):
            raise ValueError(
                f"{feature} must be a finite numeric value."
            )

        validated_readings[feature] = value

    # Arrange values in the exact training feature order
    input_data = pd.DataFrame(
        [[validated_readings[feature] for feature in FEATURES]],
        columns=FEATURES,
    )

    # Predict the fault
    predicted_fault = model.predict(input_data)[0]

    # Calculate class probability estimates
    probabilities = model.predict_proba(input_data)[0]

    fault_probabilities = {
        fault: float(probability)
        for fault, probability in zip(
            model.classes_,
            probabilities,
        )
    }

    # Return structured results
    return {
        "predicted_fault": str(predicted_fault),
        "confidence": fault_probabilities[predicted_fault],
        "probabilities": fault_probabilities,
    }


# --------------------------------------------------
# Test the prediction interface
# --------------------------------------------------

if __name__ == "__main__":

    print("=== SENTINEL-CORE PREDICTION INTERFACE ===")
    print("Model loaded successfully.")
    print(f"Model path: {MODEL_PATH}")
    print(f"Expected features: {FEATURES}")
    print(f"Target column: {TARGET}")
    print(f"Supported faults: {list(model.classes_)}")

    test_reading = {
        "Temperature": 38.2,
        "Vibration": 0.48,
        "Current": 3.25,
        "Voltage": 228.7,
        "RPM": 1480,
    }

    result = predict_fault(test_reading)

    print("\n=== PREDICTION RESULT ===")
    print(f"Predicted fault: {result['predicted_fault']}")
    print(f"Confidence: {result['confidence']:.2%}")

    print("\n=== CLASS PROBABILITIES ===")

    for fault, probability in result["probabilities"].items():
        print(f"{fault:<20} {probability:.2%}")
