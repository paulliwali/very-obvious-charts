import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")

mta_data = pd.read_csv(
    "data/MTA_Subway_Hourly_Ridership__Beginning_February_2022_20240930.csv",
    parse_dates=["transit_timestamp"],
)

# Extract payment system from fare_class_category
mta_data["payment"] = mta_data["fare_class_category"].str.split(" - ").str[0]
mta_data["year_month"] = mta_data["transit_timestamp"].dt.to_period("M")

monthly = (
    mta_data.groupby(["year_month", "payment"])["ridership"]
    .sum()
    .reset_index()
)

pivoted = monthly.pivot(index="year_month", columns="payment", values="ridership").fillna(0)

# OMNY % share
pivoted["total"] = pivoted.sum(axis=1)
pivoted["omny_pct"] = pivoted["OMNY"] / pivoted["total"] * 100

fig, ax1 = plt.subplots(figsize=(14, 6))

x = range(len(pivoted))
labels = [str(p) for p in pivoted.index]

# Stacked area
ax1.stackplot(
    x,
    pivoted["Metrocard"],
    pivoted["OMNY"],
    labels=["Metrocard", "OMNY"],
    colors=["#2196F3", "#FF9800"],
    alpha=0.8,
)
ax1.set_ylabel("Total Monthly Ridership", fontsize=12)
ax1.set_xlabel("")
ax1.tick_params(axis="x", rotation=45)
ax1.set_xticks(x[::3])
ax1.set_xticklabels(labels[::3], ha="right")
ax1.legend(loc="upper left", fontsize=10)

# Secondary axis for OMNY %
ax2 = ax1.twinx()
ax2.plot(x, pivoted["omny_pct"], color="#D32F2F", linewidth=2.5, linestyle="--", label="OMNY % Share")
ax2.set_ylabel("OMNY Share (%)", fontsize=12, color="#D32F2F")
ax2.tick_params(axis="y", labelcolor="#D32F2F")
ax2.set_ylim(0, 100)
ax2.legend(loc="center right", fontsize=10)

plt.title("OMNY Is Eating Metrocard: Monthly Ridership by Payment System", fontsize=15, pad=15)
fig.tight_layout()
plt.savefig("reports/omny_adoption.png", dpi=150)
plt.close(fig)
print("Saved reports/omny_adoption.png")
