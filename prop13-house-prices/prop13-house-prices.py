"""Did Proposition 13 send California house prices to the moon?

The obvious chart says no: the run-up that everyone blames on Prop 13 was already
running when voters went to the polls in June 1978. Data: FHFA House Price Index,
see fetch_hpi.py.

Prices are plotted as a multiple of their value the quarter Prop 13 passed, so
"4x" means a house costs four times what it did in June 1978. The y axis is log:
equal heights are equal percentage gains, which is the only way the claim in the
title — that the pre-vote run-up was the steepest stretch on the chart — is
something a reader can check by eye rather than take on trust.
"""

import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from theme import PALETTE, apply_theme, save_chart

CSV = os.path.join(HERE, "data", "hpi_ca_us.csv")
VOTE = 1978.25  # 1978Q2, Prop 13 passed June 6
RUNUP_START = 1975.0  # first quarter FHFA publishes


def growth(df, column, start_t, end_t):
    a = df.loc[(df["t"] - start_t).abs().idxmin(), column]
    b = df.loc[(df["t"] - end_t).abs().idxmin(), column]
    return b / a - 1


def annual_growth(df, column, start_t, end_t):
    """Compound growth per year — the quantity the log axis renders as slope."""
    return (1 + growth(df, column, start_t, end_t)) ** (1 / (end_t - start_t)) - 1


if __name__ == "__main__":
    apply_theme()
    df = pd.read_csv(CSV)
    end_t = df["t"].max()

    # Indexed to 100 in the source data; a multiple of the 1978 level reads better.
    df["ca_x"] = df["ca_indexed"] / 100
    df["us_x"] = df["us_indexed"] / 100

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.axvspan(RUNUP_START, VOTE, color=PALETTE["goldenrod"], alpha=0.3, zorder=0)
    ax.axvline(VOTE, color=PALETTE["text"], linewidth=1.4, linestyle=":")

    for col, label, color in [
        ("ca_x", "California", PALETTE["sienna"]),
        ("us_x", "United States", PALETTE["steel_blue"]),
    ]:
        ax.plot(df["t"], df[col], color=color, linewidth=2.8)
        ax.text(
            end_t + 0.8,
            df[col].iloc[-1],
            f"{label}\n{df[col].iloc[-1]:.1f}x",
            color=color,
            va="center",
            fontsize=13,
            fontweight="bold",
        )

    # Log axis: every gridline is a doubling, so equal steepness is equal % growth.
    ax.set_yscale("log")
    ax.set_yticks([0.5, 1, 2, 4, 8, 16])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}x"))
    ax.set_ylim(0.4, 22)
    ax.set_xlim(1974.5, end_t + 6)
    ax.set_xticks(range(1980, 2030, 10))
    ax.set_ylabel("What a house costs,\ncompared with June 1978")
    ax.grid(axis="y", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    pre_ca = growth(df, "ca_x", RUNUP_START, VOTE)
    pre_us = growth(df, "us_x", RUNUP_START, VOTE)
    pre_ca_yr = annual_growth(df, "ca_x", RUNUP_START, VOTE)
    pre_us_yr = annual_growth(df, "us_x", RUNUP_START, VOTE)
    post_ca_yr = annual_growth(df, "ca_x", VOTE, end_t)
    post_us_yr = annual_growth(df, "us_x", VOTE, end_t)

    ax.text(
        VOTE + 0.6, 18,
        "Prop 13 passes",
        ha="left", va="center", fontsize=12, style="italic", color=PALETTE["text"],
    )

    # Spell out what the log axis is doing, since a reader who misses it will
    # under-read the recent boom and misjudge every slope on the chart.
    ax.annotate(
        "",
        xy=(1984, 4), xytext=(1984, 8),
        arrowprops=dict(arrowstyle="<->", color=PALETTE["text"], linewidth=1.4),
    )
    ax.text(
        1985.2, 5.7,
        "every step up the axis is a doubling,\nso a steeper line = faster growth",
        ha="left", va="center", fontsize=11, style="italic", color=PALETTE["text"],
    )

    # Growth rates, the quantity slope encodes here.
    ax.annotate(
        f"the 3 years before the vote\nCalifornia {pre_ca_yr:+.0%} a year\n"
        f"the country {pre_us_yr:+.0%} a year",
        xy=(1976.6, 0.72),
        xytext=(1982.5, 0.45),
        fontsize=12,
        color=PALETTE["sienna"],
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=PALETTE["text"], linewidth=1.2),
    )
    ax.text(
        2003, 1.45,
        f"the 48 years after\nCalifornia {post_ca_yr:+.1%} a year\n"
        f"the country {post_us_yr:+.1%} a year",
        ha="left", va="center", fontsize=12, fontweight="bold", color=PALETTE["text"],
    )

    fig.suptitle(
        "California Housing Took Off Before Prop 13, Not After",
        fontsize=18,
        y=0.97,
    )
    ax.text(
        0.5, -0.13,
        "FHFA All-Transactions House Price Index, 1975Q1–2026Q1 · "
        "Proposition 13 passed June 6, 1978",
        transform=ax.transAxes,
        ha="center",
        fontsize=10,
        style="italic",
        color=PALETTE["text"],
    )

    ax.text(
        0.31, 0.96,
        f"Takeaway: California rose {pre_ca:.0%} against the country's {pre_us:.0%} in the\n"
        "3 years before the vote. Nothing after it is anywhere near that steep.",
        transform=ax.transAxes,
        ha="left",
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

    save_chart(fig, "prop13-house-prices", subdir=HERE)
