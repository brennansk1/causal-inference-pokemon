# Chapter 7: Saffron City --- Difference-in-Differences & Synthetic Controls

> *"Saffron City stands at the crossroads of Kanto --- and at the crossroads of causal inference. When treatment rolls out across time and space, the researcher must think carefully about what constitutes a valid comparison. The methods in this chapter exploit the panel structure of data to identify causal effects when randomization is impossible."*
> --- Professor Oak, *Lectures on Kanto Econometrics*

---

The road from Celadon leads east through the guarded gates of Saffron City, Kanto's commercial capital and home to Silph Co., the region's largest technology conglomerate. But Saffron is under siege. Team Rocket has occupied the city, seized control of Silph Co. headquarters, and disrupted the economic life of thousands of residents. In the chaos, Silph's engineers rush to complete their most ambitious project: **Shadow Surge**, a powerful new Technical Machine (TM) that teaches any compatible Pokemon a devastating Dark-type move. The TM is released first in Saffron City --- partly as a morale boost, partly because the distribution infrastructure is already in place. Over the following months, Shadow Surge rolls out to other Kanto cities: Cerulean, Vermilion, and finally Lavender Town.

This staggered rollout --- born of logistical necessity rather than scientific design --- creates a **natural experiment**. By comparing outcomes in cities that received Shadow Surge early to those that received it later (or never), we can estimate the TM's causal effect on trainer battle performance. Meanwhile, Team Rocket's invasion of Saffron itself presents a second question: what is the economic cost of the occupation? No other Kanto city was invaded, so we cannot simply compare Saffron to an untreated city. Instead, we must construct a **synthetic** version of Saffron --- a weighted combination of uninvaded cities that approximates what Saffron would have looked like absent Team Rocket's intervention.

These two problems motivate the core methods of this chapter: **difference-in-differences** (DiD) and **synthetic control**. Along the way, we will confront one of the most important methodological advances of the past decade: the discovery that the workhorse **two-way fixed effects** (TWFE) regression can produce severely biased estimates when treatment rolls out at different times and treatment effects vary across groups. The modern DiD revolution --- Goodman-Bacon, Callaway and Sant'Anna, Sun and Abraham, and others --- provides the tools to set things right.

Let us begin.

---

## 7.1 Difference-in-Differences: The Classic 2x2 Design

### The Setup

It is Month 6 of the Kanto League season. Silph Co. releases Shadow Surge in **Saffron City** but not yet in **Cerulean City**. We observe trainer battle win rates in both cities for two periods: **before** the release (Months 1--5) and **after** (Months 7--12). The question: does Shadow Surge improve battle win rates?

We have panel data on trainers in both cities across both periods. Let $Y_{it}$ denote the average battle win rate for city $i$ in period $t$. We observe four group-period means:

| | **Pre-Treatment** (Months 1--5) | **Post-Treatment** (Months 7--12) | **Change** |
|---|---|---|---|
| **Saffron** (Treated) | $\bar{Y}_{S,pre} = 0.45$ | $\bar{Y}_{S,post} = 0.58$ | $+0.13$ |
| **Cerulean** (Control) | $\bar{Y}_{C,pre} = 0.40$ | $\bar{Y}_{C,post} = 0.44$ | $+0.04$ |

This is the classic **2x2 table of means**. Notice several things. First, Saffron's win rate was higher than Cerulean's even before Shadow Surge was released --- perhaps because Saffron trainers have better access to training facilities, or because Silph employees double as competitive battlers. A naive comparison of post-treatment win rates ($0.58 - 0.44 = 0.14$) would overstate the effect by attributing this pre-existing gap to the TM.

Second, both cities experienced an increase in win rates over time. The Kanto League season naturally features rising win rates as trainers accumulate experience and evolve their Pokemon. Simply comparing Saffron's win rate before and after ($0.58 - 0.45 = 0.13$) would conflate the Shadow Surge effect with this common upward trend.

The **difference-in-differences** estimator solves both problems at once:

$$\hat{\tau}_{DiD} = (\bar{Y}_{S,post} - \bar{Y}_{S,pre}) - (\bar{Y}_{C,post} - \bar{Y}_{C,pre})$$

$$\hat{\tau}_{DiD} = (0.58 - 0.45) - (0.44 - 0.40) = 0.13 - 0.04 = 0.09$$

The first difference ($0.13$) captures the total change in Saffron, which includes both the treatment effect and the common time trend. The second difference ($0.04$) captures only the common time trend, as Cerulean was untreated. By subtracting the second from the first, we **difference out** the time trend and isolate the causal effect of Shadow Surge.

> **Definition 7.1 (Difference-in-Differences Estimator).** For a treated group $i=1$ and control group $i=0$ observed before ($t=0$) and after ($t=1$) treatment, the DiD estimator is:
>
> $$\hat{\tau}_{DiD} = (\bar{Y}_{1,1} - \bar{Y}_{1,0}) - (\bar{Y}_{0,1} - \bar{Y}_{0,0})$$
>
> Equivalently, by rearranging terms:
>
> $$\hat{\tau}_{DiD} = (\bar{Y}_{1,1} - \bar{Y}_{0,1}) - (\bar{Y}_{1,0} - \bar{Y}_{0,0})$$
>
> The first form differences over time within groups, then differences across groups. The second form differences across groups within periods, then differences over time. Both yield the same estimate.

### The Regression Formulation

The DiD estimator has an equivalent regression representation. Define:

- $\text{Treat}_i = 1$ if unit $i$ is in the treated group (Saffron), 0 otherwise
- $\text{Post}_t = 1$ if the observation is in the post-treatment period, 0 otherwise

Then estimate:

$$Y_{it} = \alpha + \beta \cdot \text{Treat}_i + \gamma \cdot \text{Post}_t + \tau \cdot (\text{Treat}_i \times \text{Post}_t) + \epsilon_{it}$$

The coefficients have clear interpretations:

- $\alpha$: the mean outcome for the control group in the pre-period ($\bar{Y}_{C,pre} = 0.40$)
- $\beta$: the pre-treatment difference between treated and control groups ($\bar{Y}_{S,pre} - \bar{Y}_{C,pre} = 0.05$). This captures time-invariant differences between the groups
- $\gamma$: the change over time in the control group ($\bar{Y}_{C,post} - \bar{Y}_{C,pre} = 0.04$). This captures the common time trend
- $\tau$: the **DiD treatment effect** --- the additional change in the treated group beyond what the control group experienced ($0.09$)

Let us verify. The four fitted values from this regression are:

| | Pre | Post |
|---|---|---|
| **Cerulean** ($\text{Treat}=0$) | $\alpha = 0.40$ | $\alpha + \gamma = 0.44$ |
| **Saffron** ($\text{Treat}=1$) | $\alpha + \beta = 0.45$ | $\alpha + \beta + \gamma + \tau = 0.54$ |

Wait --- the fitted post-treatment value for Saffron is $0.54$, not the observed $0.58$. That is precisely the point. The regression model decomposes Saffron's post-treatment outcome as:

$$\underbrace{0.58}_{\text{observed}} = \underbrace{0.40}_{\alpha} + \underbrace{0.05}_{\beta} + \underbrace{0.04}_{\gamma} + \underbrace{0.09}_{\tau}$$

The model attributes $0.40$ to the baseline, $0.05$ to being Saffron, $0.04$ to the time trend, and $0.09$ to the causal effect of Shadow Surge. The counterfactual win rate for Saffron without Shadow Surge would have been $0.40 + 0.05 + 0.04 = 0.49$ --- that is, Saffron would have followed the same trend as Cerulean, reaching $0.49$ rather than the observed $0.58$.

### Why DiD Works: Differencing Out Confounders

The power of DiD lies in what it eliminates. Consider two types of confounders:

1. **Time-invariant confounders** (fixed characteristics of cities): Saffron has better training facilities, wealthier trainers, proximity to Silph Co. These factors make Saffron's win rate permanently higher than Cerulean's. The first difference (over time) eliminates these because they are constant across periods.

2. **Common time trends** (temporal shocks affecting all cities equally): the League season progression, a region-wide weather event, the release of a new batch of wild Pokemon. The second difference (across groups) eliminates these because they affect both cities equally.

What DiD does *not* eliminate is any confounder that varies differentially across groups over time --- a shock that hits Saffron but not Cerulean (or vice versa) at the same time as treatment. This is the domain of the **parallel trends** assumption, which we address in Section 7.2.

### The Parallel Lines Diagram

The intuition behind DiD is beautifully captured by what we might call the "parallel lines diagram." Imagine a graph with time on the horizontal axis and win rate on the vertical axis. Before treatment, Saffron's line runs above Cerulean's (reflecting the pre-existing gap of $0.05$), but both lines slope upward at the same rate. At the moment of treatment (Month 6), Saffron's line jumps upward by $\tau = 0.09$ and then continues along a higher trajectory. Cerulean's line continues along its original path.

