import os
import sys
import torch
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy.ndimage import uniform_filter

# arguments
lead_time = sys.argv[1]
target_hour = sys.argv[2]

# directories
base_dir = f"/work/scratch-nopw2/mendrika/OB/predictions/t{lead_time}"

# windows
windows = [3, 9, 25, 49, 81, 121]
PIXEL_SIZE_KM = 3

# fss function
def compute_fss(pred, obs, window):
    pred = np.clip(pred, 0, 1)
    obs = np.clip(obs, 0, 1)
    f_pred = uniform_filter(pred, size=window, mode="constant")
    f_obs = uniform_filter(obs, size=window, mode="constant")
    num = np.mean((f_pred - f_obs) ** 2)
    den = np.mean(f_pred ** 2 + f_obs ** 2)
    return 1 - num / (den + 1e-8)

# recursive search
all_files = []
for root, _, files in os.walk(base_dir):
    for f in files:
        if f.endswith(".pt"):
            all_files.append(os.path.join(root, f))

# extract hour from filename
def extract_hour(path):
    name = os.path.basename(path)
    parts = name.split("_")
    if len(parts) < 3:
        return None
    timepart = parts[2].replace(".pt", "")
    if len(timepart) < 2:
        return None
    return timepart[:2]

# filter by hour
filtered_files = [p for p in all_files if extract_hour(p) == target_hour]
print(f"Found {len(filtered_files)} files at hour={target_hour} UTC")

# storage
fss_results = {w: {"model": [], "persistence": []} for w in windows}

# loop
for file_path in tqdm(filtered_files, desc="Computing FSS"):
    try:
        data = torch.load(file_path, weights_only=False)
    except Exception as e:
        print(f"Skipping {file_path}: {e}")
        continue

    gt = np.nan_to_num(data["gt"].cpu().numpy().astype(np.float32))
    pred = np.nan_to_num(data["mean"].cpu().numpy().astype(np.float32))
    persistence = np.nan_to_num(data["gt0"].cpu().numpy().astype(np.float32))

    for w in windows:
        fss_results[w]["model"].append(compute_fss(pred, gt, w))
        fss_results[w]["persistence"].append(compute_fss(persistence, gt, w))

# summary
rows = []
print(f"\nAverage FSS for hour={target_hour} UTC (lead t+{lead_time})")
print(f"{'Window':>8} | {'Scale(km)':>10} | {'Model':>10} | {'Persistence':>10}")
print("-" * 62)

for w in windows:
    scale = w * PIXEL_SIZE_KM
    mean_model = np.nanmean(fss_results[w]["model"])
    mean_persistence = np.nanmean(fss_results[w]["persistence"])
    rows.append({
        "window": w,
        "scale_km": scale,
        "model": mean_model,
        "persistence": mean_persistence
    })
    print(f"{w:>8} | {scale:>10.0f} | {mean_model:.4f} | {mean_persistence:.4f}")

# save csv
output_csv = f"/home/users/mendrika/Object-Based-LSTMConv/outputs/evaluation/fss/fss_hour_{target_hour}_t{lead_time}.csv"
os.makedirs(os.path.dirname(output_csv), exist_ok=True)
pd.DataFrame(rows).to_csv(output_csv, index=False)
print(f"\nSaved FSS summary to {output_csv}")