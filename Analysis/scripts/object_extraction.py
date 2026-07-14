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
    load_ts,
    load_roa,
    load_crr,
    load_li
)

# Expected arguments
# 1: PRODUCT (core, rdt, ts, roa, crr, li)
# 2: start YYYYMMDDHHMM
# 3: end   YYYYMMDDHHMM
# 4: threshold
# 5: min_pixels

if len(sys.argv) != 6:
    raise ValueError(
        "Usage: python extract_objects.py PRODUCT START END THRESHOLD MIN_PIXELS"
    )

product = sys.argv[1].lower()
start_str = sys.argv[2]
end_str   = sys.argv[3]
threshold = float(sys.argv[4])
min_pixels = int(sys.argv[5])


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


def load_product(product, t):

    if product == "core":
        return load_core(t)

    if product == "rdt":
        return load_rdt(t)

    if product == "ts":
        return load_ts(t)

    if product == "roa":
        return load_roa(t)

    if product == "crr":
        return load_crr(t)

    if product == "li":
        return load_li(t)

    raise ValueError(f"Unknown product: {product}")


CONTEXT_LAT_MIN = 5
CONTEXT_LAT_MAX = 20
CONTEXT_LON_MIN = -20
CONTEXT_LON_MAX = -4

extent = (
    CONTEXT_LAT_MIN,
    CONTEXT_LAT_MAX,
    CONTEXT_LON_MIN,
    CONTEXT_LON_MAX
)

tag = f"thr_{threshold}".replace(".", "p")

year = start["year"]

output_dir = f"/gws/ssde/j25b/swift/mendrika/asnie/database/{product}/{year}/{tag}"

os.makedirs(output_dir, exist_ok=True)

times = generate_time_steps(start, end)

for t in times:

    print("Processing:", t, flush=True)

    try:
        data, lats, lons = load_product(product, t)
    except FileNotFoundError as e:
        print("Missing file:", e, flush=True)
        continue

    try:
        grid = GeoGrid(lats, lons, *extent)
    except ValueError:
        print("Crop outside domain:", t, flush=True)
        continue

    data = grid.crop(data)

    if not np.any(data >= threshold):
        continue

    df = field_to_objects(
        field=data,
        threshold=threshold,
        grid=grid,
        connectivity=8,
        name=product,
        min_pixels=min_pixels
    )

    if df.empty:
        continue

    save_dataframe(df, output_dir, t)