The DiD estimate is the vertical distance between Saffron's actual post-treatment outcome and the **counterfactual** --- the dashed line showing where Saffron would have been had it followed the same trend as Cerulean. This counterfactual is constructed by taking Saffron's pre-treatment level and adding Cerulean's observed change.

> **Blue's Mistake 7.1.** *Blue compares Saffron's post-treatment win rate to Cerulean's post-treatment win rate and concludes that Shadow Surge increases win rates by* $0.58 - 0.44 = 0.14$.
>
> "I don't need your fancy double-differencing, Red. Just look at the numbers --- Saffron is 14 percentage points ahead after Shadow Surge drops. Case closed."
>
> Blue's estimate is biased upward by $0.05$ because it includes the pre-existing gap between Saffron and Cerulean that existed before Shadow Surge was ever released. Blue is attributing the effect of Saffron's superior training infrastructure to Shadow Surge. A simple post-treatment comparison confounds the treatment effect with pre-existing group differences.
>
> The correct DiD estimate of $0.09$ removes this bias by subtracting the pre-treatment gap. In potential outcomes notation, Blue is estimating $E[Y_1 | \text{Treat}=1] - E[Y_1 | \text{Treat}=0]$, which equals $\tau + (\text{pre-existing gap})$. DiD estimates $\tau$ alone.

### A Richer Worked Example

Suppose we observe not just city-level averages but trainer-level data. We have a balanced panel of 200 trainers --- 100 in Saffron and 100 in Cerulean --- observed in both periods. The regression becomes:

$$\text{WinRate}_{it} = \alpha + \beta \cdot \text{Saffron}_i + \gamma \cdot \text{Post}_t + \tau \cdot (\text{Saffron}_i \times \text{Post}_t) + \epsilon_{it}$$

Running OLS on the 400 observations (200 trainers $\times$ 2 periods), we obtain:

| Coefficient | Estimate | Std. Error | 95% CI |
|---|---|---|---|
| $\hat{\alpha}$ (Intercept) | 0.401 | 0.012 | [0.377, 0.425] |
| $\hat{\beta}$ (Saffron) | 0.049 | 0.017 | [0.016, 0.082] |
| $\hat{\gamma}$ (Post) | 0.041 | 0.014 | [0.014, 0.068] |
| $\hat{\tau}$ (Saffron $\times$ Post) | 0.089 | 0.020 | [0.050, 0.128] |

The DiD estimate is $\hat{\tau} = 0.089$ with a standard error of $0.020$, yielding a $t$-statistic of $4.45$. We reject the null hypothesis of no treatment effect at the $1\%$ level. Shadow Surge increases trainer win rates by approximately 9 percentage points.

Note: with panel data, we should cluster standard errors at the city level (see Section 7.3). With only two clusters, cluster-robust standard errors are unreliable, and alternative inference methods --- wild cluster bootstrap, randomization inference --- are preferred. This is a practical consideration we revisit below.

---

## 7.2 The Parallel Trends Assumption

### The Identifying Assumption

The DiD estimator isolates a causal effect **only if** the treated and control groups would have followed parallel paths in the absence of treatment. This is the **parallel trends assumption**, and it is the single most important assumption underlying all DiD analyses.

> **Assumption 7.1 (Parallel Trends).** In the absence of treatment, the average change in the outcome for the treated group equals the average change in the outcome for the control group:
>
> $$E[Y_{it}(0) | \text{Treat}_i = 1, t = 1] - E[Y_{it}(0) | \text{Treat}_i = 1, t = 0] = E[Y_{it}(0) | \text{Treat}_i = 0, t = 1] - E[Y_{it}(0) | \text{Treat}_i = 0, t = 0]$$
>
> Here $Y_{it}(0)$ denotes the potential outcome under no treatment. The assumption states that the treated group's counterfactual trend (under no treatment) parallels the control group's observed trend.

This assumption is fundamentally **untestable**. The left-hand side involves $E[Y_{it}(0) | \text{Treat}_i = 1, t = 1]$ --- the average untreated outcome for the treated group in the post-period. This is a counterfactual quantity that we never observe. Once Saffron receives Shadow Surge, we cannot know what Saffron's win rate would have been without it. This is simply the fundamental problem of causal inference applied to the DiD setting.

What parallel trends does *not* require:

- It does **not** require that treated and control groups have the same level of the outcome. Saffron can be permanently above Cerulean. The assumption is about *trends*, not levels.
- It does **not** require that the groups be similar on observables. They can differ on every observable characteristic --- as long as those differences produce only level shifts, not differential trends.
- It does **not** require that nothing else changes besides treatment. Other events can occur, as long as they affect both groups equally.

What parallel trends *does* require:

- No time-varying confounder that differentially affects the treated group. If Team Rocket's invasion suppresses Saffron's win rates at the same time as Shadow Surge is released, the DiD estimate will be biased downward (confounding a positive treatment effect with a negative invasion effect).
- No anticipation effects. If Saffron trainers change behavior before Shadow Surge is released (e.g., because Silph announces the TM in advance), the pre-treatment period is contaminated.
- No spillovers. If Cerulean trainers travel to Saffron to buy Shadow Surge, the control group is contaminated by treatment.

### Testing Pre-Treatment Trends: The Event Study

Although parallel trends is untestable, we can gain confidence in its plausibility (or detect violations) by examining **pre-treatment trends**. If the treated and control groups followed parallel paths before treatment, it is at least consistent with the assumption that they would have continued to do so afterward. If they diverged before treatment, the assumption is suspect.

The standard approach is the **event study** (or **leads-and-lags**) specification. Suppose we observe both cities for $T$ periods and treatment occurs at period $t^*$. Define event time as $k = t - t^*$, so $k = 0$ is the treatment period, $k < 0$ are pre-treatment periods, and $k > 0$ are post-treatment periods. Estimate:

$$Y_{it} = \alpha_i + \lambda_t + \sum_{k \neq -1} \tau_k \cdot D_{i,t-k} + \epsilon_{it}$$

where $\alpha_i$ are unit fixed effects, $\lambda_t$ are time fixed effects, and $D_{i,t-k}$ is an indicator equal to 1 if unit $i$ is in the treated group and the observation is $k$ periods from treatment. We omit $k = -1$ (the period just before treatment) as the reference category.

The estimated coefficients $\{\hat{\tau}_k\}$ trace out the **dynamic treatment effect path**:

- For $k < -1$: these are **pre-treatment coefficients** (leads). Under parallel trends, they should all be zero --- there is no treatment yet, so the treated group should not diverge from the control. If these coefficients are large and statistically significant, parallel trends is likely violated.
- For $k = 0$: this is the **on-impact** effect at the moment of treatment.
- For $k > 0$: these capture the **dynamic treatment effects** as they evolve over time.

The event study coefficient plot --- a graph with event time $k$ on the horizontal axis and $\hat{\tau}_k$ with confidence intervals on the vertical axis --- is one of the most important diagnostic tools in applied DiD research. A well-behaved plot shows pre-treatment coefficients clustered around zero (with confidence intervals overlapping zero), followed by a jump at $k = 0$ and potentially growing or declining effects in post-treatment periods.

In our Shadow Surge example, imagine we observe both Saffron and Cerulean for 12 months. Shadow Surge is released in Month 6 ($t^* = 6$). The event study plot shows:

- Months 1--4 ($k = -5$ to $k = -2$): estimated coefficients of $-0.01, 0.02, -0.01, 0.01$ --- all statistically insignificant and close to zero. Reassuring.
- Month 6 ($k = 0$): estimated coefficient of $0.07$. An immediate effect.
- Months 7--12 ($k = 1$ to $k = 6$): coefficients of $0.08, 0.09, 0.10, 0.10, 0.11, 0.11$ --- the effect grows slightly as trainers learn to use Shadow Surge effectively and then stabilizes.

This pattern is consistent with parallel trends and suggests a persistent, slightly growing treatment effect.

### When Parallel Trends Fails

Parallel trends can fail for many reasons:

1. **Differential pre-existing trends.** If Saffron's win rate was already rising faster than Cerulean's before Shadow Surge (perhaps due to ongoing Silph Co. investments in trainer development), DiD would attribute the continued divergence to the TM.

2. **Compositional changes.** If the types of trainers in Saffron change at the time of treatment (e.g., skilled trainers migrate to Saffron to access Shadow Surge), the comparison group is no longer stable.

3. **Simultaneous shocks.** If Team Rocket's invasion hits Saffron's economy at the same time as Shadow Surge is released, the estimated effect confounds the TM benefit with the invasion cost.

