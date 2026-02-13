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
    load_roa
)

# Expected arguments:
# 1: start YYYYMMDDHHMM
# 2: end   YYYYMMDDHHMM
# 3: threshold_core
# 4: threshold_roa
# 5: min_pixels

if len(sys.argv) != 6:
    raise ValueError(
        "Usage: python script.py START END THRESH_CORE THRESH_ROA MIN_PIXELS"
    )

start_str = sys.argv[1]
end_str   = sys.argv[2]
threshold_core = float(sys.argv[3])
threshold_roa  = float(sys.argv[4])
min_pixels     = int(sys.argv[5])


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
roa_tag  = f"thr_{threshold_roa}".replace(".", "p")

output_core = f"/work/scratch-nopw2/mendrika/ASNIE/core/{core_tag}"
output_roa  = f"/work/scratch-nopw2/mendrika/ASNIE/roa/{roa_tag}"

times = generate_time_steps(start, end)

for t in times:

    print("Processing:", t, flush=True)

    try:
        data_core, lats_core, lons_core = load_core(t)
        data_roa,  lats_roa,  lons_roa  = load_roa(t)
    except FileNotFoundError as e:
        print("Missing file:", e, flush=True)
        continue

    try:
        grid_core = GeoGrid(lats_core, lons_core, *extent)
        grid_roa  = GeoGrid(lats_roa,  lons_roa,  *extent)
    except ValueError:
        print("Crop outside domain:", t, flush=True)
        continue

    data_core = grid_core.crop(data_core)
    data_roa  = grid_roa.crop(data_roa)

    # if image-based, make sure they have the same shape, do the interpolation here
    # FSS calculation

    # require both products to exceed their thresholds
    if not (np.any(data_core >= threshold_core) and
            np.any(data_roa  >= threshold_roa)):
        continue

    df_core = field_to_objects(
        field=data_core,
        threshold=threshold_core,
        grid=grid_core,
        connectivity=8,
        name="core",
        min_pixels=min_pixels
    )

    df_roa = field_to_objects(
        field=data_roa,
        threshold=threshold_roa,
        grid=grid_roa,
        connectivity=8,
        name="roa",
        min_pixels=min_pixels
    )

    # require both to have objects
    if df_core.empty or df_roa.empty:
        continue

    save_dataframe(df_core, output_core, t)
    save_dataframe(df_roa, output_roa, t)
