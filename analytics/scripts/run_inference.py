
import argparse
from pathlib import Path
import sys

import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_INPUT_PATH = (
    PROJECT_ROOT / "cpp_engine" / "data" / "integration_test.csv"
)

DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "analytics"
    / "reports"
    / "integration_test_predictions.csv"
)

# Import the existing V5 prediction interface
sys.path.insert(0, str(Path(__file__).resolve().parent))
from predict_fault import predict_fault


def main():
    parser = argparse.ArgumentParser(
        description="Sentinel-Core batch fault inference"
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_PATH
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH
    )

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    print("=== SENTINEL-CORE BATCH INFERENCE ===")

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input dataset not found: {input_path}"
        )

    data = pd.read_csv(input_path)

    required_columns = [
        "Timestamp",
        "MachineID",
        "Temperature",
        "Vibration",
        "Current",
        "Voltage",
        "RPM",
        "DegradationLevel",
        "State",
        "FaultType",
    ]

    missing = [col for col in required_columns if col not in data.columns]
    if missing:
        raise ValueError(f"Missing CSV columns: {missing}")

    results = []

    for _, row in data.iterrows():
        readings = {
            "Temperature": row["Temperature"],
            "Vibration": row["Vibration"],
            "Current": row["Current"],
            "Voltage": row["Voltage"],
            "RPM": row["RPM"],
        }

        prediction = predict_fault(readings)

        results.append({
            "PredictedFault": prediction["predicted_fault"],
            "Confidence": prediction["confidence"],
            **{
                f"Prob_{fault}": probability
                for fault, probability
                in prediction["probabilities"].items()
            }
        })

    predictions = pd.DataFrame(results)

    output = pd.concat(
        [data.reset_index(drop=True), predictions],
        axis=1
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_path, index=False)

    print(f"Input records: {len(data)}")
    print(f"Output records: {len(output)}")
    print(f"Output saved: {output_path}")

    print("\nPredicted fault distribution:")
    print(output["PredictedFault"].value_counts())

    print("\nAverage model confidence:")
    print(f"{output['Confidence'].mean():.2%}")

    print("\nBatch inference completed successfully.")


if __name__ == "__main__":
    main()
