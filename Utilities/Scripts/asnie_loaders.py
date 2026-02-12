import os, bz2
import numpy as np
from pathlib import Path
from netCDF4 import Dataset, num2date
from datetime import datetime, timedelta

# Convective core

def load_core(t):

    year   = int(t["year"])
    month  = f"{int(t['month']):02d}"
    day    = f"{int(t['day']):02d}"
    hour   = f"{int(t['hour']):02d}"
    minute = f"{int(t['minute']):02d}"

    if year <= 2024:

        base = f"/gws/nopw/j04/cocoon/SSA_domain/ch9_wavelet/{year}/{month}"
        fname = f"{year}{month}{day}{hour}{minute}.nc"
        path = os.path.join(base, fname)

        if not os.path.exists(path):
            raise FileNotFoundError(f"Core file not found: {path}")

        with Dataset(path) as ds:
            cores = ds["cores"][0]

        geo = np.load("/gws/nopw/j04/cocoon/SSA_domain/lat_lon_2268_2080.npz")
        lons = geo["lon"]
        lats = geo["lat"]

    else:

        base = f"/gws/ssde/j25b/swift/rt_cores/{year}/{month}/{day}/{hour}{minute}"
        fname = f"Convective_struct_extended_{year}{month}{day}{hour}{minute}_000.nc"
        path = os.path.join(base, fname)

        if not os.path.exists(path):
            raise FileNotFoundError(f"Core file not found: {path}")

        with Dataset(path) as ds:
            cores = ds["cores"][:]

        geo = Dataset(
            "/gws/ssde/j25b/swift/rt_cores/geoloc_grids/"
            "nxny2268_2080_nxnyds164580_blobdx0.04491576_arean41_n27_27_79.nc"
        )
        lons = geo["lons_mid"][:]
        lats = geo["lats_mid"][:]
        geo.close()

    cores = np.asarray(cores)
    cores = np.ma.filled(cores, np.nan)

    return cores, lats, lons


# Rapid developing thunderstorm

def load_rdt(t, domain="WestAfrica"):

    year   = int(t["year"])
    month  = f"{int(t['month']):02d}"
    day    = f"{int(t['day']):02d}"
    hour   = f"{int(t['hour']):02d}"
    minute = f"{int(t['minute']):02d}"

    base = Path("/gws/ssde/j25b/swift/earajr/NWCSAF_archive/netcdf_2018/RDT")

    date = f"{year}{month}{day}"
    time = f"{hour}{minute}00"

    fname = f"S_NWC_RDT-CW_MSG4_{domain}-VISIR_{date}T{time}Z.nc"
    path = base / date / fname

    if not path.exists():
        raise FileNotFoundError(f"RDT file not found: {path}")

    with Dataset(path) as ds:

        cat = ds["MapCellCatType"][:]
        lat = ds["lat"][:]
        lon = ds["lon"][:]

    cat = np.ma.filled(cat, np.nan)

    return cat, lat, lon

# Load thunderstorm severity

def load_ts(t):

    year   = f"{int(t['year']):04d}"
    month  = f"{int(t['month']):02d}"
    day    = f"{int(t['day']):02d}"
    hour   = f"{int(t['hour']):02d}"
    minute = f"{int(t['minute']):02d}"

    base = Path("/gws/ssde/j25b/swift/WISER-EWSA/DWD_AI_TS/data")

    t0 = datetime(
        int(year), int(month), int(day),
        int(hour), int(minute)
    )

    # bias backwards by one cycle
    t_file = t0 - timedelta(minutes=15)
    date_str = t_file.strftime("%Y%m%d")

    guess = (
        base / date_str /
        f"TSfc{t_file:%Y%m%d%H%M}EA.nc.bz2"
    )

    if guess.exists():
        ts_file = guess
    else:
        ts_dir = base / date_str

        if not ts_dir.exists():
            raise FileNotFoundError(f"TS directory not found: {ts_dir}")

        files = [f for f in os.listdir(ts_dir) if f.startswith("TSfc")]

        if len(files) == 0:
            raise FileNotFoundError(f"No TS files in directory: {ts_dir}")

        times = [
            datetime.strptime(f[4:16], "%Y%m%d%H%M")
            for f in files
        ]

        i = min(range(len(times)), key=lambda i: abs(times[i] - t0))
        ts_file = ts_dir / files[i]

    if not ts_file.exists():
        raise FileNotFoundError(f"TS file not found: {ts_file}")

    with bz2.open(ts_file, "rb") as f:
        ds = Dataset("inmemory.nc", memory=f.read())

    ts = ds.variables["TS"][:]          # (time, lat, lon)
    time_var = ds.variables["time"]
    times = num2date(time_var[:], units=time_var.units)

    idx = np.where(times <= t0)[0]

    if len(idx) > 0:
        i = idx[-1]
    else:
        i = np.argmin([abs(t - t0) for t in times])

    ts_t0 = ts[i]
    ts_t0 = np.ma.filled(ts_t0, np.nan)

    lat = ds.variables["lat"][:]
    lon = ds.variables["lon"][:]

    ds.close()

    lons, lats = np.meshgrid(lon, lat)

    return ts_t0, lats, lons


