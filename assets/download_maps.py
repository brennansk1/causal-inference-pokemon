#!/usr/bin/env python3
"""
Generate a stylised Kanto region map showing the 10 cities with textbook
chapter annotations.

The map is drawn with matplotlib and saved to assets/maps/kanto_chapter_map.png.
No external data downloads are required.

Usage
-----
    python assets/download_maps.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # non-interactive backend for CI/headless use

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "maps"
OUTPUT_FILE = OUTPUT_DIR / "kanto_chapter_map.png"

# City coordinates (approximate layout inspired by the Kanto map)
# x increases east, y increases north
CITIES: dict[str, dict] = {
    "Pallet Town":    {"xy": (3.0, 1.0), "chapter": "Ch 1", "colour": "#E74C3C"},
    "Viridian City":  {"xy": (3.0, 2.5), "chapter": "Ch 2", "colour": "#3498DB"},
    "Pewter City":    {"xy": (3.0, 4.5), "chapter": "Ch 3", "colour": "#95A5A6"},
    "Cerulean City":  {"xy": (5.5, 5.5), "chapter": "Ch 4", "colour": "#2980B9"},
    "Vermilion City": {"xy": (5.5, 2.0), "chapter": "Ch 5", "colour": "#F39C12"},
    "Lavender Town":  {"xy": (7.5, 3.5), "chapter": "Ch 6", "colour": "#8E44AD"},
    "Celadon City":   {"xy": (4.0, 3.5), "chapter": "Ch 7", "colour": "#27AE60"},
    "Saffron City":   {"xy": (5.5, 3.5), "chapter": "Ch 8", "colour": "#F1C40F"},
    "Fuchsia City":   {"xy": (5.5, 0.5), "chapter": "Ch 9", "colour": "#E91E8B"},
    "Cinnabar Island": {"xy": (2.0, 0.0), "chapter": "Ch 10", "colour": "#C0392B"},
}

# Routes connecting cities (for drawing path lines)
ROUTES: list[tuple[str, str]] = [
    ("Pallet Town", "Viridian City"),
    ("Viridian City", "Pewter City"),
    ("Pewter City", "Cerulean City"),
    ("Cerulean City", "Saffron City"),
    ("Saffron City", "Lavender Town"),
    ("Saffron City", "Celadon City"),
    ("Saffron City", "Vermilion City"),
    ("Celadon City", "Viridian City"),
    ("Vermilion City", "Fuchsia City"),
    ("Fuchsia City", "Cinnabar Island"),
    ("Cinnabar Island", "Pallet Town"),
    ("Cerulean City", "Vermilion City"),
]

# Theme colours
BG_COLOUR = "#F5F0E1"  # parchment
ROUTE_COLOUR = "#BDC3C7"
OCEAN_COLOUR = "#D4E6F1"
TITLE_COLOUR = "#2C3E50"


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def draw_map(ax: plt.Axes) -> None:
    """Draw the full Kanto map on the given axes."""

    # Light ocean fill
    ocean = mpatches.FancyBboxPatch(
        (-0.5, -1.0), 10, 8,
        boxstyle="round,pad=0.3",
        facecolor=OCEAN_COLOUR,
        edgecolor="none",
        zorder=0,
    )
    ax.add_patch(ocean)

    # Draw a land mass polygon (simplified)
    land_x = [1.5, 2.0, 2.5, 3.5, 6.5, 8.5, 8.5, 7.0, 6.0, 5.0, 4.0, 2.5, 1.5]
    land_y = [0.5, 1.5, 3.0, 5.5, 6.5, 4.0, 2.0, 1.5, 0.0, -0.5, -0.5, 0.0, 0.5]
    ax.fill(land_x, land_y, color="#C8E6C9", alpha=0.6, zorder=1)

    # Draw routes
    for city_a, city_b in ROUTES:
        xa, ya = CITIES[city_a]["xy"]
        xb, yb = CITIES[city_b]["xy"]
        ax.plot(
            [xa, xb], [ya, yb],
            color=ROUTE_COLOUR, linewidth=2, linestyle="--",
            zorder=2, alpha=0.8,
        )

    # Draw cities
    for name, info in CITIES.items():
        x, y = info["xy"]
        colour = info["colour"]
        chapter = info["chapter"]

        # City dot
        ax.plot(x, y, "o", color=colour, markersize=14, zorder=4,
                markeredgecolor="white", markeredgewidth=1.5)

        # City name
        ax.annotate(
            name,
            xy=(x, y),
            xytext=(0, 18),
            textcoords="offset points",
            ha="center", va="bottom",
            fontsize=8, fontweight="bold",
            color=TITLE_COLOUR,
            zorder=5,
        )

        # Chapter badge
        ax.annotate(
            chapter,
            xy=(x, y),
            xytext=(0, -16),
            textcoords="offset points",
            ha="center", va="top",
            fontsize=7, fontstyle="italic",
            color=colour,
            bbox=dict(
                boxstyle="round,pad=0.2",
                facecolor="white",
                edgecolor=colour,
                alpha=0.9,
            ),
            zorder=5,
        )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor(BG_COLOUR)
    ax.set_facecolor(BG_COLOUR)

    draw_map(ax)

    # Title
    ax.set_title(
        "Kanto Region  ---  Causal Inference Chapter Map",
        fontsize=16, fontweight="bold", color=TITLE_COLOUR,
        pad=20,
    )

    # Clean up axes
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-1.5, 7.5)
    ax.set_aspect("equal")
    ax.axis("off")

    # Compass rose (simple N arrow)
    ax.annotate(
        "N",
        xy=(8.8, 6.5),
        fontsize=14, fontweight="bold", ha="center", color=TITLE_COLOUR,
    )
    ax.annotate(
        "",
        xy=(8.8, 6.3), xytext=(8.8, 5.5),
        arrowprops=dict(arrowstyle="->", color=TITLE_COLOUR, lw=2),
    )

    fig.tight_layout()
    fig.savefig(OUTPUT_FILE, dpi=200, bbox_inches="tight", facecolor=BG_COLOUR)
    plt.close(fig)

    print(f"Map saved to {OUTPUT_FILE}")
    print(f"  Size: {OUTPUT_FILE.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
