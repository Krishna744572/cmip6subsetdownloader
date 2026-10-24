"""
NEX-GDDP-CMIP6 SUBSET DOWNLOADER
Downloads only your study area through the THREDDS NetcdfSubset service,
so each yearly file is a few KB to a few MB instead of about 220 MB.
"""
import sys
import time
import requests
from pathlib import Path

OUT = Path(r"E:\PHD_AND_CLIMATE_CMIP6\Ph.D\Subset_data")
NCSS = "https://ds.nccs.nasa.gov/thredds/ncss/grid/AMES/NEX/GDDP-CMIP6"

MODELS = [
    ("UKESM1-0-LL", "r1i1p1f2", "gn"), ("TaiESM1", "r1i1p1f1", "gn"),
    ("NorESM2-MM", "r1i1p1f1", "gn"), ("NorESM2-LM", "r1i1p1f1", "gn"),
    ("NESM3", "r1i1p1f1", "gn"), ("MRI-ESM2-0", "r1i1p1f1", "gn"),
    ("MPI-ESM1-2-LR", "r1i1p1f1", "gn"), ("MPI-ESM1-2-HR", "r1i1p1f1", "gn"),
    ("MIROC6", "r1i1p1f1", "gn"), ("MIROC-ES2L", "r1i1p1f2", "gn"),
    ("KIOST-ESM", "r1i1p1f1", "gr1"), ("KACE-1-0-G", "r1i1p1f1", "gr"),
    ("IPSL-CM6A-LR", "r1i1p1f1", "gr"), ("INM-CM5-0", "r1i1p1f1", "gr1"),
    ("INM-CM4-8", "r1i1p1f1", "gr1"), ("IITM-ESM", "r1i1p1f1", "gn"),
    ("HadGEM3-GC31-MM", "r1i1p1f3", "gn"), ("HadGEM3-GC31-LL", "r1i1p1f3", "gn"),
    ("GISS-E2-1-G", "r1i1p1f2", "gn"), ("GFDL-ESM4", "r1i1p1f1", "gr1"),
    ("GFDL-CM4_gr2", "r1i1p1f1", "gr2"), ("GFDL-CM4", "r1i1p1f1", "gr1"),
    ("FGOALS-g3", "r3i1p1f1", "gn"), ("EC-Earth3-Veg-LR", "r1i1p1f1", "gr"),
    ("EC-Earth3", "r1i1p1f1", "gr"), ("CanESM5", "r1i1p1f1", "gn"),
    ("CNRM-ESM2-1", "r1i1p1f2", "gr"), ("CNRM-CM6-1", "r1i1p1f2", "gr"),
    ("CMCC-ESM2", "r1i1p1f1", "gn"), ("CMCC-CM2-SR5", "r1i1p1f1", "gn"),
    ("CESM2-WACCM", "r3i1p1f1", "gn"), ("CESM2", "r4i1p1f1", "gn"),
    ("BCC-CSM2-MR", "r1i1p1f1", "gn"), ("ACCESS-ESM1-5", "r1i1p1f1", "gn"),
    ("ACCESS-CM2", "r1i1p1f1", "gn"),
]
SCENARIOS = ["historical", "ssp126", "ssp245", "ssp370", "ssp585"]
VARIABLES = ["pr", "tasmin", "tasmax", "tas", "sfcWind", "rsds", "rlds", "huss", "hurs"]


def pick(options, prompt, allow_all=True):
    for i, o in enumerate(options, 1):
        print(f"{i:02d}. {o}")
    if allow_all:
        print("00. ALL")
    s = input(prompt + " (example 1 or 2,3,5): ").strip()
    if s in ("0", "00"):
        return list(options)
    return [options[int(x) - 1] for x in s.split(",")]


def is_netcdf(path):
    with open(path, "rb") as f:
        head = f.read(4)
    return head[:3] == b"CDF" or head == b"\x89HDF"


def fetch(url, params, out, tries=5):
    if out.exists() and out.stat().st_size > 0 and is_netcdf(out):
        print("Already done:", out.name)
        return True
    part = out.with_suffix(".part")
    for i in range(tries):
        try:
            with requests.get(url, params=params, stream=True, timeout=300) as r:
                r.raise_for_status()
                with open(part, "wb") as f:
                    for chunk in r.iter_content(1 << 20):
                        f.write(chunk)
            if is_netcdf(part):
                part.replace(out)
                print("Downloaded:", out.name, f"({out.stat().st_size/1024:.0f} KB)")
                return True
            print("Reply was not a NetCDF file, retrying")
        except Exception as e:
            print("Error:", e)
        time.sleep(5 * (i + 1))
    return False


print("Select CMIP6 model\n")
names = [m[0] for m in MODELS]
for i, n in enumerate(names, 1):
    print(f"{i:02d}. {n}")
mi = int(input("\nEnter model number: ")) - 1
MODEL, RPF, GRID = MODELS[mi]
FILE_MODEL = "GFDL-CM4" if MODEL == "GFDL-CM4_gr2" else MODEL

print("\nScenarios")
scs = pick(SCENARIOS, "Choose scenarios")
print("\nVariables")
vars_ = pick(VARIABLES, "Choose variables")
y1 = int(input("Start year: "))
y2 = int(input("End year: "))

print("\nStudy area in decimal degrees (grid is 0.25 degrees, add a small margin)")
south = float(input("South latitude: "))
north = float(input("North latitude: "))
west = float(input("West longitude: "))
east = float(input("East longitude: "))
if south >= north or west >= east:
    sys.exit("Invalid box: south must be below north and west below east")

failed = []
for var in vars_:
    for sc in scs:
        lo, hi = (1950, 2014) if sc == "historical" else (2015, 2100)
        folder = OUT / var / sc / MODEL
        folder.mkdir(parents=True, exist_ok=True)
        print(f"\n{MODEL} {sc} {var}")
        for year in range(max(y1, lo), min(y2, hi) + 1):
            fname = f"{var}_day_{FILE_MODEL}_{sc}_{RPF}_{GRID}_{year}_v2.0.nc"
            url = f"{NCSS}/{MODEL}/{sc}/{RPF}/{var}/{fname}"
            params = {"var": var, "north": north, "south": south,
                      "east": east, "west": west, "horizontalStride": 1,
                      "temporal": "all", "accept": "netcdf"}
            out = folder / f"{var}_{MODEL}_{sc}_{year}.nc"
            if not fetch(url, params, out):
                failed.append(out.name)

print("\nFinished.")
if failed:
    print("These files failed, run again to retry them:")
    for n in failed:
        print(" ", n)
