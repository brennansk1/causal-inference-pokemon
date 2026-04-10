"""
Reusable causal inference estimators for Causal Inference: A Pokemon Approach.

Every estimator returns either a plain dictionary or a pandas DataFrame so that
results are easy to inspect in a notebook.  The implementations are intentionally
transparent -- students can read the source to see exactly what each estimator
does.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
from scipy import stats


# ---------------------------------------------------------------------------
# Difference in means (Neyman estimator)
# ---------------------------------------------------------------------------

def difference_in_means(
    y: np.ndarray,
    treatment: np.ndarray,
) -> Dict[str, float]:
    """Estimate the Average Treatment Effect via a simple difference in means.

    Parameters
    ----------
    y : array-like
        Outcome variable.
    treatment : array-like
        Binary treatment indicator (0/1).

    Returns
    -------
    dict
        Keys: ``estimate``, ``se``, ``ci_lower``, ``ci_upper``, ``p_value``.
    """
    y = np.asarray(y, dtype=float)
    treatment = np.asarray(treatment, dtype=float)

    y1 = y[treatment == 1]
    y0 = y[treatment == 0]
    n1, n0 = len(y1), len(y0)

    estimate = y1.mean() - y0.mean()
    se = np.sqrt(y1.var(ddof=1) / n1 + y0.var(ddof=1) / n0)
    t_stat = estimate / se
    df = n1 + n0 - 2
    p_value = float(2 * stats.t.sf(np.abs(t_stat), df))
    ci_lower = estimate - 1.96 * se
    ci_upper = estimate + 1.96 * se

    return {
        "estimate": float(estimate),
        "se": float(se),
        "ci_lower": float(ci_lower),
        "ci_upper": float(ci_upper),
        "p_value": p_value,
    }


# ---------------------------------------------------------------------------
# Randomisation inference (Fisher's exact test)
# ---------------------------------------------------------------------------

def randomization_inference(
    y: np.ndarray,
    treatment: np.ndarray,
    n_perms: int = 5000,
    seed: int = 151,
) -> Dict[str, float]:
    """Fisher-style randomisation inference for the sharp null.

    Parameters
    ----------
    y : array-like
        Outcome variable.
    treatment : array-like
        Binary treatment indicator.
    n_perms : int, default 5000
        Number of random permutations.
    seed : int, default 151
        Random seed (151 = original Kanto Pokedex size).

    Returns
    -------
    dict
        Keys: ``observed_diff``, ``p_value``, ``n_perms``.
    """
    rng = np.random.default_rng(seed)
    y = np.asarray(y, dtype=float)
    treatment = np.asarray(treatment, dtype=float)

    n_treated = int(treatment.sum())
    observed_diff = y[treatment == 1].mean() - y[treatment == 0].mean()

    null_diffs = np.empty(n_perms)
    for i in range(n_perms):
        perm = rng.permutation(treatment)
        null_diffs[i] = y[perm == 1].mean() - y[perm == 0].mean()

    p_value = float(np.mean(np.abs(null_diffs) >= np.abs(observed_diff)))

    return {
        "observed_diff": float(observed_diff),
        "p_value": p_value,
        "n_perms": n_perms,
    }


# ---------------------------------------------------------------------------
# Propensity score estimation
# ---------------------------------------------------------------------------

def propensity_score(
    X: np.ndarray,
    treatment: np.ndarray,
    model: str = "logit",
) -> np.ndarray:
    """Estimate propensity scores via logistic regression.

    Parameters
    ----------
    X : array-like of shape (n, p)
        Covariate matrix.
    treatment : array-like of shape (n,)
        Binary treatment indicator.
    model : str, default 'logit'
        Currently only ``'logit'`` is supported.

    Returns
    -------
    np.ndarray
        Estimated propensity scores in [0, 1].
    """
    X = np.asarray(X, dtype=float)
    treatment = np.asarray(treatment, dtype=float).ravel()

    if X.ndim == 1:
        X = X.reshape(-1, 1)

    if model != "logit":
        raise ValueError(f"Unsupported model: '{model}'. Use 'logit'.")

    # Add intercept
    X_int = np.column_stack([np.ones(X.shape[0]), X])

    # Fit logistic regression via iteratively reweighted least squares (IRLS)
    beta = np.zeros(X_int.shape[1])
    for _ in range(50):  # max iterations
        p = _sigmoid(X_int @ beta)
        p = np.clip(p, 1e-10, 1 - 1e-10)
        W = np.diag(p * (1 - p))
        # Newton-Raphson update
        gradient = X_int.T @ (treatment - p)
        hessian = -X_int.T @ W @ X_int
        try:
            delta = np.linalg.solve(hessian, gradient)
        except np.linalg.LinAlgError:
            break
        beta -= delta
        if np.max(np.abs(delta)) < 1e-8:
            break

    ps = _sigmoid(X_int @ beta)
    return np.clip(ps, 1e-6, 1 - 1e-6)


def _sigmoid(z: np.ndarray) -> np.ndarray:
    """Numerically stable sigmoid function."""
    return np.where(
        z >= 0,
        1 / (1 + np.exp(-z)),
        np.exp(z) / (1 + np.exp(z)),
    )


# ---------------------------------------------------------------------------
# Inverse probability weighting (Horvitz-Thompson / Hajek)
# ---------------------------------------------------------------------------

def ipw_estimate(
    y: np.ndarray,
    treatment: np.ndarray,
    propensity_scores: np.ndarray,
    estimator: str = "hajek",
) -> Dict[str, float]:
    """Inverse-probability-weighted ATE estimator.

    Parameters
    ----------
    y : array-like
        Outcome.
    treatment : array-like
        Binary treatment indicator.
    propensity_scores : array-like
        Estimated P(Treatment=1|X) for each unit.
    estimator : str, default 'hajek'
        ``'hajek'`` (normalised) or ``'ht'`` (Horvitz-Thompson).

    Returns
    -------
    dict
        Keys: ``estimate``, ``se``, ``ci_lower``, ``ci_upper``.
    """
    y = np.asarray(y, dtype=float)
    d = np.asarray(treatment, dtype=float)
    ps = np.asarray(propensity_scores, dtype=float)
    n = len(y)

    w1 = d / ps
    w0 = (1 - d) / (1 - ps)

    if estimator == "hajek":
        mu1 = np.sum(w1 * y) / np.sum(w1)
        mu0 = np.sum(w0 * y) / np.sum(w0)
    elif estimator == "ht":
        mu1 = np.sum(w1 * y) / n
        mu0 = np.sum(w0 * y) / n
    else:
        raise ValueError(f"Unknown estimator '{estimator}'. Use 'hajek' or 'ht'.")

    estimate = mu1 - mu0

    # Influence-function-based SE (for Hajek)
    phi1 = w1 * (y - mu1)
    phi0 = w0 * (y - mu0)
    phi = phi1 - phi0
    se = float(np.sqrt(np.var(phi, ddof=1) / n))
    ci_lower = estimate - 1.96 * se
    ci_upper = estimate + 1.96 * se

    return {
        "estimate": float(estimate),
        "se": se,
        "ci_lower": float(ci_lower),
        "ci_upper": float(ci_upper),
    }


# ---------------------------------------------------------------------------
# Doubly robust / AIPW
# ---------------------------------------------------------------------------

def doubly_robust(
    y: np.ndarray,
    treatment: np.ndarray,
    X: np.ndarray,
    propensity_scores: Optional[np.ndarray] = None,
) -> Dict[str, float]:
    """Augmented inverse-probability-weighted (AIPW) estimator.

    Combines an outcome model (OLS) with inverse probability weighting for
    double robustness.

    Parameters
    ----------
    y : array-like
        Outcome.
    treatment : array-like
        Binary treatment indicator.
    X : array-like of shape (n, p)
        Covariates.
    propensity_scores : array-like, optional
        Pre-estimated propensity scores.  If *None*, they are estimated
        internally via logistic regression on *X*.

    Returns
    -------
    dict
        Keys: ``estimate``, ``se``, ``ci_lower``, ``ci_upper``.
    """
    y = np.asarray(y, dtype=float)
    d = np.asarray(treatment, dtype=float)
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    n = len(y)

    if propensity_scores is None:
        ps = propensity_score(X, d)
    else:
        ps = np.asarray(propensity_scores, dtype=float)

    # Outcome models: OLS for treated and control separately
    X_int = np.column_stack([np.ones(n), X])

    treated_idx = d == 1
    control_idx = d == 0

    beta1 = _ols_fit(X_int[treated_idx], y[treated_idx])
    beta0 = _ols_fit(X_int[control_idx], y[control_idx])

    mu1_hat = X_int @ beta1  # predicted outcome under treatment
    mu0_hat = X_int @ beta0  # predicted outcome under control

    # AIPW scores
    psi1 = mu1_hat + d * (y - mu1_hat) / ps
    psi0 = mu0_hat + (1 - d) * (y - mu0_hat) / (1 - ps)
    tau_i = psi1 - psi0

    estimate = float(tau_i.mean())
    se = float(np.std(tau_i, ddof=1) / np.sqrt(n))
    ci_lower = estimate - 1.96 * se
    ci_upper = estimate + 1.96 * se

    return {
        "estimate": estimate,
        "se": se,
        "ci_lower": float(ci_lower),
        "ci_upper": float(ci_upper),
    }


def _ols_fit(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Fit OLS and return coefficient vector."""
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    return beta


