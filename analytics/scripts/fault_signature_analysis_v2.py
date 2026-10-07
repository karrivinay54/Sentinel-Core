from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "cpp_engine" / "data" / "sensor_data_v2.csv"


# Healthy operating points defined by the Digital Twin
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


def calculate_fault_signatures(df):
    """
    Calculate absolute and percentage deviation
    from the Digital Twin healthy baseline.
    """

    fault_means = (
        df[df["FaultType"] != "NONE"]
        .groupby("FaultType")[SENSOR_COLUMNS]
        .mean()
    )

    delta = fault_means.copy()

    for sensor in SENSOR_COLUMNS:
        delta[sensor] = (
            fault_means[sensor]
            - HEALTHY_BASELINE[sensor]
        )

    percentage_delta = delta.copy()

    for sensor in SENSOR_COLUMNS:
        percentage_delta[sensor] = (
            delta[sensor]
            / HEALTHY_BASELINE[sensor]
            * 100
        )
    # Compare fault conditions against the actual healthy
    # (NONE) observations present in the V2 dataset.
    healthy_means = (
        df[df["FaultType"] == "NONE"][SENSOR_COLUMNS]
        .mean()
    )

    dataset_delta = fault_means.subtract(healthy_means)

    dataset_percentage_delta = (
        dataset_delta
        .divide(healthy_means)
        * 100
    )

    return (
        fault_means,
        delta,
        percentage_delta,
        dataset_delta,
        dataset_percentage_delta,
    )


def main():

    df = load_dataset()

    print("Sentinel-Core Fault Signature Analysis")
    print("======================================")

    print("\nHealthy baseline:")
    for sensor, value in HEALTHY_BASELINE.items():
        print(f"{sensor:20s}: {value}")
    fault_means, delta, percentage_delta, dataset_delta, dataset_percentage_delta = (
        calculate_fault_signatures(df)
    )

    print("\nMean sensor values by fault:")
    print(
        fault_means.round(4).to_string()
    )

    print("\nAbsolute deviation from healthy baseline:")
    print(
        delta.round(4).to_string()
    )

    print("\nPercentage deviation from healthy baseline:")
    print(
        percentage_delta.round(2).to_string()
    )
    print("\nActual V2 healthy baseline (NONE):")
    healthy_means = (
        df[df["FaultType"] == "NONE"][SENSOR_COLUMNS]
        .mean()
    )
    print(
        healthy_means.round(4).to_string()
    )

    print("\nDeviation from actual V2 healthy baseline:")
    print(
        dataset_delta.round(4).to_string()
    )

    print("\nPercentage deviation from actual V2 healthy baseline:")
    print(
        dataset_percentage_delta.round(2).to_string()
    )


if __name__ == "__main__":
    main()