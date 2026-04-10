"""
Tests for kanto_utils.causal estimators.

These tests exercise the estimator functions from kanto_utils.causal using
synthetic fixtures from conftest.py, so no real data files are needed.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from kanto_utils.causal import (
    difference_in_means,
    randomization_inference,
    propensity_score,
    ipw_estimate,
    doubly_robust,
    wald_estimator,
    two_stage_ls,
    sharp_rdd,
    did_estimate,
    balance_table,
)


# =========================================================================
# difference_in_means
# =========================================================================

class TestDifferenceInMeans:
    """Tests for the Neyman difference-in-means estimator."""

    def test_returns_expected_keys(self, simple_treatment_df):
        df = simple_treatment_df
        result = difference_in_means(
            y=df["outcome"].values,
            treatment=df["treatment"].values,
        )
        expected_keys = {"estimate", "se", "ci_lower", "ci_upper", "p_value"}
        assert set(result.keys()) == expected_keys

    def test_ate_positive(self, simple_treatment_df):
        """With a true effect of +3, the estimate should be positive."""
        df = simple_treatment_df
        result = difference_in_means(df["outcome"].values, df["treatment"].values)
        assert result["estimate"] > 0

    def test_ate_close_to_true_effect(self, simple_treatment_df):
        """Estimate should be within ~2 SE of the true effect (3.0)."""
        df = simple_treatment_df
        result = difference_in_means(df["outcome"].values, df["treatment"].values)
        assert abs(result["estimate"] - 3.0) < 2 * result["se"] + 1.0

    def test_confidence_interval_covers_truth(self, simple_treatment_df):
        """95% CI should contain the true ATE of 3.0."""
        df = simple_treatment_df
        result = difference_in_means(df["outcome"].values, df["treatment"].values)
        assert result["ci_lower"] < 3.0 < result["ci_upper"]

    def test_se_positive(self, simple_treatment_df):
        df = simple_treatment_df
        result = difference_in_means(df["outcome"].values, df["treatment"].values)
        assert result["se"] > 0

    def test_p_value_in_unit_interval(self, simple_treatment_df):
        df = simple_treatment_df
        result = difference_in_means(df["outcome"].values, df["treatment"].values)
        assert 0 <= result["p_value"] <= 1

    def test_significant_at_05(self, simple_treatment_df):
        """With n=200 and effect=3, should reject at alpha=0.05."""
        df = simple_treatment_df
        result = difference_in_means(df["outcome"].values, df["treatment"].values)
        assert result["p_value"] < 0.05

    def test_equal_outcomes_zero_effect(self):
        treatment = np.array([0] * 50 + [1] * 50)
        outcome = np.array([10.0] * 100)
        result = difference_in_means(outcome, treatment)
        assert result["estimate"] == pytest.approx(0.0)

    def test_large_sample_convergence(self):
        """With a very large sample the estimate should be very close."""
        rng = np.random.default_rng(42)
        n = 10_000
        t = np.array([0] * (n // 2) + [1] * (n // 2))
        y = 5.0 + 2.0 * t + rng.normal(0, 1, size=n)
        result = difference_in_means(y, t)
        assert abs(result["estimate"] - 2.0) < 0.1


# =========================================================================
# randomization_inference
# =========================================================================

class TestRandomizationInference:
    """Tests for Fisher-style randomisation inference."""

    def test_returns_expected_keys(self, simple_treatment_df):
        df = simple_treatment_df
        result = randomization_inference(
            df["outcome"].values, df["treatment"].values, n_perms=200
        )
        assert set(result.keys()) == {"observed_diff", "p_value", "n_perms"}

    def test_p_value_in_unit_interval(self, simple_treatment_df):
        df = simple_treatment_df
        result = randomization_inference(
            df["outcome"].values, df["treatment"].values, n_perms=200
        )
        assert 0 <= result["p_value"] <= 1

    def test_significant_with_strong_effect(self, simple_treatment_df):
        df = simple_treatment_df
        result = randomization_inference(
            df["outcome"].values, df["treatment"].values, n_perms=500
        )
        assert result["p_value"] < 0.05

    def test_n_perms_stored(self, simple_treatment_df):
        df = simple_treatment_df
        result = randomization_inference(
            df["outcome"].values, df["treatment"].values, n_perms=300
        )
        assert result["n_perms"] == 300

    def test_no_effect_high_p_value(self):
        """Permutation test should not reject when there is no effect."""
        rng = np.random.default_rng(42)
        n = 100
        t = np.array([0] * 50 + [1] * 50)
        y = rng.normal(10, 1, size=n)  # no treatment effect
        result = randomization_inference(y, t, n_perms=500)
        assert result["p_value"] > 0.05


# =========================================================================
# propensity_score
# =========================================================================

class TestPropensityScore:
    """Tests for propensity score estimation."""

    def test_returns_correct_length(self, simple_treatment_df):
        df = simple_treatment_df
        ps = propensity_score(
            X=df["covariate"].values,
            treatment=df["treatment"].values,
        )
        assert len(ps) == len(df)

    def test_scores_in_zero_one(self, simple_treatment_df):
        df = simple_treatment_df
        ps = propensity_score(
            X=df["covariate"].values,
            treatment=df["treatment"].values,
        )
        assert np.all(ps > 0)
        assert np.all(ps < 1)

    def test_scores_near_half_for_random_assignment(self):
        """With no confounding, propensity scores should be near 0.5."""
        rng = np.random.default_rng(42)
        n = 500
        X = rng.normal(0, 1, size=(n, 1))
        t = rng.choice([0, 1], size=n)
        ps = propensity_score(X, t)
        assert np.abs(np.mean(ps) - 0.5) < 0.15

    def test_raises_for_unsupported_model(self, simple_treatment_df):
        df = simple_treatment_df
        with pytest.raises(ValueError, match="Unsupported model"):
            propensity_score(
                X=df["covariate"].values,
                treatment=df["treatment"].values,
                model="probit",
            )


# =========================================================================
# ipw_estimate
# =========================================================================

class TestIPWEstimate:
    """Tests for the inverse probability weighting estimator."""

    def test_returns_expected_keys(self, simple_treatment_df):
        df = simple_treatment_df
        ps = propensity_score(df["covariate"].values, df["treatment"].values)
        result = ipw_estimate(
            y=df["outcome"].values,
            treatment=df["treatment"].values,
            propensity_scores=ps,
        )
        assert set(result.keys()) == {"estimate", "se", "ci_lower", "ci_upper"}

    def test_hajek_estimate_positive(self, simple_treatment_df):
        df = simple_treatment_df
        ps = propensity_score(df["covariate"].values, df["treatment"].values)
        result = ipw_estimate(df["outcome"].values, df["treatment"].values, ps)
        assert result["estimate"] > 0

    def test_ht_estimate_positive(self, simple_treatment_df):
        df = simple_treatment_df
        ps = propensity_score(df["covariate"].values, df["treatment"].values)
        result = ipw_estimate(
            df["outcome"].values, df["treatment"].values, ps, estimator="ht"
        )
        assert result["estimate"] > 0

    def test_raises_for_unknown_estimator(self, simple_treatment_df):
        df = simple_treatment_df
        ps = np.full(len(df), 0.5)
        with pytest.raises(ValueError, match="Unknown estimator"):
            ipw_estimate(df["outcome"].values, df["treatment"].values, ps, estimator="xyz")


# =========================================================================
# doubly_robust
# =========================================================================

class TestDoublyRobust:
    """Tests for the AIPW / doubly robust estimator."""

    def test_returns_expected_keys(self, simple_treatment_df):
        df = simple_treatment_df
        result = doubly_robust(
            y=df["outcome"].values,
            treatment=df["treatment"].values,
            X=df["covariate"].values,
        )
        assert set(result.keys()) == {"estimate", "se", "ci_lower", "ci_upper"}

    def test_estimate_near_truth(self, simple_treatment_df):
        df = simple_treatment_df
        result = doubly_robust(
            df["outcome"].values, df["treatment"].values, df["covariate"].values
        )
        assert abs(result["estimate"] - 3.0) < 2.0

    def test_ci_covers_truth(self, simple_treatment_df):
        df = simple_treatment_df
        result = doubly_robust(
            df["outcome"].values, df["treatment"].values, df["covariate"].values
        )
        assert result["ci_lower"] < 3.0 < result["ci_upper"]

    def test_with_precomputed_ps(self, simple_treatment_df):
        df = simple_treatment_df
        ps = propensity_score(df["covariate"].values, df["treatment"].values)
        result = doubly_robust(
            df["outcome"].values, df["treatment"].values,
            df["covariate"].values, propensity_scores=ps
        )
        assert "estimate" in result


# =========================================================================
# wald_estimator
# =========================================================================

class TestWaldEstimator:
    """Tests for the Wald (IV) estimator."""

    def test_returns_expected_keys(self, sample_iv):
        df = sample_iv
        result = wald_estimator(
            y=df["rare_pokemon_caught"].values,
            treatment=df["safari_visit"].values,
            instrument=df["lottery_win"].values,
        )
        expected = {"estimate", "se", "ci_lower", "ci_upper",
                    "first_stage", "reduced_form"}
        assert set(result.keys()) == expected

    def test_first_stage_positive(self, sample_iv):
        """Winning the lottery should increase safari visits."""
        df = sample_iv
        result = wald_estimator(
            df["rare_pokemon_caught"].values,
            df["safari_visit"].values,
            df["lottery_win"].values,
        )
        assert result["first_stage"] > 0

    def test_raises_on_weak_instrument(self):
        """Should raise when the instrument has zero first stage."""
        rng = np.random.default_rng(42)
        n = 100
        z = rng.choice([0, 1], size=n)
        d = rng.choice([0, 1], size=n)  # unrelated to z
        y = rng.normal(0, 1, size=n)
        # With a random instrument, first stage might be near zero
        # Force a zero first stage
        d_means_equal = np.where(z == 1, 0.5, 0.5)
        d_exact = np.array([0, 1] * (n // 2))  # 50% in each z group
        # Make first stage exactly zero
        treatment = np.zeros(n)
        treatment[::2] = 1  # every other
        instrument = np.zeros(n)
        instrument[:n // 2] = 1
        # Shuffle to break any correlation
        rng.shuffle(treatment)
        # Force exact same mean in both z groups
        with pytest.raises(ValueError, match="[Ff]irst stage"):
            wald_estimator(y, treatment, instrument)


# =========================================================================
# two_stage_ls
# =========================================================================

class TestTwoStageLS:
    """Tests for the 2SLS estimator."""

    def test_returns_expected_keys(self, sample_iv):
        df = sample_iv
        result = two_stage_ls(
            y=df["rare_pokemon_caught"].values,
            treatment=df["safari_visit"].values,
            instrument=df["lottery_win"].values,
        )
        expected = {"estimate", "se", "ci_lower", "ci_upper", "first_stage_f"}
        assert set(result.keys()) == expected

    def test_with_covariates(self, sample_iv):
        df = sample_iv
        result = two_stage_ls(
            y=df["rare_pokemon_caught"].values,
            treatment=df["safari_visit"].values,
            instrument=df["lottery_win"].values,
            X=df["trainer_level"].values,
        )
        assert "estimate" in result

    def test_first_stage_f_positive(self, sample_iv):
        df = sample_iv
        result = two_stage_ls(
            df["rare_pokemon_caught"].values,
            df["safari_visit"].values,
            df["lottery_win"].values,
        )
        assert result["first_stage_f"] > 0


# =========================================================================
# sharp_rdd
# =========================================================================

class TestSharpRDD:
    """Tests for the local-linear RDD estimator."""

    def test_returns_expected_keys(self):
        rng = np.random.default_rng(42)
        n = 500
        x = rng.uniform(-5, 5, size=n)
        y = 2.0 + 3.0 * (x >= 0) + 0.5 * x + rng.normal(0, 1, size=n)
        result = sharp_rdd(x, y, cutoff=0.0)
        expected = {"estimate", "se", "ci_lower", "ci_upper",
                    "bandwidth", "n_left", "n_right"}
        assert set(result.keys()) == expected

    def test_detects_discontinuity(self):
        """Should detect a jump of 3 at the cutoff."""
        rng = np.random.default_rng(42)
        n = 1000
        x = rng.uniform(-5, 5, size=n)
        y = 10.0 + 3.0 * (x >= 0) + 0.5 * x + rng.normal(0, 0.5, size=n)
        result = sharp_rdd(x, y, cutoff=0.0)
        assert abs(result["estimate"] - 3.0) < 2.0

    def test_no_discontinuity(self):
        """With no jump, estimate should be near zero."""
        rng = np.random.default_rng(42)
        n = 1000
        x = rng.uniform(-5, 5, size=n)
        y = 10.0 + 0.5 * x + rng.normal(0, 0.5, size=n)
        result = sharp_rdd(x, y, cutoff=0.0)
        assert abs(result["estimate"]) < 1.5

    def test_raises_on_too_few_obs(self):
        x = np.array([1.0, 2.0])
        y = np.array([5.0, 6.0])
        with pytest.raises(ValueError, match="Too few observations"):
            sharp_rdd(x, y, cutoff=0.0, bandwidth=0.5)

    def test_custom_kernel(self):
        rng = np.random.default_rng(42)
        n = 500
        x = rng.uniform(-5, 5, size=n)
        y = 10.0 + 3.0 * (x >= 0) + rng.normal(0, 1, size=n)
        for kernel in ("triangular", "uniform", "epanechnikov"):
            result = sharp_rdd(x, y, cutoff=0.0, kernel=kernel)
            assert "estimate" in result

    def test_raises_on_unknown_kernel(self):
        x = np.linspace(-5, 5, 100)
        y = np.ones(100)
        with pytest.raises(ValueError, match="Unknown kernel"):
            sharp_rdd(x, y, cutoff=0.0, kernel="gaussian")


# =========================================================================
# did_estimate
# =========================================================================

class TestDiDEstimate:
    """Tests for the 2x2 difference-in-differences estimator."""

    def test_returns_expected_keys(self):
        rng = np.random.default_rng(42)
        result = did_estimate(
            y_pre_treat=rng.normal(10, 1, 50),
            y_post_treat=rng.normal(15, 1, 50),
            y_pre_ctrl=rng.normal(10, 1, 50),
            y_post_ctrl=rng.normal(12, 1, 50),
        )
        expected = {"estimate", "se", "ci_lower", "ci_upper",
                    "diff_treated", "diff_control"}
        assert set(result.keys()) == expected

    def test_detects_treatment_effect(self):
        """Treated group gains 5, control gains 2 => DiD = 3."""
        rng = np.random.default_rng(42)
        n = 200
        result = did_estimate(
            y_pre_treat=rng.normal(10, 1, n),
            y_post_treat=rng.normal(15, 1, n),
            y_pre_ctrl=rng.normal(10, 1, n),
            y_post_ctrl=rng.normal(12, 1, n),
        )
        assert abs(result["estimate"] - 3.0) < 1.0

    def test_zero_effect(self):
        """Parallel trends + no effect => DiD = 0."""
        rng = np.random.default_rng(42)
        n = 200
        result = did_estimate(
            y_pre_treat=rng.normal(10, 1, n),
            y_post_treat=rng.normal(12, 1, n),
            y_pre_ctrl=rng.normal(10, 1, n),
            y_post_ctrl=rng.normal(12, 1, n),
        )
        assert abs(result["estimate"]) < 1.0

    def test_se_positive(self):
        rng = np.random.default_rng(42)
        result = did_estimate(
            rng.normal(10, 1, 50),
            rng.normal(15, 1, 50),
            rng.normal(10, 1, 50),
            rng.normal(12, 1, 50),
        )
        assert result["se"] > 0


# =========================================================================
# balance_table
# =========================================================================

class TestBalanceTable:
    """Tests for the balance table function."""

    def test_returns_dataframe(self, simple_treatment_df):
        df = simple_treatment_df
        bt = balance_table(df, "treatment", ["outcome", "covariate"])
        assert isinstance(bt, pd.DataFrame)

    def test_correct_columns(self, simple_treatment_df):
        df = simple_treatment_df
        bt = balance_table(df, "treatment", ["outcome", "covariate"])
        expected_cols = {"mean_treated", "mean_control", "std_diff",
                         "var_treated", "var_control", "p_value"}
        assert set(bt.columns) == expected_cols

    def test_correct_rows(self, simple_treatment_df):
        df = simple_treatment_df
        covariates = ["outcome", "covariate"]
        bt = balance_table(df, "treatment", covariates)
        assert list(bt.index) == covariates

    def test_std_diff_near_zero_for_balanced_covariate(self, simple_treatment_df):
        """The covariate is independent of treatment, so std_diff ~ 0."""
        df = simple_treatment_df
        bt = balance_table(df, "treatment", ["covariate"])
        assert abs(bt.loc["covariate", "std_diff"]) < 0.5

    def test_outcome_imbalanced(self, simple_treatment_df):
        """Outcome differs by treatment (effect=3), so std_diff should be large."""
        df = simple_treatment_df
        bt = balance_table(df, "treatment", ["outcome"])
        assert abs(bt.loc["outcome", "std_diff"]) > 0.5


# =========================================================================
# Integration test: RCT fixture end-to-end
# =========================================================================

class TestRCTEndToEnd:
    """End-to-end test using the sample_rct fixture."""

    def test_difference_in_means_on_rct(self, sample_rct):
        result = difference_in_means(
            y=sample_rct["outcome_power"].values,
            treatment=sample_rct["treatment"].values,
        )
        # True effect is ~5; with small n, be generous
        assert result["estimate"] > 0

    def test_balance_table_on_rct(self, sample_rct):
        bt = balance_table(sample_rct, "treatment", ["base_power"])
        assert isinstance(bt, pd.DataFrame)
        assert len(bt) == 1
