import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from theme import PALETTE, apply_theme, save_chart

apply_theme()

mta_data = pd.read_csv(
    "data/MTA_Subway_Hourly_Ridership__Beginning_February_2022_20240930.csv",
    parse_dates=["transit_timestamp"],
)

mta_data["hour"] = mta_data["transit_timestamp"].dt.hour

hourly_borough = (
    mta_data.groupby(["borough", "hour"])["ridership"]
    .mean()
    .reset_index()
)

pivoted = hourly_borough.pivot(index="hour", columns="borough", values="ridership")

normalized = pivoted / pivoted.max()

col_order = pivoted.sum().sort_values(ascending=False).index.tolist()
normalized = normalized[col_order]

fig, ax = plt.subplots(figsize=(8, 10))
sns.heatmap(
    normalized,
    cmap="YlOrRd",
    linewidths=0.5,
    linecolor=PALETTE["bg"],
    ax=ax,
    vmin=0,
    vmax=1,
    cbar_kws={"label": "Ridership (fraction of borough peak)"},
)

ax.set_ylabel("Hour of Day")
ax.set_xlabel("")
ax.set_title(
    "Manhattan Never Sleeps (But the Bronx Does)\nMean Hourly Ridership Normalized per Borough",
    pad=15,
)

hour_labels = [f"{h}:00" for h in range(24)]
ax.set_yticklabels(hour_labels, rotation=0)

save_chart(fig, "borough_heatmap")
