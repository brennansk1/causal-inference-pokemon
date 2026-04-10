"""
Pytest fixtures for Causal Inference: A Pokemon Approach test suite.

Provides reusable sample DataFrames that mirror the structure of the
project's datasets, so tests can run without the real CSV files.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


# ---------------------------------------------------------------------------
# Random seed for reproducibility
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def set_random_seed():
    """Set numpy random seed before every test."""
    np.random.seed(42)


# ---------------------------------------------------------------------------
# Sample DataFrames
# ---------------------------------------------------------------------------

@pytest.fixture()
def sample_trainers() -> pd.DataFrame:
    """Small trainers dataset mirroring kanto_trainers.csv structure."""
    rng = np.random.default_rng(42)
    n = 100
    return pd.DataFrame({
        "trainer_id": range(1, n + 1),
        "starter": rng.choice(["Bulbasaur", "Charmander", "Squirtle"], size=n),
        "badges": rng.integers(0, 9, size=n),
        "experience": rng.integers(100, 50000, size=n),
        "team_size": rng.integers(1, 7, size=n),
        "wins": rng.integers(0, 200, size=n),
        "losses": rng.integers(0, 100, size=n),
        "region": "Kanto",
    })


@pytest.fixture()
def sample_battles() -> pd.DataFrame:
    """Small battles dataset mirroring kanto_battles.csv structure."""
    rng = np.random.default_rng(42)
    n = 200
    types = ["Fire", "Water", "Grass", "Electric", "Normal", "Psychic"]
    return pd.DataFrame({
        "battle_id": range(1, n + 1),
        "pokemon_a": rng.choice(range(1, 152), size=n),
        "pokemon_b": rng.choice(range(1, 152), size=n),
        "type_a": rng.choice(types, size=n),
        "type_b": rng.choice(types, size=n),
        "level_a": rng.integers(5, 100, size=n),
        "level_b": rng.integers(5, 100, size=n),
        "winner": rng.choice(["a", "b"], size=n),
    })


@pytest.fixture()
def sample_cities_panel() -> pd.DataFrame:
    """Small cities panel dataset mirroring kanto_cities_panel.csv structure."""
    cities = [
        "Pallet Town", "Viridian City", "Pewter City", "Cerulean City",
        "Vermilion City", "Lavender Town", "Celadon City", "Saffron City",
        "Fuchsia City", "Cinnabar Island",
    ]
    periods = list(range(1, 11))
    rng = np.random.default_rng(42)

    rows = []
    for city in cities:
        # Some cities get the gym earlier
        gym_period = rng.choice([3, 5, 7, None])
        for t in periods:
            has_gym = int(gym_period is not None and t >= gym_period)
            rows.append({
                "city": city,
                "period": t,
                "has_gym": has_gym,
                "population": int(rng.integers(500, 10000)),
                "pokemon_center_visits": int(rng.integers(50, 1000)),
                "avg_trainer_level": float(rng.uniform(10, 60)),
            })
    return pd.DataFrame(rows)


@pytest.fixture()
def sample_rct() -> pd.DataFrame:
    """Small RCT dataset mirroring pewter_protein_rct.csv structure."""
    rng = np.random.default_rng(42)
    n = 80
    treatment = rng.choice([0, 1], size=n)
    # Treatment effect of ~5 points
    outcome = 50 + 5 * treatment + rng.normal(0, 10, size=n)
    return pd.DataFrame({
        "pokemon_id": range(1, n + 1),
        "treatment": treatment,
        "protein_dose": treatment * rng.uniform(10, 30, size=n),
        "base_power": rng.integers(30, 80, size=n),
        "outcome_power": outcome.round(1),
        "species": rng.choice(["Geodude", "Onix", "Zubat", "Sandshrew"], size=n),
    })


@pytest.fixture()
def sample_iv() -> pd.DataFrame:
    """Small IV dataset mirroring safari_zone_lottery.csv structure."""
    rng = np.random.default_rng(42)
    n = 120
    lottery_win = rng.choice([0, 1], size=n, p=[0.7, 0.3])
    # Instrument -> treatment (compliance ~80%)
    safari_visit = (lottery_win * (rng.uniform(size=n) < 0.8)).astype(int)
    # Treatment -> outcome
    rare_pokemon = safari_visit * rng.integers(0, 5, size=n)
    return pd.DataFrame({
        "trainer_id": range(1, n + 1),
        "lottery_win": lottery_win,
        "safari_visit": safari_visit,
        "rare_pokemon_caught": rare_pokemon,
        "trainer_level": rng.integers(10, 60, size=n),
    })


@pytest.fixture()
def simple_treatment_df() -> pd.DataFrame:
    """Minimal treatment/outcome DataFrame for testing estimators."""
    rng = np.random.default_rng(42)
    n = 200
    treatment = np.array([0] * (n // 2) + [1] * (n // 2))
    outcome = 10.0 + 3.0 * treatment + rng.normal(0, 2, size=n)
    covariate = rng.normal(5, 1, size=n)
    return pd.DataFrame({
        "treatment": treatment,
        "outcome": outcome,
        "covariate": covariate,
    })
