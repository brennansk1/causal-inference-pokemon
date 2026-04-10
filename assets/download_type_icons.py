#!/usr/bin/env python3
"""
Generate Pokemon type badge SVGs for all 18 types.

Each badge is a rounded-rectangle pill with the type name in white text on a
background colour that matches the canonical game colour for that type.  Files
are saved to assets/sprites/types/{type_name}.svg.

Usage
-----
    python assets/download_type_icons.py
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "sprites" / "types"

# Canonical Pokemon type colours (hex)
TYPE_COLOURS: dict[str, str] = {
    "Normal":   "#A8A878",
    "Fire":     "#F08030",
    "Water":    "#6890F0",
    "Electric": "#F8D030",
    "Grass":    "#78C850",
    "Ice":      "#98D8D8",
    "Fighting": "#C03028",
    "Poison":   "#A040A0",
    "Ground":   "#E0C068",
    "Flying":   "#A890F0",
    "Psychic":  "#F85888",
    "Bug":      "#A8B820",
    "Rock":     "#B8A038",
    "Ghost":    "#705898",
    "Dragon":   "#7038F8",
    "Dark":     "#705848",
    "Steel":    "#B8B8D0",
    "Fairy":    "#EE99AC",
}

# Badge dimensions
BADGE_WIDTH = 120
BADGE_HEIGHT = 32
CORNER_RADIUS = 8
FONT_SIZE = 14

# SVG template
SVG_TEMPLATE = """\
<svg xmlns="http://www.w3.org/2000/svg"
     width="{width}" height="{height}"
     viewBox="0 0 {width} {height}">
  <rect x="0" y="0" width="{width}" height="{height}"
        rx="{rx}" ry="{rx}"
        fill="{colour}" />
  <text x="{cx}" y="{cy}"
        font-family="Arial, Helvetica, sans-serif"
        font-size="{font_size}" font-weight="bold"
        fill="white" text-anchor="middle"
        dominant-baseline="central">
    {label}
  </text>
</svg>
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def generate_badge(type_name: str, colour: str, dest: Path) -> None:
    """Write a single SVG badge file."""
    svg = SVG_TEMPLATE.format(
        width=BADGE_WIDTH,
        height=BADGE_HEIGHT,
        rx=CORNER_RADIUS,
        colour=colour,
        cx=BADGE_WIDTH // 2,
        cy=BADGE_HEIGHT // 2,
        font_size=FONT_SIZE,
        label=type_name.upper(),
    )
    dest.write_text(svg, encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Generating type badges in {OUTPUT_DIR}")

    for type_name, colour in TYPE_COLOURS.items():
        dest = OUTPUT_DIR / f"{type_name.lower()}.svg"
        generate_badge(type_name, colour, dest)
        print(f"  {type_name:10s}  {colour}  -> {dest.name}")

    print(f"\nDone!  {len(TYPE_COLOURS)} badges generated.")


if __name__ == "__main__":
    main()