What to do when parallel trends is implausible:

- **Conditional parallel trends**: control for observables that might drive differential trends. The assumption weakens to: parallel trends holds conditional on covariates $X$. This leads to regression-adjusted DiD or methods like Callaway and Sant'Anna (2021) with outcome regression or inverse probability weighting.
- **Triple differences (DDD)**: add a third difference using a within-group comparison that is unaffected by treatment (Section 7.5).
- **Sensitivity analysis**: bound the treatment effect under specified violations of parallel trends (Rambachan and Roth, 2023).
- **Choose a better control group**: perhaps a city more similar to Saffron would provide more plausible parallel trends.

> **Professor Oak Explains 7.1.** "Think of parallel trends like this. You and Blue are both training your Pokemon. Every day, you both gain about the same amount of experience --- you are on parallel paths. Then you receive the Shadow Surge TM, and your win rate jumps. If I want to estimate how much Shadow Surge helped you, I can look at how much your win rate exceeded Blue's, beyond what the pre-existing gap would have predicted. But if you also started training twice as hard on the same day you got the TM --- for reasons having nothing to do with the TM --- then I would incorrectly attribute your extra improvement to Shadow Surge. Parallel trends says: absent the TM, you and Blue would have continued on parallel paths."

---

## 7.3 Two-Way Fixed Effects (TWFE) Regression

### The Model

With panel data on multiple cities over multiple time periods, researchers naturally extend the DiD framework to **two-way fixed effects** regression:

$$Y_{it} = \alpha_i + \lambda_t + \tau D_{it} + \epsilon_{it}$$

where:

- $Y_{it}$ is the outcome for city $i$ in period $t$
- $\alpha_i$ is a **unit fixed effect** for city $i$: a city-specific intercept that absorbs all time-invariant characteristics (geography, population, infrastructure quality, gym leader difficulty)
- $\lambda_t$ is a **time fixed effect** for period $t$: a time-specific intercept that absorbs all common temporal shocks (region-wide weather, League calendar effects, macroeconomic conditions)
- $D_{it}$ is a treatment indicator equal to 1 if city $i$ has been treated by period $t$, and 0 otherwise
- $\tau$ is the coefficient of interest --- the average treatment effect
- $\epsilon_{it}$ is an idiosyncratic error term

The unit fixed effects perform the same role as the $\beta \cdot \text{Treat}_i$ term in the 2x2 regression: they absorb permanent differences between treated and control units. The time fixed effects perform the same role as $\gamma \cdot \text{Post}_t$: they absorb common temporal variation. Together, they generalize DiD to settings with many units and many periods.

### Equivalence to DiD in the 2x2 Case

In the simple 2x2 setting (two groups, two periods), TWFE and the DiD regression are numerically identical. To see this, note that with two groups and two periods, the unit fixed effect $\alpha_i$ is fully captured by a single group dummy, and the time fixed effect $\lambda_t$ is fully captured by a single period dummy. The TWFE model reduces to:

$$Y_{it} = \alpha + \beta \cdot \text{Treat}_i + \gamma \cdot \text{Post}_t + \tau \cdot (\text{Treat}_i \times \text{Post}_t) + \epsilon_{it}$$

where the interaction term $\text{Treat}_i \times \text{Post}_t$ is exactly the treatment indicator $D_{it}$ (since treatment turns on for the treated group in the post period). This is the DiD regression from Section 7.1. The equivalence is exact: the same OLS coefficient $\hat{\tau}$ results from either specification.

### Adding Covariates

In practice, we often add time-varying covariates $X_{it}$ to improve precision or to make the parallel trends assumption more plausible conditional on observables:

$$Y_{it} = \alpha_i + \lambda_t + \tau D_{it} + X_{it}'\delta + \epsilon_{it}$$

For example, we might control for the average level of trainers' Pokemon ($\text{AvgLevel}_{it}$), the number of active trainers in the city ($\text{NumTrainers}_{it}$), or local economic conditions ($\text{GDP}_{it}$). These covariates must be **time-varying** because time-invariant covariates are already absorbed by the unit fixed effects $\alpha_i$.

A word of caution: covariates that are themselves affected by treatment (post-treatment variables or "bad controls") should not be included, as they can introduce bias. If Shadow Surge causes more trainers to battle (increasing $\text{NumTrainers}_{it}$), conditioning on the number of trainers would block part of the causal pathway.

### Inference: Clustering Standard Errors

With panel data, observations within the same city are correlated over time: if Saffron has a good month, it is likely to have another good month next period. Standard OLS standard errors ignore this correlation and are typically too small, leading to over-rejection of the null hypothesis.

The standard solution is to **cluster standard errors at the unit level** (city level). Cluster-robust standard errors allow for arbitrary within-cluster correlation in the errors. The cluster-robust variance estimator is:

$$\hat{V}^{CR} = (X'X)^{-1} \left( \sum_{i=1}^{N} X_i' \hat{\epsilon}_i \hat{\epsilon}_i' X_i \right) (X'X)^{-1}$$

where $X_i$ is the matrix of regressors for unit $i$ and $\hat{\epsilon}_i$ is the vector of residuals for unit $i$. This estimator is consistent as the number of clusters $N \to \infty$, but can perform poorly with few clusters. A commonly cited rule of thumb is that at least 30--50 clusters are needed for reliable inference.

In Kanto, we have at most 10 cities --- far too few for asymptotic cluster-robust inference. In such settings, researchers turn to:

- **Wild cluster bootstrap** (Cameron, Gelbach, and Miller, 2008): a resampling method that provides better finite-sample performance with few clusters
- **Randomization inference**: permute the treatment assignment across cities and compute the distribution of the test statistic under the null
- **Aggregation**: work with city-level averages and use $t$-tests with appropriate degrees of freedom

### The Appeal of TWFE --- and Its Trap

TWFE seems like the ideal generalization of DiD: include fixed effects for units and time, throw in the treatment indicator, and estimate the average effect. For decades, this was the standard approach in economics, political science, and other social sciences. Thousands of published papers used exactly this specification.

But beginning in the late 2010s, a series of landmark papers revealed a disturbing fact: **when treatment is adopted at different times by different units, and treatment effects are heterogeneous, the TWFE estimator can be severely biased.** It can even give the wrong sign.

This is the TWFE trap, and it awaits us in Section 7.4.

---

## 7.4 Staggered Treatment and the Modern DiD Revolution

### The Setting: Shadow Surge Rolls Out Across Kanto

Silph Co.'s release of Shadow Surge is not simultaneous. Due to production constraints and distribution logistics, the TM reaches different cities at different times:

| City | Treatment Cohort | Treatment Period |
|---|---|---|
| **Saffron** | Early Adopter | Period 6 |
| **Cerulean** | Mid Adopter | Period 10 |
| **Vermilion** | Late Adopter | Period 14 |
| **Lavender** | Latest Adopter | Period 18 |
| **Pewter** | Never Treated | --- |
| **Celadon** | Never Treated | --- |
| **Fuchsia** | Never Treated | --- |
| **Cinnabar** | Never Treated | --- |

We observe all 8 cities for 24 periods. The outcome is average trainer win rate. A natural instinct is to estimate the TWFE regression:

$$Y_{it} = \alpha_i + \lambda_t + \tau D_{it} + \epsilon_{it}$$

where $D_{it} = 1$ once city $i$ has received Shadow Surge. We obtain $\hat{\tau}^{TWFE} = 0.052$, and it is statistically significant. Case closed?

Not even close.

### Why Naive TWFE Fails with Staggered Adoption

The fundamental problem is that TWFE does not estimate a single, clean DiD. Instead, as Goodman-Bacon (2021) demonstrated, the TWFE coefficient is a **weighted average of all possible 2x2 DiD estimates** that can be constructed from the data. Some of these 2x2 comparisons are perfectly valid. Others are deeply problematic.

To understand why, consider what OLS does when it estimates the TWFE model. The Frisch-Waugh-Lovell theorem tells us that the coefficient $\hat{\tau}$ is obtained by regressing the residualized outcome (after removing unit and time fixed effects) on the residualized treatment indicator. This process implicitly creates comparisons between:

1. **Newly-treated units vs. never-treated units.** Saffron (treated in period 6) is compared to Pewter (never treated). This is a valid 2x2 DiD.

2. **Newly-treated units vs. not-yet-treated units.** Saffron (treated in period 6) is compared to Cerulean (not treated until period 10), using periods before and after Saffron's treatment but before Cerulean's. This is also valid --- Cerulean is a clean control during this window.

