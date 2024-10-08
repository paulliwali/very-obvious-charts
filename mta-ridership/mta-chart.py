import matplotlib.pyplot as plt
from math import pi
import pandas as pd
import seaborn as sns

YEAR = 2024
BOROUGHS = ["Bronx", "Brooklyn", "Manhattan", "Queens"]

hour_in_a_day = [str(i) for i in range(24)]  # 24 hours from 0 to 23
n_hours = len(hour_in_a_day)

# Calculate angle for each hour (24-hour format)
angles = [n / float(n_hours) * 2 * pi for n in range(n_hours)]
angles += angles[:1]

mta_data = pd.read_csv(
    "data/MTA_Subway_Hourly_Ridership__Beginning_February_2022_20240930.csv",
    parse_dates=["transit_timestamp"],
)

mta_data = mta_data.loc[
    mta_data["fare_class_category"].isin(
        [
            "Metrocard - Fair Fare",
            "Metrocard - Seniors & Disability",
            "Metrocard - Students",
            "OMNY - Full Fare",
            "OMNY - Seniors & Disability",
            "OMNY - Students",
        ]
    )
]
mta_data["year"] = mta_data["transit_timestamp"].dt.year
mta_data["hour"] = mta_data["transit_timestamp"].dt.hour

mta_hourly_mean_ridership = (
    mta_data.groupby(["borough", "fare_class_category", "year", "hour"])[["ridership"]]
    .mean()
    .reset_index()
)

# Create a color palette using seaborn to add hue for each fare class category
palette = sns.color_palette(
    "tab10", len(mta_hourly_mean_ridership["fare_class_category"].unique())
)
color_map = dict(
    zip(mta_hourly_mean_ridership["fare_class_category"].unique(), palette)
)


def plot_onto_axes(
    ax, metro_data, omny_data, metro_label, omny_label, color_metro, color_omny, angles
):
    # Plot each dataset
    ax.plot(angles, metro_data, color=color_metro, linewidth=2, label=metro_label)
    ax.plot(
        angles,
        omny_data,
        color=color_omny,
        linewidth=2,
        linestyle="--",
        label=omny_label,
    )


fare_categories = [
    ("Fair Fare", "Metrocard - Fair Fare", "OMNY - Full Fare"),
    (
        "Seniors & Disability",
        "Metrocard - Seniors & Disability",
        "OMNY - Seniors & Disability",
    ),
    ("Students", "Metrocard - Students", "OMNY - Students"),
]


for borough in BOROUGHS:
    fig, axes = plt.subplots(1, 3, figsize=(24, 8), subplot_kw=dict(polar=True))
    fig.suptitle(
        f"{borough} - Metrocard vs OMNY Ridership for Fair Fare, Seniors, and Students ({YEAR})",
        fontsize=16,
    )

    # Shade the background to represent day and night
    for ax in axes:
        ax.fill_between(
            angles,
            0,
            1,
            where=[(19 <= i or i < 8) for i in range(24)]
            + [(19 <= i or i < 8) for i in range(1)],
            color="lightgray",
            alpha=0.3,
        )

    for ax, (title, metro_category, omny_category) in zip(axes, fare_categories):
        metro_data = mta_hourly_mean_ridership.loc[
            (mta_hourly_mean_ridership["borough"] == borough)
            & (mta_hourly_mean_ridership["year"] == YEAR)
            & (mta_hourly_mean_ridership["fare_class_category"] == metro_category),
            "ridership",
        ].to_list()

        omny_data = mta_hourly_mean_ridership.loc[
            (mta_hourly_mean_ridership["borough"] == borough)
            & (mta_hourly_mean_ridership["year"] == YEAR)
            & (mta_hourly_mean_ridership["fare_class_category"] == omny_category),
            "ridership",
        ].to_list()

        if len(metro_data) == 24 and len(omny_data) == 24:
            # Normalize the data separately for Metrocard and OMNY
            max_metro = max(metro_data)
            max_omny = max(omny_data)
            if max_metro > 0:
                metro_data = [x / max_metro for x in metro_data]
            if max_omny > 0:
                omny_data = [x / max_omny for x in omny_data]
            # To close the polygon, we append the first value to the end
            metro_data += metro_data[:1]
            omny_data += omny_data[:1]
            plot_onto_axes(
                ax=ax,
                metro_data=metro_data,
                omny_data=omny_data,
                metro_label=metro_category,
                omny_label=omny_category,
                color_metro=color_map[metro_category],
                color_omny=color_map[omny_category],
                angles=angles,
            )

        # Rotate the direction to make it clockwise
        ax.set_theta_direction(-1)

        # Rotate the starting position to align 0 at the top (12 o'clock position)
        ax.set_theta_offset(pi / 2)

        # Add the category labels to the chart (0 to 23 hours)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(hour_in_a_day)

        ax.set_title(title, fontsize=14)
        ax.legend(loc="upper right", fontsize=10, frameon=True)

    # Adjust layout
    plt.tight_layout(rect=[0, 0.1, 1, 0.95], w_pad=5, h_pad=2)

    # Save the plot locally
    plt.savefig(f"reports/{borough}_ridership_comparison.png")
    plt.close(fig)
# Adjust layout
plt.tight_layout(rect=[0, 0.1, 1, 0.95], w_pad=5, h_pad=2)
