"""Upscale tiny Game Boy sprites and the FireRed region map to printable sizes.

The pret/pokered trainer sprites are 56x56 grayscale Game Boy graphics. The
FireRed region map is 128x160 indexed-color. At native resolution they are
unreadable in a printed textbook. Nearest-neighbor upscaling preserves the
pixelart aesthetic while making them legible.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent

UPSCALES = [
    # (source dir, file glob, scale factor)
    (ROOT / "characters", "*.png", 4),   # 56x56  -> 224x224
    (ROOT / "badges",     "*.png", 2),   # 85x85  -> 170x170
    (ROOT / "maps",       "kanto_region_map_firered.png", 4),  # 128x160 -> 512x640
]


def upscale(src_path: Path, scale: int) -> None:
    """Upscale a single image with nearest-neighbor and overwrite."""
    img = Image.open(src_path)
    if img.size[0] >= 200:  # already large enough
        return
    new_size = (img.size[0] * scale, img.size[1] * scale)
    upsized = img.resize(new_size, Image.NEAREST)
    # Convert palette to RGBA so embedding works in HTML/PDF
    if upsized.mode in ("L", "P", "LA"):
        upsized = upsized.convert("RGBA")
    upsized.save(src_path)
    print(f"  {src_path.name:32} {img.size} -> {new_size}")


def main() -> None:
    print("Upscaling pixel-art assets for print legibility")
    print("=" * 60)
    total = 0
    for directory, pattern, scale in UPSCALES:
        if not directory.exists():
            continue
        files = sorted(directory.glob(pattern))
        if not files:
            continue
        print(f"\n{directory.name}/  ({pattern})  scale={scale}x")
        for f in files:
            upscale(f, scale)
            total += 1
    print(f"\nDone! Upscaled {total} images.")


if __name__ == "__main__":
    main()