# ---------------------------------------------------------------------------
# Instrumental variables
# ---------------------------------------------------------------------------

def wald_estimator(
    y: np.ndarray,
    treatment: np.ndarray,
    instrument: np.ndarray,
) -> Dict[str, float]:
    """Wald (IV) estimator for a binary instrument.

    Parameters
    ----------
    y : array-like
        Outcome.
    treatment : array-like
        Endogenous treatment (can be continuous or binary).
    instrument : array-like
        Binary instrument.

    Returns
    -------
    dict
        Keys: ``estimate``, ``se``, ``ci_lower``, ``ci_upper``,
        ``first_stage``, ``reduced_form``.
    """
    y = np.asarray(y, dtype=float)
    d = np.asarray(treatment, dtype=float)
    z = np.asarray(instrument, dtype=float)
    n = len(y)

    z1 = z == 1
    z0 = z == 0

    # Reduced form: E[Y|Z=1] - E[Y|Z=0]
    reduced_form = y[z1].mean() - y[z0].mean()
    # First stage: E[D|Z=1] - E[D|Z=0]
    first_stage = d[z1].mean() - d[z0].mean()

    if np.abs(first_stage) < 1e-12:
        raise ValueError("First stage is essentially zero -- weak instrument.")

    estimate = reduced_form / first_stage

    # Delta-method SE
    n1, n0 = z1.sum(), z0.sum()
    var_rf = y[z1].var(ddof=1) / n1 + y[z0].var(ddof=1) / n0
    var_fs = d[z1].var(ddof=1) / n1 + d[z0].var(ddof=1) / n0
    # Approximate SE via delta method: se(a/b) ~ |a/b| * sqrt(var_a/a^2 + var_b/b^2)
    se = float(np.abs(estimate) * np.sqrt(
        var_rf / (reduced_form ** 2 + 1e-30) + var_fs / (first_stage ** 2 + 1e-30)
    ))
    ci_lower = estimate - 1.96 * se
    ci_upper = estimate + 1.96 * se

    return {
        "estimate": float(estimate),
        "se": se,
        "ci_lower": float(ci_lower),
        "ci_upper": float(ci_upper),
        "first_stage": float(first_stage),
        "reduced_form": float(reduced_form),
    }


