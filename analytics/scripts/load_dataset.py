from pathlib import Path
import pandas as pd


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Dataset path
DATASET_PATH = PROJECT_ROOT / "cpp_engine" / "data" / "sensor_data.csv"


def load_dataset():
    """Load the Sentinel-Core simulation dataset."""
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH)

    return df


if __name__ == "__main__":
    df = load_dataset()

    print("Sentinel-Core Dataset")
    print("----------------------")
    print(f"Path  : {DATASET_PATH}")
    print(f"Shape : {df.shape}")

    print("\nColumns:")
    for column in df.columns:
        print(f" - {column}")

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nUnique Machines:")
    print(df["MachineID"].unique())

    print("\nMachine Distribution:")
    print(df["MachineID"].value_counts().sort_index())

    print("\nState Distribution:")
    print(df["State"].value_counts())

    print("\nFault Distribution:")
    print(df["FaultType"].value_counts())

    print("\nNumerical Summary:")
    print(
        df[
            [
                "Temperature",
                "Vibration",
                "Current",
                "Voltage",
                "RPM",
                "DegradationLevel",
            ]
        ].describe()
    )
    