3. **Newly-treated units vs. already-treated units.** Here is the problem. When Cerulean receives Shadow Surge in period 10, TWFE may use Saffron --- which has been treated since period 6 --- as a "control" unit. But Saffron is not an untreated control. It is an already-treated unit whose treatment effect may be evolving over time. If Shadow Surge's effect grows as trainers master the TM (a dynamic, heterogeneous treatment effect), then Saffron's rising win rate in periods 6--10 will make it look like Cerulean's treatment *reduced* its win rate relative to Saffron. This is nonsensical.

This third type of comparison --- using already-treated units as controls --- can produce **negative weights** on some group-time average treatment effects on the treated (ATTs). When treatment effects are heterogeneous across cohorts or grow over time, these negative weights can cause the TWFE estimate to be biased, and in extreme cases, to have the **wrong sign**: TWFE reports a negative effect even though the true effect is positive for every group at every time.

### The Goodman-Bacon (2021) Decomposition

Andrew Goodman-Bacon's landmark paper provides an exact decomposition of the TWFE coefficient. Consider a balanced panel with multiple treatment cohorts and some never-treated units. The TWFE estimator $\hat{\tau}^{TWFE}$ can be written as:

$$\hat{\tau}^{TWFE} = \sum_{k} \sum_{l \neq k} s_{kl} \cdot \hat{\tau}_{kl}^{2x2}$$

where $\hat{\tau}_{kl}^{2x2}$ is the 2x2 DiD estimate using cohort $k$ as the "treated" group and cohort $l$ as the "control" group, and $s_{kl}$ is a weight that depends on the group sizes and the variance of the treatment indicator for that particular 2x2 comparison. The weights $s_{kl}$ are guaranteed to sum to one, but they are **not** guaranteed to be non-negative when already-treated units serve as controls.

The decomposition reveals three types of 2x2 comparisons:

**Type 1: Timing groups vs. never-treated.** Cohort $k$ (treated at some point) is compared to the never-treated pool. These comparisons are clean and receive positive weights. The weight depends on the cohort's size and the fraction of the sample period during which it is treated.

**Type 2: Earlier-treated vs. later-treated (using the later group as control).** Saffron (treated in period 6) is the treated group, and Cerulean (treated in period 10) serves as control during periods 6--9. This is valid: Cerulean is genuinely untreated during this window.

**Type 3: Later-treated vs. earlier-treated (using the earlier group as control).** Cerulean (treated in period 10) is the treated group, and Saffron (already treated since period 6) serves as "control." This is the **forbidden comparison**. The weight on this comparison is positive in the Goodman-Bacon decomposition, but the DiD estimate itself may be biased because Saffron is not an untreated control.

#### Worked Example: Negative Weights in Kanto

Suppose the true ATT of Shadow Surge is:

- Saffron: effect grows from 0.05 in the first period to 0.15 after 12 periods (dynamic, increasing effect as trainers learn to use the TM)
- Cerulean: effect grows similarly, 0.05 to 0.10 over 8 treated periods
- Vermilion: 0.05 to 0.08 over 4 treated periods
- Lavender: 0.05 (only treated for 2 periods)

The simple average ATT across all group-time cells is approximately $0.08$. Now consider what TWFE does.

When Vermilion becomes treated in period 14, TWFE uses Saffron (treated since period 6) as one of the "control" units. By period 14, Saffron's treatment effect has grown to about 0.12. Between periods 14 and 24, Saffron's treatment effect continues to grow (from 0.12 to 0.15). This upward trajectory in Saffron's outcomes --- driven by the maturing treatment effect --- makes Vermilion look worse by comparison. The 2x2 DiD estimate from this comparison could be much smaller than Vermilion's true effect, or even negative.

In our simulation, the Goodman-Bacon decomposition yields:

| Comparison Type | Average 2x2 DiD | Weight |
|---|---|---|
| Treated vs. Never-Treated | 0.085 | 0.45 |
| Earlier vs. Later (later as control) | 0.073 | 0.30 |
| Later vs. Earlier (earlier as control) | 0.021 | 0.25 |

The TWFE estimate is: $0.085 \times 0.45 + 0.073 \times 0.30 + 0.021 \times 0.25 = 0.038 + 0.022 + 0.005 = 0.065$.

The TWFE estimate of $0.065$ is substantially below the true average ATT of $0.08$. The "later vs. earlier" comparisons pull the estimate downward because the already-treated cities' rising treatment effects contaminate the control group. In more extreme scenarios --- particularly when early-treated units have large, growing effects and later-treated units have smaller effects --- the TWFE estimate can be near zero or even negative despite all true effects being positive.

This is Team Rocket's hidden scheme: an estimator that looked trustworthy is secretly corrupted by its own internal comparisons.

### Callaway and Sant'Anna (2021): Group-Time ATTs

Brantly Callaway and Pedro Sant'Anna proposed a clean solution: estimate the treatment effect separately for each **cohort** (group of units treated at the same time) at each **time period**, using only valid comparisons.

> **Definition 7.2 (Group-Time Average Treatment Effect).** For treatment cohort $g$ (the set of units first treated in period $g$) at time period $t \geq g$, the group-time ATT is:
>
> $$ATT(g, t) = E[Y_{it}(g) - Y_{it}(0) | G_i = g]$$
>
> where $Y_{it}(g)$ is the potential outcome under treatment that began in period $g$ and $Y_{it}(0)$ is the potential outcome under no treatment.

The key innovation is in the choice of **comparison group**. Callaway and Sant'Anna use either:

- **Never-treated units** as the comparison group, or
- **Not-yet-treated units** (units whose treatment has not yet begun as of period $t$) as the comparison group

Both choices avoid the forbidden comparison of using already-treated units as controls.

For each $(g, t)$ pair, the estimator is essentially a 2x2 DiD comparing cohort $g$ to the chosen comparison group, using periods $g-1$ (the period just before treatment) and $t$ as the two time periods. This yields a clean estimate of $ATT(g, t)$.

Estimation proceeds via one of three approaches:

1. **Outcome regression**: model the counterfactual outcome using a regression on the comparison group's outcomes, then compute the treatment effect as the difference between treated outcomes and the fitted counterfactual
2. **Inverse probability weighting (IPW)**: weight the comparison group to match the treated group's covariate distribution
3. **Doubly robust**: combine outcome regression and IPW to achieve consistency if *either* the outcome model or the propensity score model is correctly specified

The collection of $ATT(g, t)$ estimates can be **aggregated** in various ways:

- **Simple average** (overall ATT): $\hat{\tau} = \frac{1}{|\mathcal{G}|} \sum_{g \in \mathcal{G}} \frac{1}{T - g + 1} \sum_{t=g}^{T} \widehat{ATT}(g, t)$
- **Dynamic effects** (event-study): average across cohorts at each event time $e = t - g$, yielding $\hat{\tau}_e = \frac{1}{|\mathcal{G}_e|} \sum_{g \in \mathcal{G}_e} \widehat{ATT}(g, g+e)$
- **Cohort-specific effects**: average across time within each cohort $g$
- **Calendar-time effects**: average across cohorts within each period $t$

In our Shadow Surge example, the Callaway-Sant'Anna estimates (using never-treated as comparison) yield:

| | $t=6$ | $t=10$ | $t=14$ | $t=18$ | $t=24$ |
|---|---|---|---|---|---|
| $ATT(\text{Saffron}, t)$ | 0.05 | 0.09 | 0.12 | 0.14 | 0.15 |
| $ATT(\text{Cerulean}, t)$ | --- | 0.05 | 0.07 | 0.09 | 0.10 |
| $ATT(\text{Vermilion}, t)$ | --- | --- | 0.05 | 0.07 | 0.08 |
| $ATT(\text{Lavender}, t)$ | --- | --- | --- | 0.05 | 0.06 |

Each cell is a clean, interpretable treatment effect. The simple average across all filled cells is $0.081$, much closer to the truth than TWFE's $0.065$.

### Sun and Abraham (2021): Interaction-Weighted Estimator

Liyang Sun and Sarah Abraham proposed a closely related approach that works within the regression framework that applied researchers are familiar with. Their key insight: the standard event study regression with cohort-specific indicators,

$$Y_{it} = \alpha_i + \lambda_t + \sum_{g \in \mathcal{G}} \sum_{e \neq -1} \tau_{g,e} \cdot \mathbf{1}[G_i = g] \cdot \mathbf{1}[t - g = e] + \epsilon_{it}$$

identifies the cohort-specific treatment effects $\tau_{g,e}$ cleanly. The problem with standard TWFE event studies is that they constrain all cohorts to have the same effect at each event time $e$, which introduces contamination. Sun and Abraham's estimator:

1. Estimates cohort-specific effects $\hat{\tau}_{g,e}$ by interacting the event-time indicators with cohort indicators
2. Aggregates across cohorts using appropriate weights (e.g., cohort shares) to obtain the **interaction-weighted** (IW) estimator for each event time

