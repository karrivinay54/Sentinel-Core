
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.io import loadmat
from scipy.stats import kurtosis, skew

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "datasets" / "paderborn" / "raw"
OUT = ROOT / "datasets" / "paderborn" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

# Folder names are used as the initial condition labels.
LABELS = {
    "K001": "HEALTHY",
    "K002": "HEALTHY",
    "K003": "HEALTHY",
    "KA04": "OUTER_RACE_FAULT",
    "KA05": "OUTER_RACE_FAULT",
    "KA06": "OUTER_RACE_FAULT",
    "KI04": "INNER_RACE_FAULT",
    "KI05": "INNER_RACE_FAULT",
    "KI07": "INNER_RACE_FAULT",
}

def extract_features(signal):
    signal = np.asarray(signal, dtype=np.float64).ravel()
    signal = signal[np.isfinite(signal)]

    if signal.size < 10:
        raise ValueError("Signal is too short or contains no usable samples.")

    abs_signal = np.abs(signal)
    rms = float(np.sqrt(np.mean(signal ** 2)))
    mean_abs = float(np.mean(abs_signal))
    peak = float(np.max(abs_signal))

    return {
        "sample_count": int(signal.size),
        "mean": float(np.mean(signal)),
        "std": float(np.std(signal)),
        "rms": rms,
        "peak_abs": peak,
        "peak_to_peak": float(np.ptp(signal)),
        "crest_factor": peak / rms if rms > 0 else 0.0,
        "mean_absolute": mean_abs,
        "skewness": float(skew(signal, bias=False)),
        "kurtosis": float(kurtosis(signal, fisher=True, bias=False)),
    }

def main():
    rows = []
    errors = []

    for bearing_folder, label in LABELS.items():
        search_root = RAW / bearing_folder
        files = sorted(search_root.rglob("*.mat"))

        print(f"{bearing_folder}: found {len(files)} MAT files")

        for path in files:
            try:
                mat = loadmat(
                    path,
                    squeeze_me=True,
                    struct_as_record=False
                )

                record = mat.get(path.stem)
                if record is None:
                    raise KeyError(
                        f"Expected MATLAB variable {path.stem!r} not found"
                    )
                vibration = None
                for channel in record.Y:
                    if getattr(channel, "Name", "") == "vibration_1":
                        vibration = np.asarray(channel.Data)
                        break

                if vibration is None:
                    raise KeyError("vibration_1 channel not found")

                features = extract_features(vibration)

                # Keep bearing identity separate for grouped evaluation.
                bearing_id = bearing_folder
                rows.append({
                    "file": path.name,
                    "bearing_id": bearing_id,
                    "condition": label,
                    "source_folder": bearing_folder,
                    **features,
                })

            except Exception as exc:
                errors.append({
                    "file": str(path),
                    "error": str(exc),
                })

    output = OUT / "paderborn_vibration_features.csv"
    pd.DataFrame(rows).to_csv(output, index=False)

    print("\n=== FEATURE EXTRACTION SUMMARY ===")
    print("Successful files:", len(rows))
    print("Failed files:", len(errors))
    print("Output:", output)

    if rows:
        result = pd.DataFrame(rows)
        print("\nRows per condition:")
        print(result["condition"].value_counts().to_string())

    if errors:
        error_path = OUT / "paderborn_extraction_errors.csv"
        pd.DataFrame(errors).to_csv(error_path, index=False)
        print("Errors saved to:", error_path)
        print(pd.DataFrame(errors).head(10).to_string(index=False))

if __name__ == "__main__":
    main()
