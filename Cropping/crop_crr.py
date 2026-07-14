import os
import sys
import numpy as np

sys.path.insert(1, "/home/users/mendrika/ASNIE/Utilities/Scripts")

from asnie_utils import generate_time_steps
from asnie_loaders import load_crr


if len(sys.argv) != 3:
    raise ValueError(
        "Usage: python crop_crr.py START END"
    )

start_str = sys.argv[1]
end_str   = sys.argv[2]


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


# Madagascar crop indices (CRR grid)
y0, y1 = 1673, 2167
x0, x1 = 2242, 2565

times = generate_time_steps(start, end)

for t in times:

    print("Processing:", t, flush=True)

    try:
        data, _, _ = load_crr(t)
    except Exception as e:
        print(f"Error reading file: {t} | {e}", flush=True)
        continue


    # Crop to Madagascar
    data = data[y0:y1+1, x0:x1+1]

    # Reduce precision
    data = data.astype(np.float32)

    year  = t["year"]
    month = f"{t['month']:02d}"

    output_dir = f"/work/scratch-nopw2/mendrika/mdg/crr/{year}/{month}"
    os.makedirs(output_dir, exist_ok=True)


    outfile = (
        f"{output_dir}/crr_"
        f"{t['year']}{t['month']:02d}{t['day']:02d}"
        f"{t['hour']:02d}{t['minute']:02d}.npy"
    )

    np.save(outfile, data)