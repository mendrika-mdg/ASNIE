import os
import sys
import numpy as np
from scipy.ndimage import maximum_filter

sys.path.insert(1, "/home/users/mendrika/ASNIE/Utilities/Scripts")

from asnie_utils import (
    GeoGrid,
    generate_time_steps,
    field_to_objects,
    save_dataframe
)

from asnie_loaders import (
    load_core,
    load_li
)

# Arguments:
# 1: START YYYYMMDDHHMM
# 2: END   YYYYMMDDHHMM
# 3: THRESH_CORE
# 4: THRESH_LI
# 5: MIN_PIXELS_CORE
# 6: MIN_PIXELS_LI

if len(sys.argv) != 7:
    raise ValueError(
        "Usage: python script.py START END THRESH_CORE THRESH_LI "
        "MIN_PIXELS_CORE MIN_PIXELS_LI"
    )

start_str = sys.argv[1]
end_str   = sys.argv[2]
threshold_core = float(sys.argv[3])
threshold_li   = float(sys.argv[4])
min_pixels_core = int(sys.argv[5])
min_pixels_li   = int(sys.argv[6])


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

extent = (5, 20, -20, -4)

core_tag = f"thr_{threshold_core}".replace(".", "p")
li_tag   = f"thr_{threshold_li}".replace(".", "p")

output_core = f"/work/scratch-nopw2/mendrika/ASNIE/final-database/LI/core/{core_tag}"
output_li   = f"/work/scratch-nopw2/mendrika/ASNIE/final-database/LI/li/{li_tag}"

os.makedirs(output_core, exist_ok=True)
os.makedirs(output_li, exist_ok=True)

times = generate_time_steps(start, end)

for t in times:

    print("Processing:", t, flush=True)

    try:
        ctt, lats_c, lons_c = load_core(t)
        li,  lats_l, lons_l = load_li(t)
    except FileNotFoundError as e:
        print("Missing file:", e, flush=True)
        continue

    try:
        grid_core = GeoGrid(lats_c, lons_c, *extent)
        grid_li   = GeoGrid(lats_l, lons_l, *extent)
    except ValueError:
        print("Crop outside domain:", t, flush=True)
        continue

    ctt = grid_core.crop(ctt)
    li  = grid_li.crop(li)

    ctt = np.where(np.isfinite(ctt), ctt, np.nan)
    li  = np.where(np.isfinite(li), li, np.nan)

    # Smooth lightning
    li_filtered = maximum_filter(li, size=3)

    # CTT-based core objects (cold tail → invert sign)
    df_core = field_to_objects(
        field=-ctt,
        threshold=threshold_core,
        grid=grid_core,
        connectivity=8,
        name="core",
        min_pixels=min_pixels_core
    )

    # Lightning objects
    df_li = field_to_objects(
        field=li_filtered,
        threshold=threshold_li,
        grid=grid_li,
        connectivity=8,
        name="li",
        min_pixels=min_pixels_li
    )

    if not df_core.empty:
        save_dataframe(df_core, output_core, t)

    if not df_li.empty:
        save_dataframe(df_li, output_li, t)
