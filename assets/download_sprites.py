#!/usr/bin/env python3
"""
Download front sprites for all 151 Kanto Pokemon from PokeAPI's GitHub repo.

Sprites are saved to assets/sprites/front/{id}.png.  Already-downloaded files
are skipped so the script is safe to re-run.

Usage
-----
    python assets/download_sprites.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import requests
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SPRITE_URL = (
    "https://raw.githubusercontent.com/PokeAPI/sprites/"
    "master/sprites/pokemon/{id}.png"
)
KANTO_RANGE = range(1, 152)  # 1-151 inclusive

# Resolve output directory relative to this script
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "sprites" / "front"

# Polite request settings
REQUEST_TIMEOUT = 30  # seconds
RETRY_LIMIT = 3
RETRY_DELAY = 2  # seconds between retries
HEADERS = {"User-Agent": "CausalInferencePokemonTextbook/1.0"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def download_sprite(pokemon_id: int, dest: Path) -> bool:
    """Download a single sprite.  Returns True on success, False on failure."""
    url = SPRITE_URL.format(id=pokemon_id)
    for attempt in range(1, RETRY_LIMIT + 1):
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT, headers=HEADERS)
            response.raise_for_status()
            dest.write_bytes(response.content)
            return True
        except requests.RequestException as exc:
            if attempt < RETRY_LIMIT:
                time.sleep(RETRY_DELAY)
            else:
                tqdm.write(f"  [ERROR] #{pokemon_id}: {exc}")
                return False
    return False  # unreachable, but keeps mypy happy


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    skipped = 0
    downloaded = 0
    failed = 0

    print(f"Downloading Kanto sprites to {OUTPUT_DIR}")
    print(f"  Range: #{KANTO_RANGE.start} - #{KANTO_RANGE.stop - 1}")
    print()

    for pid in tqdm(KANTO_RANGE, desc="Sprites", unit="sprite"):
        dest = OUTPUT_DIR / f"{pid}.png"

        # Skip files that already exist and are non-empty
        if dest.exists() and dest.stat().st_size > 0:
            skipped += 1
            continue

        if download_sprite(pid, dest):
            downloaded += 1
        else:
            failed += 1

    print()
    print(f"Done!  downloaded={downloaded}  skipped={skipped}  failed={failed}")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