def two_stage_ls(
    y: np.ndarray,
    treatment: np.ndarray,
    instrument: np.ndarray,
    X: Optional[np.ndarray] = None,
) -> Dict[str, float]:
    """Two-stage least squares (2SLS) estimator.

    Parameters
    ----------
    y : array-like
        Outcome.
    treatment : array-like
        Endogenous treatment.
    instrument : array-like
        Instrument(s).  Can be 1-D (single instrument) or 2-D.
    X : array-like, optional
        Exogenous covariates to include in both stages.

    Returns
    -------
    dict
        Keys: ``estimate``, ``se``, ``ci_lower``, ``ci_upper``,
        ``first_stage_f``.
    """
    y = np.asarray(y, dtype=float)
    d = np.asarray(treatment, dtype=float).ravel()
    z = np.asarray(instrument, dtype=float)
    if z.ndim == 1:
        z = z.reshape(-1, 1)
    n = len(y)

    # Build matrices
    intercept = np.ones((n, 1))
    if X is not None:
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        W = np.column_stack([intercept, X])  # exogenous regressors
    else:
        W = intercept

    Z_full = np.column_stack([W, z])  # all instruments + exogenous

    # --- First stage: regress D on Z_full ---
    beta_fs = _ols_fit(Z_full, d)
    d_hat = Z_full @ beta_fs

    # First-stage F-statistic (on excluded instruments only)
    d_resid_full = d - d_hat
    beta_w = _ols_fit(W, d)
    d_resid_restricted = d - W @ beta_w
    ss_full = np.sum(d_resid_full ** 2)
    ss_restricted = np.sum(d_resid_restricted ** 2)
    q = z.shape[1]  # number of excluded instruments
    k = Z_full.shape[1]
    f_stat = ((ss_restricted - ss_full) / q) / (ss_full / (n - k))

    # --- Second stage: regress Y on (W, D_hat) ---
    X_second = np.column_stack([W, d_hat])
    beta_2sls = _ols_fit(X_second, y)

    # The coefficient on D_hat is our 2SLS estimate
    estimate = float(beta_2sls[-1])

    # SE using original residuals (not fitted)
    X_second_orig = np.column_stack([W, d])
    resid = y - X_second_orig @ beta_2sls
    sigma2 = float(np.sum(resid ** 2) / (n - X_second.shape[1]))
    # Variance of beta using (X_2'X_2)^-1 * sigma^2, but with X_second (fitted D)
    try:
        cov_matrix = sigma2 * np.linalg.inv(X_second.T @ X_second)
        se = float(np.sqrt(np.abs(cov_matrix[-1, -1])))
    except np.linalg.LinAlgError:
        se = float("nan")

    ci_lower = estimate - 1.96 * se
    ci_upper = estimate + 1.96 * se

    return {
        "estimate": estimate,
        "se": se,
        "ci_lower": float(ci_lower),
        "ci_upper": float(ci_upper),
        "first_stage_f": float(f_stat),
    }


