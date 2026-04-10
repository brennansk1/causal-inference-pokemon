"""
Data loading utilities for Causal Inference: A Pokemon Approach.

Each function loads one of the 11 datasets shipped in ``data/raw/`` and returns
a pandas DataFrame.  Paths are resolved relative to the project root so the
helpers work both when the package is installed and when notebooks are run from
the repository checkout.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd

# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

def _find_data_dir() -> Path:
    """Locate the ``data/raw`` directory relative to the package source tree.

    Resolution strategy (first match wins):
      1. Walk up from this file until we find a directory that contains
         ``data/raw/``.  This works for in-tree development and editable
         installs.
      2. Fall back to a ``DATA_DIR`` environment variable if set.
    """
    import os

    # Strategy 1: walk upward from this file
    anchor = Path(__file__).resolve().parent
    for parent in (anchor, *anchor.parents):
        candidate = parent / "data" / "raw"
        if candidate.is_dir():
            return candidate

    # Strategy 2: environment variable override
    env = os.environ.get("KANTO_DATA_DIR")
    if env is not None:
        p = Path(env)
        if p.is_dir():
            return p

    raise FileNotFoundError(
        "Could not locate the data/raw/ directory. "
        "Make sure you are running from inside the textbook repository or set "
        "the KANTO_DATA_DIR environment variable to the path of data/raw/."
    )


def _load_csv(filename: str, **kwargs) -> pd.DataFrame:
    """Load a CSV from the data directory with sensible defaults."""
    path = _find_data_dir() / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}\n"
            f"Make sure '{filename}' is present in data/raw/."
        )
    return pd.read_csv(path, **kwargs)


# ---------------------------------------------------------------------------
# Public loaders
# ---------------------------------------------------------------------------

def load_trainers(**kwargs) -> pd.DataFrame:
    """Load the Kanto trainers cross-sectional dataset.

    Contains trainer-level attributes such as experience, badges earned,
    Pokemon team composition, starter choice, and battle statistics.

    Returns
    -------
    pd.DataFrame
        One row per trainer.
    """
    return _load_csv("kanto_trainers.csv", **kwargs)


def load_battles(**kwargs) -> pd.DataFrame:
    """Load the Kanto battles dataset.

    Records of individual Pokemon battles including participants, types,
    levels, moves used, and outcomes.

    Returns
    -------
    pd.DataFrame
        One row per battle.
    """
    return _load_csv("kanto_battles.csv", **kwargs)


def load_cities_panel(**kwargs) -> pd.DataFrame:
    """Load the Kanto cities panel dataset.

    Longitudinal data on Kanto cities over time, tracking Gym presence,
    population, economy, and Pokemon Center usage.  Useful for
    difference-in-differences and panel methods.

    Returns
    -------
    pd.DataFrame
        One row per city-period.
    """
    return _load_csv("kanto_cities_panel.csv", **kwargs)


def load_protein_rct(**kwargs) -> pd.DataFrame:
    """Load the Pewter Protein RCT dataset.

    Data from a randomised controlled trial in Pewter City studying the
    effect of protein supplements on Pokemon battle performance.

    Returns
    -------
    pd.DataFrame
        One row per Pokemon in the trial.
    """
    return _load_csv("pewter_protein_rct.csv", **kwargs)


def load_ss_anne(**kwargs) -> pd.DataFrame:
    """Load the S.S. Anne passengers dataset.

    Passenger manifest and outcomes from the S.S. Anne voyage, useful for
    selection-on-observables examples and matching.

    Returns
    -------
    pd.DataFrame
        One row per passenger.
    """
    return _load_csv("ss_anne_passengers.csv", **kwargs)


def load_safari_lottery(**kwargs) -> pd.DataFrame:
    """Load the Safari Zone lottery dataset.

    Lottery-based access to the Safari Zone creates an instrumental variable
    for rare-Pokemon ownership.

    Returns
    -------
    pd.DataFrame
        One row per participant.
    """
    return _load_csv("safari_zone_lottery.csv", **kwargs)


def load_happiness(**kwargs) -> pd.DataFrame:
    """Load the happiness evolution dataset.

    Tracks Pokemon happiness levels over time and evolution events.  Useful
    for regression-discontinuity designs around happiness thresholds.

    Returns
    -------
    pd.DataFrame
        One row per Pokemon-period observation.
    """
    return _load_csv("happiness_evolution.csv", **kwargs)


def load_shadow_surge(**kwargs) -> pd.DataFrame:
    """Load the Shadow Surge staggered adoption dataset.

    Cities adopt the Shadow Surge policy at different times, enabling
    staggered difference-in-differences estimation.

    Returns
    -------
    pd.DataFrame
        One row per city-period.
    """
    return _load_csv("shadow_surge_staggered.csv", **kwargs)


def load_elite_four(**kwargs) -> pd.DataFrame:
    """Load the Elite Four panel dataset.

    Panel data tracking challengers' attempts against the Elite Four,
    including preparation, team composition, and outcomes.

    Returns
    -------
    pd.DataFrame
        One row per challenger-attempt.
    """
    return _load_csv("elite_four_panel.csv", **kwargs)


def load_double_battles(**kwargs) -> pd.DataFrame:
    """Load the double battles dataset.

    Records of double battles (2v2) with interaction effects, useful for
    studying treatment-effect heterogeneity and mediation.

    Returns
    -------
    pd.DataFrame
        One row per battle.
    """
    return _load_csv("double_battles.csv", **kwargs)


def load_johto(**kwargs) -> pd.DataFrame:
    """Load the Johto transportability dataset.

    Data from the Johto region for external validity and transportability
    analyses -- do causal effects estimated in Kanto generalise to Johto?

    Returns
    -------
    pd.DataFrame
        One row per observation in Johto.
    """
    return _load_csv("johto_transportability.csv", **kwargs)
