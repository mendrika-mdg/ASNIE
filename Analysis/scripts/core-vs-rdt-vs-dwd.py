import os
import sys
import numpy as np

sys.path.insert(1, "/home/users/mendrika/ASNIE/Utilities/Scripts")

from asnie_utils import (
    GeoGrid,
    generate_time_steps,
    field_to_objects,
    save_dataframe
)

from asnie_loaders import (
    load_core,
    load_rdt,
    load_ts
)

# Expected arguments:
# 1: start YYYYMMDDHHMM
# 2: end   YYYYMMDDHHMM
# 3: threshold_core
# 4: threshold_rdt
# 5: threshold_ts
# 6: min_pixels

if len(sys.argv) != 7:
    raise ValueError(
        "Usage: python script.py START END THRESH_CORE THRESH_RDT THRESH_TS MIN_PIXELS"
    )

start_str = sys.argv[1]
end_str   = sys.argv[2]

threshold_core = float(sys.argv[3])
threshold_rdt  = float(sys.argv[4])
threshold_ts   = float(sys.argv[5])

min_pixels = int(sys.argv[6])


def str_to_time_dict(s):
    return dict(
        year=int(s[0:4]),
        month=int(s[4:6]),
        day=int(s[6:8]),
        hour=int(s[8:10]),
        minute=int(s[10:12])
    )


start = str_to_time_dict(start_str)
end   = str_to_time_dict(end_str)

CONTEXT_LAT_MIN = 5
CONTEXT_LAT_MAX = 20
CONTEXT_LON_MIN = -20
CONTEXT_LON_MAX = -4

extent = (
    CONTEXT_LAT_MIN, CONTEXT_LAT_MAX,
    CONTEXT_LON_MIN, CONTEXT_LON_MAX
)

core_tag = f"thr_{threshold_core}".replace(".", "p")
rdt_tag  = f"thr_{threshold_rdt}".replace(".", "p")
ts_tag   = f"thr_{threshold_ts}".replace(".", "p")

output_core = f"/work/scratch-nopw2/mendrika/ASNIE/final-database/RDT_DWDTS/core/{core_tag}"
output_rdt  = f"/work/scratch-nopw2/mendrika/ASNIE/final-database/RDT_DWDTS/rdt/{rdt_tag}"
output_ts   = f"/work/scratch-nopw2/mendrika/ASNIE/final-database/RDT_DWDTS/dwdts/{ts_tag}"

os.makedirs(output_core, exist_ok=True)
os.makedirs(output_rdt, exist_ok=True)
os.makedirs(output_ts, exist_ok=True)

times = generate_time_steps(start, end)

for t in times:

    print("Processing:", t, flush=True)

    try:
        data_core, lats_core, lons_core = load_core(t)
        data_rdt,  lats_rdt,  lons_rdt  = load_rdt(t)
        data_ts,   lats_ts,   lons_ts   = load_ts(t)
    except FileNotFoundError as e:
        print("Missing file:", e, flush=True)
        continue

    try:
        grid_core = GeoGrid(lats_core, lons_core, *extent)
        grid_rdt  = GeoGrid(lats_rdt,  lons_rdt,  *extent)
        grid_ts   = GeoGrid(lats_ts,   lons_ts,   *extent)
    except ValueError:
        print("Crop outside domain:", t, flush=True)
        continue

    data_core = grid_core.crop(data_core)
    data_rdt  = grid_rdt.crop(data_rdt)
    data_ts   = grid_ts.crop(data_ts)

    df_core = field_to_objects(
        field=data_core,
        threshold=threshold_core,
        grid=grid_core,
        connectivity=8,
        name="core",
        min_pixels=min_pixels
    )

    df_rdt = field_to_objects(
        field=data_rdt,
        threshold=threshold_rdt,
        grid=grid_rdt,
        connectivity=8,
        name="rdt",
        min_pixels=min_pixels
    )

    df_ts = field_to_objects(
        field=data_ts,
        threshold=threshold_ts,
        grid=grid_ts,
        connectivity=8,
        name="dwdts",
        min_pixels=min_pixels
    )

    if df_core.empty and df_rdt.empty and df_ts.empty:
        continue

    if not df_core.empty:
        save_dataframe(df_core, output_core, t)

    if not df_rdt.empty:
        save_dataframe(df_rdt, output_rdt, t)

    if not df_ts.empty:
        save_dataframe(df_ts, output_ts, t)