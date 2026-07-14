import os
import sys
import numpy as np
import pandas as pd
from scipy.ndimage import label

sys.path.insert(1, "/home/users/mendrika/ASNIE/Utilities/Scripts")

from asnie_utils import (
    GeoGrid,
    generate_time_steps,
    field_to_objects
)

from asnie_loaders import (
    load_core,
    load_rdt
)

if len(sys.argv) != 5:
    raise ValueError(
        "Usage: python script.py START END THRESH_CORE MIN_PIXELS"
    )

start_str = sys.argv[1]
end_str = sys.argv[2]

threshold_core = float(sys.argv[3])
min_pixels = int(sys.argv[4])

def str_to_time_dict(s):
    return dict(
        year=int(s[0:4]),
        month=int(s[4:6]),
        day=int(s[6:8]),
        hour=int(s[8:10]),
        minute=int(s[10:12])
    )

start = str_to_time_dict(start_str)
end = str_to_time_dict(end_str)

CONTEXT_LAT_MIN = 5
CONTEXT_LAT_MAX = 20
CONTEXT_LON_MIN = -20
CONTEXT_LON_MAX = -4

extent = (
    CONTEXT_LAT_MIN, CONTEXT_LAT_MAX,
    CONTEXT_LON_MIN, CONTEXT_LON_MAX
)

times = generate_time_steps(start, end)

results = []

for t in times:

    print("Processing:", t, flush=True)

    try:
        data_core, lats_core, lons_core = load_core(t)
        data_rdt, lats_rdt, lons_rdt = load_rdt(t)
    except FileNotFoundError as e:
        print("Missing file:", e, flush=True)
        continue

    try:
        grid_core = GeoGrid(lats_core, lons_core, *extent)
        grid_rdt = GeoGrid(lats_rdt, lons_rdt, *extent)
    except ValueError:
        print("Crop outside domain:", t, flush=True)
        continue

    data_core = grid_core.crop(data_core)
    data_rdt = grid_rdt.crop(data_rdt)

    df_core = field_to_objects(
        field=data_core,
        threshold=threshold_core,
        grid=grid_core,
        connectivity=8,
        name="core",
        min_pixels=min_pixels
    )

    if df_core.empty:
        continue

    core_lat_c = df_core["lat_centroid"].values
    core_lon_c = df_core["lon_centroid"].values

    mask_rdt = data_rdt > 0

    ys, xs = grid_rdt.query_many(core_lat_c, core_lon_c)

    inside = mask_rdt[ys, xs]

    fraction_inside = inside.mean()
    fraction_outside = 1 - fraction_inside

    labels, n_rdt = label(mask_rdt)

    core_labels = labels[ys, xs]

    counts = np.bincount(core_labels, minlength=n_rdt + 1)[1:]

    mean_cores_per_rdt = np.nan
    max_cores_per_rdt = np.nan

    if counts.size > 0:
        mean_cores_per_rdt = counts.mean()
        max_cores_per_rdt = counts.max()

    fraction_rdt_with_core = np.nan
    core_density = np.nan

    if n_rdt > 0:
        fraction_rdt_with_core = np.sum(counts > 0) / n_rdt
        core_density = len(df_core) / n_rdt

    results.append({
        "year": t["year"],
        "month": t["month"],
        "day": t["day"],
        "hour": t["hour"],
        "minute": t["minute"],
        "n_cores": len(df_core),
        "n_rdt_objects": n_rdt,
        "fraction_core_inside_rdt": fraction_inside,
        "fraction_core_outside_rdt": fraction_outside,
        "fraction_rdt_with_core": fraction_rdt_with_core,
        "mean_cores_per_rdt": mean_cores_per_rdt,
        "max_cores_per_rdt": max_cores_per_rdt,
        "core_density": core_density
    })

if len(results) == 0:
    print("No valid timesteps processed.", flush=True)
    sys.exit()

df_results = pd.DataFrame(results)

output_dir = "/gws/ssde/j25b/swift/mendrika/asnie/database/rdt"

os.makedirs(output_dir, exist_ok=True)

output_file = (
    f"{output_dir}/core_rdt_statistics_"
    f"{start_str}_{end_str}_"
    f"thr_core_{threshold_core:.3f}.csv"
)

df_results.to_csv(output_file, index=False)

print("Saved results to:", output_file, flush=True)