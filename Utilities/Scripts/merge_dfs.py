import sys
from pathlib import Path
import pandas as pd


# Expect PRODUCT THRESH BASE_PATH
if len(sys.argv) != 4:
    raise ValueError(
        "Usage: python merge_dfs.py PRODUCT THRESH BASE_PATH"
    )

product = sys.argv[1].strip().lower()
thr_in = sys.argv[2].strip()
base_path = Path(sys.argv[3])

if product not in {"core", "roa"}:
    raise ValueError("PRODUCT must be 'core' or 'roa'")

# Normalise threshold tag to match folder naming
if thr_in.startswith("thr_"):
    thr_val = thr_in[4:]
else:
    thr_val = thr_in

thr_tag = f"thr_{thr_val}".replace(".", "p")

input_folder = base_path / product / thr_tag

if not input_folder.exists():
    raise FileNotFoundError(f"Folder not found: {input_folder}")

files = sorted(input_folder.glob("*.csv"))

if len(files) == 0:
    raise ValueError(f"No CSV files found in {input_folder}")

dfs = []

# Read all CSV files and attach time metadata
for i, f in enumerate(files):

    if i % 1000 == 0:
        print(f"Reading file {i}/{len(files)}", flush=True)

    df = pd.read_csv(f)

    dt = pd.to_datetime(f.stem, format="%Y%m%d%H%M")
    df["time"] = dt
    df["year"] = dt.year
    df["month"] = dt.month
    df["day"] = dt.day
    df["hour"] = dt.hour

    dfs.append(df)

df_all = pd.concat(dfs, ignore_index=True)

# Create parquet output directory
output_dir = base_path / "parquet"
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / f"{product}_{thr_tag}.parquet"

df_all.to_parquet(output_file, index=False)

print("Saved:", output_file)
