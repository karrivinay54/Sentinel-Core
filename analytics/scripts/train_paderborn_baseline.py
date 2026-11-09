from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import LeaveOneGroupOut
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "datasets" / "paderborn" / "processed" / "paderborn_vibration_features.csv"
MODEL_DIR = ROOT / "analytics" / "models" / "real_data"
REPORT_DIR = ROOT / "analytics" / "reports" / "real_data"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)
FEATURES = [
    "std",
    "rms",
    "peak_abs",
    "peak_to_peak",
    "crest_factor",
    "mean_absolute",
    "skewness",
    "kurtosis",
]
LABELS = ["HEALTHY", "INNER_RACE_FAULT", "OUTER_RACE_FAULT"]
def make_model():
    return RandomForestClassifier(
        n_estimators=300,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
def main():
    df = pd.read_csv(DATA)
    required = FEATURES + ["condition", "bearing_id", "file"]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required CSV columns: {missing}")
    if df[required].isna().any().any():
        raise ValueError("Missing values found in required columns.")
    X = df[FEATURES].astype(float)
    y = df["condition"].astype(str)
    groups = df["bearing_id"].astype(str)
    if set(y.unique()) != set(LABELS):
        raise ValueError(f"Unexpected labels: {sorted(y.unique())}")
    if groups.nunique() < 3:
        raise ValueError("Too few distinct bearings for grouped evaluation.")
    print("Dataset shape:", df.shape)
    print("Features:", FEATURES)
    print("Bearings:", sorted(groups.unique()))
    print("\nStarting leave-one-bearing-out evaluation...")
    cv = LeaveOneGroupOut()
    predictions = np.empty(len(df), dtype=object)
    fold_rows = []
    for fold, (train_idx, test_idx) in enumerate(
        cv.split(X, y, groups=groups), start=1
    ):
        model = make_model()
        model.fit(X.iloc[train_idx], y.iloc[train_idx])
        predicted = model.predict(X.iloc[test_idx])
        predictions[test_idx] = predicted
        held_out = sorted(groups.iloc[test_idx].unique())
        fold_accuracy = accuracy_score(y.iloc[test_idx], predicted)
        fold_rows.append({
            "fold": fold,
            "held_out_bearing": ",".join(held_out),
            "test_recordings": len(test_idx),
            "accuracy": fold_accuracy,
        })
        print(
            f"Fold {fold}/{groups.nunique()} | "
            f"Held out: {held_out} | "
            f"Accuracy: {fold_accuracy:.4f}"
        )
    overall_accuracy = accuracy_score(y, predictions)
    report = classification_report(
        y,
        predictions,
        labels=LABELS,
        target_names=LABELS,
        digits=4,
        zero_division=0,
    )
    matrix = confusion_matrix(y, predictions, labels=LABELS)
    print("\n=== BEARING-GROUPED EVALUATION ===")
    print(f"Overall out-of-fold accuracy: {overall_accuracy:.4f}")
    print("\nClassification report:")
    print(report)
    print("Confusion matrix (rows=true, columns=predicted):")
    print(pd.DataFrame(
        matrix,
        index=LABELS,
        columns=LABELS,
    ).to_string())
    pd.DataFrame(fold_rows).to_csv(
        REPORT_DIR / "paderborn_lobo_fold_metrics.csv",
        index=False,
    )
    prediction_df = df[["file", "bearing_id", "condition"]].copy()
    prediction_df["predicted_condition"] = predictions
    prediction_df["correct"] = (
        prediction_df["condition"] == prediction_df["predicted_condition"]
    )
    prediction_df.to_csv(
        REPORT_DIR / "paderborn_lobo_predictions.csv",
        index=False,
    )
    metrics = {
        "dataset": "Paderborn Bearing DataCenter",
        "evaluation": "LeaveOneGroupOut by bearing_id",
        "recordings": int(len(df)),
        "distinct_bearings": int(groups.nunique()),
        "features": FEATURES,
        "labels": LABELS,
        "overall_out_of_fold_accuracy": float(overall_accuracy),
        "classification_report": classification_report(
            y,
            predictions,
            labels=LABELS,
            target_names=LABELS,
            output_dict=True,
            zero_division=0,
        ),
        "confusion_matrix_labels_order": LABELS,
        "confusion_matrix": matrix.tolist(),
        "warning": (
            "Preliminary result on nine selected bearings only; "
            "not proof of generalization to industrial machines."
        ),
    }
    with open(
        REPORT_DIR / "paderborn_lobo_metrics.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(metrics, f, indent=2)
    with open(
        REPORT_DIR / "paderborn_lobo_classification_report.txt",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(f"Overall out-of-fold accuracy: {overall_accuracy:.4f}\n\n")
        f.write(report)
        f.write("\nConfusion matrix (rows=true, columns=predicted):\n")
        f.write(pd.DataFrame(
            matrix,
            index=LABELS,
            columns=LABELS,
        ).to_string())
        f.write("\n")
    print("\nTraining final model on all available recordings...")
    final_model = make_model()
    final_model.fit(X, y)
    artifact = {
        "model": final_model,
        "features": FEATURES,
        "labels": LABELS,
        "dataset": "Paderborn Bearing DataCenter",
        "evaluation": "LeaveOneGroupOut by bearing_id",
    }
    model_path = MODEL_DIR / "paderborn_bearing_classifier.pkl"
    joblib.dump(artifact, model_path)
    importance = pd.DataFrame({
        "feature": FEATURES,
        "importance": final_model.feature_importances_,
    }).sort_values("importance", ascending=False)
    importance.to_csv(
        REPORT_DIR / "paderborn_feature_importance.csv",
        index=False,
    )
    print("\nFeature importance:")
    print(importance.to_string(index=False))
    print("\nSaved model:", model_path)
    print("Saved reports:", REPORT_DIR)
    print("\nEvaluation completed. V5 artifacts were not modified.")
if __name__ == "__main__":
    main()
