import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(1, "/home/users/mendrika/ASNIE/Utilities/Scripts")

from asnie_utils import (
    GeoGrid,
    generate_time_steps,
    field_to_objects,
    save_dataframe
)

from asnie_loaders import (
    load_rdt_object,
    load_crr
)

# Expected arguments:
# 1: start YYYYMMDDHHMM
# 2: end YYYYMMDDHHMM
# 3: threshold_crr
# 4: min_pixels
# 5: domain name

if len(sys.argv) != 6:
    raise ValueError(
        "Usage: python script.py START END THRESH_CRR MIN_PIXELS DOMAIN"
    )

start_str = sys.argv[1]
end_str = sys.argv[2]
threshold_crr = float(sys.argv[3])
min_pixels = int(sys.argv[4])
DOMAIN_NAME = sys.argv[5]


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

output_rdt = (
    f"/gws/ssde/j25b/swift/mendrika/asnie/paper/"
    f"rdt-vs-crr/{DOMAIN_NAME}/rdt"
)

output_crr = (
    f"/gws/ssde/j25b/swift/mendrika/asnie/paper/"
    f"rdt-vs-crr/{DOMAIN_NAME}/crr"
)

os.makedirs(output_rdt, exist_ok=True)
os.makedirs(output_crr, exist_ok=True)

times = generate_time_steps(start, end)

for t in times:

    print("Processing:", t, flush=True)

    try:
        rdt = load_rdt_object(t)
        data_crr, lats_crr, lons_crr = load_crr(t)
    except FileNotFoundError as e:
        print("Missing file:", e, flush=True)
        continue

    # select RDT objects whose centres are inside the domain
    rdt_mask = (
        (rdt["lat"] >= lat_min)
        & (rdt["lat"] <= lat_max)
        & (rdt["lon"] >= lon_min)
        & (rdt["lon"] <= lon_max)
    )

    if not np.any(rdt_mask):
        continue

    rdt_domain = {
        key: value[rdt_mask]
        for key, value in rdt.items()
    }

    # clean padded RDT contours
    lat_contours = []
    lon_contours = []

    for lat_contour, lon_contour in zip(
        rdt_domain["lat_contour"],
        rdt_domain["lon_contour"]
    ):

        valid = (
            np.isfinite(lat_contour)
            & np.isfinite(lon_contour)
            & (lat_contour != -9999)
            & (lon_contour != -9999)
        )

        lat_contours.append(lat_contour[valid])
        lon_contours.append(lon_contour[valid])

    df_rdt = pd.DataFrame({
        "id": rdt_domain["id"],
        "conv_type": rdt_domain["conv_type"],
        "phase_life": rdt_domain["phase_life"],
        "severity_type": rdt_domain["severity_type"],
        "severity_intensity": rdt_domain["severity_intensity"],
        "lat": rdt_domain["lat"],
        "lon": rdt_domain["lon"],
        "surface": rdt_domain["surface"],
        "lat_contour": lat_contours,
        "lon_contour": lon_contours
    })

    try:
        grid_crr = GeoGrid(lats_crr, lons_crr, *extent)
    except ValueError:
        print("Crop outside domain:", t, flush=True)
        continue

    data_crr = grid_crr.crop(data_crr)

    if not np.any(data_crr >= threshold_crr):
        continue

    df_crr = field_to_objects(
        field=data_crr,
        threshold=threshold_crr,
        grid=grid_crr,
        connectivity=8,
        name="crr",
        min_pixels=min_pixels
    )

    # require both products to have objects
    if df_rdt.empty or df_crr.empty:
        continue

    save_dataframe(df_rdt, output_rdt, t)
    save_dataframe(df_crr, output_crr, t)