import os
import sys

import matplotlib.pyplot as plt
import polars as pl
import seaborn as sns
from gender_guesser.detector import Detector
from nba_api.stats.static import players

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from theme import PALETTE, apply_theme, save_chart

GENDER_ORDER = ["male", "mostly_male", "andy", "unknown", "mostly_female", "female"]
GENDER_LABELS = {
    "male": "Male",
    "mostly_male": "Mostly\nMale",
    "andy": "Androgynous",
    "unknown": "Unknown",
    "mostly_female": "Mostly\nFemale",
    "female": "Female",
}

if __name__ == "__main__":
    apply_theme()
    sns.set_palette(PALETTE["accents"])

    all_players = players.get_players()
    nba_player_df = pl.DataFrame(all_players)

    gender_detector = Detector()
    nba_player_df = nba_player_df.with_columns(
        pl.col("first_name")
        .map_elements(lambda x: gender_detector.get_gender(x), return_dtype=pl.Utf8)
        .alias("gender")
    )

    gender_counts = (
        nba_player_df.group_by("gender")
        .len()
        .sort("len", descending=True)
    )
    print(gender_counts)

    # Order categories for the chart
    ordered = []
    for g in GENDER_ORDER:
        row = gender_counts.filter(pl.col("gender") == g)
        if len(row) > 0:
            ordered.append({"gender": g, "count": row["len"][0]})
    plot_df = pl.DataFrame(ordered)

    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    bars = ax.bar(
        range(len(plot_df)),
        plot_df["count"],
        color=PALETTE["accents"][0],
        edgecolor=PALETTE["text"],
        linewidth=0.8,
    )

    # Add count labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 15,
            str(int(height)),
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight="bold",
        )

    ax.set_xticks(range(len(plot_df)))
    ax.set_xticklabels([GENDER_LABELS[g] for g in plot_df["gender"]])
    ax.set_ylabel("Number of Players")
    ax.set_xlabel("")
    fig.suptitle(
        "NBA Players' Gender Guessed by First Name",
        fontsize=18,
        y=0.97,
    )
    ax.text(
        0.5, -0.18,
        f"All {len(nba_player_df):,} NBA players (historical) · gender-guesser library",
        transform=ax.transAxes,
        ha="center",
        fontsize=10,
        style="italic",
        color=PALETTE["text"],
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Takeaway
    ax.text(
        0.98, 0.95,
        "Takeaway: NBA players\ntend to have male names.",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=13,
        fontweight="bold",
        color=PALETTE["text"],
        bbox=dict(
            boxstyle="round,pad=0.4",
            facecolor=PALETTE["goldenrod"],
            edgecolor=PALETTE["text"],
            alpha=0.85,
        ),
    )

    save_chart(fig, "nba-player-gender-guess", subdir=".")
