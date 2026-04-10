"""
structural_equations.py
=======================
Core data-generating process (DGP) module for
*Causal Inference: A Pokemon Approach -- Kanto Region Edition*.

Every function returns a pandas DataFrame whose causal structure is fully
documented in the textbook appendix.  The single source of randomness is
``np.random.default_rng(151)`` (one Mew to rule them all).

Datasets
--------
1.  kanto_trainers          -- cross-sectional trainer-level data (42 cols)
2.  kanto_battles           -- battle-level panel
3.  kanto_cities_panel      -- city x month panel (DiD + invasions)
4.  pewter_protein_rct      -- RCT with noncompliance (IV preview)
5.  ss_anne_passengers      -- matching / propensity-score data
6.  safari_zone_lottery     -- IV dataset
7.  happiness_evolution     -- RDD dataset (sharp + fuzzy)
8.  shadow_surge_staggered  -- staggered DiD
9.  elite_four_panel        -- sequential battles, dynamic treatment
10. double_battles          -- interference / spillover
11. johto_trainers          -- transportability / external validity
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Global RNG -- every function draws from the *same* generator so the full
# collection is reproducible in sequence.
# ---------------------------------------------------------------------------
RNG = np.random.default_rng(151)

# ---------------------------------------------------------------------------
# Shared constants
# ---------------------------------------------------------------------------
KANTO_TOWNS = [
    "Pallet Town", "Viridian City", "Pewter City", "Cerulean City",
    "Vermilion City", "Lavender Town", "Celadon City", "Fuchsia City",
    "Saffron City", "Cinnabar Island",
]

KANTO_STARTERS = {
    "Grass": "Bulbasaur",
    "Fire": "Charmander",
    "Water": "Squirtle",
}

JOHTO_TOWNS = [
    "New Bark Town", "Cherrygrove City", "Violet City", "Azalea Town",
    "Goldenrod City", "Ecruteak City", "Olivine City", "Cianwood City",
    "Mahogany Town", "Blackthorn City",
]

JOHTO_STARTERS = {
    "Grass": "Chikorita",
    "Fire": "Cyndaquil",
    "Water": "Totodile",
}

POKEMON_TYPES = [
    "Normal", "Fire", "Water", "Electric", "Grass", "Ice",
    "Fighting", "Poison", "Ground", "Flying", "Psychic",
    "Bug", "Rock", "Ghost", "Dragon",
]

# Trainer name pools (thematic)
_FIRST_NAMES = [
    "Ash", "Gary", "Misty", "Brock", "Erika", "Surge", "Sabrina", "Koga",
    "Blaine", "Giovanni", "Lorelei", "Bruno", "Agatha", "Lance", "Bill",
    "Daisy", "Jessie", "James", "Richie", "Casey", "Tracey", "Todd",
    "Duplica", "AJ", "Giselle", "Joe", "Samurai", "Lara", "Dario",
    "Stella", "Koji", "Aya", "Janine", "Falkner", "Bugsy", "Whitney",
    "Morty", "Chuck", "Jasmine", "Pryce", "Clair", "Will", "Karen",
    "Red", "Blue", "Green", "Yellow", "Silver", "Gold", "Crystal",
]


def _clip(arr, lo, hi):
    """Clip array to [lo, hi]."""
    return np.clip(arr, lo, hi)


def _logistic(x):
    """Numerically stable logistic / sigmoid."""
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


def _sample_names(n: int) -> list[str]:
    """Return *n* trainer names (first name + 4-digit ID suffix)."""
    first = RNG.choice(_FIRST_NAMES, size=n, replace=True)
    suffix = RNG.integers(1000, 9999, size=n)
    return [f"{f}_{s}" for f, s in zip(first, suffix)]


# ===================================================================
# 1. KANTO TRAINERS -- cross-sectional, 42 columns
# ===================================================================
def generate_kanto_trainers(n: int = 2000) -> pd.DataFrame:
    """
    Cross-sectional dataset of Kanto trainers.

    Causal graph (simplified):
        Latent {patience, natural_talent, dedication}
        wealth --> dept_store_spending, starter_type bias, exp_share_used
        trainer_experience --> strategy_score, starter_type, cave_training
        patience --> safari_zone_visits, strategy_score
        natural_talent --> strategy_score, team_avg_iv_total
        dedication --> play_hours, potions_purchased, tm_count
        strategy_score + team_level_avg + type_diversity + items
            --> badges --> elite_four outcomes
    """
    rng = RNG  # alias for brevity

    # -- IDs and names --
    trainer_id = np.arange(1, n + 1)
    trainer_name = _sample_names(n)

    # -- Hometown (uniform across 10 Kanto towns) --
    hometown = rng.choice(KANTO_TOWNS, size=n, replace=True)

    # -- Latent variables (hidden from students initially) --
    patience = rng.uniform(0, 100, size=n)
    natural_talent = rng.uniform(0, 100, size=n)
    dedication = rng.uniform(0, 100, size=n)

    # -- Wealth (1-5 ordinal, slight hometown effect) --
    hometown_wealth_bonus = np.array([
        0.3 if h in ("Celadon City", "Saffron City") else
        -0.3 if h in ("Lavender Town", "Pallet Town") else 0.0
        for h in hometown
    ])
    wealth_raw = rng.normal(3.0 + hometown_wealth_bonus, 0.8)
    wealth = _clip(np.round(wealth_raw), 1, 5).astype(int)

    # -- Trainer experience (years, 0-15) --
    trainer_experience = _clip(rng.exponential(4.0, size=n), 0, 15).round(1)

    # -- Starter type (wealth biases toward fire, experience biases toward
    #    water for "meta" reasons) -- softmax over three utilities
    u_grass = 0.0 + 0.05 * (trainer_experience - 4)  # baseline
    u_fire = 0.1 + 0.15 * (wealth - 3)               # wealthier -> fire
    u_water = -0.05 + 0.12 * (trainer_experience - 4) # experienced -> water
    stack = np.column_stack([
        np.exp(u_grass), np.exp(u_fire), np.exp(u_water),
    ])
    stack = stack / stack.sum(axis=1, keepdims=True)
    starter_idx = np.array([rng.choice(3, p=row) for row in stack])
    type_labels = ["Grass", "Fire", "Water"]
    starter_type = np.array([type_labels[i] for i in starter_idx])
    starter_species = np.array([KANTO_STARTERS[t] for t in starter_type])

    # -- Team statistics --
    team_size = _clip(
        rng.poisson(4.5 + 0.1 * trainer_experience, size=n), 1, 6
    ).astype(int)
    team_level_avg = _clip(
        20 + 3 * trainer_experience + 0.15 * dedication
        + rng.normal(0, 5, n), 5, 100
    ).round(1)
    team_level_max = _clip(
        team_level_avg + rng.exponential(8, n), team_level_avg, 100
    ).round(1)
    team_avg_iv_total = _clip(
        45 + 0.4 * natural_talent + rng.normal(0, 8, n), 0, 186
    ).round(1)
    type_diversity = _clip(
        rng.poisson(2 + 0.03 * trainer_experience + 0.01 * patience, size=n),
        1, 6,
    ).astype(int)

    # -- Trainer characteristics --
    play_hours = _clip(
        50 + 5 * dedication + 10 * trainer_experience
        + rng.normal(0, 40, n), 10, 999
    ).round(0).astype(int)

    strategy_score = _clip(
        20 + 0.25 * patience + 0.3 * natural_talent
        + 1.5 * trainer_experience + rng.normal(0, 8, n),
        0, 100,
    ).round(1)

    cave_training = (
        rng.uniform(size=n) < _logistic(
            -1.5 + 0.15 * trainer_experience + 0.02 * dedication
        )
    ).astype(int)

    safari_zone_visits = _clip(
        rng.poisson(1 + 0.04 * patience, size=n), 0, 30
    ).astype(int)

    # -- Items & spending --
    dept_store_spending = _clip(
        500 * wealth + 50 * play_hours * 0.01 + rng.normal(0, 300, n),
        0, 10000,
    ).round(0).astype(int)

    potions_purchased = _clip(
        10 + 0.3 * dedication + 0.05 * play_hours
        + rng.normal(0, 8, n), 0, 200
    ).round(0).astype(int)

    revives_used = _clip(
        rng.poisson(2 + 0.02 * play_hours, size=n), 0, 50
    ).astype(int)

    tm_count = _clip(
        2 + 0.1 * dedication + 0.3 * trainer_experience
        + rng.normal(0, 3, n), 0, 50
    ).round(0).astype(int)

    exp_share_used = (
        rng.uniform(size=n) < _logistic(
            -1.0 + 0.4 * (wealth - 3) + 0.1 * trainer_experience
        )
    ).astype(int)

    held_item_count = _clip(
        rng.poisson(1.5 + 0.1 * wealth + 0.05 * tm_count, size=n),
        0, 6,
    ).astype(int)

    rare_candy_used = _clip(
        rng.poisson(0.5 + 0.15 * (wealth - 1), size=n), 0, 20
    ).astype(int)

    # -- Training decisions --
    gym_pokemon_center_visits = _clip(
        rng.poisson(8 + 0.1 * play_hours, size=n), 0, 100
    ).astype(int)

    fishing_attempts = _clip(
        rng.poisson(3 + 0.03 * patience, size=n), 0, 50
    ).astype(int)

    traded_pokemon_count = _clip(
        rng.poisson(1 + 0.05 * trainer_experience, size=n), 0, 15
    ).astype(int)

    # -- Outcomes --
    # badges (0-8): core outcome driven by strategy, team, items
    badge_logit = (
        -4.0
        + 0.04 * strategy_score
        + 0.03 * team_level_avg
        + 0.15 * type_diversity
        + 0.01 * tm_count
        + 0.005 * dept_store_spending / 100
        + 0.3 * exp_share_used
        + 0.01 * held_item_count
    )
    # Convert to expected badges via scaled logistic
    badge_prob = _logistic(badge_logit)
    badges = _clip(
        np.floor(badge_prob * 9 + rng.normal(0, 0.6, n)), 0, 8
    ).astype(int)

    # Elite Four attempt requires 8 badges
    elite_four_attempted = (badges == 8).astype(int)

    # Elite Four win probability (conditional on attempting)
    ef_logit = (
        -3.0
        + 0.05 * strategy_score
        + 0.04 * team_level_avg
        + 0.2 * type_diversity
        + 0.02 * tm_count
        + 0.01 * natural_talent
    )
    ef_prob = _logistic(ef_logit)
    elite_four_wins_raw = (rng.uniform(size=n) < ef_prob).astype(int)
    elite_four_wins = elite_four_wins_raw * elite_four_attempted

    champion_defeated = np.zeros(n, dtype=int)
    champ_logit = ef_logit + 0.5  # slightly harder
    champ_prob = _logistic(champ_logit - 1.0)
    champion_defeated_raw = (rng.uniform(size=n) < champ_prob).astype(int)
    champion_defeated = champion_defeated_raw * elite_four_wins

    hall_of_fame_time = np.full(n, np.nan)
    hof_mask = champion_defeated == 1
    hall_of_fame_time[hof_mask] = _clip(
        play_hours[hof_mask] + rng.normal(20, 10, hof_mask.sum()),
        play_hours[hof_mask], 1200,
    ).round(0)

    total_battles_won = _clip(
        50 + 8 * trainer_experience + 0.3 * strategy_score
        + 0.2 * team_level_avg + rng.normal(0, 30, n),
        0, 999,
    ).round(0).astype(int)

    total_pokemon_caught = _clip(
        10 + 0.1 * play_hours + 0.05 * patience
        + 2 * safari_zone_visits + rng.normal(0, 10, n),
        1, 151,
    ).round(0).astype(int)

    pokedex_completion = _clip(
        total_pokemon_caught / 151 * 100, 0, 100
    ).round(1)

    # -- Hidden genetics (revealed in later chapters) --
    team_avg_ev_total = _clip(
        100 + 2 * play_hours * 0.1 + 1.5 * cave_training * 50
        + rng.normal(0, 30, n), 0, 510
    ).round(1)

    team_happiness_avg = _clip(
        120 + 0.3 * patience + 0.2 * dedication
        + rng.normal(0, 20, n), 0, 255
    ).round(1)

    team_friendship_max = _clip(
        team_happiness_avg + rng.exponential(15, n), 0, 255
    ).round(1)

    df = pd.DataFrame({
        "trainer_id": trainer_id,
        "trainer_name": trainer_name,
        "hometown": hometown,
        "starter_type": starter_type,
        "starter_species": starter_species,
        "team_size": team_size,
        "team_level_avg": team_level_avg,
        "team_level_max": team_level_max,
        "team_avg_iv_total": team_avg_iv_total,
        "team_avg_ev_total": team_avg_ev_total,
        "type_diversity": type_diversity,
        "trainer_experience": trainer_experience,
        "play_hours": play_hours,
        "strategy_score": strategy_score,
        "wealth": wealth,
        "cave_training": cave_training,
        "safari_zone_visits": safari_zone_visits,
        "dept_store_spending": dept_store_spending,
        "potions_purchased": potions_purchased,
        "revives_used": revives_used,
        "tm_count": tm_count,
        "exp_share_used": exp_share_used,
        "held_item_count": held_item_count,
        "rare_candy_used": rare_candy_used,
        "gym_pokemon_center_visits": gym_pokemon_center_visits,
        "fishing_attempts": fishing_attempts,
        "traded_pokemon_count": traded_pokemon_count,
        "team_happiness_avg": team_happiness_avg,
        "team_friendship_max": team_friendship_max,
        "badges": badges,
        "elite_four_attempted": elite_four_attempted,
        "elite_four_wins": elite_four_wins,
        "champion_defeated": champion_defeated,
        "hall_of_fame_time": hall_of_fame_time,
        "total_battles_won": total_battles_won,
        "total_pokemon_caught": total_pokemon_caught,
        "pokedex_completion": pokedex_completion,
        # Hidden / latent -- revealed in appendix / later chapters
        "patience": patience.round(2),
        "natural_talent": natural_talent.round(2),
        "dedication": dedication.round(2),
        # Remaining columns to reach 42
        "hometown_gym_type": [
            {"Pallet Town": "None", "Viridian City": "Ground",
             "Pewter City": "Rock", "Cerulean City": "Water",
             "Vermilion City": "Electric", "Lavender Town": "Ghost",
             "Celadon City": "Grass", "Fuchsia City": "Poison",
             "Saffron City": "Psychic", "Cinnabar Island": "Fire"}[h]
            for h in hometown
        ],
        "region": "Kanto",
    })

    assert df.shape[1] == 42, f"Expected 42 columns, got {df.shape[1]}"
    return df


# ===================================================================
# 2. KANTO BATTLES -- battle-level data, 28 columns
# ===================================================================
def generate_kanto_battles(
    n: int = 50_000,
    trainers_df: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """
    Battle-level dataset.  Each row is one battle.

    Types: wild, trainer, gym, elite_four.
    Includes type-advantage multipliers, weather, terrain, held items, crits.
    """
    rng = RNG

    if trainers_df is None:
        trainers_df = generate_kanto_trainers()

    n_trainers = len(trainers_df)

    # -- Battle metadata --
    battle_id = np.arange(1, n + 1)

    # Assign each battle to a trainer (weighted by play_hours)
    weights = trainers_df["play_hours"].values.astype(float)
    weights /= weights.sum()
    trainer_idx = rng.choice(n_trainers, size=n, p=weights)
    trainer_id = trainers_df["trainer_id"].values[trainer_idx]

    # Battle type distribution
    battle_type_probs = [0.45, 0.35, 0.15, 0.05]  # wild, trainer, gym, e4
    battle_type = rng.choice(
        ["wild", "trainer", "gym", "elite_four"],
        size=n, p=battle_type_probs,
    )

    # -- Attacker stats (from trainer's team) --
    attacker_level = _clip(
        trainers_df["team_level_avg"].values[trainer_idx]
        + rng.normal(0, 5, n), 1, 100,
    ).round(0).astype(int)

    attacker_type = rng.choice(POKEMON_TYPES, size=n)

    # -- Defender stats --
    defender_level_base = np.where(
        battle_type == "wild",
        _clip(attacker_level * 0.7 + rng.normal(0, 8, n), 2, 100),
        np.where(
            battle_type == "gym",
            _clip(attacker_level * 1.1 + rng.normal(0, 5, n), 5, 100),
            np.where(
                battle_type == "elite_four",
                _clip(attacker_level * 1.2 + rng.normal(0, 4, n), 50, 100),
                _clip(attacker_level + rng.normal(0, 10, n), 2, 100),
            ),
        ),
    ).round(0).astype(int)
    defender_level = _clip(defender_level_base, 1, 100)
    defender_type = rng.choice(POKEMON_TYPES, size=n)

    # -- Type advantage multiplier --
    # Simplified: 2.0 if super-effective, 0.5 if not very effective, 1.0 neutral
    # Use a deterministic hash for consistency
    type_advantage = np.ones(n)
    for i in range(n):
        pair_hash = hash((attacker_type[i], defender_type[i])) % 10
        if pair_hash < 2:
            type_advantage[i] = 2.0
        elif pair_hash < 4:
            type_advantage[i] = 0.5
        else:
            type_advantage[i] = 1.0

    # -- Weather & terrain --
    weather = rng.choice(
        ["clear", "rain", "sun", "sandstorm", "hail"],
        size=n, p=[0.50, 0.20, 0.15, 0.10, 0.05],
    )
    terrain = rng.choice(
        ["grass", "cave", "water", "urban", "mountain"],
        size=n, p=[0.30, 0.20, 0.15, 0.20, 0.15],
    )

    # Weather multiplier (rain boosts water, sun boosts fire, etc.)
    weather_multiplier = np.ones(n)
    weather_multiplier[(weather == "rain") & (attacker_type == "Water")] = 1.5
    weather_multiplier[(weather == "sun") & (attacker_type == "Fire")] = 1.5
    weather_multiplier[(weather == "rain") & (attacker_type == "Fire")] = 0.5
    weather_multiplier[(weather == "sun") & (attacker_type == "Water")] = 0.5

    # -- Held item & move power --
    held_item = rng.choice(
        ["none", "leftovers", "choice_band", "focus_sash", "berry"],
        size=n, p=[0.40, 0.15, 0.15, 0.15, 0.15],
    )
    held_item_bonus = np.where(
        held_item == "choice_band", 1.3,
        np.where(held_item == "leftovers", 1.05, 1.0),
    )

    move_power = _clip(rng.normal(75, 20, n), 20, 150).round(0).astype(int)
    move_accuracy = _clip(rng.normal(90, 10, n), 30, 100).round(0).astype(int)
    move_hit = (rng.uniform(size=n) * 100 < move_accuracy).astype(int)

    # Critical hit (6.25% base rate)
    critical_hit = (rng.uniform(size=n) < 0.0625).astype(int)
    crit_multiplier = np.where(critical_hit, 1.5, 1.0)

    # -- Strategy (from trainer) --
    strategy = trainers_df["strategy_score"].values[trainer_idx]

    # -- Damage calculation --
    raw_damage = (
        (2 * attacker_level / 5 + 2) * move_power / 50
        * type_advantage
        * weather_multiplier
        * held_item_bonus
        * crit_multiplier
        * move_hit
        * (1 + 0.005 * strategy)
    )
    damage_dealt = _clip(raw_damage + rng.normal(0, 5, n), 0, 999).round(1)

    # -- Battle outcome --
    win_logit = (
        -0.5
        + 0.02 * (attacker_level - defender_level)
        + 0.5 * np.log(np.maximum(type_advantage, 0.1))
        + 0.3 * (weather_multiplier - 1.0)
        + 0.01 * strategy
        + 0.005 * damage_dealt
    )
    win_prob = _logistic(win_logit)
    battle_won = (rng.uniform(size=n) < win_prob).astype(int)

    # -- Turns to resolve --
    turns = _clip(rng.poisson(4, size=n), 1, 30).astype(int)

    # -- Experience gained --
    exp_gained = _clip(
        defender_level * 5 * battle_won
        * np.where(battle_type == "gym", 2.0,
                   np.where(battle_type == "elite_four", 3.0, 1.0))
        + rng.normal(0, 20, n),
        0, 5000,
    ).round(0).astype(int)

    # -- Pokemon fainted (attacker side) --
    pokemon_fainted = (
        (rng.uniform(size=n) < (1 - win_prob) * 0.6)
    ).astype(int)

    df = pd.DataFrame({
        "battle_id": battle_id,
        "trainer_id": trainer_id,
        "battle_type": battle_type,
        "attacker_level": attacker_level,
        "attacker_type": attacker_type,
        "defender_level": defender_level,
        "defender_type": defender_type,
        "type_advantage": type_advantage,
        "weather": weather,
        "weather_multiplier": weather_multiplier,
        "terrain": terrain,
        "held_item": held_item,
        "held_item_bonus": held_item_bonus,
        "move_power": move_power,
        "move_accuracy": move_accuracy,
        "move_hit": move_hit,
        "critical_hit": critical_hit,
        "crit_multiplier": crit_multiplier,
        "damage_dealt": damage_dealt,
        "strategy_score": strategy.round(1),
        "turns": turns,
        "battle_won": battle_won,
        "exp_gained": exp_gained,
        "pokemon_fainted": pokemon_fainted,
        "win_prob": win_prob.round(4),
        "attacker_hp_remaining_pct": _clip(
            rng.beta(2 + 3 * battle_won, 2 + 3 * (1 - battle_won), size=n),
            0, 1,
        ).round(3),
        "defender_hp_remaining_pct": _clip(
            rng.beta(2 + 3 * (1 - battle_won), 2 + 3 * battle_won, size=n),
            0, 1,
        ).round(3),
        "reward_money": _clip(
            battle_won * defender_level * 50
            * np.where(battle_type == "gym", 5, 1)
            + rng.normal(0, 100, n),
            0, 50000,
        ).round(0).astype(int),
    })

    assert df.shape[1] == 28, f"Expected 28 columns, got {df.shape[1]}"
    return df


# ===================================================================
# 3. KANTO CITIES PANEL -- city x month, DiD + invasion
# ===================================================================
def generate_cities_panel(
    n_cities: int = 8,
    n_periods: int = 24,
) -> pd.DataFrame:
    """
    Panel: 8 cities x 24 months.

    Treatments:
    - shadow_surge (staggered adoption):
        Saffron=6, Cerulean=10, Vermilion=14, Lavender=18.
        Others never adopt.
    - team_rocket_invasion: a shock event.

    Outcome: avg_trainer_level, monthly_battles, pokemon_center_visits,
    gym_revenue.
    """
    rng = RNG

    cities = [
        "Pewter City", "Cerulean City", "Vermilion City", "Lavender Town",
        "Celadon City", "Fuchsia City", "Saffron City", "Cinnabar Island",
    ]

    # Staggered adoption periods (0 = never treated)
    adoption = {
        "Saffron City": 6, "Cerulean City": 10,
        "Vermilion City": 14, "Lavender Town": 18,
        "Pewter City": 0, "Celadon City": 0,
        "Fuchsia City": 0, "Cinnabar Island": 0,
    }

    # City-level fixed effects (baseline trainer level)
    city_fe = {
        "Pewter City": 28, "Cerulean City": 33, "Vermilion City": 35,
        "Lavender Town": 25, "Celadon City": 38, "Fuchsia City": 30,
        "Saffron City": 42, "Cinnabar Island": 36,
    }

    # Team Rocket invasion: hits Saffron in period 8, Celadon in period 12
    rocket_invasion = {
        ("Saffron City", 8): 1, ("Saffron City", 9): 1,
        ("Celadon City", 12): 1, ("Celadon City", 13): 1,
    }

    rows = []
    for city in cities:
        base_level = city_fe[city]
        adopt_period = adoption[city]

        for t in range(1, n_periods + 1):
            # Time trend (common)
            time_trend = 0.5 * t

            # Treatment indicator
            treated = 1 if (adopt_period > 0 and t >= adopt_period) else 0
            periods_treated = max(0, t - adopt_period) if adopt_period > 0 else 0

            # Treatment effect (grows with exposure, heterogeneous by city)
            treat_effect = treated * (3.0 + 0.4 * periods_treated)
            if city == "Saffron City":
                treat_effect *= 1.3  # Saffron benefits more (bigger city)

            # Team Rocket invasion shock
            invaded = rocket_invasion.get((city, t), 0)
            invasion_effect = -8.0 * invaded

            # Outcome: avg_trainer_level
            avg_trainer_level = (
                base_level + time_trend + treat_effect + invasion_effect
                + rng.normal(0, 1.5)
            )

            # Monthly battles
            monthly_battles = _clip(
                500 + 20 * base_level + 30 * t + 100 * treated
                - 200 * invaded + rng.normal(0, 80),
                100, 5000,
            ).round(0)

            # Pokemon center visits
            pokemon_center_visits = _clip(
                300 + 10 * base_level + 5 * t - 50 * treated
                + 150 * invaded + rng.normal(0, 50),
                50, 3000,
            ).round(0)

            # Gym revenue
            gym_revenue = _clip(
                10000 + 500 * base_level + 200 * t + 2000 * treated
                - 5000 * invaded + rng.normal(0, 1000),
                0, 100000,
            ).round(0)

            # Population (slowly growing)
            population = int(
                5000 + 200 * base_level + 50 * t + rng.normal(0, 100)
            )

            rows.append({
                "city": city,
                "period": t,
                "shadow_surge_adopted": treated,
                "adoption_period": adopt_period if adopt_period > 0 else np.nan,
                "periods_since_adoption": periods_treated,
                "team_rocket_invasion": invaded,
                "avg_trainer_level": round(avg_trainer_level, 1),
                "monthly_battles": int(monthly_battles),
                "pokemon_center_visits": int(pokemon_center_visits),
                "gym_revenue": int(gym_revenue),
                "population": population,
                "city_fe": base_level,
            })

    return pd.DataFrame(rows)


# ===================================================================
# 4. PEWTER PROTEIN RCT -- RCT with noncompliance
# ===================================================================
def generate_protein_rct(n: int = 200) -> pd.DataFrame:
    """
    RCT: Protein supplement effect on beating Brock (Pewter Gym).

    Noncompliance:
    - complier (~60%): takes treatment iff assigned
    - always_taker (~15%): takes protein regardless
    - never_taker (~25%): never takes protein

    This lets students practice ITT, CACE/LATE, and IV estimation.
    """
    rng = RNG

    trainer_id = np.arange(1, n + 1)

    # Pre-treatment covariates
    starter_type = rng.choice(["Grass", "Fire", "Water"], size=n)
    team_level = _clip(rng.normal(14, 3, n), 5, 25).round(0).astype(int)
    trainer_experience = _clip(rng.exponential(2, n), 0, 10).round(1)
    strategy_score = _clip(
        30 + 0.5 * trainer_experience * 10 + rng.normal(0, 8, n), 0, 100
    ).round(1)

    # Compliance type (latent)
    comp_probs = [0.60, 0.15, 0.25]
    compliance_type = rng.choice(
        ["complier", "always_taker", "never_taker"],
        size=n, p=comp_probs,
    )

    # Random assignment (balanced)
    treatment_assigned = np.zeros(n, dtype=int)
    treatment_assigned[rng.permutation(n)[:n // 2]] = 1

    # Treatment received (depends on compliance type and assignment)
    treatment_received = np.where(
        compliance_type == "always_taker", 1,
        np.where(
            compliance_type == "never_taker", 0,
            treatment_assigned,  # compliers follow assignment
        ),
    )

    # True causal effect of protein: ~+15pp on win probability
    # Type advantage matters: Water/Grass >> Fire against Brock (Rock type)
    type_bonus = np.where(
        starter_type == "Water", 1.0,
        np.where(starter_type == "Grass", 0.8, -0.6),  # Fire is bad vs Rock
    )

    win_logit = (
        -3.5
        + 0.12 * team_level
        + 0.01 * strategy_score
        + type_bonus
        + 0.7 * treatment_received   # protein effect (causal)
    )
    win_prob = _logistic(win_logit)
    brock_win = (rng.uniform(size=n) < win_prob).astype(int)

    # Post-battle stats (type_bonus on original scale for damage calc)
    type_damage_bonus = np.where(
        starter_type == "Water", 20,
        np.where(starter_type == "Grass", 18, -5),
    )
    damage_to_onix = _clip(
        50 + 3 * team_level + type_damage_bonus + 15 * treatment_received
        + rng.normal(0, 15, n), 0, 200,
    ).round(0).astype(int)

    pokemon_remaining = _clip(
        rng.poisson(2 + 2 * brock_win, size=n), 0, 6
    ).astype(int)

    df = pd.DataFrame({
        "trainer_id": trainer_id,
        "treatment_assigned": treatment_assigned,
        "treatment_received": treatment_received,
        "compliance_type": compliance_type,
        "starter_type": starter_type,
        "team_level": team_level,
        "trainer_experience": trainer_experience,
        "strategy_score": strategy_score,
        "brock_win": brock_win,
        "damage_to_onix": damage_to_onix,
        "pokemon_remaining": pokemon_remaining,
        "win_prob": win_prob.round(4),
    })

    return df


# ===================================================================
# 5. SS ANNE PASSENGERS -- matching dataset
# ===================================================================
def generate_ss_anne(n: int = 400) -> pd.DataFrame:
    """
    Matching / propensity score dataset.

    Treatment: thunder_training (Lt. Surge's special training session).
    Outcome: surge_gym_win.

    Confounders observed: team_level, trainer_experience, badges_pre,
                          electric_type_count, strategy_score.
    Confounders hidden (revealed later): patience, natural_talent.

    Selection into thunder_training is driven by both observed and
    unobserved confounders -- classic selection bias.
    """
    rng = RNG

    trainer_id = np.arange(1, n + 1)

    # Latent confounders
    patience = rng.uniform(0, 100, n)
    natural_talent = rng.uniform(0, 100, n)

    # Observed pre-treatment
    team_level = _clip(
        20 + 0.2 * natural_talent + rng.normal(0, 5, n), 5, 60
    ).round(0).astype(int)

    trainer_experience = _clip(
        rng.exponential(3, n) + 0.02 * patience, 0, 12
    ).round(1)

    badges_pre = _clip(
        rng.poisson(2 + 0.03 * trainer_experience * 10, size=n), 0, 5
    ).astype(int)

    electric_type_count = _clip(
        rng.poisson(0.8 + 0.01 * natural_talent, size=n), 0, 4
    ).astype(int)

    strategy_score = _clip(
        25 + 0.2 * patience + 0.25 * natural_talent
        + 1.0 * trainer_experience + rng.normal(0, 8, n),
        0, 100,
    ).round(1)

    starter_type = rng.choice(["Grass", "Fire", "Water"], size=n)

    wealth = _clip(rng.normal(3, 0.8, n).round(), 1, 5).astype(int)

    # Selection into treatment (thunder_training)
    # Driven by both observed AND unobserved confounders
    treat_logit = (
        -4.0
        + 0.04 * team_level
        + 0.12 * trainer_experience
        + 0.3 * electric_type_count
        + 0.01 * strategy_score
        + 0.012 * patience          # unobserved
        + 0.008 * natural_talent    # unobserved
    )
    treat_prob = _logistic(treat_logit)
    thunder_training = (rng.uniform(size=n) < treat_prob).astype(int)

    # Outcome: surge_gym_win
    # True treatment effect of thunder_training: +15pp
    win_logit = (
        -2.5
        + 0.05 * team_level
        + 0.1 * trainer_experience
        + 0.4 * electric_type_count
        + 0.02 * strategy_score
        + 0.01 * patience
        + 0.015 * natural_talent
        + 0.7 * thunder_training    # causal effect
    )
    win_prob = _logistic(win_logit)
    surge_gym_win = (rng.uniform(size=n) < win_prob).astype(int)

    # Post-battle
    turns_to_win = np.where(
        surge_gym_win == 1,
        _clip(rng.poisson(6, n), 1, 30),
        _clip(rng.poisson(10, n), 3, 30),
    ).astype(int)

    pokemon_remaining = _clip(
        rng.poisson(2 + 2 * surge_gym_win, size=n), 0, 6
    ).astype(int)

    propensity_true = treat_prob.round(4)

    df = pd.DataFrame({
        "trainer_id": trainer_id,
        "thunder_training": thunder_training,
        "team_level": team_level,
        "trainer_experience": trainer_experience,
        "badges_pre": badges_pre,
        "electric_type_count": electric_type_count,
        "strategy_score": strategy_score,
        "starter_type": starter_type,
        "wealth": wealth,
        "surge_gym_win": surge_gym_win,
        "turns_to_win": turns_to_win,
        "pokemon_remaining": pokemon_remaining,
        "propensity_true": propensity_true,
        # Hidden -- revealed in later exercises
        "patience": patience.round(2),
        "natural_talent": natural_talent.round(2),
    })

    return df


# ===================================================================
# 6. SAFARI ZONE LOTTERY -- instrumental variables
# ===================================================================
def generate_safari_lottery(n: int = 600) -> pd.DataFrame:
    """
    IV dataset: Safari Zone Lottery.

    Instrument:  lottery_won (random ticket draw)
    Treatment:   safari_attended (whether trainer actually went)
    Outcome:     battle_wins_post (post-safari battle performance)

    Unobserved confounder: patience (affects both safari attendance
    and battle performance).

    Compliance types:
    - complier: attends iff lottery won
    - always_taker: attends regardless (pays scalper)
    - never_taker: never attends even if won
    """
    rng = RNG

    trainer_id = np.arange(1, n + 1)

    # Latent
    patience = rng.uniform(0, 100, n)
    motivation = rng.uniform(0, 100, n)  # another latent driver

    # Observed pre-treatment
    team_level = _clip(rng.normal(30, 8, n), 5, 60).round(0).astype(int)
    trainer_experience = _clip(rng.exponential(3.5, n), 0, 12).round(1)
    badges = _clip(rng.poisson(3, n), 0, 8).astype(int)
    strategy_score = _clip(
        30 + 0.2 * patience + 0.15 * motivation + rng.normal(0, 10, n),
        0, 100,
    ).round(1)

    # Pre-treatment outcome (for comparison)
    battle_wins_pre = _clip(
        20 + 0.5 * team_level + 0.3 * strategy_score
        + 0.1 * patience + rng.normal(0, 10, n),
        0, 100,
    ).round(0).astype(int)

    # Compliance type (driven by patience -- unobserved confounder)
    # Patient trainers are more likely to be always_takers or compliers
    # (they'll find a way to attend regardless)
    comp_logit_always = -3.0 + 0.04 * patience  # ~10-25% always_taker
    comp_logit_never = -0.5 - 0.03 * patience   # ~15-30% never_taker
    p_always = _logistic(comp_logit_always)
    p_never = _logistic(comp_logit_never)
    p_complier = 1.0 - p_always - p_never
    # Ensure valid probabilities
    comp_stack = np.column_stack([p_always, p_complier, np.maximum(p_never, 0.05)])
    comp_stack = np.maximum(comp_stack, 0.02)
    comp_stack = comp_stack / comp_stack.sum(axis=1, keepdims=True)
    comp_labels = ["always_taker", "complier", "never_taker"]
    compliance_type = np.array([
        rng.choice(comp_labels, p=row) for row in comp_stack
    ])

    # Instrument: lottery (random -- excludability satisfied)
    lottery_won = rng.binomial(1, 0.5, n)

    # Treatment received (depends on compliance + instrument)
    safari_attended = np.where(
        compliance_type == "always_taker", 1,
        np.where(
            compliance_type == "never_taker", 0,
            lottery_won,
        ),
    )

    # Outcome: battle_wins_post
    # Safari has TRUE causal effect: +8 wins (diverse pokemon, rare catches)
    # But patience also drives outcomes (omitted variable)
    battle_wins_post = _clip(
        battle_wins_pre
        + 8.0 * safari_attended              # causal effect
        + 0.15 * patience                     # unobserved confounder
        + 0.05 * motivation
        + rng.normal(0, 6, n),
        0, 150,
    ).round(0).astype(int)

    # Pokemon caught in safari
    pokemon_caught_safari = np.where(
        safari_attended == 1,
        _clip(rng.poisson(5 + 0.03 * patience, n), 0, 30),
        0,
    ).astype(int)

    df = pd.DataFrame({
        "trainer_id": trainer_id,
        "lottery_won": lottery_won,
        "safari_attended": safari_attended,
        "compliance_type": compliance_type,
        "team_level": team_level,
        "trainer_experience": trainer_experience,
        "badges": badges,
        "strategy_score": strategy_score,
        "battle_wins_pre": battle_wins_pre,
        "battle_wins_post": battle_wins_post,
        "pokemon_caught_safari": pokemon_caught_safari,
        # Hidden
        "patience": patience.round(2),
        "motivation": motivation.round(2),
    })

    return df


# ===================================================================
# 7. HAPPINESS EVOLUTION -- RDD
# ===================================================================
def generate_happiness_evolution(n: int = 800) -> pd.DataFrame:
    """
    Regression discontinuity: happiness threshold for evolution.

    Running variable: happiness_score (150-280)
    Threshold: 220 (pokemon evolves at >= 220)
    Sharp treatment: evolved (happiness >= 220)
    Fuzzy treatment: trainer_pressed_b (some trainers cancel evolution)

    Outcome: battle_performance_post
    """
    rng = RNG

    pokemon_id = np.arange(1, n + 1)

    # Running variable: happiness score
    # Generate around the threshold with a nice spread
    happiness_score = _clip(
        rng.normal(220, 30, n), 150, 280
    ).round(1)

    # Sharp treatment: evolved iff happiness >= 220
    above_threshold = (happiness_score >= 220).astype(int)

    # Fuzzy component: some trainers press B to cancel evolution
    # ~15% of those above threshold press B (more likely if just barely above)
    distance_above = np.maximum(happiness_score - 220, 0)
    press_b_prob = np.where(
        above_threshold == 1,
        _logistic(-1.5 - 0.03 * distance_above),  # less likely to cancel if way above
        0,
    )
    trainer_pressed_b = (rng.uniform(size=n) < press_b_prob).astype(int)

    # Actual evolution (sharp minus those who pressed B)
    evolved = (above_threshold & ~trainer_pressed_b.astype(bool)).astype(int)

    # Pre-treatment covariates
    pokemon_level = _clip(rng.normal(30, 8, n), 10, 60).round(0).astype(int)
    friendship_days = _clip(
        (happiness_score - 100) * 0.5 + rng.normal(0, 10, n), 1, 100
    ).round(0).astype(int)
    trainer_skill = _clip(rng.normal(50, 15, n), 0, 100).round(1)
    pokemon_species = rng.choice(
        ["Eevee", "Golbat", "Chansey", "Pichu", "Togepi"],
        size=n,
    )

    # Outcome: battle_performance_post
    # True causal effect of evolution: +12 points
    # Smooth function of happiness on both sides (potential outcomes continuous)
    baseline = (
        30
        + 0.15 * happiness_score
        + 0.3 * pokemon_level
        + 0.1 * trainer_skill
    )

    battle_performance_post = _clip(
        baseline
        + 12.0 * evolved  # sharp discontinuity for evolved
        + rng.normal(0, 5, n),
        0, 120,
    ).round(1)

    # Also generate what we'd see for "intent to treat" (above threshold)
    battle_performance_itt = _clip(
        baseline
        + 12.0 * above_threshold * 0.85  # attenuated by non-compliance
        + rng.normal(0, 5, n),
        0, 120,
    ).round(1)

    # Potential outcomes (for teaching)
    y0 = _clip(baseline + rng.normal(0, 5, n), 0, 120).round(1)
    y1 = _clip(baseline + 12.0 + rng.normal(0, 5, n), 0, 120).round(1)

    df = pd.DataFrame({
        "pokemon_id": pokemon_id,
        "happiness_score": happiness_score,
        "above_threshold": above_threshold,
        "trainer_pressed_b": trainer_pressed_b,
        "evolved": evolved,
        "pokemon_level": pokemon_level,
        "friendship_days": friendship_days,
        "trainer_skill": trainer_skill,
        "pokemon_species": pokemon_species,
        "battle_performance_post": battle_performance_post,
        "battle_performance_itt": battle_performance_itt,
        # Potential outcomes (revealed in solutions)
        "y0": y0,
        "y1": y1,
    })

    return df


# ===================================================================
# 8. SHADOW SURGE STAGGERED -- staggered DiD
# ===================================================================
def generate_shadow_surge_staggered(
    n_cities: int = 8,
    n_periods: int = 24,
) -> pd.DataFrame:
    """
    Staggered difference-in-differences.

    Treated cities (adoption period):
        Saffron City (6), Cerulean City (10),
        Vermilion City (14), Lavender Town (18).
    Never-treated:
        Celadon City, Fuchsia City, Pewter City, Cinnabar Island.

    Outcome: avg_pokemon_level (city-month level).

    Features heterogeneous + dynamic treatment effects so TWFE is biased.
    Students learn Callaway-Sant'Anna, Sun-Abraham, Goodman-Bacon.
    """
    rng = RNG

    cities = [
        "Saffron City", "Cerulean City", "Vermilion City", "Lavender Town",
        "Celadon City", "Fuchsia City", "Pewter City", "Cinnabar Island",
    ]

    adoption = {
        "Saffron City": 6, "Cerulean City": 10,
        "Vermilion City": 14, "Lavender Town": 18,
        "Celadon City": 0, "Fuchsia City": 0,
        "Pewter City": 0, "Cinnabar Island": 0,
    }

    # City-level intercepts
    city_intercept = {
        "Saffron City": 42, "Cerulean City": 35, "Vermilion City": 33,
        "Lavender Town": 26, "Celadon City": 38, "Fuchsia City": 30,
        "Pewter City": 28, "Cinnabar Island": 36,
    }

    # Heterogeneous treatment effects by cohort
    # Early adopters get bigger effects (Saffron is tech-savvy)
    te_by_city = {
        "Saffron City": 5.0, "Cerulean City": 3.5,
        "Vermilion City": 2.5, "Lavender Town": 2.0,
    }

    rows = []
    for city in cities:
        alpha = city_intercept[city]
        g = adoption[city]  # cohort (0 = never)

        for t in range(1, n_periods + 1):
            # Common time trend (parallel in absence of treatment)
            time_effect = 0.4 * t + 0.01 * t ** 2 * 0.1

            # Treatment status
            treated = 1 if (g > 0 and t >= g) else 0
            rel_time = (t - g) if g > 0 else np.nan

            # Dynamic treatment effect: grows then stabilises
            if treated:
                periods_post = t - g
                base_te = te_by_city.get(city, 0)
                # Effect ramps up then levels off (log growth)
                dynamic_te = base_te * np.log1p(periods_post)
            else:
                dynamic_te = 0.0

            # No anticipation: pre-treatment effect = 0
            # (Students can test this)

            avg_pokemon_level = (
                alpha + time_effect + dynamic_te + rng.normal(0, 1.0)
            )

            # Secondary outcomes
            gym_challengers = int(_clip(
                100 + 3 * alpha + 5 * t + 20 * treated + rng.normal(0, 15),
                10, 500,
            ))
            potion_sales = int(_clip(
                200 + 5 * alpha + 8 * t + 40 * treated + rng.normal(0, 30),
                20, 1000,
            ))

            rows.append({
                "city": city,
                "period": t,
                "cohort": g if g > 0 else np.nan,
                "treated": treated,
                "rel_time": rel_time if treated or (g > 0) else np.nan,
                "avg_pokemon_level": round(avg_pokemon_level, 2),
                "gym_challengers": gym_challengers,
                "potion_sales": potion_sales,
                "city_intercept": alpha,
                "true_te": round(dynamic_te, 4),
            })

    return pd.DataFrame(rows)


# ===================================================================
# 9. ELITE FOUR PANEL -- sequential battles, dynamic treatment
# ===================================================================
def generate_elite_four_panel(n_trainers: int = 500) -> pd.DataFrame:
    """
    Panel of trainers facing the Elite Four (4 sequential battles):
    Lorelei (Ice), Bruno (Fighting), Agatha (Ghost), Lance (Dragon).

    Time-varying treatment: item_used (healing item between rounds).
    Time-varying confounder: fatigue (accumulates), morale (fluctuates).
    Mediator: pokemon_health_entering (health going into battle).

    This dataset teaches:
    - Time-varying treatments / g-computation
    - Mediation analysis
    - Sequential decision making
    """
    rng = RNG

    opponents = ["Lorelei", "Bruno", "Agatha", "Lance"]
    opponent_types = ["Ice", "Fighting", "Ghost", "Dragon"]
    opponent_difficulty = [0.5, 0.6, 0.7, 0.9]  # Lance is hardest

    rows = []

    for tid in range(1, n_trainers + 1):
        # Trainer-level covariates (time-invariant)
        team_level = int(_clip(rng.normal(55, 8), 35, 80))
        strategy = round(_clip(rng.normal(60, 15), 10, 100), 1)
        type_coverage = int(_clip(rng.poisson(4), 1, 6))
        badges = 8  # everyone here has 8 badges

        # Initial state
        health = 100.0
        fatigue = 0.0
        morale = 70 + rng.normal(0, 10)
        still_alive = True

        for battle_idx, (opp, opp_type, diff) in enumerate(
            zip(opponents, opponent_types, opponent_difficulty)
        ):
            if not still_alive:
                # Trainer already lost -- still record the row
                rows.append({
                    "trainer_id": tid,
                    "battle_round": battle_idx + 1,
                    "opponent": opp,
                    "opponent_type": opp_type,
                    "team_level": team_level,
                    "strategy_score": strategy,
                    "type_coverage": type_coverage,
                    "fatigue": round(fatigue, 2),
                    "morale": round(morale, 2),
                    "pokemon_health_entering": round(health, 2),
                    "item_used": 0,
                    "item_type": "none",
                    "battle_won": 0,
                    "damage_taken": 0.0,
                    "damage_dealt": 0.0,
                    "turns": 0,
                    "still_in_tournament": 0,
                })
                continue

            # Decision to use item (time-varying treatment)
            # More likely when health is low or fatigue is high
            item_logit = (
                -1.0
                - 0.03 * health
                + 0.02 * fatigue
                - 0.01 * morale
                + 0.01 * strategy  # strategic trainers use items wisely
            )
            item_prob = _logistic(item_logit)
            item_used = int(rng.uniform() < item_prob)

            item_types = ["potion", "full_restore", "revive", "x_attack"]
            item_type = rng.choice(item_types) if item_used else "none"

            # Item effect on health (mediator)
            if item_used:
                if item_type == "full_restore":
                    health = min(100, health + 60)
                elif item_type == "potion":
                    health = min(100, health + 30)
                elif item_type == "revive":
                    health = min(100, health + 40)
                # x_attack doesn't heal

            pokemon_health_entering = health

            # Battle outcome
            win_logit = (
                -1.5 - 2.0 * diff
                + 0.04 * team_level
                + 0.02 * strategy
                + 0.15 * type_coverage
                + 0.01 * pokemon_health_entering
                - 0.02 * fatigue
                + 0.01 * morale
                + 0.3 * (item_type == "x_attack")
            )
            win_prob = _logistic(win_logit)
            battle_won = int(rng.uniform() < win_prob)

            # Damage exchanged
            damage_taken = round(_clip(
                30 * diff + 10 - 0.1 * strategy + rng.normal(0, 10), 0, 80
            ), 1)
            damage_dealt = round(_clip(
                20 + 0.3 * team_level + 0.1 * strategy
                + 10 * (item_type == "x_attack") + rng.normal(0, 10),
                0, 150,
            ), 1)

            turns = int(_clip(rng.poisson(5 + 2 * diff), 1, 25))

            rows.append({
                "trainer_id": tid,
                "battle_round": battle_idx + 1,
                "opponent": opp,
                "opponent_type": opp_type,
                "team_level": team_level,
                "strategy_score": strategy,
                "type_coverage": type_coverage,
                "fatigue": round(fatigue, 2),
                "morale": round(morale, 2),
                "pokemon_health_entering": round(pokemon_health_entering, 2),
                "item_used": item_used,
                "item_type": item_type,
                "battle_won": battle_won,
                "damage_taken": damage_taken,
                "damage_dealt": damage_dealt,
                "turns": turns,
                "still_in_tournament": 1,
            })

            # Update state for next round
            health = max(0, health - damage_taken)
            fatigue = min(100, fatigue + 10 + 5 * (1 - battle_won) + rng.normal(0, 3))
            morale = _clip(
                morale + 15 * battle_won - 20 * (1 - battle_won) + rng.normal(0, 5),
                0, 100,
            )

            if not battle_won:
                still_alive = False

    return pd.DataFrame(rows)


# ===================================================================
# 10. DOUBLE BATTLES -- interference / spillover
# ===================================================================
def generate_double_battles(n: int = 1000) -> pd.DataFrame:
    """
    Interference / spillover dataset.

    In double battles two pokemon fight side by side.  Some moves
    (Earthquake, Surf, Discharge) hit the partner -- SUTVA violation.

    Treatment: pokemon_a_move_type (spread vs single-target)
    Outcome: battle_won, pokemon_b_hp_lost (spillover)
    """
    rng = RNG

    battle_id = np.arange(1, n + 1)

    # Pokemon A (the one whose move choice we study)
    pokemon_a_level = _clip(rng.normal(45, 10, n), 10, 80).round(0).astype(int)
    pokemon_a_type = rng.choice(
        ["Ground", "Water", "Electric", "Fire", "Normal"], size=n,
    )
    pokemon_a_attack = _clip(
        50 + 0.8 * pokemon_a_level + rng.normal(0, 10, n), 10, 200
    ).round(0).astype(int)

    # Pokemon B (partner)
    pokemon_b_level = _clip(rng.normal(45, 10, n), 10, 80).round(0).astype(int)
    pokemon_b_type = rng.choice(
        ["Flying", "Grass", "Psychic", "Fire", "Water"], size=n,
    )
    pokemon_b_hp = _clip(
        80 + 2 * pokemon_b_level + rng.normal(0, 15, n), 30, 250
    ).round(0).astype(int)

    # Opponents
    opp1_level = _clip(rng.normal(45, 10, n), 10, 80).round(0).astype(int)
    opp2_level = _clip(rng.normal(45, 10, n), 10, 80).round(0).astype(int)

    # Treatment: spread move (Earthquake, Surf, etc.) vs single-target
    # More likely when opponents are both threatening; less likely with Flying partner
    spread_logit = (
        0.2
        + 0.005 * pokemon_a_attack
        - 0.8 * (pokemon_b_type == "Flying").astype(float)  # careful with partner
        - 0.005 * pokemon_b_hp  # less worried if partner is tanky
        + 0.005 * (opp1_level + opp2_level)  # more tempting vs strong foes
    )
    spread_prob = _logistic(spread_logit)
    used_spread_move = (rng.uniform(size=n) < spread_prob).astype(int)

    move_name = np.where(
        used_spread_move,
        np.where(
            pokemon_a_type == "Ground", "Earthquake",
            np.where(
                pokemon_a_type == "Water", "Surf",
                np.where(
                    pokemon_a_type == "Electric", "Discharge",
                    "Bulldoze",
                ),
            ),
        ),
        rng.choice(["Thunderbolt", "Flamethrower", "Ice Beam", "Psychic", "Body Slam"], size=n),
    )

    # Damage to opponents (spread moves hit both but at 75% power)
    spread_power_mult = np.where(used_spread_move, 0.75, 1.0)
    damage_to_opp1 = _clip(
        pokemon_a_attack * spread_power_mult * rng.uniform(0.8, 1.2, n)
        + rng.normal(0, 10, n), 0, 300,
    ).round(1)
    damage_to_opp2 = np.where(
        used_spread_move,
        _clip(
            pokemon_a_attack * 0.75 * rng.uniform(0.8, 1.2, n)
            + rng.normal(0, 10, n), 0, 300,
        ),
        0,  # single target doesn't hit second opponent
    ).round(1)

    # SPILLOVER: spread move also hits partner!
    # This is the key interference effect
    # Ground-type Earthquake is devastating unless partner is Flying
    # Electric Discharge hurts Water partners extra
    partner_vulnerable = np.where(
        (pokemon_a_type == "Ground") & (pokemon_b_type == "Flying"), 0.0,  # immune
        np.where(
            (pokemon_a_type == "Ground") & (pokemon_b_type != "Flying"), 1.5,  # Earthquake hurts
            np.where(
                (pokemon_a_type == "Electric") & (pokemon_b_type == "Water"), 2.0,
                np.where(
                    (pokemon_a_type == "Water") & (pokemon_b_type == "Fire"), 1.5,
                    0.6,  # base spillover for other spread moves
                ),
            ),
        ),
    )
    spillover_damage = np.where(
        used_spread_move,
        _clip(
            pokemon_a_attack * 0.75 * partner_vulnerable
            + rng.normal(0, 8, n),
            0, 300,
        ),
        0,
    ).round(1)

    pokemon_b_hp_remaining = _clip(
        pokemon_b_hp - spillover_damage, 0, 250
    ).round(0).astype(int)

    pokemon_b_fainted = (pokemon_b_hp_remaining == 0).astype(int)

    # Battle outcome (spread moves are good against 2 opponents but hurt partner)
    win_logit = (
        -0.5
        + 0.02 * pokemon_a_level
        + 0.02 * pokemon_b_level * (1 - pokemon_b_fainted * 0.8)
        - 0.015 * opp1_level
        - 0.015 * opp2_level
        + 0.005 * damage_to_opp1
        + 0.005 * damage_to_opp2
        - 0.01 * spillover_damage  # hurting partner is bad
    )
    win_prob = _logistic(win_logit)
    battle_won = (rng.uniform(size=n) < win_prob).astype(int)

    # Trainer coordination score (how well the pair works together)
    coordination = _clip(rng.normal(50, 15, n), 0, 100).round(1)

    df = pd.DataFrame({
        "battle_id": battle_id,
        "pokemon_a_level": pokemon_a_level,
        "pokemon_a_type": pokemon_a_type,
        "pokemon_a_attack": pokemon_a_attack,
        "pokemon_b_level": pokemon_b_level,
        "pokemon_b_type": pokemon_b_type,
        "pokemon_b_hp": pokemon_b_hp,
        "opp1_level": opp1_level,
        "opp2_level": opp2_level,
        "used_spread_move": used_spread_move,
        "move_name": move_name,
        "damage_to_opp1": damage_to_opp1,
        "damage_to_opp2": damage_to_opp2,
        "spillover_damage": spillover_damage,
        "pokemon_b_hp_remaining": pokemon_b_hp_remaining,
        "pokemon_b_fainted": pokemon_b_fainted,
        "partner_vulnerable": partner_vulnerable.round(2),
        "battle_won": battle_won,
        "coordination": coordination,
        "win_prob": win_prob.round(4),
    })

    return df


# ===================================================================
# 11. JOHTO TRAINERS -- transportability / external validity
# ===================================================================
def generate_johto_transportability(n: int = 1000) -> pd.DataFrame:
    """
    Same schema as kanto_trainers but with Johto distributions.

    Key differences for transportability analysis:
    - Johto starters: Chikorita, Cyndaquil, Totodile
    - Different town distribution and wealth patterns
    - Higher average patience (Johto culture)
    - Lower average wealth (less urbanised)
    - Same causal structure, different covariate distributions
    """
    rng = RNG

    trainer_id = np.arange(1, n + 1)
    trainer_name = _sample_names(n)

    hometown = rng.choice(JOHTO_TOWNS, size=n, replace=True)

    # Johto has higher patience on average
    patience = _clip(rng.uniform(10, 100, n) + 10, 0, 100)
    natural_talent = rng.uniform(0, 100, n)
    dedication = rng.uniform(5, 100, n)

    # Johto is less wealthy on average
    hometown_wealth_bonus = np.array([
        0.4 if h == "Goldenrod City" else
        -0.4 if h in ("New Bark Town", "Azalea Town") else 0.0
        for h in hometown
    ])
    wealth_raw = rng.normal(2.5 + hometown_wealth_bonus, 0.8)
    wealth = _clip(np.round(wealth_raw), 1, 5).astype(int)

    trainer_experience = _clip(rng.exponential(3.5, size=n), 0, 15).round(1)

    # Johto starter type distribution (Cyndaquil is popular) -- softmax
    u_grass = -0.2 + 0.06 * (patience - 50) * 0.01   # slightly less chosen
    u_fire = 0.3 + 0.15 * (wealth - 3)                # Cyndaquil is popular
    u_water = 0.0 + 0.10 * (trainer_experience - 3)
    stack = np.column_stack([
        np.exp(u_grass), np.exp(u_fire), np.exp(u_water),
    ])
    stack = stack / stack.sum(axis=1, keepdims=True)
    starter_idx = np.array([rng.choice(3, p=row) for row in stack])
    type_labels = ["Grass", "Fire", "Water"]
    starter_type = np.array([type_labels[i] for i in starter_idx])
    starter_species = np.array([JOHTO_STARTERS[t] for t in starter_type])

    # Team stats (same structural equations, different noise)
    team_size = _clip(
        rng.poisson(4.0 + 0.1 * trainer_experience, size=n), 1, 6
    ).astype(int)
    team_level_avg = _clip(
        18 + 2.8 * trainer_experience + 0.12 * dedication
        + rng.normal(0, 5, n), 5, 100,
    ).round(1)
    team_level_max = _clip(
        team_level_avg + rng.exponential(7, n), team_level_avg, 100,
    ).round(1)
    team_avg_iv_total = _clip(
        42 + 0.4 * natural_talent + rng.normal(0, 8, n), 0, 186,
    ).round(1)
    type_diversity = _clip(
        rng.poisson(2 + 0.03 * trainer_experience + 0.01 * patience, size=n),
        1, 6,
    ).astype(int)

    play_hours = _clip(
        45 + 4.5 * dedication + 9 * trainer_experience
        + rng.normal(0, 35, n), 10, 999,
    ).round(0).astype(int)

    strategy_score = _clip(
        22 + 0.28 * patience + 0.28 * natural_talent
        + 1.4 * trainer_experience + rng.normal(0, 8, n),
        0, 100,
    ).round(1)

    cave_training = (
        rng.uniform(size=n) < _logistic(
            -1.5 + 0.14 * trainer_experience + 0.02 * dedication
        )
    ).astype(int)

    safari_zone_visits = _clip(
        rng.poisson(1.2 + 0.05 * patience, size=n), 0, 30,
    ).astype(int)

    dept_store_spending = _clip(
        400 * wealth + 40 * play_hours * 0.01 + rng.normal(0, 250, n),
        0, 8000,
    ).round(0).astype(int)

    potions_purchased = _clip(
        8 + 0.28 * dedication + 0.04 * play_hours
        + rng.normal(0, 7, n), 0, 200,
    ).round(0).astype(int)

    revives_used = _clip(
        rng.poisson(1.5 + 0.02 * play_hours, size=n), 0, 50,
    ).astype(int)

    tm_count = _clip(
        1.5 + 0.08 * dedication + 0.25 * trainer_experience
        + rng.normal(0, 3, n), 0, 50,
    ).round(0).astype(int)

    exp_share_used = (
        rng.uniform(size=n) < _logistic(
            -1.2 + 0.35 * (wealth - 3) + 0.08 * trainer_experience
        )
    ).astype(int)

    held_item_count = _clip(
        rng.poisson(1.2 + 0.08 * wealth + 0.04 * tm_count, size=n), 0, 6,
    ).astype(int)

    rare_candy_used = _clip(
        rng.poisson(0.3 + 0.1 * (wealth - 1), size=n), 0, 20,
    ).astype(int)

    gym_pokemon_center_visits = _clip(
        rng.poisson(7 + 0.08 * play_hours, size=n), 0, 100,
    ).astype(int)

    fishing_attempts = _clip(
        rng.poisson(4 + 0.04 * patience, size=n), 0, 50,
    ).astype(int)

    traded_pokemon_count = _clip(
        rng.poisson(1.2 + 0.06 * trainer_experience, size=n), 0, 15,
    ).astype(int)

    # Outcomes (same structural equations as Kanto)
    badge_logit = (
        -4.0
        + 0.04 * strategy_score
        + 0.03 * team_level_avg
        + 0.15 * type_diversity
        + 0.01 * tm_count
        + 0.005 * dept_store_spending / 100
        + 0.3 * exp_share_used
        + 0.01 * held_item_count
    )
    badge_prob = _logistic(badge_logit)
    badges = _clip(
        np.floor(badge_prob * 9 + rng.normal(0, 0.6, n)), 0, 8,
    ).astype(int)

    elite_four_attempted = (badges == 8).astype(int)

    ef_logit = (
        -3.0
        + 0.05 * strategy_score
        + 0.04 * team_level_avg
        + 0.2 * type_diversity
        + 0.02 * tm_count
        + 0.01 * natural_talent
    )
    ef_prob = _logistic(ef_logit)
    elite_four_wins_raw = (rng.uniform(size=n) < ef_prob).astype(int)
    elite_four_wins = elite_four_wins_raw * elite_four_attempted

    champion_defeated_raw = (
        rng.uniform(size=n) < _logistic(ef_logit - 0.5)
    ).astype(int)
    champion_defeated = champion_defeated_raw * elite_four_wins

    hall_of_fame_time = np.full(n, np.nan)
    hof_mask = champion_defeated == 1
    hall_of_fame_time[hof_mask] = _clip(
        play_hours[hof_mask] + rng.normal(20, 10, hof_mask.sum()),
        play_hours[hof_mask], 1200,
    ).round(0)

    total_battles_won = _clip(
        45 + 7 * trainer_experience + 0.28 * strategy_score
        + 0.18 * team_level_avg + rng.normal(0, 25, n),
        0, 999,
    ).round(0).astype(int)

    total_pokemon_caught = _clip(
        8 + 0.08 * play_hours + 0.05 * patience
        + 2 * safari_zone_visits + rng.normal(0, 10, n),
        1, 251,
    ).round(0).astype(int)

    pokedex_completion = _clip(
        total_pokemon_caught / 251 * 100, 0, 100,
    ).round(1)

    team_avg_ev_total = _clip(
        90 + 1.8 * play_hours * 0.1 + 1.3 * cave_training * 50
        + rng.normal(0, 25, n), 0, 510,
    ).round(1)

    team_happiness_avg = _clip(
        130 + 0.3 * patience + 0.2 * dedication
        + rng.normal(0, 18, n), 0, 255,
    ).round(1)

    team_friendship_max = _clip(
        team_happiness_avg + rng.exponential(15, n), 0, 255,
    ).round(1)

    # Johto gym types
    johto_gym_types = {
        "New Bark Town": "None", "Cherrygrove City": "None",
        "Violet City": "Flying", "Azalea Town": "Bug",
        "Goldenrod City": "Normal", "Ecruteak City": "Ghost",
        "Olivine City": "Steel", "Cianwood City": "Fighting",
        "Mahogany Town": "Ice", "Blackthorn City": "Dragon",
    }

    df = pd.DataFrame({
        "trainer_id": trainer_id,
        "trainer_name": trainer_name,
        "hometown": hometown,
        "starter_type": starter_type,
        "starter_species": starter_species,
        "team_size": team_size,
        "team_level_avg": team_level_avg,
        "team_level_max": team_level_max,
        "team_avg_iv_total": team_avg_iv_total,
        "team_avg_ev_total": team_avg_ev_total,
        "type_diversity": type_diversity,
        "trainer_experience": trainer_experience,
        "play_hours": play_hours,
        "strategy_score": strategy_score,
        "wealth": wealth,
        "cave_training": cave_training,
        "safari_zone_visits": safari_zone_visits,
        "dept_store_spending": dept_store_spending,
        "potions_purchased": potions_purchased,
        "revives_used": revives_used,
        "tm_count": tm_count,
        "exp_share_used": exp_share_used,
        "held_item_count": held_item_count,
        "rare_candy_used": rare_candy_used,
        "gym_pokemon_center_visits": gym_pokemon_center_visits,
        "fishing_attempts": fishing_attempts,
        "traded_pokemon_count": traded_pokemon_count,
        "team_happiness_avg": team_happiness_avg,
        "team_friendship_max": team_friendship_max,
        "badges": badges,
        "elite_four_attempted": elite_four_attempted,
        "elite_four_wins": elite_four_wins,
        "champion_defeated": champion_defeated,
        "hall_of_fame_time": hall_of_fame_time,
        "total_battles_won": total_battles_won,
        "total_pokemon_caught": total_pokemon_caught,
        "pokedex_completion": pokedex_completion,
        "patience": patience.round(2),
        "natural_talent": natural_talent.round(2),
        "dedication": dedication.round(2),
        "hometown_gym_type": [johto_gym_types[h] for h in hometown],
        "region": "Johto",
    })

    assert df.shape[1] == 42, f"Expected 42 columns, got {df.shape[1]}"
    return df


# ===================================================================
# Convenience: generate all datasets
# ===================================================================
def generate_all() -> dict[str, pd.DataFrame]:
    """
    Generate all 11 datasets and return them as a dict.
    The global RNG is seeded once at module load (seed=151),
    so calling this function always produces identical results.
    """
    trainers = generate_kanto_trainers()
    return {
        "kanto_trainers": trainers,
        "kanto_battles": generate_kanto_battles(trainers_df=trainers),
        "kanto_cities_panel": generate_cities_panel(),
        "pewter_protein_rct": generate_protein_rct(),
        "ss_anne_passengers": generate_ss_anne(),
        "safari_zone_lottery": generate_safari_lottery(),
        "happiness_evolution": generate_happiness_evolution(),
        "shadow_surge_staggered": generate_shadow_surge_staggered(),
        "elite_four_panel": generate_elite_four_panel(),
        "double_battles": generate_double_battles(),
        "johto_trainers": generate_johto_transportability(),
    }
