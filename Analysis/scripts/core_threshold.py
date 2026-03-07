import os
import sys
import numpy as np

sys.path.insert(1, "/home/users/mendrika/ASNIE/Utilities/Scripts")

from asnie_utils import GeoGrid, generate_time_steps
from asnie_loaders import load_core


def str_to_time_dict(s):
    return dict(
        year=int(s[0:4]),
        month=int(s[4:6]),
        day=int(s[6:8]),
        hour=int(s[8:10]),
        minute=int(s[10:12])
    )


# JJAS 2025
start = str_to_time_dict("202506010000")
end   = str_to_time_dict("202509302345")


# Western Sahel domain
CONTEXT_LAT_MIN = 5
CONTEXT_LAT_MAX = 20
CONTEXT_LON_MIN = -20
CONTEXT_LON_MAX = -4

extent = (
    CONTEXT_LAT_MIN, CONTEXT_LAT_MAX,
    CONTEXT_LON_MIN, CONTEXT_LON_MAX
)


output_path = "/work/scratch-nopw2/mendrika/ASNIE/analysis/core_ctt_distribution_JJAS2025_masked.dat"

times = generate_time_steps(start, end)


# First pass: count pixels (CTT <= -40°C only)
total_pixels = 0

for t in times:

    try:
        data_core, lats_core, lons_core = load_core(t)
    except FileNotFoundError:
        continue

    try:
        grid_core = GeoGrid(lats_core, lons_core, *extent)
    except ValueError:
        continue

    data_core = grid_core.crop(data_core)

    mask = np.isfinite(data_core) & (data_core <= -40.0)
    total_pixels += np.count_nonzero(mask)


if total_pixels == 0:
    raise RuntimeError("No valid CTT ≤ -40°C found for JJAS 2025")


print("Total deep-cloud pixels (≤ -40°C):", total_pixels, flush=True)


# Allocate memmap
os.makedirs(os.path.dirname(output_path), exist_ok=True)

ctt_memmap = np.memmap(
    output_path,
    dtype="float32",
    mode="w+",
    shape=(total_pixels,)
)


# Second pass: fill array
idx = 0

for t in times:

    print("Processing:", t, flush=True)

    try:
        data_core, lats_core, lons_core = load_core(t)
    except FileNotFoundError:
        continue

    try:
        grid_core = GeoGrid(lats_core, lons_core, *extent)
    except ValueError:
        continue

    data_core = grid_core.crop(data_core)

    mask = np.isfinite(data_core) & (data_core <= -40.0)
    values = data_core[mask].astype("float32")

    n = len(values)
    if n == 0:
        continue

    ctt_memmap[idx:idx+n] = values
    idx += n


ctt_memmap.flush()


# Statistics
print("Saved:", output_path, flush=True)
print("Mean:", np.mean(ctt_memmap), flush=True)
print("Median:", np.median(ctt_memmap), flush=True)
print("10th percentile (intense deep cloud):", np.percentile(ctt_memmap, 10), flush=True)
print("5th percentile (extreme deep convection):", np.percentile(ctt_memmap, 5), flush=True)