# Rain over africa

def load_roa(t):

    year   = f"{int(t['year']):04d}"
    month  = f"{int(t['month']):02d}"
    day    = f"{int(t['day']):02d}"
    hour   = f"{int(t['hour']):02d}"
    minute = f"{int(t['minute']):02d}"

    base = Path("/gws/ssde/j25b/swift/RoA")

    t0 = datetime(int(year), int(month), int(day),
                  int(hour), int(minute))
    t1 = t0 + timedelta(minutes=15)

    candidates = []
    for sat in ["MSG4", "MSG3"]:
        fname = (
            f"{sat}{t0:%Y%m%d}"
            f"-S{t0:%H%M}"
            f"-E{t1:%H%M}.nc"
        )
        candidates.append(base / year / month / fname)

    path = next((p for p in candidates if p.exists()), None)

    if path is None:
        raise FileNotFoundError(f"RoA file not found for time {t}")

    with Dataset(path) as ds:

        lat = ds.variables["latitude"][:]
        lon = ds.variables["longitude"][:]

        var = ds.variables["posterior_mean"]
        roa_raw = var[:]

        scale = getattr(var, "scale_factor", 1.0)
        offset = getattr(var, "add_offset", 0.0)

        roa = roa_raw * scale + offset
        roa = np.ma.filled(roa, np.nan)

    lons, lats = np.meshgrid(lon, lat)

    return roa, lats, lons

# Convective rainfall rate

def load_crr(t):

    year   = f"{int(t['year']):04d}"
    month  = f"{int(t['month']):02d}"
    day    = f"{int(t['day']):02d}"
    hour   = f"{int(t['hour']):02d}"
    minute = f"{int(t['minute']):02d}"

    base = Path("/gws/ssde/j25b/swift/WISER-EWSA/Leeds_CRR/data")

    t_dt = datetime(
        int(year), int(month), int(day),
        int(hour), int(minute)
    )

    date_str = t_dt.strftime("%Y%m%d")

    file_path = (
        base / date_str / "CRR" /
        f"S_NWC_CRR_MSG3_Africa-VISIR_{t_dt:%Y%m%dT%H%M}00Z.nc"
    )

    if not file_path.exists():
        raise FileNotFoundError(f"CRR file not found: {file_path}")

    with Dataset(file_path, mode="r") as ds:

        lat = ds.variables["lat"][:]
        lon = ds.variables["lon"][:]

        var = ds.variables["crr_intensity"]
        crr_raw = var[:]

        scale = getattr(var, "scale_factor", 1.0)
        offset = getattr(var, "add_offset", 0.0)

        crr = crr_raw * scale + offset
        crr = np.ma.filled(crr, np.nan)

    lons, lats = np.meshgrid(lon, lat)

    return crr, lats, lons


# MTG Lightning

def load_li(t):

    year   = f"{int(t['year']):04d}"
    month  = f"{int(t['month']):02d}"
    day    = f"{int(t['day']):02d}"
    hour   = f"{int(t['hour']):02d}"
    minute = f"{int(t['minute']):02d}"

    base = Path("/gws/ssde/j25b/swift/MTG_LI_pan_Africa")

    t_dt = datetime(
        int(year), int(month), int(day),
        int(hour), int(minute)
    )

    date_str = t_dt.strftime("%Y%m%d")

    file_path = (
        base / date_str /
        f"flash_accumulation_{t_dt:%Y%m%d%H%M%S}_15mins.nc"
    )

    if not file_path.exists():
        raise FileNotFoundError(f"LI file not found: {file_path}")

    with Dataset(file_path) as ds:

        lat = ds.variables["latitude"][:]
        lon = ds.variables["longitude"][:]

        flash = ds.variables["flash_accumulation"][:]
        flash = np.ma.filled(flash, np.nan)

    lons, lats = np.meshgrid(lon, lat)

    return flash, lats, lons
