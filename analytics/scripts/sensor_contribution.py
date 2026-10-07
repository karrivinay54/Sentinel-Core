from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "cpp_engine" / "data" / "sensor_data_v2.csv"

OUTPUT_DIR = PROJECT_ROOT / "analytics" / "plots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


HEALTHY_BASELINE = {
    "Temperature": 36.8,
    "Vibration": 0.32,
    "Current": 3.05,
    "Voltage": 229.6,
    "RPM": 1498,
}

SENSOR_COLUMNS = list(HEALTHY_BASELINE.keys())


def load_dataset():
    return pd.read_csv(DATASET_PATH)


def calculate_percentage_deviation(df):
    fault_means = (
        df[df["FaultType"] != "NONE"]
        .groupby("FaultType")[SENSOR_COLUMNS]
        .mean()
    )

    deviation = fault_means.copy()

    for sensor in SENSOR_COLUMNS:
        deviation[sensor] = (
            (
                fault_means[sensor]
                - HEALTHY_BASELINE[sensor]
            )
            / HEALTHY_BASELINE[sensor]
            * 100
        )

    return deviation


def main():

    df = load_dataset()

    deviation = calculate_percentage_deviation(df)

    # Absolute magnitude of deviation
    contribution = deviation.abs()

    print("Sentinel-Core Sensor Contribution Analysis")
    print("===========================================")

    print("\nAbsolute percentage deviation:")
    print(contribution.round(2).to_string())

    print("\nDominant sensor by fault:")

    for fault in contribution.index:
        dominant_sensor = contribution.loc[fault].idxmax()
        dominant_value = contribution.loc[fault].max()

        print(
            f"{fault:20s} -> "
            f"{dominant_sensor} "
            f"({dominant_value:.2f}%)"
        )

    # Plot
    ax = contribution.plot(
        kind="bar",
        figsize=(10, 6)
    )

    ax.set_title(
        "Sensor Contribution by Fault Type"
    )
    ax.set_xlabel("Fault Type")
    ax.set_ylabel(
        "Absolute Percentage Deviation (%)"
    )

    plt.xticks(rotation=30)
    plt.grid(axis="y")
    plt.tight_layout()

    output_path = (
        OUTPUT_DIR / "sensor_contribution_by_fault_v2.png"
    )

    plt.savefig(output_path, dpi=150)
    plt.close()

    print(
        f"\nPlot saved to: {output_path}"
    )


if __name__ == "__main__":
    main()