# Prop 13 and California House Prices

Did California's 1978 property tax cap send house prices to the moon? California
against the US, plotted as a multiple of what a house cost the quarter Prop 13
passed. The y axis is log, so every gridline is a doubling and a steeper line
means faster growth — the chart's claim is about growth rates, and that is the
axis where rates read as steepness.

## Run

```bash
uv run python prop13-house-prices/fetch_hpi.py
uv run python prop13-house-prices/prop13-house-prices.py
```

`fetch_hpi.py` downloads two FHFA CSVs (cached in `data/fhfa_raw/`) and writes
`data/hpi_ca_us.csv` with both series indexed to 1978Q2.

## Data

[FHFA All-Transactions House Price Index](https://www.fhfa.gov/data/hpi/datasets),
quarterly, 1975Q1 – 2026Q1 — state file for California, national file for the US.
The all-transactions index is the only public house price series reaching back
before Proposition 13.

Note the FHFA CSVs ship with no header row; columns are code, year, quarter, index.

See [TAKEAWAY.md](TAKEAWAY.md) for the numbers, the mechanisms, and the caveats.
