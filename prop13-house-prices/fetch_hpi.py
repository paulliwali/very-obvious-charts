"""Download the FHFA House Price Index for California and the US.

All-Transactions index, quarterly, 1975Q1 onward — the only public house price
series that starts before Proposition 13 passed in June 1978.

https://www.fhfa.gov/data/hpi/datasets
"""

import os
import urllib.request

import pandas as pd

BASE = "https://www.fhfa.gov/hpi/download/quarterly_datasets/"
FILES = {"state": "hpi_at_state.csv", "us": "hpi_at_us_and_census.csv"}
COLUMNS = ["code", "year", "quarter", "hpi"]  # the FHFA CSVs ship without a header

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
RAW_DIR = os.path.join(DATA_DIR, "fhfa_raw")
OUT_CSV = os.path.join(DATA_DIR, "hpi_ca_us.csv")

PROP13_YEAR, PROP13_QUARTER = 1978, 2  # passed June 6, 1978


def download(name):
    path = os.path.join(RAW_DIR, FILES[name])
    if os.path.exists(path):
        return path
    os.makedirs(RAW_DIR, exist_ok=True)
    req = urllib.request.Request(BASE + FILES[name], headers={"User-Agent": "Mozilla/5.0"})
    print(f"Downloading FHFA {FILES[name]}...")
    with urllib.request.urlopen(req, timeout=90) as resp, open(path, "wb") as fh:
        fh.write(resp.read())
    return path


if __name__ == "__main__":
    state = pd.read_csv(download("state"), names=COLUMNS)
    nation = pd.read_csv(download("us"), names=COLUMNS)

    ca = state[state["code"] == "CA"]
    usa = nation[nation["code"] == "USA"]

    df = ca.merge(usa, on=["year", "quarter"], suffixes=("_ca", "_us"))
    df = df[["year", "quarter", "hpi_ca", "hpi_us"]]
    df["t"] = df["year"] + (df["quarter"] - 1) / 4

    base = df[(df["year"] == PROP13_YEAR) & (df["quarter"] == PROP13_QUARTER)].iloc[0]
    df["ca_indexed"] = df["hpi_ca"] / base["hpi_ca"] * 100
    df["us_indexed"] = df["hpi_us"] / base["hpi_us"] * 100
    df["ca_premium"] = df["ca_indexed"] / df["us_indexed"]

    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(OUT_CSV, index=False)
    print(f"Saved {OUT_CSV} ({len(df)} quarters, {df['t'].min():.2f}–{df['t'].max():.2f})")
