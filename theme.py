# theme.py — "Vintage Field Notebook" theme
import os
import urllib.request

import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt


PALETTE = {
    "bg": "#E6CDB5",
    "text": "#3E2723",
    "grid": "#D7C4A7",
    "sienna": "#A0522D",
    "steel_blue": "#4682B4",
    "goldenrod": "#DAA520",
    "olive": "#6B8E23",
    "saddle_brown": "#8B4513",
    "accents": ["#A0522D", "#4682B4", "#DAA520", "#6B8E23", "#8B4513"],
}

_FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
_FONT_NAME = "Architects Daughter"
_FONT_URL = (
    "https://github.com/google/fonts/raw/main/ofl/architectsdaughter/"
    "ArchitectsDaughter-Regular.ttf"
)


def _ensure_font():
    """Download and register Architects Daughter if not already cached."""
    os.makedirs(_FONT_DIR, exist_ok=True)
    ttf_path = os.path.join(_FONT_DIR, "ArchitectsDaughter-Regular.ttf")

    if not os.path.exists(ttf_path):
        print(f"Downloading {_FONT_NAME} font...")
        urllib.request.urlretrieve(_FONT_URL, ttf_path)
        print(f"Saved to {ttf_path}")

    # Register with matplotlib if not already known
    known = {f.name for f in fm.fontManager.ttflist}
    if _FONT_NAME not in known:
        fm.fontManager.addfont(ttf_path)


def apply_theme():
    """Activate the Vintage Field Notebook look."""
    _ensure_font()

    rc = {
        "font.family": _FONT_NAME,
        "figure.facecolor": PALETTE["bg"],
        "axes.facecolor": PALETTE["bg"],
        "text.color": PALETTE["text"],
        "axes.labelcolor": PALETTE["text"],
        "xtick.color": PALETTE["text"],
        "ytick.color": PALETTE["text"],
        "axes.edgecolor": PALETTE["text"],
        "grid.color": PALETTE["grid"],
        "figure.figsize": (12, 7),
        "figure.dpi": 150,
        "font.size": 11,
        "axes.titlesize": 16,
        "axes.labelsize": 13,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "legend.fontsize": 11,
        "legend.facecolor": PALETTE["bg"],
        "legend.edgecolor": PALETTE["text"],
    }
    matplotlib.rcParams.update(rc)


def save_chart(fig, filename, subdir="."):
    """Save figure to <subdir>/reports/<filename>.png and close it."""
    out_dir = os.path.join(subdir, "reports")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{filename}.png")
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    print(f"Saved {path}")


def get_colors(n):
    """Return the first *n* accent colors from the palette."""
    return PALETTE["accents"][:n]
