#!/usr/bin/env python3
"""
generate_all.py
===============
Master script that generates all 11 datasets for
*Causal Inference: A Pokemon Approach -- Kanto Region Edition*.

Usage
-----
    python data/dgp/generate_all.py          # from project root
    python generate_all.py                   # from data/dgp/

Outputs land in ``data/raw/`` as CSV files.  The global seed is 151.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Resolve paths -- works whether invoked from project root or data/dgp/
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent          # data/dgp/
PROJECT_ROOT = SCRIPT_DIR.parent.parent               # project root
RAW_DIR = PROJECT_ROOT / "data" / "raw"

# Ensure the DGP package is importable
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import structural_equations as dgp  # noqa: E402


# ---------------------------------------------------------------------------
# Dataset manifest: (function, filename, description)
# ---------------------------------------------------------------------------
MANIFEST = [
    (dgp.generate_kanto_trainers,          "kanto_trainers.csv",
     "Cross-sectional trainer data (42 cols)"),
    # kanto_battles is special -- it depends on kanto_trainers
    (None,                                 "kanto_battles.csv",
     "Battle-level data (28 cols)"),
    (dgp.generate_cities_panel,            "kanto_cities_panel.csv",
     "City x month panel (DiD + invasions)"),
    (dgp.generate_protein_rct,             "pewter_protein_rct.csv",
     "RCT with noncompliance"),
    (dgp.generate_ss_anne,                 "ss_anne_passengers.csv",
     "Matching / propensity-score data"),
    (dgp.generate_safari_lottery,          "safari_zone_lottery.csv",
     "Instrumental variables data"),
    (dgp.generate_happiness_evolution,     "happiness_evolution.csv",
     "Regression discontinuity data"),
    (dgp.generate_shadow_surge_staggered,  "shadow_surge_staggered.csv",
     "Staggered DiD data"),
    (dgp.generate_elite_four_panel,        "elite_four_panel.csv",
     "Sequential battles, dynamic treatment"),
    (dgp.generate_double_battles,          "double_battles.csv",
     "Interference / spillover data"),
    (dgp.generate_johto_transportability,  "johto_trainers.csv",
     "Transportability / external validity"),
]


def _fmt_size(path: Path) -> str:
    """Human-readable file size."""
    size = path.stat().st_size
    for unit in ("B", "KB", "MB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"


def main() -> None:
    print("=" * 64)
    print("  Causal Inference: A Pokemon Approach")
    print("  Data Generating Process  --  seed = 151")
    print("=" * 64)
    print()

    # Create output directory
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {RAW_DIR}")
    print()

    overall_start = time.time()
    trainers_df = None

    for func, filename, desc in MANIFEST:
        print(f"  Generating {filename:<35s} ...", end="", flush=True)
        t0 = time.time()

        if filename == "kanto_trainers.csv":
            df = func()
            trainers_df = df  # cache for battles
        elif filename == "kanto_battles.csv":
            df = dgp.generate_kanto_battles(trainers_df=trainers_df)
        else:
            df = func()

        out_path = RAW_DIR / filename
        df.to_csv(out_path, index=False)
        elapsed = time.time() - t0

        print(
            f"  {df.shape[0]:>6,} rows x {df.shape[1]:>2} cols  "
            f"({_fmt_size(out_path):>10})  [{elapsed:.1f}s]"
        )

    total = time.time() - overall_start
    print()
    print("-" * 64)
    print(f"  All 11 datasets written to {RAW_DIR}")
    print(f"  Total time: {total:.1f}s")
    print("-" * 64)

    # Summary table
    print()
    print(f"  {'Dataset':<35s} {'Rows':>8s} {'Cols':>5s} {'Size':>10s}")
    print(f"  {'-'*35} {'-'*8} {'-'*5} {'-'*10}")
    for _, filename, _ in MANIFEST:
        p = RAW_DIR / filename
        import pandas as pd
        info = pd.read_csv(p, nrows=0)
        n_rows = sum(1 for _ in open(p)) - 1  # fast line count
        print(
            f"  {filename:<35s} {n_rows:>8,} {len(info.columns):>5}  {_fmt_size(p):>9}"
        )
    print()


if __name__ == "__main__":
    main()
