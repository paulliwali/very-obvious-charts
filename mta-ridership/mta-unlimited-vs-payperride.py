import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from theme import PALETTE, apply_theme, save_chart

apply_theme()

FARE_CLASSES = [
    "Metrocard - Unlimited 30-Day",
    "Metrocard - Unlimited 7-Day",
    "Metrocard - Full Fare",
    "OMNY - Full Fare",
]

COLORS = {
    "Metrocard - Unlimited 30-Day": PALETTE["sienna"],
    "Metrocard - Unlimited 7-Day": PALETTE["goldenrod"],
    "Metrocard - Full Fare": PALETTE["steel_blue"],
    "OMNY - Full Fare": PALETTE["olive"],
}

STYLES = {
    "Metrocard - Unlimited 30-Day": "-",
    "Metrocard - Unlimited 7-Day": "--",
    "Metrocard - Full Fare": "-",
    "OMNY - Full Fare": "--",
}

mta_data = pd.read_csv(
    os.path.join(HERE, "data", "MTA_Subway_Hourly_Ridership__Beginning_February_2022_20240930.csv"),
    parse_dates=["transit_timestamp"],
)

mta_data = mta_data.loc[mta_data["fare_class_category"].isin(FARE_CLASSES)]
mta_data["hour"] = mta_data["transit_timestamp"].dt.hour

hourly = (
    mta_data.groupby(["fare_class_category", "hour"])["ridership"]
    .mean()
    .reset_index()
)

hourly["normalized"] = hourly.groupby("fare_class_category")["ridership"].transform(
    lambda s: s / s.max()
)

fig, ax = plt.subplots(figsize=(12, 6))

for fare_class in FARE_CLASSES:
    subset = hourly.loc[hourly["fare_class_category"] == fare_class]
    ax.plot(
        subset["hour"],
        subset["normalized"],
        color=COLORS[fare_class],
        linestyle=STYLES[fare_class],
        linewidth=2.5,
        label=fare_class,
    )

ax.set_xlabel("Hour of Day")
ax.set_ylabel("Ridership (normalized to peak)")
ax.set_xticks(range(24))
ax.set_xticklabels([f"{h}" for h in range(24)])
ax.set_title(
    "Unlimited Cards Are for Commuters\nNormalized Hourly Ridership by Fare Class",
    pad=15,
)
ax.legend()

save_chart(fig, "unlimited_vs_payperride", subdir=HERE)
