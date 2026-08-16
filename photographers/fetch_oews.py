"""Download BLS OEWS national files (2003-2025) and extract photography occupations.

OEWS = Occupational Employment and Wage Statistics. One zip per survey year at
https://www.bls.gov/oes/special-requests/oesm{yy}nat.zip

Caveat baked into this data: OEWS counts wage-and-salary jobs only. Self-employed
photographers (a majority of the trade) are not in these numbers.
"""

import os
import re
import glob
import zipfile
import urllib.request

import pandas as pd

# BLS blocks generic user agents; their policy asks for a contact address.
USER_AGENT = "very-obvious-charts/1.0 (paulliwali@hotmail.com)"
URL = "https://www.bls.gov/oes/special-requests/oesm{yy}nat.zip"
YEARS = range(2003, 2026)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
RAW_DIR = os.path.join(DATA_DIR, "oews_raw")
OUT_CSV = os.path.join(DATA_DIR, "oews_photography.csv")

OCCUPATIONS = {
    "00-0000": "All occupations",
    "27-4021": "Photographers",
    "51-9131": "Photographic process workers",           # pre-2010 SOC
    "51-9132": "Photographic processing machine operators",  # pre-2010 SOC
    "51-9151": "Photographic process workers and machine operators",  # 2010+ SOC
    "27-4031": "Camera operators, TV/video/film",
    "27-4032": "Film and video editors",
    "27-4011": "Audio and video technicians",
}


def download(year):
    yy = f"{year % 100:02d}"
    path = os.path.join(RAW_DIR, f"oesm{yy}nat.zip")
    if os.path.exists(path):
        return path
    os.makedirs(RAW_DIR, exist_ok=True)
    req = urllib.request.Request(URL.format(yy=yy), headers={"User-Agent": USER_AGENT})
    print(f"Downloading OEWS {year}...")
    with urllib.request.urlopen(req, timeout=60) as resp, open(path, "wb") as fh:
        fh.write(resp.read())
    return path


def national_sheet(zip_path):
    """Unpack and return the path of the national data workbook."""
    out_dir = zip_path[: -len(".zip")]
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(out_dir)
    hits = [
        p
        for p in glob.glob(f"{out_dir}/**/*", recursive=True)
        if re.search(r"national.*_dl\.xlsx?$", os.path.basename(p), re.I)
    ]
    if not hits:
        raise FileNotFoundError(f"no national workbook in {zip_path}")
    return hits[0]


def read_year(year):
    df = pd.read_excel(national_sheet(download(year)), dtype=str)
    df.columns = [c.lower() for c in df.columns]

    # 2019+ files ship every industry and ownership crosstab; keep the
    # cross-industry, all-ownership rows so every year means the same thing.
    if "naics" in df.columns:
        df = df[df["naics"].str.strip() == "000000"]
    if "own_code" in df.columns:
        df = df[df["own_code"].str.strip() == "1235"]

    df["occ_code"] = df["occ_code"].str.strip()
    df = df[df["occ_code"].isin(OCCUPATIONS)]

    rows = []
    for _, r in df.iterrows():
        emp = str(r["tot_emp"]).replace(",", "").strip()
        rows.append(
            {
                "year": year,
                "occ_code": r["occ_code"],
                "occ_title": OCCUPATIONS[r["occ_code"]],
                "employment": float(emp) if emp.replace(".", "", 1).isdigit() else None,
            }
        )
    return rows


if __name__ == "__main__":
    records = []
    for year in YEARS:
        records.extend(read_year(year))

    out = pd.DataFrame(records)
    os.makedirs(DATA_DIR, exist_ok=True)
    out.to_csv(OUT_CSV, index=False)
    print(f"Saved {OUT_CSV} ({len(out)} rows, {out['year'].nunique()} years)")
