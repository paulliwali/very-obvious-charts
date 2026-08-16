"""Generate profile-picture logos: crops of this repo's own charts.

Same look as the plots — flat notebook paper, smooth thick strokes, palette
colours, no decoration. Lines run off the edges so the mark reads as a
close crop of a real chart rather than an icon of one. Square 1024x1024,
composed for the circular crop Instagram applies to profile pictures.
"""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from theme import PALETTE, apply_theme

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "reports")
SIZE_PX = 1024
DPI = 128
BLEED = 0.06  # how far strokes run past the frame


def new_canvas():
    fig = plt.figure(figsize=(SIZE_PX / DPI, SIZE_PX / DPI), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_axis_off()
    ax.set_facecolor(PALETTE["bg"])
    return fig, ax


def fit(v, lo, hi, vmin=None, vmax=None):
    """Map a series onto [lo, hi] using a shared min/max across series."""
    v = np.asarray(v, float)
    vmin = np.nanmin(v) if vmin is None else vmin
    vmax = np.nanmax(v) if vmax is None else vmax
    return lo + (v - vmin) / (vmax - vmin) * (hi - lo)


def save(fig, path):
    fig.savefig(path, dpi=DPI, facecolor=PALETTE["bg"])
    plt.close(fig)
    print(f"Saved {path}")


def variant_prop13(path):
    """California against the country, cropped to the divergence."""
    df = pd.read_csv(os.path.join(HERE, "prop13-house-prices", "data", "hpi_ca_us.csv"))
    # Log scale, as a price index deserves: the exponential straightens out and
    # the gap between the two lines becomes the subject.
    ca_l, us_l = np.log(df["ca_indexed"]), np.log(df["us_indexed"])

    x = fit(df["t"], -BLEED, 1 + BLEED)
    lo, hi = min(ca_l.min(), us_l.min()), max(ca_l.max(), us_l.max())
    ca = fit(ca_l, 0.12, 0.88, lo, hi)
    us = fit(us_l, 0.12, 0.88, lo, hi)

    fig, ax = new_canvas()
    ax.plot(x, us, color=PALETTE["steel_blue"], lw=17, solid_capstyle="round")
    ax.plot(x, ca, color=PALETTE["sienna"], lw=17, solid_capstyle="round")
    save(fig, path)


def variant_photo(path):
    """The photo-lab collapse: one line falls off the bottom, one holds."""
    csv = os.path.join(HERE, "photographers", "data", "oews_photography.csv")
    wide = pd.read_csv(csv).pivot_table(
        index="year", columns="occ_code", values="employment", aggfunc="first"
    )
    wide["photo_lab"] = wide[["51-9131", "51-9132", "51-9151"]].sum(axis=1, min_count=1)

    x = fit(wide.index, -BLEED, 1 + BLEED)
    series = [
        ("photo_lab", PALETTE["steel_blue"], 17),
        ("27-4021", PALETTE["sienna"], 17),
        ("27-4032", PALETTE["olive"], 11),
    ]
    idx = {c: wide[c] / wide.loc[2007, c] * 100 for c, _, _ in series}
    lo = min(float(s.min()) for s in idx.values())
    hi = max(float(s.max()) for s in idx.values())

    fig, ax = new_canvas()
    ax.axhline(fit([100], 0.10, 0.90, lo, hi)[0], color=PALETTE["grid"], lw=5)
    for code, color, lw in series:
        ax.plot(x, fit(idx[code], 0.10, 0.90, lo, hi), color=color, lw=lw,
                solid_capstyle="round")
    save(fig, path)


def variant_fan(path):
    """No data — four palette series spreading apart, the house pattern."""
    t = np.linspace(-BLEED, 1 + BLEED, 300)
    spread = np.clip((t - 0.08) / 0.92, 0, None) ** 1.6

    fig, ax = new_canvas()
    for k, color in zip(
        [1.00, 0.34, -0.30, -0.86],
        [PALETTE["sienna"], PALETTE["goldenrod"], PALETTE["steel_blue"], PALETTE["olive"]],
    ):
        wave = 0.02 * np.sin(t * 7 + k * 3)
        ax.plot(t, 0.5 + k * 0.44 * spread + wave, color=color, lw=17,
                solid_capstyle="round")
    save(fig, path)


VARIANTS = {
    "logo-prop13": variant_prop13,
    "logo-photo": variant_photo,
    "logo-fan": variant_fan,
}


if __name__ == "__main__":
    apply_theme()
    os.makedirs(OUT_DIR, exist_ok=True)
    wanted = sys.argv[1:] or VARIANTS
    for name in wanted:
        VARIANTS[name](os.path.join(OUT_DIR, f"{name}.png"))
