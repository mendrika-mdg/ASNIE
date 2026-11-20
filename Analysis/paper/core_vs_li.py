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
    load_li
)

# Expected arguments:
# 1: start YYYYMMDDHHMM
# 2: end YYYYMMDDHHMM
# 3: threshold_core
# 4: threshold_li
# 5: min_pixels_core
# 6: min_pixels_li
# 7: domain name

if len(sys.argv) != 8:
    raise ValueError(
        "Usage: python script.py START END THRESH_CORE THRESH_LI "
        "MIN_PIXELS_CORE MIN_PIXELS_LI DOMAIN"
    )

start_str = sys.argv[1]
end_str = sys.argv[2]
threshold_core = float(sys.argv[3])
threshold_li = float(sys.argv[4])
min_pixels_core = int(sys.argv[5])
min_pixels_li = int(sys.argv[6])
DOMAIN_NAME = sys.argv[7]


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

if DOMAIN_NAME == "WA":
    lat_min = 3
    lat_max = 20
    lon_min = -20
    lon_max = 8

elif DOMAIN_NAME == "EA":
    lat_min = -8
    lat_max = 16
    lon_min = 30
    lon_max = 52

elif DOMAIN_NAME == "CA":
    lat_min = -8
    lat_max = 10
    lon_min = 8
    lon_max = 30

elif DOMAIN_NAME == "SA":
    lat_min = -35
    lat_max = -8
    lon_min = 10
    lon_max = 42

# smaller subdomains due to old files from different projects
elif DOMAIN_NAME == "ea":
    lat_min = -8
    lat_max = 13.5
    lon_min = 30
    lon_max = 52

elif DOMAIN_NAME == "sa":
    lat_min = -19
    lat_max = -8
    lon_min = 10
    lon_max = 42

else:
    raise ValueError(f"Unknown domain: {DOMAIN_NAME}")

extent = (
    lat_min, lat_max,
    lon_min, lon_max
)

threshold_tag = f"{threshold_li:g}"

output_core = (
    f"/gws/ssde/j25b/swift/mendrika/asnie/paper/"
    f"core-vs-li/{DOMAIN_NAME}/core/{threshold_tag}"
)

output_li = (
    f"/gws/ssde/j25b/swift/mendrika/asnie/paper/"
    f"core-vs-li/{DOMAIN_NAME}/li/{threshold_tag}"
)

os.makedirs(output_core, exist_ok=True)
os.makedirs(output_li, exist_ok=True)

times = generate_time_steps(start, end)

for t in times:

    print("Processing:", t, flush=True)

    try:
        data_core, lats_core, lons_core = load_core(t)
        data_li, lats_li, lons_li = load_li(t)
    except FileNotFoundError as e:
        print("Missing file:", e, flush=True)
        continue

    try:
        grid_core = GeoGrid(lats_core, lons_core, *extent)
        grid_li = GeoGrid(lats_li, lons_li, *extent)
    except ValueError:
        print("Crop outside domain:", t, flush=True)
        continue

    data_core = grid_core.crop(data_core)
    data_li = grid_li.crop(data_li)

    data_core = np.where(
        np.isfinite(data_core),
        data_core,
        np.nan
    )

    data_li = np.where(
        np.isfinite(data_li),
        data_li,
        np.nan
    )

    # require both products to exceed their thresholds
    if not (
        np.any(data_core >= threshold_core)
        and np.any(data_li >= threshold_li)
    ):
        continue

    # Core objects
    df_core = field_to_objects(
        field=data_core,
        threshold=threshold_core,
        grid=grid_core,
        connectivity=8,
        name="core",
        min_pixels=min_pixels_core
    )

    # Lightning objects
    df_li = field_to_objects(
        field=data_li,
        threshold=threshold_li,
        grid=grid_li,
        connectivity=8,
        name="li",
        min_pixels=min_pixels_li
    )

    # require both to have objects
    if df_core.empty or df_li.empty:
        continue

    save_dataframe(df_core, output_core, t)
    save_dataframe(df_li, output_li, t)