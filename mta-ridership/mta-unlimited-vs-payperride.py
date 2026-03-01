import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")

FARE_CLASSES = [
    "Metrocard - Unlimited 30-Day",
    "Metrocard - Unlimited 7-Day",
    "Metrocard - Full Fare",
    "OMNY - Full Fare",
]

COLORS = {
    "Metrocard - Unlimited 30-Day": "#1565C0",
    "Metrocard - Unlimited 7-Day": "#42A5F5",
    "Metrocard - Full Fare": "#E65100",
    "OMNY - Full Fare": "#FF9800",
}

STYLES = {
    "Metrocard - Unlimited 30-Day": "-",
    "Metrocard - Unlimited 7-Day": "--",
    "Metrocard - Full Fare": "-",
    "OMNY - Full Fare": "--",
}

mta_data = pd.read_csv(
    "data/MTA_Subway_Hourly_Ridership__Beginning_February_2022_20240930.csv",
    parse_dates=["transit_timestamp"],
)

mta_data = mta_data.loc[mta_data["fare_class_category"].isin(FARE_CLASSES)]
mta_data["hour"] = mta_data["transit_timestamp"].dt.hour

hourly = (
    mta_data.groupby(["fare_class_category", "hour"])["ridership"]
    .mean()
    .reset_index()
)

# Normalize each fare class to its own peak hour
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

ax.set_xlabel("Hour of Day", fontsize=12)
ax.set_ylabel("Ridership (normalized to peak)", fontsize=12)
ax.set_xticks(range(24))
ax.set_xticklabels([f"{h}" for h in range(24)])
ax.set_title(
    "Unlimited Cards Are for Commuters\nNormalized Hourly Ridership by Fare Class",
    fontsize=14,
    pad=15,
)
ax.legend(fontsize=10)

fig.tight_layout()
plt.savefig("reports/unlimited_vs_payperride.png", dpi=150)
plt.close(fig)
print("Saved reports/unlimited_vs_payperride.png")
