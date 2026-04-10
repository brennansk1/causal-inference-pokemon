"""Insert image references into the chapter markdown files.

Run from the project root. This script is idempotent — each insertion is
guarded by a unique HTML comment marker so re-running it won't duplicate.

Image paths are written relative to the chapter file location
(`../../assets/...`) so they resolve from both the chapter directory and the
build directory.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent.parent
CHAPTERS = ROOT / "textbook" / "chapters"

# Asset path is relative from a chapter file (textbook/chapters/foo.md)
A = "../../assets"


def insert_after(text: str, anchor: str, block: str, marker: str) -> str:
    """Insert `block` immediately after the first line containing `anchor`.

    Idempotent: if the marker comment already appears in the text, return
    unchanged.
    """
    if marker in text:
        return text
    lines = text.splitlines(keepends=True)
    out = []
    inserted = False
    for line in lines:
        out.append(line)
        if not inserted and anchor in line:
            out.append("\n")
            out.append(f"<!-- {marker} -->\n")
            out.append(block.rstrip() + "\n\n")
            inserted = True
    if not inserted:
        # Fall back: append at end
        out.append("\n")
        out.append(f"<!-- {marker} -->\n")
        out.append(block.rstrip() + "\n")
    return "".join(out)


def figure(src: str, caption: str, width: str = "60%") -> str:
    return (
        f'<figure>\n'
        f'<img src="{src}" alt="{caption}" style="width:{width}; max-width:520px; display:block; margin:1em auto;">\n'
        f'<figcaption>{caption}</figcaption>\n'
        f'</figure>\n'
    )


def badge(name: str, display: str) -> str:
    return (
        f'<figure style="text-align:center; margin:1.5em auto;">\n'
        f'<img src="{A}/badges/{name}_badge.png" alt="{display} Badge" '
        f'style="width:140px; display:block; margin:0 auto;">\n'
        f'<figcaption><strong>{display} Badge earned!</strong></figcaption>\n'
        f'</figure>\n'
    )


def character(name: str, display: str, side: str = "right") -> str:
    return (
        f'<figure style="float:{side}; margin:0 0 12px 16px; max-width:140px;">\n'
        f'<img src="{A}/characters/{name}.png" alt="{display}" '
        f'style="width:120px; display:block; image-rendering: pixelated;">\n'
        f'<figcaption style="font-size:0.85em; text-align:center;">{display}</figcaption>\n'
        f'</figure>\n'
    )


# ---------------------------------------------------------------------------
# Per-chapter insertions
# ---------------------------------------------------------------------------
def edit_ch01():
    f = CHAPTERS / "ch01_pallet_town.md"
    text = f.read_text()
    text = insert_after(
        text,
        "# Chapter 1:",
        figure(f"{A}/maps/kanto_map.png", "The Kanto region — your journey begins in Pallet Town.", "75%"),
        "FIG-CH01-MAP",
    )
    text = insert_after(
        text,
        "# Chapter 1:",
        character("oak", "Professor Oak", "right"),
        "FIG-CH01-OAK",
    )
    f.write_text(text)


def edit_ch02():
    f = CHAPTERS / "ch02_pewter_city.md"
    text = f.read_text()
    text = insert_after(
        text,
        "# Chapter 2:",
        character("brock", "Brock, Pewter Gym Leader", "right"),
        "FIG-CH02-BROCK",
    )
    text = insert_after(
        text,
        "## Chapter Summary",
        badge("boulder", "Boulder"),
        "FIG-CH02-BADGE",
    )
    f.write_text(text)


def edit_ch03():
    f = CHAPTERS / "ch03_cerulean_city.md"
    text = f.read_text()
    text = insert_after(
        text,
        "# Chapter 3:",
        character("misty", "Misty, Cerulean Gym Leader", "right"),
        "FIG-CH03-MISTY",
    )
    text = insert_after(
        text,
        "## 3.6",
        figure(f"{A}/diagrams/dag_three_structures.png",
               "The three atomic DAG structures: fork, chain, and collider.", "85%"),
        "FIG-CH03-THREE",
    )
    text = insert_after(
        text,
        "## 3.7",
        figure(f"{A}/diagrams/dag_kanto_trainer.png",
               "The Kanto Trainer DAG (latent vs observed nodes).", "75%"),
        "FIG-CH03-DAG",
    )
    text = insert_after(
        text,
        "## Chapter Summary",
        badge("cascade", "Cascade"),
        "FIG-CH03-BADGE",
    )
    f.write_text(text)


def edit_ch04():
    f = CHAPTERS / "ch04_vermilion_city.md"
    text = f.read_text()
    text = insert_after(
        text,
        "# Chapter 4:",
        character("surge", "Lt. Surge, Vermilion Gym Leader", "right"),
        "FIG-CH04-SURGE",
    )
    text = insert_after(
        text,
        "## Chapter Summary",
        badge("thunder", "Thunder"),
        "FIG-CH04-BADGE",
    )
    f.write_text(text)


def edit_ch05():
    f = CHAPTERS / "ch05_celadon_city.md"
    text = f.read_text()
    text = insert_after(
        text,
        "# Chapter 5:",
        character("erika", "Erika, Celadon Gym Leader", "right"),
        "FIG-CH05-ERIKA",
    )
    text = insert_after(
        text,
        "## 5.3",
        figure(f"{A}/diagrams/dag_bad_control.png",
               "Controlling for a post-treatment variable blocks the causal pathway.", "70%"),
        "FIG-CH05-BAD",
    )
    text = insert_after(
        text,
        "## Chapter Summary",
        badge("rainbow", "Rainbow"),
        "FIG-CH05-BADGE",
    )
    f.write_text(text)


def edit_ch06():
    f = CHAPTERS / "ch06_fuchsia_cinnabar.md"
    text = f.read_text()
    text = insert_after(
        text,
        "# Chapter 6:",
        character("koga", "Koga, Fuchsia Gym Leader", "right"),
        "FIG-CH06-KOGA",
    )
    text = insert_after(
        text,
        "## 6.1",
        figure(f"{A}/diagrams/dag_iv.png",
               "Instrumental variables: Z affects Y only through D.", "70%"),
        "FIG-CH06-IV",
    )
    text = insert_after(
        text,
        "## 6.5",
        figure(f"{A}/diagrams/rdd_evolution.png",
               "Sharp Regression Discontinuity at the evolution threshold.", "80%"),
        "FIG-CH06-RDD",
    )
    text = insert_after(
        text,
        "## Chapter Summary",
        '<div style="display:flex; gap:24px; justify-content:center; margin:1.5em 0;">\n'
        f'<figure><img src="{A}/badges/soul_badge.png" style="width:120px;"><figcaption><strong>Soul Badge!</strong></figcaption></figure>\n'
        f'<figure><img src="{A}/badges/volcano_badge.png" style="width:120px;"><figcaption><strong>Volcano Badge!</strong></figcaption></figure>\n'
        '</div>\n',
        "FIG-CH06-BADGE",
    )
    f.write_text(text)


def edit_ch07():
    f = CHAPTERS / "ch07_saffron_city.md"
    text = f.read_text()
    text = insert_after(
        text,
        "# Chapter 7:",
        character("sabrina", "Sabrina, Saffron Gym Leader", "right"),
        "FIG-CH07-SABRINA",
    )
    text = insert_after(
        text,
        "## 7.1",
        figure(f"{A}/diagrams/did_parallel_trends.png",
               "Difference-in-differences with parallel trends and a counterfactual.", "85%"),
        "FIG-CH07-DID",
    )
    text = insert_after(
        text,
        "## Chapter Summary",
        badge("marsh", "Marsh"),
        "FIG-CH07-BADGE",
    )
    f.write_text(text)


def edit_ch08():
    f = CHAPTERS / "ch08_indigo_plateau.md"
    text = f.read_text()
    # Composite Elite Four header
    elite_four = (
        '<div style="display:flex; gap:8px; justify-content:center; margin:1em 0;">\n'
        f'<figure><img src="{A}/characters/lorelei.png" style="width:90px;"><figcaption>Lorelei</figcaption></figure>\n'
        f'<figure><img src="{A}/characters/bruno.png" style="width:90px;"><figcaption>Bruno</figcaption></figure>\n'
        f'<figure><img src="{A}/characters/agatha.png" style="width:90px;"><figcaption>Agatha</figcaption></figure>\n'
        f'<figure><img src="{A}/characters/lance.png" style="width:90px;"><figcaption>Lance</figcaption></figure>\n'
        '</div>\n'
    )
    text = insert_after(text, "# Chapter 8:", elite_four, "FIG-CH08-ELITE4")
    text = insert_after(
        text,
        "## 8.1",
        figure(f"{A}/diagrams/dag_mediation.png",
               "Mediation: total effect = direct (NDE) + indirect through M (NIE).", "70%"),
        "FIG-CH08-MED",
    )
    text = insert_after(
        text,
        "## 8.11",
        character("blue", "Rival Blue, the Champion", "right"),
        "FIG-CH08-BLUE",
    )
    text = insert_after(
        text,
        "## Chapter Summary",
        # Final all-eight-badges montage
        '<div style="display:flex; flex-wrap:wrap; gap:8px; justify-content:center; margin:1.5em 0;">\n'
        + "".join(
            f'<img src="{A}/badges/{n}_badge.png" alt="{d}" style="width:80px;">\n'
            for n, d in [
                ("boulder", "Boulder"), ("cascade", "Cascade"), ("thunder", "Thunder"),
                ("rainbow", "Rainbow"), ("soul", "Soul"), ("marsh", "Marsh"),
                ("volcano", "Volcano"), ("earth", "Earth"),
            ]
        )
        + '</div>\n<p style="text-align:center; font-weight:bold; color:#EE1515;">Champion! All eight badges earned.</p>\n',
        "FIG-CH08-CHAMPION",
    )
    f.write_text(text)


def main():
    print("Embedding visual elements into chapter markdown files...")
    edit_ch01()
    edit_ch02()
    edit_ch03()
    edit_ch04()
    edit_ch05()
    edit_ch06()
    edit_ch07()
    edit_ch08()
    print("Done. Each chapter now contains image references.")


if __name__ == "__main__":
    main()