This approach yields an event study plot that is robust to treatment effect heterogeneity across cohorts --- unlike the naive TWFE event study, which can show spurious pre-trends or distorted post-treatment dynamics even when all individual cohort effects are clean.

### de Chaisemartin and D'Haultfouille (2020): Instantaneous Effects

Clement de Chaisemartin and Xavier D'Haultfouille took a different but complementary approach. They showed that even in a simple two-period, two-group setting, the TWFE estimator can be decomposed as a weighted sum of individual-level treatment effects where some weights may be negative.

Their proposed estimator, $\hat{\tau}_{DH}$, focuses on the **instantaneous treatment effect** --- the effect of treatment on switchers (units whose treatment status changes) at the moment of switching. It compares switchers to non-switchers in the same period, using a single pre-treatment period as baseline. This avoids contamination from dynamic effects and is robust to heterogeneity.

For each period $t$ in which some units switch from untreated to treated, define:

$$\hat{\tau}_{DH,t} = \frac{1}{|S_t|} \sum_{i \in S_t} (Y_{it} - Y_{i,t-1}) - \frac{1}{|N_t|} \sum_{i \in N_t} (Y_{it} - Y_{i,t-1})$$

where $S_t$ is the set of units that switch to treatment in period $t$ and $N_t$ is the set of units that remain untreated in period $t$. The overall estimator averages across switching periods with appropriate weights.

This estimator is particularly useful when the researcher is primarily interested in the immediate impact of treatment rather than its long-run dynamics.

### Borusyak, Jaravel, and Spiess (2024): The Imputation Estimator

Kirill Borusyak, Xavier Jaravel, and Jann Spiess proposed an elegant and efficient approach: the **imputation estimator**. The logic is transparent:

1. **Estimate the counterfactual model using only untreated observations.** Fit the TWFE model $Y_{it} = \alpha_i + \lambda_t + \epsilon_{it}$ using only observations where $D_{it} = 0$ (units that have not yet been treated, or are never treated). This gives estimated fixed effects $\hat{\alpha}_i$ and $\hat{\lambda}_t$.

2. **Impute the counterfactual for treated observations.** For each treated observation $(i, t)$ with $D_{it} = 1$, predict what the outcome would have been absent treatment: $\hat{Y}_{it}(0) = \hat{\alpha}_i + \hat{\lambda}_t$.

3. **Compute the treatment effect as the difference.** $\hat{\tau}_{it} = Y_{it} - \hat{Y}_{it}(0)$.

4. **Aggregate.** Average the individual treatment effects across groups, event times, or overall.

The imputation estimator is efficient (it uses all untreated observations to estimate the fixed effects) and transparent (the counterfactual construction is explicit). It is numerically equivalent to the Callaway-Sant'Anna estimator under homogeneous treatment effects, but can be more efficient when the panel is large.

In our example, the imputation approach estimates $\hat{\alpha}_i$ and $\hat{\lambda}_t$ from the 4 never-treated cities across all 24 periods, plus the pre-treatment periods of the 4 treated cities. It then predicts each treated city's counterfactual and computes the gap.

### Comparing Estimators: The Revelation

Let us line up the estimates for the overall average treatment effect of Shadow Surge:

| Estimator | Estimate | True ATT |
|---|---|---|
| Naive TWFE | 0.065 | 0.081 |
| Goodman-Bacon (diagnostic) | --- (decomposition, not an estimator) | --- |
| Callaway-Sant'Anna | 0.081 | 0.081 |
| Sun-Abraham | 0.080 | 0.081 |
| de Chaisemartin-D'Haultfouille | 0.078 | 0.081 |
| Borusyak-Jaravel-Spiess | 0.081 | 0.081 |

The modern estimators all recover the truth (up to sampling error). TWFE is biased downward by about 20% because of contamination from the already-treated comparisons. In settings with more dramatic heterogeneity, the bias can be far worse.

> **Professor Oak Explains 7.2.** "Think of it this way. You are trying to measure how much a Rare Candy boosts a Pokemon's CP. You give Rare Candies to different Pokemon at different times. If you use a Pokemon that already received a Rare Candy as a 'control' for a newly treated Pokemon, and the early Pokemon is still gaining CP from its candy, you will underestimate the effect for the new Pokemon. The modern methods say: only compare to Pokemon that have not yet received any Rare Candy. That way, your control group is truly untreated."

> **Blue's Mistake 7.2.** *Blue runs a TWFE regression on the staggered Shadow Surge data and reports that the TM increases win rates by only 5.2 percentage points.*
>
> "Standard errors are tiny, $R^2$ is huge, fixed effects on both dimensions --- this is airtight, Red."
>
> Blue's estimate is contaminated by comparisons where already-treated cities serve as controls. With dynamic treatment effects that grow over time, these comparisons generate downward bias. The true average effect is about 8 percentage points. Blue's "airtight" regression is secretly comparing newly-treated cities to cities whose treatment effects are still maturing, making the new treatment look less effective than it actually is.
>
> **Lesson:** In staggered settings, always run a Goodman-Bacon decomposition to check for problematic comparisons, and use a heterogeneity-robust estimator.

### Practical Guidance for Applied Researchers

The modern DiD literature has converged on several practical recommendations:

1. **Always plot the raw data.** Before running any regression, plot the outcome time series for each cohort. Visual inspection can reveal violations of parallel trends, anticipation effects, or differential pre-treatment dynamics.

2. **Run the Goodman-Bacon decomposition** as a diagnostic. If the weight on already-treated comparisons is small, TWFE may be approximately unbiased. If it is large, modern estimators are essential.

3. **Use a heterogeneity-robust estimator.** Callaway-Sant'Anna and Borusyak-Jaravel-Spiess are the most commonly used. Both are available in standard software packages (`did` in R, `csdid` in Stata, `did` in Python).

