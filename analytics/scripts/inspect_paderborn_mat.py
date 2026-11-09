
from pathlib import Path
import numpy as np
from scipy.io import loadmat

root = Path(__file__).resolve().parents[2]
folder = root / "datasets" / "paderborn" / "raw" / "K001" / "K001"
path = sorted(folder.glob("*.mat"))[0]

data = loadmat(path, squeeze_me=True, struct_as_record=False)
record = data[path.stem]

def inspect_value(name, value, depth=0):
    indent = "  " * depth
    print(f"{indent}{name}: {type(value).__name__}")

    if hasattr(value, "_fieldnames"):
        for field in value._fieldnames:
            inspect_value(field, getattr(value, field), depth + 1)

    elif isinstance(value, np.ndarray):
        print(f"{indent}  shape={value.shape}, dtype={value.dtype}")

        if value.dtype == object:
            for i, item in enumerate(value.flat):
                inspect_value(f"[{i}]", item, depth + 1)
        elif np.issubdtype(value.dtype, np.number):
            finite = value[np.isfinite(value)]
            if finite.size:
                print(
                    f"{indent}  min={finite.min():.6g}, "
                    f"max={finite.max():.6g}, "
                    f"mean={finite.mean():.6g}"
                )
    elif isinstance(value, (str, bytes)):
        print(f"{indent}  value={value}")
    elif np.isscalar(value):
        print(f"{indent}  value={value}")

for field in record._fieldnames:
    if field in ("X", "Y", "Info", "Description"):
        print(f"\n=== {field} ===")
        inspect_value(field, getattr(record, field))
