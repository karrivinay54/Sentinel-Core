from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "cpp_engine" / "data" / "sensor_data_v2.csv"

OUTPUT_DIR = PROJECT_ROOT / "analytics" / "plots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset():
    return pd.read_csv(DATASET_PATH)


def plot_sensor_vs_degradation(df):
    sensors = [
        "Temperature",
        "Vibration",
        "Current",
        "Voltage",
        "RPM",
    ]

    for sensor in sensors:
        plt.figure(figsize=(8, 5))

        for machine_id in sorted(df["MachineID"].unique()):
            machine_data = df[df["MachineID"] == machine_id]

            plt.plot(
                machine_data["DegradationLevel"],
                machine_data[sensor],
                marker="o",
                markersize=3,
                label=machine_id,
            )

        plt.xlabel("Degradation Level")
        plt.ylabel(sensor)
        plt.title(f"{sensor} vs Degradation Level")
        plt.legend()
        plt.grid(True)

        output_path = OUTPUT_DIR / f"{sensor.lower()}_vs_degradation_v2.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()


def plot_fault_means(df):
    sensors = [
        "Temperature",
        "Vibration",
        "Current",
        "Voltage",
        "RPM",
    ]

    fault_means = df.groupby("FaultType")[sensors].mean()

    for sensor in sensors:
        plt.figure(figsize=(8, 5))

        fault_means[sensor].plot(
            kind="bar"
        )

        plt.xlabel("Fault Type")
        plt.ylabel(sensor)
        plt.title(f"{sensor} by Fault Type")
        plt.xticks(rotation=30)
        plt.grid(axis="y")

        output_path = OUTPUT_DIR / f"{sensor.lower()}_by_fault_v2.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()


def main():
    df = load_dataset()

    print("Generating Sentinel-Core visualizations...")

    plot_sensor_vs_degradation(df)
    plot_fault_means(df)

    print(f"Plots saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()