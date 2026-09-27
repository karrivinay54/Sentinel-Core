from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "cpp_engine" / "data" / "sensor_data.csv"

OUTPUT_DIR = PROJECT_ROOT / "analytics" / "plots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


SENSOR_COLUMNS = [
    "Temperature",
    "Vibration",
    "Current",
    "Voltage",
    "RPM",
]


def load_dataset():
    return pd.read_csv(DATASET_PATH)


def main():
    df = load_dataset()

    print("Sentinel-Core Correlation Analysis")
    print("==================================")

    # Correlation of sensors with degradation
    degradation_corr = (
        df[SENSOR_COLUMNS + ["DegradationLevel"]]
        .corr()["DegradationLevel"]
        .drop("DegradationLevel")
        .sort_values(
            key=lambda values: values.abs(),
            ascending=False
        )
    )

    print("\nSensor correlation with DegradationLevel:")
    print(degradation_corr.round(4).to_string())

    # Full sensor correlation matrix
    correlation_matrix = df[
        SENSOR_COLUMNS
    ].corr()

    print("\nSensor correlation matrix:")
    print(correlation_matrix.round(4).to_string())

    # Save correlation matrix
    correlation_matrix.to_csv(
        OUTPUT_DIR / "sensor_correlation_matrix.csv"
    )

    # Plot sensor vs degradation correlation
    plt.figure(figsize=(8, 5))

    degradation_corr.sort_values().plot(
        kind="barh"
    )

    plt.xlabel("Pearson Correlation")
    plt.ylabel("Sensor")
    plt.title(
        "Sensor Correlation with Degradation Level"
    )
    plt.grid(axis="x")

    plt.tight_layout()

    output_path = (
        OUTPUT_DIR
        / "sensor_degradation_correlation.png"
    )

    plt.savefig(output_path, dpi=150)
    plt.close()

    print(
        f"\nCorrelation plot saved to: {output_path}"
    )

    print(
        f"Correlation matrix saved to: "
        f"{OUTPUT_DIR / 'sensor_correlation_matrix.csv'}"
    )


if __name__ == "__main__":
    main()