# ---------------------------------------------------------------------------
# Sharp RDD
# ---------------------------------------------------------------------------

def sharp_rdd(
    running_var: np.ndarray,
    outcome: np.ndarray,
    cutoff: float,
    bandwidth: Optional[float] = None,
    kernel: str = "triangular",
) -> Dict[str, float]:
    """Local-linear regression-discontinuity estimator.

    Parameters
    ----------
    running_var : array-like
        Running / forcing variable.
    outcome : array-like
        Outcome.
    cutoff : float
        RD cutoff.
    bandwidth : float, optional
        Bandwidth around the cutoff.  If *None*, uses Silverman's rule of
        thumb on the running variable as a simple default.
    kernel : str, default 'triangular'
        Kernel for local weighting: ``'triangular'``, ``'uniform'``, or
        ``'epanechnikov'``.

    Returns
    -------
    dict
        Keys: ``estimate``, ``se``, ``ci_lower``, ``ci_upper``,
        ``bandwidth``, ``n_left``, ``n_right``.
    """
    x = np.asarray(running_var, dtype=float)
    y = np.asarray(outcome, dtype=float)
    c = float(cutoff)

    # Default bandwidth: Silverman ROT
    if bandwidth is None:
        bandwidth = 1.06 * np.std(x) * len(x) ** (-1 / 5)

    mask = np.abs(x - c) <= bandwidth
    x_bw = x[mask]
    y_bw = y[mask]

    left = x_bw < c
    right = x_bw >= c
    n_left = int(left.sum())
    n_right = int(right.sum())

    if n_left < 2 or n_right < 2:
        raise ValueError(
            f"Too few observations within bandwidth ({n_left} left, "
            f"{n_right} right). Try a larger bandwidth."
        )

    # Kernel weights
    u = (x_bw - c) / bandwidth
    if kernel == "triangular":
        w = np.maximum(1 - np.abs(u), 0)
    elif kernel == "epanechnikov":
        w = np.maximum(0.75 * (1 - u ** 2), 0)
    elif kernel == "uniform":
        w = np.ones_like(u)
    else:
        raise ValueError(f"Unknown kernel '{kernel}'.")

    # Fit local linear on each side
    def _wls(x_side, y_side, w_side):
        """Weighted least squares: y ~ a + b*(x - c)."""
        X = np.column_stack([np.ones(len(x_side)), x_side - c])
        W = np.diag(w_side)
        XtWX = X.T @ W @ X
        XtWy = X.T @ W @ y_side
        try:
            beta = np.linalg.solve(XtWX, XtWy)
        except np.linalg.LinAlgError:
            beta = np.linalg.lstsq(XtWX, XtWy, rcond=None)[0]
        resid = y_side - X @ beta
        sigma2 = float(np.sum(w_side * resid ** 2) / max(np.sum(w_side) - 2, 1))
        try:
            var_beta = sigma2 * np.linalg.inv(XtWX)
        except np.linalg.LinAlgError:
            var_beta = sigma2 * np.linalg.pinv(XtWX)
        return beta[0], var_beta[0, 0]

    intercept_right, var_right = _wls(x_bw[right], y_bw[right], w[right])
    intercept_left, var_left = _wls(x_bw[left], y_bw[left], w[left])

    estimate = intercept_right - intercept_left
    se = float(np.sqrt(var_right + var_left))
    ci_lower = estimate - 1.96 * se
    ci_upper = estimate + 1.96 * se

    return {
        "estimate": float(estimate),
        "se": se,
        "ci_lower": float(ci_lower),
        "ci_upper": float(ci_upper),
        "bandwidth": float(bandwidth),
        "n_left": n_left,
        "n_right": n_right,
    }


