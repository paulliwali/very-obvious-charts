"""Did smartphones kill the professional photographer? BLS says: not the photographer.

Indexes US wage-and-salary employment to 2007 = 100 (the year the iPhone shipped)
for photographers, photo-lab workers, and film/video editors.
Data: BLS OEWS national files, see fetch_oews.py.
"""

import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from theme import PALETTE, apply_theme, save_chart

CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "oews_photography.csv")
BASE_YEAR = 2007  # iPhone launch

# Photo-lab work was split across two SOC codes until the 2010 revision merged them.
LAB_CODES = ["51-9131", "51-9132", "51-9151"]

SERIES = [
    ("photo_lab", "Photo-lab &\nfilm processing", PALETTE["steel_blue"], 2.6),
    ("27-4021", "Photographers", PALETTE["sienna"], 3.4),
    ("27-4032", "Film & video\neditors", PALETTE["olive"], 2.6),
    ("00-0000", "All US jobs", PALETTE["saddle_brown"], 1.6),
]


def load():
    df = pd.read_csv(CSV)
    wide = df.pivot_table(index="year", columns="occ_code", values="employment", aggfunc="first")
    wide["photo_lab"] = wide[LAB_CODES].sum(axis=1, min_count=1)
    return wide


if __name__ == "__main__":
    apply_theme()
    wide = load()

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.axhline(100, color=PALETTE["grid"], linewidth=1)

    for code, label, color, width in SERIES:
        indexed = wide[code] / wide.loc[BASE_YEAR, code] * 100
        dashed = code == "00-0000"
        ax.plot(
            indexed.index,
            indexed.values,
            color=color,
            linewidth=width,
            linestyle="--" if dashed else "-",
            marker="" if dashed else "o",
            markersize=4,
            alpha=0.75 if dashed else 1.0,
        )
        ax.text(
            indexed.index[-1] + 0.35,
            indexed.iloc[-1],
            f"{label}\n{indexed.iloc[-1]:.0f}",
            color=color,
            va="center",
            fontsize=12,
            fontweight="bold",
        )

    # iPhone launch line
    ax.axvline(BASE_YEAR, color=PALETTE["text"], linewidth=1.2, linestyle=":")
    ax.annotate(
        "iPhone ships",
        xy=(BASE_YEAR, 175),
        xytext=(2004.2, 188),
        fontsize=12,
        style="italic",
        color=PALETTE["text"],
        arrowprops=dict(arrowstyle="->", color=PALETTE["text"], linewidth=1.2),
    )

    ax.set_xlim(2002.5, 2029.5)
    ax.set_ylim(-6, 200)
    ax.set_xticks(range(2003, 2026, 2))
    ax.set_yticks(range(0, 201, 50))
    ax.set_ylabel(f"Employment, indexed to {BASE_YEAR} = 100")
    ax.grid(axis="y", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.suptitle(
        "Smartphones Didn't Kill Photographers. They Killed the Photo Lab.",
        fontsize=18,
        y=0.97,
    )
    ax.text(
        0.5, -0.14,
        "US wage-and-salary employment · BLS Occupational Employment & Wage Statistics, "
        "2003–2025 · excludes self-employed",
        transform=ax.transAxes,
        ha="center",
        fontsize=10,
        style="italic",
        color=PALETTE["text"],
    )

    photog_chg = wide.loc[2025, "27-4021"] / wide.loc[BASE_YEAR, "27-4021"] - 1
    lab_chg = wide.loc[2025, "photo_lab"] / wide.loc[BASE_YEAR, "photo_lab"] - 1
    ax.text(
        0.02, 0.06,
        f"Takeaway: since 2007, photographers are down {abs(photog_chg):.0%}.\n"
        f"The people who developed the film are down {abs(lab_chg):.0%}.",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
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

    save_chart(fig, "photographers-vs-photo-labs", subdir=os.path.dirname(os.path.abspath(__file__)))
