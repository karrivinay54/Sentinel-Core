from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "cpp_engine" / "data" / "sensor_data.csv"


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

    print("Sentinel-Core Within-Machine Correlation Analysis")
    print("=================================================")

    for machine_id in sorted(df["MachineID"].unique()):

        machine_data = df[
            df["MachineID"] == machine_id
        ]

        fault_type = machine_data["FaultType"].unique()

        print("\n----------------------------------------")
        print(f"Machine   : {machine_id}")
        print(f"Fault     : {fault_type}")
        print(f"Records   : {len(machine_data)}")
        print("----------------------------------------")

        correlation = (
            machine_data[
                SENSOR_COLUMNS + ["DegradationLevel"]
            ]
            .corr()["DegradationLevel"]
            .drop("DegradationLevel")
            .sort_values(
                key=lambda values: values.abs(),
                ascending=False
            )
        )

        print(
            correlation.round(4).to_string()
        )


if __name__ == "__main__":
    main()