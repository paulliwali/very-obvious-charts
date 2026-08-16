# Photographers vs. the Photo Lab

Did smartphones kill the professional photographer? BLS payroll data, indexed to
2007 (the year the iPhone shipped).

## Run

```bash
uv run python photographers/fetch_oews.py
uv run python photographers/photographers-vs-photo-labs.py
```

`fetch_oews.py` downloads the BLS OEWS national files for 2003–2025 (~23 zips,
cached in `data/oews_raw/`) and writes `data/oews_photography.csv`. The chart
script reads only that CSV.

## Data

[BLS Occupational Employment and Wage Statistics](https://www.bls.gov/oes/tables.htm),
national cross-industry files, May 2003 – May 2025. Wage-and-salary employment
only — self-employed photographers are excluded. Photo-lab work moved from SOC
51-9131 + 51-9132 to a merged 51-9151 in the 2010 SOC revision; the script sums
across all three.

See [TAKEAWAY.md](TAKEAWAY.md) for the numbers and the caveats.
