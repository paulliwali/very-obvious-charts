import os
import sys
from math import pi

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from theme import PALETTE, apply_theme, save_chart

apply_theme()

YEAR = 2024
BOROUGHS = ["Bronx", "Brooklyn", "Manhattan", "Queens"]

hour_in_a_day = [str(i) for i in range(24)]
n_hours = len(hour_in_a_day)

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

COLOR_METRO = PALETTE["sienna"]
COLOR_OMNY = PALETTE["steel_blue"]


def plot_onto_axes(ax, metro_data, omny_data, angles):
    ax.plot(angles, metro_data, color=COLOR_METRO, linewidth=2.5, label="Metrocard")
    ax.plot(angles, omny_data, color=COLOR_OMNY, linewidth=2.5, linestyle="--", label="OMNY")


# Ordered young → old
fare_categories = [
    ("* Students *", "Metrocard - Students", "OMNY - Students"),
    ("~ Fair Fare ~", "Metrocard - Fair Fare", "OMNY - Full Fare"),
    ("+ Seniors & Disability +", "Metrocard - Seniors & Disability", "OMNY - Seniors & Disability"),
]


for borough in BOROUGHS:
    fig, axes = plt.subplots(1, 3, figsize=(24, 10), subplot_kw=dict(polar=True))
    fig.suptitle(
        f"{borough} — Metrocard vs OMNY Ridership ({YEAR})",
        y=0.98,
    )

    for ax in axes:
        ax.set_facecolor(PALETTE["bg"])
        ax.grid(color=PALETTE["text"], alpha=0.25, linewidth=0.8)
        ax.spines["polar"].set_color(PALETTE["text"])
        ax.spines["polar"].set_alpha(0.4)
        ax.fill_between(
            angles,
            0,
            1,
            where=[(19 <= i or i < 8) for i in range(24)]
            + [(19 <= i or i < 8) for i in range(1)],
            color=PALETTE["grid"],
            alpha=0.3,
        )

    for i, (ax, (title, metro_category, omny_category)) in enumerate(
        zip(axes, fare_categories)
    ):
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
            max_metro = max(metro_data)
            max_omny = max(omny_data)
            if max_metro > 0:
                metro_data = [x / max_metro for x in metro_data]
            if max_omny > 0:
                omny_data = [x / max_omny for x in omny_data]
            metro_data += metro_data[:1]
            omny_data += omny_data[:1]
            plot_onto_axes(ax, metro_data, omny_data, angles)

        ax.set_theta_direction(-1)
        ax.set_theta_offset(pi / 2)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(hour_in_a_day, fontsize=13)
        ax.tick_params(axis="y", labelsize=11)
        ax.set_title(title, pad=20, fontsize=18)

        # Only show legend on the first subplot
        if i == 0:
            ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), frameon=True, fontsize=12)

    # Age progression arrow below subplots
    fig.text(0.5, 0.02, "Youngest  ----------->  Oldest",
             ha="center", fontsize=14, color=PALETTE["text"], alpha=0.6)
    fig.subplots_adjust(top=0.88, bottom=0.08, wspace=0.4)
    save_chart(fig, f"{borough}_ridership_comparison")