# ---------------------------------------------------------------------------
# 2x2 Difference-in-Differences
# ---------------------------------------------------------------------------

def did_estimate(
    y_pre_treat: np.ndarray,
    y_post_treat: np.ndarray,
    y_pre_ctrl: np.ndarray,
    y_post_ctrl: np.ndarray,
) -> Dict[str, float]:
    """Classic 2x2 difference-in-differences estimator.

    Parameters
    ----------
    y_pre_treat : array-like
        Outcome for treated group in the pre-period.
    y_post_treat : array-like
        Outcome for treated group in the post-period.
    y_pre_ctrl : array-like
        Outcome for control group in the pre-period.
    y_post_ctrl : array-like
        Outcome for control group in the post-period.

    Returns
    -------
    dict
        Keys: ``estimate``, ``se``, ``ci_lower``, ``ci_upper``,
        ``diff_treated``, ``diff_control``.
    """
    y_pre_treat = np.asarray(y_pre_treat, dtype=float)
    y_post_treat = np.asarray(y_post_treat, dtype=float)
    y_pre_ctrl = np.asarray(y_pre_ctrl, dtype=float)
    y_post_ctrl = np.asarray(y_post_ctrl, dtype=float)

    diff_treated = y_post_treat.mean() - y_pre_treat.mean()
    diff_control = y_post_ctrl.mean() - y_pre_ctrl.mean()
    estimate = diff_treated - diff_control

    n1_pre, n1_post = len(y_pre_treat), len(y_post_treat)
    n0_pre, n0_post = len(y_pre_ctrl), len(y_post_ctrl)

    # SE via variance of each group-period mean
    se = float(np.sqrt(
        y_pre_treat.var(ddof=1) / n1_pre
        + y_post_treat.var(ddof=1) / n1_post
        + y_pre_ctrl.var(ddof=1) / n0_pre
        + y_post_ctrl.var(ddof=1) / n0_post
    ))

    ci_lower = estimate - 1.96 * se
    ci_upper = estimate + 1.96 * se

    return {
        "estimate": float(estimate),
        "se": se,
        "ci_lower": float(ci_lower),
        "ci_upper": float(ci_upper),
        "diff_treated": float(diff_treated),
        "diff_control": float(diff_control),
    }


# ---------------------------------------------------------------------------
# Balance table
# ---------------------------------------------------------------------------

def balance_table(
    df: pd.DataFrame,
    treatment_col: str,
    covariate_cols: Sequence[str],
) -> pd.DataFrame:
    """Compute a balance table with standardised mean differences.

    Parameters
    ----------
    df : pd.DataFrame
        Data.
    treatment_col : str
        Binary treatment column name.
    covariate_cols : sequence of str
        Covariate column names to compare.

    Returns
    -------
    pd.DataFrame
        Columns: ``mean_treated``, ``mean_control``, ``std_diff``,
        ``var_treated``, ``var_control``, ``p_value``.
    """
    treated = df[df[treatment_col] == 1]
    control = df[df[treatment_col] == 0]

    rows = []
    for col in covariate_cols:
        yt = treated[col].astype(float)
        yc = control[col].astype(float)

        mean_t = yt.mean()
        mean_c = yc.mean()
        var_t = yt.var(ddof=1)
        var_c = yc.var(ddof=1)

        pooled_sd = np.sqrt((var_t + var_c) / 2)
        std_diff = (mean_t - mean_c) / pooled_sd if pooled_sd > 0 else 0.0

        # Two-sample t-test p-value
        t_stat, p_val = stats.ttest_ind(yt, yc, equal_var=False)

        rows.append({
            "covariate": col,
            "mean_treated": round(mean_t, 4),
            "mean_control": round(mean_c, 4),
            "std_diff": round(std_diff, 4),
            "var_treated": round(var_t, 4),
            "var_control": round(var_c, 4),
            "p_value": round(float(p_val), 4),
        })

    return pd.DataFrame(rows).set_index("covariate")
