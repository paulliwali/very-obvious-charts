import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from theme import PALETTE, apply_theme, save_chart

apply_theme()

mta_data = pd.read_csv(
    os.path.join(HERE, "data", "MTA_Subway_Hourly_Ridership__Beginning_February_2022_20240930.csv"),
    parse_dates=["transit_timestamp"],
)

mta_data["payment"] = mta_data["fare_class_category"].str.split(" - ").str[0]
mta_data["year_month"] = mta_data["transit_timestamp"].dt.to_period("M")

monthly = (
    mta_data.groupby(["year_month", "payment"])["ridership"]
    .sum()
    .reset_index()
)

pivoted = monthly.pivot(index="year_month", columns="payment", values="ridership").fillna(0)

pivoted["total"] = pivoted.sum(axis=1)
pivoted["omny_pct"] = pivoted["OMNY"] / pivoted["total"] * 100

fig, ax1 = plt.subplots(figsize=(14, 6))

x = range(len(pivoted))
labels = [str(p) for p in pivoted.index]

ax1.stackplot(
    x,
    pivoted["Metrocard"],
    pivoted["OMNY"],
    labels=["Metrocard", "OMNY"],
    colors=[PALETTE["steel_blue"], PALETTE["goldenrod"]],
    alpha=0.8,
)
ax1.set_ylabel("Total Monthly Ridership")
ax1.set_xlabel("")
ax1.tick_params(axis="x", rotation=45)
ax1.set_xticks(x[::3])
ax1.set_xticklabels(labels[::3], ha="right")
ax1.legend(loc="upper left")

ax2 = ax1.twinx()
ax2.plot(x, pivoted["omny_pct"], color=PALETTE["sienna"], linewidth=2.5, linestyle="--", label="OMNY % Share")
ax2.set_ylabel("OMNY Share (%)", color=PALETTE["sienna"])
ax2.tick_params(axis="y", labelcolor=PALETTE["sienna"])
ax2.set_ylim(0, 100)
ax2.legend(loc="center right")

plt.title("OMNY Is Eating Metrocard: Monthly Ridership by Payment System", pad=15)

save_chart(fig, "omny_adoption", subdir=HERE)
