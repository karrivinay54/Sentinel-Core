from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "cpp_engine" / "data" / "sensor_data.csv"


def load_dataset():
    return pd.read_csv(DATASET_PATH)


def main():
    df = load_dataset()

    sensor_columns = [
        "Temperature",
        "Vibration",
        "Current",
        "Voltage",
        "RPM",
    ]

    print("Sentinel-Core Fault Analysis")
    print("============================")

    print("\nMean sensor values by fault:")
    print(
        df.groupby("FaultType")[sensor_columns]
        .mean()
        .round(4)
    )

    print("\nMean sensor values by machine:")
    print(
        df.groupby("MachineID")[sensor_columns]
        .mean()
        .round(4)
    )

    print("\nMean sensor values by state:")
    print(
        df.groupby("State")[sensor_columns]
        .mean()
        .round(4)
    )


if __name__ == "__main__":
    main()