4. **Report the event study plot** from a robust estimator (Sun-Abraham or Callaway-Sant'Anna), not from a naive TWFE event study. The naive event study can show spurious pre-trends or mask true dynamics.

5. **Be explicit about the comparison group.** State whether you are using never-treated or not-yet-treated units as the comparison group, and discuss the implications.

6. **Test for pre-trends** using the robust event study. If pre-treatment coefficients are significantly different from zero, parallel trends is suspect even with the correct estimator.

---

## 7.5 Triple Differences (DDD)

### Motivation

Sometimes the parallel trends assumption is hard to defend, even with careful control group selection. Return to the Shadow Surge example. Suppose that Saffron City, in addition to receiving Shadow Surge, also received a major Silph Co. investment in Pokemon Centers that improved trainer rest and recovery. If this investment occurred at the same time as the TM release, DiD cannot separate the effect of Shadow Surge from the effect of better Pokemon Centers. Both Saffron-specific changes happened simultaneously.

But here is additional variation we can exploit: not all trainers in Saffron use Shadow Surge. Only trainers with Dark-type or compatible Pokemon can learn the move. Trainers with incompatible teams (say, pure Psychic-type specialists in Saffron's famous Psychic gym) cannot use the TM at all. These non-users are exposed to the same Pokemon Center investment but not to the Shadow Surge treatment.

This creates a **third difference**: within Saffron, we can compare users vs. non-users to isolate the effect of the TM itself.

### The DDD Estimator

Define three dimensions of variation:

- **City**: Saffron (treated) vs. Cerulean (control)
- **Time**: Before vs. After Shadow Surge release
- **Trainer type**: Users (compatible Pokemon) vs. Non-users (incompatible Pokemon)

The **triple differences** estimator is:

$$\hat{\tau}_{DDD} = \Big[(\bar{Y}_{S,U,post} - \bar{Y}_{S,U,pre}) - (\bar{Y}_{S,N,post} - \bar{Y}_{S,N,pre})\Big] - \Big[(\bar{Y}_{C,U,post} - \bar{Y}_{C,U,pre}) - (\bar{Y}_{C,N,post} - \bar{Y}_{C,N,pre})\Big]$$

where $S/C$ indexes Saffron/Cerulean, $U/N$ indexes Users/Non-users, and $pre/post$ indexes time periods.

The first bracket is a DiD within Saffron comparing users to non-users. This differences out any Saffron-specific shocks (like the Pokemon Center investment) that affect all trainers equally. The second bracket is the same DiD within Cerulean, which accounts for any differential trends between user-types and non-user-types that are common across cities.

The regression formulation includes all main effects, two-way interactions, and the triple interaction:

$$Y_{itk} = \alpha + \beta_1 \text{Treat}_i + \beta_2 \text{Post}_t + \beta_3 \text{User}_k + \beta_4 (\text{Treat}_i \times \text{Post}_t) + \beta_5 (\text{Treat}_i \times \text{User}_k) + \beta_6 (\text{Post}_t \times \text{User}_k) + \tau (\text{Treat}_i \times \text{Post}_t \times \text{User}_k) + \epsilon_{itk}$$

The coefficient $\tau$ on the triple interaction is the DDD estimate.

### A Worked Example

| | Saffron, Users | Saffron, Non-users | Cerulean, Users | Cerulean, Non-users |
|---|---|---|---|---|
| Pre | 0.45 | 0.42 | 0.40 | 0.38 |
| Post | 0.60 | 0.49 | 0.46 | 0.42 |
| Change | +0.15 | +0.07 | +0.06 | +0.04 |

DiD within Saffron (Users vs Non-users): $0.15 - 0.07 = 0.08$

DiD within Cerulean (Users vs Non-users): $0.06 - 0.04 = 0.02$

DDD: $0.08 - 0.02 = 0.06$

The DDD estimate of $0.06$ removes both city-specific shocks (via the within-city comparison) and common user-type trends (via the cross-city comparison). The $0.02$ differential in Cerulean reflects the fact that "user-type" trainers may naturally improve faster than "non-user-type" trainers regardless of Shadow Surge. DDD nets this out.

### When DDD Helps and When It Does Not

DDD helps when:

- A within-group comparison (users vs. non-users) is available
- City-specific shocks contaminate the standard DiD
- The within-group comparison is not itself contaminated (non-users in Saffron are truly unaffected by Shadow Surge)

DDD does not help when:

- The within-group "control" (non-users) is affected by treatment through spillovers (e.g., non-users benefit because their user-type teammates win more battles, improving the team's reputation)
- The differential trends between user-types and non-user-types vary across cities for reasons other than treatment
- The additional differencing reduces statistical power significantly (DDD estimates are noisier than DiD)

---

## 7.6 Synthetic Control Method

### The Problem: Team Rocket's Invasion

We now turn to the second causal question in Saffron City. Team Rocket invaded Saffron in Period 8, occupying Silph Co. headquarters and disrupting commercial activity. We want to estimate the economic impact of the invasion. The outcome is $Y_{it}$, an index of economic activity for city $i$ in period $t$.

Unlike the Shadow Surge rollout, the invasion affected only one city. There is no "control Saffron" that was not invaded. Moreover, no single uninvaded city is a convincing counterfactual: Celadon is a commercial hub but differs in industrial composition; Vermilion is a port city with different economic drivers; Cerulean relies heavily on tourism. Each is similar to Saffron in some ways but different in others.

The **synthetic control method** (Abadie and Gardeazabal, 2003; Abadie, Diamond, and Hainmueller, 2010) solves this problem by constructing a **weighted combination** of untreated cities that closely matches Saffron's pre-treatment characteristics and outcomes. This "Synthetic Saffron" provides the counterfactual.

### The Method

Suppose we have $J + 1$ cities, where city $j = 0$ (Saffron) is treated and cities $j = 1, \ldots, J$ are potential controls (the **donor pool**). We observe outcomes $Y_{jt}$ for $t = 1, \ldots, T$, with treatment occurring at period $T_0 + 1$.

> **Definition 7.3 (Synthetic Control).** A synthetic control for the treated unit is a weighted average of donor pool units with weights $w = (w_1, \ldots, w_J)'$ satisfying:
>
> $$w_j \geq 0 \quad \text{for all } j = 1, \ldots, J$$
> $$\sum_{j=1}^{J} w_j = 1$$
>
> The weights are chosen to minimize the distance between the treated unit's pre-treatment characteristics and the weighted average of the donors' characteristics:
>
> $$w^* = \arg\min_{w} \| X_0 - X_1 w \|_V = \arg\min_{w} (X_0 - X_1 w)' V (X_0 - X_1 w)$$
>
> where $X_0$ is a vector of pre-treatment characteristics for the treated unit, $X_1$ is a matrix of pre-treatment characteristics for the donor pool, and $V$ is a positive semi-definite weighting matrix.

The pre-treatment characteristics $X$ typically include:

- **Pre-treatment outcomes** $Y_{j,1}, \ldots, Y_{j,T_0}$: matching on the entire pre-treatment outcome trajectory is the most important determinant of fit
- **Predictor variables**: observable characteristics that drive the outcome (population, GDP, number of Pokemon gyms, industrial composition)

The non-negativity and summing-to-one constraints ensure that the synthetic control is an **interpolation** (not extrapolation) of the donor pool. This prevents the method from constructing implausible counterfactuals by assigning negative weights or weights that sum to more than one.

The weighting matrix $V$ determines the relative importance of each predictor in the matching. It can be specified by the researcher or chosen via cross-validation to minimize the mean squared prediction error in the pre-treatment period.

### Estimating the Treatment Effect

Once the optimal weights $w^*$ are determined, the **synthetic control estimate** of the treatment effect at each post-treatment period $t > T_0$ is:

$$\hat{\tau}_t = Y_{0,t} - \sum_{j=1}^{J} w_j^* Y_{j,t}$$

This is the gap between Saffron's actual economic activity and the weighted average of the donor cities' economic activity. If the synthetic control closely matches Saffron in the pre-treatment period, the post-treatment gap is a credible estimate of the causal effect of Team Rocket's invasion.

### Constructing Synthetic Saffron

We have seven potential donor cities. The pre-treatment characteristics include average economic activity (Periods 1--7), population, number of registered trainers, and distance to the nearest port. The optimization finds:

| Donor City | Weight |
|---|---|
| Celadon | 0.42 |
| Vermilion | 0.31 |
| Cerulean | 0.18 |
| Pewter | 0.09 |
| Fuchsia | 0.00 |
| Cinnabar | 0.00 |
| Lavender | 0.00 |

Synthetic Saffron is primarily a blend of Celadon (the other major commercial center), Vermilion (a port city with substantial economic activity), and Cerulean (a mid-sized city with tourism). Fuchsia, Cinnabar, and Lavender receive zero weight --- they are too dissimilar to be useful.

Let us examine the pre-treatment fit:

| Characteristic | Saffron (Actual) | Synthetic Saffron |
|---|---|---|
| Avg. Econ. Activity (Per. 1--7) | 87.3 | 86.8 |
| Population (thousands) | 145 | 141 |
| Registered Trainers | 2,340 | 2,290 |
| Distance to Port (km) | 35 | 38 |

The pre-treatment match is excellent. More importantly, the pre-treatment outcome trajectory of Synthetic Saffron closely tracks actual Saffron:

| Period | Saffron | Synthetic Saffron | Gap |
|---|---|---|---|
| 1 | 85.2 | 84.9 | 0.3 |
| 2 | 86.1 | 85.8 | 0.3 |
| 3 | 86.8 | 86.5 | 0.3 |
| 4 | 87.5 | 87.1 | 0.4 |
| 5 | 88.0 | 87.7 | 0.3 |
| 6 | 88.4 | 88.2 | 0.2 |
| 7 | 88.9 | 88.6 | 0.3 |
| **8 (Invasion)** | **84.1** | **89.1** | **-5.0** |
| 9 | 80.5 | 89.5 | -9.0 |
| 10 | 78.2 | 89.9 | -11.7 |
| 11 | 76.8 | 90.2 | -13.4 |
| 12 | 77.5 | 90.6 | -13.1 |

The pre-treatment gaps are tiny (around 0.3), confirming a good fit. After the invasion, Saffron's economic activity plummets while Synthetic Saffron continues its upward trajectory. The estimated effect of the invasion is devastating: by Period 12, Saffron's economy is 13.1 index points below its synthetic counterfactual, a decline of roughly 14.5%.

### Inference via Placebo Tests

Standard inference (confidence intervals, $p$-values) is not straightforward for synthetic control because there is typically only one treated unit. Instead, Abadie, Diamond, and Hainmueller propose **placebo tests** (or "in-space" placebos):

1. **Apply the synthetic control method to every donor city in turn**, pretending each is the "treated" unit and using the remaining donors (plus, optionally, the actual treated unit in the pre-treatment period) as the donor pool.

2. **Compute the post-treatment gap** for each placebo unit. If the method is well-calibrated, placebo units should show small post-treatment gaps (since they were not actually treated).

3. **Compare Saffron's gap to the distribution of placebo gaps.** If Saffron's gap is unusually large relative to the placebo distribution, the effect is statistically significant.

A common refinement uses the **ratio of post-treatment RMSPE to pre-treatment RMSPE** for each unit:

$$\text{Ratio}_j = \frac{\text{RMSPE}_{j,post}}{\text{RMSPE}_{j,pre}}$$

where $\text{RMSPE}_{j,post} = \sqrt{\frac{1}{T - T_0} \sum_{t=T_0+1}^{T} (Y_{jt} - \hat{Y}_{jt}^{synth})^2}$ and similarly for the pre-treatment period. A large ratio indicates a genuine treatment effect (large post-treatment gap) rather than poor pre-treatment fit (which would inflate both numerator and denominator).

In our example, Saffron's RMSPE ratio is 38.7. The largest placebo ratio is 4.2 (for Celadon). Saffron's ratio dwarfs all placebos. The implied $p$-value is $1/8 = 0.125$ if we simply rank the ratios (with 8 total units), which is not significant at the 5% level. This highlights a limitation of synthetic control: with few donor units, the permutation distribution has limited resolution. With 20 or more donors, a $p$-value of $1/20 = 0.05$ is achievable.

> **Professor Oak Explains 7.3.** "The synthetic control method is like constructing a custom Pokemon team. No single Pokemon can perfectly replicate the strengths of your Charizard. But perhaps a team of Arcanine (42%), Gyarados (31%), Vaporeon (18%), and Golem (9%) comes very close in terms of stats and type coverage. If your Charizard suddenly loses a battle it should have won, and this team of substitutes performs normally, you know something happened specifically to Charizard --- it was not just bad luck affecting all Fire-types."

---

## 7.7 Extensions and Frontiers

### Augmented Synthetic Control (Ben-Michael, Feller, and Rothstein, 2021)

Standard synthetic control can struggle when no convex combination of donor units closely matches the treated unit's pre-treatment trajectory. The **Augmented Synthetic Control Method (ASCM)** addresses this by adding a **bias correction** term based on an outcome model.

The ASCM estimate is:

$$\hat{\tau}_t^{ASCM} = \hat{\tau}_t^{SC} + \sum_{j=1}^{J} (w_j^* - \frac{1}{J}) \cdot (\hat{m}(X_j, t) - \hat{m}(X_0, t))$$

where $\hat{m}(\cdot)$ is a fitted outcome model (e.g., a ridge regression of $Y_{jt}$ on pre-treatment covariates) and $w_j^*$ are the synthetic control weights. The correction term adjusts for residual imbalance between the synthetic control and the treated unit. If the standard synthetic control achieves perfect balance, the correction is zero and ASCM reduces to standard SC. If balance is imperfect, the outcome model fills the gap.

ASCM is doubly robust in spirit: it is consistent if either the synthetic control provides a good match or the outcome model is correctly specified. It also provides valid confidence intervals based on asymptotic theory, avoiding the need for permutation-based inference.

### Synthetic Difference-in-Differences (Arkhangelsky et al., 2021)

Dmitry Arkhangelsky, Susan Athey, David Hirshberg, Guido Imbens, and Stefan Wager proposed the **Synthetic Difference-in-Differences (SDiD)** estimator, which elegantly combines the strengths of DiD and synthetic control.

Standard DiD uses equal weights on all control units but requires parallel trends. Standard SC uses optimized unit weights but does not adjust for time trends. SDiD uses **both** unit weights (like SC) and time weights (novel) to achieve a "best of both worlds" estimator.

The SDiD estimator solves:

$$(\hat{\tau}^{SDiD}, \hat{\mu}, \hat{\alpha}, \hat{\lambda}) = \arg\min_{\tau, \mu, \alpha, \lambda} \sum_{i} \sum_{t} (\hat{\omega}_i^{unit} \cdot \hat{\omega}_t^{time}) \cdot (Y_{it} - \mu - \alpha_i - \lambda_t - \tau D_{it})^2$$

where $\hat{\omega}_i^{unit}$ are unit weights (constructed similarly to SC weights) and $\hat{\omega}_t^{time}$ are time weights that upweight pre-treatment periods most similar to the post-treatment period. This combination makes SDiD robust to failures of parallel trends (via unit weights) and to poor pre-treatment fit (via time weights that focus on the most relevant pre-treatment periods).

In simulations, SDiD tends to have lower variance than SC (because it leverages the panel structure more efficiently) and lower bias than DiD (because it does not require strict parallel trends).

### Penalized Synthetic Control (Abadie and L'Hour, 2021)

Standard synthetic control imposes strict non-negativity and summing-to-one constraints, which may exclude useful donor units or produce sparse weight vectors. **Penalized synthetic control** relaxes these constraints by adding a penalty term that encourages sparsity while allowing more flexible weight structures:

$$w^* = \arg\min_{w} \| X_0 - X_1 w \|^2 + \lambda \| w \|_p$$

where $\lambda$ is a regularization parameter and $\| \cdot \|_p$ is a norm penalty ($p = 1$ for lasso-type sparsity, $p = 2$ for ridge-type shrinkage). The penalty helps in settings with many donor units where overfitting is a concern, and it can improve the method's performance when the donor pool is large relative to the pre-treatment periods.

### Matrix Completion Methods (Athey et al., 2021)

An alternative framework treats the causal inference problem as a **matrix completion** problem. Arrange the panel data as a matrix with units as rows and time periods as columns. The treated observations are "missing" in the sense that we observe $Y_{it}(1)$ but want $Y_{it}(0)$. Under the assumption that the matrix of untreated potential outcomes has low rank (i.e., outcomes are driven by a small number of latent factors), techniques from the matrix completion literature --- such as nuclear norm minimization --- can "fill in" the missing entries.

The matrix completion approach is particularly attractive when:

- The number of treated units is large relative to the donor pool
- Treatment effects vary across units and time in complex ways
- The researcher wants to avoid specifying a particular model for the counterfactual

This method nests both DiD (which assumes a rank-2 structure: unit effects plus time effects) and synthetic control (which constructs the counterfactual as a weighted average of rows) as special cases.

### Difference-in-Discontinuities

When treatment is assigned by a threshold rule that changes over time, the **difference-in-discontinuities** design combines RDD and DiD. For example, suppose Silph Co. distributes Shadow Surge to trainers with 5 or more gym badges, and this threshold is lowered to 3 badges in the post-period. By comparing the RDD estimate at the threshold before and after the policy change, researchers can difference out any time-invariant confounders at the cutoff.

This method is useful in settings where neither RDD alone (because the cutoff changes) nor DiD alone (because treatment assignment is not cleanly separated across groups) provides identification, but their combination does.

---

## Chapter Summary

This chapter covered the family of methods that exploit **panel data** --- repeated observations on the same units over time --- to identify causal effects. We began with the classic **2x2 difference-in-differences** design, which eliminates time-invariant confounders (via within-unit differencing) and common time trends (via cross-group differencing) to isolate treatment effects. The parallel trends assumption --- that treated and control units would have followed the same trajectory absent treatment --- is the key identifying assumption, and while it is fundamentally untestable, event study plots provide crucial diagnostic evidence.

We then examined **two-way fixed effects** regression as the natural panel data generalization of DiD. While TWFE is equivalent to DiD in the simple 2x2 case, it produces biased estimates when treatment is **staggered** across units and treatment effects are heterogeneous. The Goodman-Bacon decomposition reveals why: TWFE implicitly uses already-treated units as controls, generating contaminated comparisons. The modern DiD revolution --- **Callaway and Sant'Anna**, **Sun and Abraham**, **de Chaisemartin and D'Haultfouille**, **Borusyak, Jaravel, and Spiess** --- provides heterogeneity-robust estimators that use only clean comparisons.

For settings with a single treated unit and no obvious control, the **synthetic control method** constructs a data-driven counterfactual from a weighted combination of donor units. Inference proceeds via placebo tests. Extensions including **augmented synthetic control**, **synthetic difference-in-differences**, and **matrix completion** further enrich the toolkit.

These methods are the workhorses of modern policy evaluation, program evaluation, and empirical social science. Mastering them equips the researcher to extract causal knowledge from the rich panel data structures that arise naturally in observational settings.

---

## Professor Oak's Review Questions

1. **Explain in your own words** why the DiD estimator requires two differences rather than one. What specific type of bias does each difference eliminate? Illustrate with the Shadow Surge example.

2. **State the parallel trends assumption** formally. Why is it untestable? What is the best available diagnostic, and what are its limitations?

3. **In the 2x2 setting**, show algebraically that the DiD estimator from the table of means is identical to the OLS coefficient $\hat{\tau}$ on the interaction term $\text{Treat}_i \times \text{Post}_t$.

4. **Explain the Goodman-Bacon decomposition** intuitively. What are the three types of 2x2 comparisons, and why is the "already-treated as control" comparison problematic?

5. **Compare and contrast** the Callaway-Sant'Anna and Borusyak-Jaravel-Spiess estimators. How do they handle the staggered treatment problem differently, and under what conditions might one be preferred over the other?

6. **Describe the synthetic control method's** approach to inference. Why can't we simply compute standard errors as in a regression? What determines the smallest achievable $p$-value in a placebo test with $J$ donor units?

---

## Trainer Challenge Exercises

### Exercise 7.1: Compute a 2x2 DiD

The Kanto Pokemon League introduced a new battle format ("Double Battles") in Vermilion City in Season 3 but not in Pewter City. Average trainer participation rates (in battles per month) are shown below:

| | Season 2 (Pre) | Season 4 (Post) |
|---|---|---|
| Vermilion (Treated) | 12.4 | 18.7 |
| Pewter (Control) | 9.8 | 13.2 |

**(a)** Compute the DiD estimate of the effect of Double Battles on participation.

**(b)** Write out the corresponding regression equation and state the value of each coefficient ($\alpha, \beta, \gamma, \tau$).

**(c)** What is the counterfactual participation rate for Vermilion in Season 4 under the parallel trends assumption?

**(d)** Blue claims the effect is $18.7 - 13.2 = 5.5$. Explain his mistake.

### Exercise 7.2: Event Study Interpretation

A researcher estimates an event study for the effect of Shadow Surge on trainer win rates across Kanto cities. The estimated coefficients (with 95% confidence intervals) at each event time relative to treatment ($k = -1$ omitted) are:

| Event Time $k$ | $\hat{\tau}_k$ | 95% CI |
|---|---|---|
| $-5$ | $-0.02$ | $[-0.06, 0.02]$ |
| $-4$ | $0.01$ | $[-0.03, 0.05]$ |
| $-3$ | $-0.01$ | $[-0.05, 0.03]$ |
| $-2$ | $0.03$ | $[-0.01, 0.07]$ |
| $-1$ | (omitted) | --- |
| $0$ | $0.08$ | $[0.04, 0.12]$ |
| $1$ | $0.10$ | $[0.06, 0.14]$ |
| $2$ | $0.11$ | $[0.07, 0.15]$ |
| $3$ | $0.09$ | $[0.05, 0.13]$ |
| $4$ | $0.10$ | $[0.06, 0.14]$ |

**(a)** Sketch the event study coefficient plot with confidence intervals.

**(b)** Do the pre-treatment coefficients support the parallel trends assumption? Explain.

**(c)** Describe the dynamic treatment effect pattern. Is the effect immediate or gradual? Does it persist, grow, or fade?

**(d)** A skeptic notes that $\hat{\tau}_{-2} = 0.03$ is the largest pre-treatment coefficient and worries about anticipation effects. How would you respond?

### Exercise 7.3: Identifying TWFE Bias

Consider a staggered DiD setting with three treatment cohorts (treated in periods 4, 8, and 12) and one never-treated group. The true treatment effect is constant at $\tau = 5$ for all groups in all post-treatment periods (homogeneous effects). A researcher runs TWFE and obtains $\hat{\tau}^{TWFE} = 5.0$.

**(a)** Is the TWFE estimate biased in this case? Explain why or why not.

**(b)** Now suppose the true effect grows over time: $\tau_k = 2 + 0.5k$ where $k$ is the number of periods since treatment. The researcher again runs TWFE and obtains $\hat{\tau}^{TWFE} = 3.8$, while the true average ATT across all treated unit-periods is $5.2$. Explain the source and direction of the bias.

**(c)** The researcher runs a Goodman-Bacon decomposition and finds that 35% of the TWFE weight comes from comparisons where already-treated units serve as controls. What does this tell you?

**(d)** Recommend a specific modern estimator and explain how it would fix the problem.

### Exercise 7.4: Construct a Synthetic Control

Team Rocket briefly occupied Celadon City's Game Corner in Period 10, causing economic disruption. You observe economic activity indices for five cities over 16 periods (treatment at period 10 for Celadon only):

**Pre-treatment averages (Periods 1--9):**

| City | Econ. Index | Population | Trainer Count |
|---|---|---|---|
| Celadon (Treated) | 92.0 | 130 | 2,100 |
| Cerulean | 78.0 | 95 | 1,500 |
| Vermilion | 85.0 | 110 | 1,800 |
| Fuchsia | 72.0 | 80 | 1,200 |
| Lavender | 65.0 | 60 | 900 |

**(a)** Explain intuitively why no single control city is a good match for Celadon. Which city or cities seem closest?

**(b)** Suppose the optimal synthetic control weights are: Vermilion (0.55), Cerulean (0.30), Fuchsia (0.15), Lavender (0.00). Compute the synthetic Celadon's pre-treatment average economic index. How does it compare to Celadon's actual value?

**(c)** In Period 12, Celadon's economic index is 83.0. The synthetic control's predicted value is 93.5. What is the estimated treatment effect of the Team Rocket occupation in Period 12?

**(d)** You run placebo tests by applying synthetic control to each donor city. The post/pre RMSPE ratios are: Celadon (15.2), Vermilion (2.1), Cerulean (3.5), Fuchsia (1.8), Lavender (1.2). What can you conclude about the statistical significance of the effect?

---

## Further Reading

- **Angrist, J. D. and Pischke, J.-S.** (2009). *Mostly Harmless Econometrics.* Princeton University Press. Chapters 5 and 8 provide an accessible introduction to DiD and panel methods.

- **Goodman-Bacon, A.** (2021). "Difference-in-Differences with Variation in Treatment Timing." *Econometrica*, 89(5), 2261--2290. The foundational decomposition paper that revealed the TWFE bias.

- **Callaway, B. and Sant'Anna, P. H. C.** (2021). "Difference-in-Differences with Multiple Time Periods." *Journal of Econometrics*, 225(2), 200--230. The leading heterogeneity-robust DiD estimator.

- **Sun, L. and Abraham, S.** (2021). "Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects." *Journal of Econometrics*, 225(2), 175--199. The interaction-weighted estimator for clean event studies.

- **de Chaisemartin, C. and D'Haultfouille, X.** (2020). "Two-Way Fixed Effects Estimators with Heterogeneous Treatment Effects." *American Economic Review*, 110(9), 2964--2996. Negative weights and the instantaneous treatment effect.

- **Borusyak, K., Jaravel, X., and Spiess, J.** (2024). "Revisiting Event-Study Designs: Robust and Efficient Estimation." *Review of Economic Studies*, 91(6), 3253--3285. The imputation estimator.

- **Abadie, A., Diamond, A., and Hainmueller, J.** (2010). "Synthetic Control Methods for Comparative Case Studies." *Journal of the American Statistical Association*, 105(490), 493--505. The foundational synthetic control paper.

- **Abadie, A., Diamond, A., and Hainmueller, J.** (2015). "Comparative Politics and the Synthetic Control Method." *American Journal of Political Science*, 59(2), 495--510. Application to political science.

- **Abadie, A.** (2021). "Using Synthetic Controls: Feasibility, Data Requirements, and Methodological Aspects." *Journal of Economic Literature*, 59(2), 391--425. Comprehensive methodological review.

- **Arkhangelsky, D., Athey, S., Hirshberg, D. A., Imbens, G. W., and Wager, S.** (2021). "Synthetic Difference-in-Differences." *American Economic Review*, 111(12), 4088--4118. The SDiD estimator combining SC and DiD.

- **Ben-Michael, E., Feller, A., and Rothstein, J.** (2021). "The Augmented Synthetic Control Method." *Journal of the American Statistical Association*, 116(536), 1789--1803. Bias correction for SC.

- **Roth, J., Sant'Anna, P. H. C., Bilinski, A., and Poe, J.** (2023). "What's Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature." *Journal of Econometrics*, 235(2), 2218--2244. An excellent survey of the modern DiD revolution.

- **Rambachan, A. and Roth, J.** (2023). "A More Credible Approach to Parallel Trends." *Review of Economic Studies*, 90(5), 2555--2591. Sensitivity analysis for violations of parallel trends.

---

## Badge Earned: Marsh Badge

*You have defeated Sabrina, the Psychic-type Gym Leader of Saffron City, and earned the Marsh Badge. You have mastered the art of differencing --- across time, across groups, and across synthetic counterfactuals. You understand why naive two-way fixed effects can deceive, and you know how to deploy the modern toolkit of heterogeneity-robust estimators. You can construct synthetic controls from weighted combinations of donor units and conduct inference through placebo tests. The Marsh Badge certifies your command of panel data methods for causal inference.*

*Badges earned: Boulder, Cascade, Thunder, Rainbow, Soul, Volcano, Marsh (7/8)*

---

> **Next Chapter Preview:** *Victory Road leads to the Indigo Plateau, where the Elite Four await. Each champion guards a frontier of causal inference: mediation analysis reveals the mechanisms through which causes operate; heterogeneous treatment effects uncover for whom treatments work best; sensitivity analysis probes the robustness of our conclusions to hidden bias; and interference --- the bane of SUTVA --- forces us to confront a world where one unit's treatment affects another's outcome. The path is steep, but the summit offers a commanding view of the entire causal landscape...*
