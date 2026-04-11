"""Download real Pokemon visual assets from open community repositories.

Sources:
  - Kanto gym badges:    PokeAPI/sprites (sprites/badges/{1..8}.png)
  - Type icons:          PokeAPI/sprites (sprites/types/generation-viii/sword-shield/{1..18}.png)
  - Trainer characters:  pret/pokered (gfx/trainers/*.png) -- original Gen 1 graphics
  - Kanto town map:      pret/pokered (gfx/town_map/town_map.png) -- original Gen 1 map

The pret/pokered repository is the disassembly of Pokemon Red and contains the
original Game Boy graphics (1996), which are used here for educational purposes.
The PokeAPI/sprites repository aggregates sprites from the games for community use.

If a download fails, the previously generated SVG fallback in the same directory
remains in place.
"""
from pathlib import Path
import urllib.request
import urllib.error

ROOT = Path(__file__).parent

# ---------------------------------------------------------------------------
# Kanto gym badges (PokeAPI sprite IDs 1-8 are the Kanto badges in order)
# ---------------------------------------------------------------------------
BADGES = {
    1: ("boulder",  "Boulder"),
    2: ("cascade",  "Cascade"),
    3: ("thunder",  "Thunder"),
    4: ("rainbow",  "Rainbow"),
    5: ("soul",     "Soul"),
    6: ("marsh",    "Marsh"),
    7: ("volcano",  "Volcano"),
    8: ("earth",    "Earth"),
}

BADGE_URL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/badges/{id}.png"

# ---------------------------------------------------------------------------
# Type icons (PokeAPI type IDs 1-18, sword-shield generation)
# ---------------------------------------------------------------------------
TYPES = {
    1:  "normal",   2:  "fighting", 3:  "flying",  4:  "poison",
    5:  "ground",   6:  "rock",     7:  "bug",     8:  "ghost",
    9:  "steel",    10: "fire",     11: "water",   12: "grass",
    13: "electric", 14: "psychic",  15: "ice",     16: "dragon",
    17: "dark",     18: "fairy",
}
TYPE_URL = (
    "https://raw.githubusercontent.com/PokeAPI/sprites/master/"
    "sprites/types/generation-viii/sword-shield/{id}.png"
)

# ---------------------------------------------------------------------------
# Trainers (pret/pokered Gen 1 disassembly graphics)
# ---------------------------------------------------------------------------
POKERED_BASE = "https://raw.githubusercontent.com/pret/pokered/master/gfx/trainers/{file}.png"

CHARACTERS = {
    "oak":         "prof.oak",      # Professor Oak
    "blue":        "rival3",        # Rival Blue (final form)
    "blue_young":  "rival1",        # Rival Blue (early game)
    "brock":       "brock",
    "misty":       "misty",
    "surge":       "lt.surge",
    "erika":       "erika",
    "koga":        "koga",
    "sabrina":     "sabrina",
    "blaine":      "blaine",
    "giovanni":    "giovanni",
    "lorelei":     "lorelei",
    "bruno":       "bruno",
    "agatha":      "agatha",
    "lance":       "lance",
    "rocket":      "rocket",        # Team Rocket grunt
}

# Nurse Joy is not in the Gen 1 game graphics (she debuted as a generic NPC),
# so her portrait ships as `characters/nurse_joy.webp` (sourced manually) rather
# than being downloaded from pret/pokered.

# ---------------------------------------------------------------------------
# Kanto map (pret/pokered town map)
# ---------------------------------------------------------------------------
TOWN_MAP_URL = "https://raw.githubusercontent.com/pret/pokered/master/gfx/town_map/town_map.png"


def download(url: str, dest: Path) -> bool:
    """Download a file. Return True if successful."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "causal-inference-pokemon/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        return True
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
        print(f"  FAILED: {dest.name} ({exc})")
        return False


def download_badges() -> int:
    print("\n[1/4] Downloading real Kanto gym badge images from PokeAPI...")
    out = ROOT / "badges"
    ok = 0
    for id_, (name, display) in BADGES.items():
        dest = out / f"{name}_badge.png"
        url = BADGE_URL.format(id=id_)
        if download(url, dest):
            print(f"  {display:8} -> {dest.name}")
            ok += 1
    print(f"  Got {ok}/{len(BADGES)} real badge images.")
    return ok


def download_types() -> int:
    print("\n[2/4] Downloading real type icons from PokeAPI...")
    out = ROOT / "sprites" / "types"
    ok = 0
    for id_, name in TYPES.items():
        dest = out / f"{name}.png"
        url = TYPE_URL.format(id=id_)
        if download(url, dest):
            ok += 1
    print(f"  Got {ok}/{len(TYPES)} real type icons.")
    return ok


def download_characters() -> int:
    print("\n[3/4] Downloading real trainer sprites from pret/pokered (Gen 1)...")
    out = ROOT / "characters"
    ok = 0
    for name, source_file in CHARACTERS.items():
        dest = out / f"{name}.png"
        url = POKERED_BASE.format(file=source_file)
        if download(url, dest):
            print(f"  {name:12} -> {dest.name}")
            ok += 1
    print(f"  Got {ok}/{len(CHARACTERS)} real character sprites.")
    return ok


def download_map() -> int:
    print("\n[4/4] Downloading real Kanto town map from pret/pokered...")
    out = ROOT / "maps"
    dest = out / "kanto_town_map.png"
    if download(TOWN_MAP_URL, dest):
        print(f"  Saved -> {dest}")
        return 1
    return 0


def main() -> None:
    print("=" * 60)
    print("Downloading real Pokemon visual assets")
    print("=" * 60)
    n_badges = download_badges()
    n_types = download_types()
    n_chars = download_characters()
    n_map = download_map()

    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"  Badges:     {n_badges}/8")
    print(f"  Types:      {n_types}/18")
    print(f"  Characters: {n_chars}/{len(CHARACTERS)}")
    print(f"  Map:        {n_map}/1")
    print()
    print("Any failures fall back to the SVG versions in the same directories.")


if __name__ == "__main__":
    main()
