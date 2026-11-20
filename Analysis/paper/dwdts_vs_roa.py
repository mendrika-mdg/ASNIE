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
    load_ts,
    load_roa
)

# Expected arguments:
# 1: start YYYYMMDDHHMM
# 2: end YYYYMMDDHHMM
# 3: threshold_ts
# 4: threshold_roa
# 5: min_pixels
# 6: domain name

if len(sys.argv) != 7:
    raise ValueError(
        "Usage: python script.py START END THRESH_TS THRESH_ROA MIN_PIXELS DOMAIN"
    )

start_str = sys.argv[1]
end_str = sys.argv[2]
threshold_ts = float(sys.argv[3])
threshold_roa = float(sys.argv[4])
min_pixels = int(sys.argv[5])
DOMAIN_NAME = sys.argv[6]


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

output_ts = f"/gws/ssde/j25b/swift/mendrika/asnie/paper/ts-vs-roa/{DOMAIN_NAME}/ts"
output_roa = f"/gws/ssde/j25b/swift/mendrika/asnie/paper/ts-vs-roa/{DOMAIN_NAME}/roa"

os.makedirs(output_ts, exist_ok=True)
os.makedirs(output_roa, exist_ok=True)

# choosing months should be done here
times = generate_time_steps(start, end)

for t in times:

    print("Processing:", t, flush=True)

    try:
        data_ts, lats_ts, lons_ts = load_ts(t)
        data_roa, lats_roa, lons_roa = load_roa(t)
    except FileNotFoundError as e:
        print("Missing file:", e, flush=True)
        continue

    try:
        grid_ts = GeoGrid(lats_ts, lons_ts, *extent)
        grid_roa = GeoGrid(lats_roa, lons_roa, *extent)
    except ValueError:
        print("Crop outside domain:", t, flush=True)
        continue

    data_ts = grid_ts.crop(data_ts)
    data_roa = grid_roa.crop(data_roa)

    # require both products to exceed their thresholds
    if not (
        np.any(data_ts >= threshold_ts)
        and np.any(data_roa >= threshold_roa)
    ):
        continue

    df_ts = field_to_objects(
        field=data_ts,
        threshold=threshold_ts,
        grid=grid_ts,
        connectivity=8,
        name="ts",
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
    if df_ts.empty or df_roa.empty:
        continue

    save_dataframe(df_ts, output_ts, t)
    save_dataframe(df_roa, output_roa, t)