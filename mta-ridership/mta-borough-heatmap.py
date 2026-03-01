import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="white")

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

# Normalize each borough column to its own max (0–1 scale)
normalized = pivoted / pivoted.max()

# Reorder columns by total ridership descending
col_order = pivoted.sum().sort_values(ascending=False).index.tolist()
normalized = normalized[col_order]

fig, ax = plt.subplots(figsize=(8, 10))
sns.heatmap(
    normalized,
    cmap="YlOrRd",
    linewidths=0.5,
    linecolor="white",
    ax=ax,
    vmin=0,
    vmax=1,
    cbar_kws={"label": "Ridership (fraction of borough peak)"},
)

ax.set_ylabel("Hour of Day", fontsize=12)
ax.set_xlabel("")
ax.set_title(
    "Manhattan Never Sleeps (But the Bronx Does)\nMean Hourly Ridership Normalized per Borough",
    fontsize=14,
    pad=15,
)

# Label hour ticks nicely
hour_labels = [f"{h}:00" for h in range(24)]
ax.set_yticklabels(hour_labels, rotation=0)

fig.tight_layout()
plt.savefig("reports/borough_heatmap.png", dpi=150)
plt.close(fig)
print("Saved reports/borough_heatmap.png")
