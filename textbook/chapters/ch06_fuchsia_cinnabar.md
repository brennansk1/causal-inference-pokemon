# Chapter 6: Fuchsia City & Cinnabar Island — Instrumental Variables & Regression Discontinuity

> *"Sometimes the path forward is not straight. The Safari Zone lottery ticket in your pocket and the happiness meter on your Pokedex — these indirect tools are your keys to causal truth."*
> — Professor Oak

---

Your journey through Kanto has taken you from the clean experiments of Pewter City to the observational thickets of Celadon City. You have learned to draw DAGs, match on observables, weight by propensity scores, and build doubly robust estimators. But every method you have used so far shares a common assumption: that you can measure and adjust for *all* the confounders that stand between you and a causal estimate.

What happens when you cannot?

This chapter takes you to two new destinations that answer that question. In **Fuchsia City**, the Safari Zone runs a lottery that creates a natural experiment — an *instrumental variable* that lets you estimate causal effects even when critical confounders are unobserved. Then on **Cinnabar Island**, the happiness evolution threshold at 220 creates a sharp discontinuity — a *regression discontinuity design* that exploits the arbitrary cutoff to identify causal effects for Pokemon near the boundary.

These two methods — IV and RDD — are the workhorses of modern applied causal inference. They are what allow researchers to make credible causal claims from observational data when selection on observables fails. Together, they earn you two badges: the **Soul Badge** from Fuchsia and the **Volcano Badge** from Cinnabar.

Let us begin.

---

# Part I: Instrumental Variables (Fuchsia City)

*You arrive in Fuchsia City, home of the Safari Zone. The warden tells you that admission is expensive — 500 Pokedollars per visit — but each week, a lottery awards free passes to randomly selected trainers. Some winners go, some do not. Some losers pay their own way in. The question on every trainer's mind: does Safari Zone training actually improve battle performance?*

---

## 6.1 The Instrumental Variables Idea

### The Problem: Unobserved Confounding

Suppose you want to estimate the causal effect of attending Safari Zone training ($D_i$) on battle performance ($Y_i$, measured as win rate in the next 20 battles). You have observational data on hundreds of trainers in Fuchsia City. Some attended the Safari Zone; others did not. The naive comparison of mean outcomes is:

$$\bar{Y}_{\text{attendees}} - \bar{Y}_{\text{non-attendees}} = 0.68 - 0.45 = 0.23$$

A 23-percentage-point advantage! But should you believe this is causal?

Consider the following DAG:

```
    Patience (U)
      /       \
     v         v
Safari Zone → Battle
Attendance    Performance
   (D)          (Y)
```

**Patience** — the willingness to grind, to wait in tall grass, to carefully plan strategy — is an *unobserved confounder*. Patient trainers are both more likely to attend the Safari Zone (they enjoy the slow-paced catching game) and more likely to win battles (patience helps in competitive play). Patience is not recorded in any dataset. You cannot measure it, match on it, or include it in a regression.

This is the fundamental problem. No matter how sophisticated your regression model, no matter how carefully you construct propensity scores, you cannot adjust for what you cannot see. The backdoor path $D \leftarrow U \rightarrow Y$ remains open, and your estimate is biased.

Let us formalize this. Write the outcome model as:

$$Y_i = \alpha + \tau D_i + \gamma U_i + \epsilon_i$$

where $U_i$ is patience (unobserved). OLS of $Y$ on $D$ omits $U$. By the omitted variable bias formula:

$$\hat{\tau}_{\text{OLS}} \xrightarrow{p} \tau + \gamma \cdot \frac{\text{Cov}(D, U)}{\text{Var}(D)}$$

Since $\gamma > 0$ (patience helps win battles) and $\text{Cov}(D, U) > 0$ (patient people attend more), the bias term $\gamma \cdot \frac{\text{Cov}(D, U)}{\text{Var}(D)} > 0$. OLS *overstates* the benefit of Safari Zone training. The 23-percentage-point gap is inflated by selection bias.

Previous chapters taught you to handle confounders by conditioning on them. In Chapter 4, you learned to match patient trainers to patient non-trainers. In Chapter 5, you learned to weight by the propensity score. But all those methods require that patience is *measured*. What if your dataset contains only attendance, win rate, trainer level, and badges — but no measure of patience? Then matching on observables misses the key confounder, the propensity score omits a critical variable, and doubly robust estimation is only as good as its component models, both of which are misspecified.

The methods of Chapters 3-5 are sometimes called **selection on observables** strategies. They work beautifully when all confounders are measured, but they are powerless against unobserved confounding. This is not a minor limitation — in practice, the most important confounders are often the ones you cannot measure: motivation, ability, risk tolerance, or, in our case, patience.

You need a fundamentally different strategy. You need an **instrument**.

### The Instrument: The Safari Zone Lottery

Every week, the Fuchsia City Warden draws names from the trainer registry for free Safari Zone passes. The lottery is random — it does not depend on patience, skill, or any other characteristic of the trainer. Let $Z_i$ denote whether trainer $i$ won the lottery:

$$Z_i = \begin{cases} 1 & \text{if trainer } i \text{ won a free pass} \\ 0 & \text{otherwise} \end{cases}$$

Now consider the updated DAG:

```
                Patience (U)
                  /       \
                 v         v
  Lottery → Safari Zone → Battle
   (Z)     Attendance    Performance
              (D)          (Y)
```

The lottery $Z$ affects attendance $D$ (winners are more likely to go), but the lottery has no *direct* effect on battle outcomes. Winning a lottery ticket does not make you a better battler. The only way the lottery could affect your win rate is *through* its effect on whether you actually attend the Safari Zone.

This is the instrumental variables idea: find a variable that shifts the treatment but has no other pathway to the outcome.

### The Three IV Assumptions

For the lottery $Z$ to serve as a valid instrument for the effect of attendance $D$ on performance $Y$, three conditions must hold:

> **Definition 6.1 (Instrumental Variable Assumptions).** A variable $Z$ is a valid instrument for the causal effect of treatment $D$ on outcome $Y$ if:
>
> 1. **Relevance (First Stage):** $\text{Cov}(Z, D) \neq 0$. The instrument must actually affect the treatment. The lottery must change attendance behavior.
>
> 2. **Independence (Exogeneity):** $Z \perp\!\!\!\perp (Y(1), Y(0), D(1), D(0))$. The instrument is independent of potential outcomes and potential treatment assignments. The lottery is as-if randomly assigned.
>
> 3. **Exclusion Restriction:** $Z$ affects $Y$ *only through* $D$. There is no direct arrow from $Z$ to $Y$. Winning the lottery does not improve your battle performance except by getting you into the Safari Zone.

Let us examine each assumption in detail.

**Relevance** is the most straightforward. If the lottery does not change anyone's behavior — if the same people would attend regardless of whether they win — then the instrument is useless. We need the lottery to actually move the needle on attendance. This is *testable*: we can regress $D$ on $Z$ and check whether the coefficient is statistically and economically significant.

**Independence** (also called exogeneity or the "as-if random" condition) requires that the instrument is not correlated with any confounders — observed or unobserved. Because the lottery is literally random, this is highly plausible. Random assignment of $Z$ guarantees that winners and losers are comparable in expectation on all observed and unobserved characteristics, including patience. This assumption would be violated if, for example, patient trainers were more likely to enter the lottery — but we assume all registered trainers are automatically entered.

Note the key difference from the "selection on observables" assumption. In Chapters 4-5, you needed $D \perp\!\!\!\perp (Y(1), Y(0)) \mid X$ — independence of treatment and potential outcomes conditional on observables. Here, you need $Z \perp\!\!\!\perp (Y(1), Y(0), D(1), D(0))$ — independence of the *instrument* and potential outcomes/treatments, but with *no conditioning required* (because the instrument itself is randomly assigned). You have traded the problem of conditioning on the right variables for the problem of finding a valid instrument.

**Exclusion restriction** is the most subtle and the most consequential. It requires that the *only* channel through which the lottery affects battle performance is through Safari Zone attendance. This would be violated if, say, winning the lottery made trainers feel lucky and therefore more confident in battle — a psychological boost unrelated to Safari Zone training. Or if lottery winners celebrated by buying better healing items with the money they saved on admission. These are "direct effects" of $Z$ on $Y$ that bypass $D$.

> **Professor Oak Explains: The Exclusion Restriction**
>
> "The exclusion restriction is what makes IV powerful — and what makes it fragile. It says the instrument is like a key that only fits one lock. The lottery key opens the Safari Zone door, and that door is the *only* way it could possibly affect your battle record. If the key also opens a second door — say, a door to a free Rare Candy shop — then the instrument is invalid.
>
> "You cannot test the exclusion restriction with data. It is a *substantive assumption* that must be defended on theoretical and institutional grounds. This is why the choice of instrument is as much an art as a science."

### The Wald Estimator

Given a valid instrument, how do we actually compute the causal effect? The key insight is to decompose the problem into two observable relationships.

**The reduced form** is the effect of the instrument on the outcome:

$$\text{Reduced Form} = E[Y_i | Z_i = 1] - E[Y_i | Z_i = 0]$$

This tells us: how much better do lottery winners perform, on average, compared to losers? This is the *intent-to-treat* (ITT) effect — the effect of being *assigned* to the instrument, regardless of whether you actually attended the Safari Zone.

**The first stage** is the effect of the instrument on the treatment:

$$\text{First Stage} = E[D_i | Z_i = 1] - E[D_i | Z_i = 0]$$

This tells us: how much more likely are lottery winners to actually attend, compared to losers? This is the *compliance rate* — the fraction of people whose behavior is changed by the instrument.

The **Wald estimator** is their ratio:

> **Definition 6.2 (Wald Estimator).** The instrumental variables estimate of the causal effect of $D$ on $Y$ using instrument $Z$ is:
>
> $$\hat{\tau}_{IV} = \frac{E[Y_i | Z_i = 1] - E[Y_i | Z_i = 0]}{E[D_i | Z_i = 1] - E[D_i | Z_i = 0]} = \frac{\text{Reduced Form (ITT)}}{\text{First Stage (Compliance)}}$$

The intuition is beautiful. The reduced form captures the total effect of the lottery on outcomes — but this effect is "diluted" because not everyone who wins the lottery actually attends, and some who lose attend anyway. The first stage measures exactly how much dilution there is. Dividing by the first stage rescales the ITT effect to reflect the causal effect *per unit of treatment actually induced by the instrument*.

Think of it this way: if the lottery increases attendance by 30 percentage points and improves outcomes by 6 percentage points, then each unit of attendance induced by the lottery is worth $0.06 / 0.30 = 0.20$ — a 20-percentage-point improvement in win rate.

The Wald estimator can also be derived algebraically from the IV moment condition. Under the three assumptions, we have:

$$\text{Cov}(Z, \epsilon) = 0 \quad \text{(exogeneity + exclusion)}$$

Starting from $Y_i = \beta_0 + \tau D_i + \epsilon_i$ and using the moment condition:

$$\hat{\tau}_{IV} = \frac{\text{Cov}(Z, Y)}{\text{Cov}(Z, D)} = \frac{\frac{1}{n}\sum_i (Z_i - \bar{Z})(Y_i - \bar{Y})}{\frac{1}{n}\sum_i (Z_i - \bar{Z})(D_i - \bar{D})}$$

When $Z$ is binary, this simplifies exactly to the Wald ratio above. This moment condition perspective generalizes naturally to the case of continuous instruments and multiple regressors, which is the foundation of 2SLS.

### Worked Example: Safari Zone Lottery

Suppose we observe the following data from the `safari_zone_lottery.csv` dataset, summarized by lottery status:

| | $Z = 1$ (Winners) | $Z = 0$ (Losers) |
|---|---|---|
| $n$ | 200 | 300 |
| Mean attendance ($\bar{D}$) | 0.72 | 0.30 |
| Mean win rate ($\bar{Y}$) | 0.58 | 0.50 |

**First stage:**

$$E[D | Z = 1] - E[D | Z = 0] = 0.72 - 0.30 = 0.42$$

Lottery winners are 42 percentage points more likely to attend the Safari Zone. The instrument is strong.

**Reduced form (ITT):**

$$E[Y | Z = 1] - E[Y | Z = 0] = 0.58 - 0.50 = 0.08$$

Lottery winners have a win rate that is 8 percentage points higher. But this is the ITT — the effect of the lottery, not the effect of attendance.

**Wald estimator:**

$$\hat{\tau}_{IV} = \frac{0.08}{0.42} = 0.190$$

The IV estimate of the causal effect of Safari Zone attendance on battle win rate is **19.0 percentage points**. Compare this to the naive OLS estimate of 23 percentage points. The difference — about 4 percentage points — is the upward bias from unobserved patience confounding.

Let us trace through the logic once more to make sure the intuition is fully clear. The reduced form of 0.08 tells us that lottery winners have better outcomes — but not *dramatically* better, because only 42% of winners actually changed their behavior due to the lottery. The rest are always-takers (who would have attended anyway) and never-takers (who ignored the free pass). The 0.08 is a "watered-down" version of the true causal effect, watered down by the fact that most people were not affected by the instrument. Dividing by 0.42 "concentrates" the effect back onto the people whose behavior actually changed — the compliers — giving us the 19.0-percentage-point effect for this group.

> **Blue's Mistake: "Why Not Just Compare Attendees?"**
>
> Blue looks at the data and scoffs. "Why bother with this lottery nonsense? Just compare people who went to the Safari Zone with people who didn't. Attendees win 23% more — that's the answer."
>
> Blue's mistake is selection bias from unobserved confounding. Patient trainers self-select into the Safari Zone *and* independently perform better in battles. By comparing attendees to non-attendees, Blue is conflating the causal effect of training with the pre-existing advantage of patient people. The IV estimate of 19 percentage points strips away this selection bias by using only the variation in attendance that was *induced by the lottery* — variation that is, by construction, uncorrelated with patience.

---

## 6.2 Two-Stage Least Squares (2SLS)

The Wald estimator is elegant but limited: it handles only a single binary instrument and a single binary treatment, with no covariates. In practice, we often want to include control variables for efficiency, handle continuous instruments or treatments, or use multiple instruments simultaneously. **Two-Stage Least Squares (2SLS)** is the generalization that handles all of these cases.

### The Two Stages

**First stage:** Regress the endogenous treatment $D$ on the instrument $Z$ and any exogenous covariates $X$:

$$D_i = \pi_0 + \pi_1 Z_i + X_i'\pi_2 + v_i \tag{First Stage}$$

Save the predicted values $\hat{D}_i = \hat{\pi}_0 + \hat{\pi}_1 Z_i + X_i'\hat{\pi}_2$. These fitted values represent the part of treatment variation that is *explained by the instrument* (and covariates), stripped of the endogenous component driven by unobserved confounders.

**Second stage:** Regress the outcome $Y$ on the predicted treatment $\hat{D}$ and the same covariates $X$:

$$Y_i = \beta_0 + \beta_1 \hat{D}_i + X_i'\beta_2 + \epsilon_i \tag{Second Stage}$$

The coefficient $\hat{\beta}_1$ is the 2SLS estimate of the causal effect.

### Why Does This Work?

The key insight is that $\hat{D}_i$ contains only the variation in $D$ that comes from the instrument $Z$ — the exogenous, "as-if random" variation. All the endogenous variation — the part of attendance driven by patience and other unobserved confounders — is absorbed into the first-stage residual $v_i$ and discarded. By regressing $Y$ on $\hat{D}$ instead of $D$, we isolate the causal effect.

Formally, the OLS estimator using $D$ directly is biased because $\text{Cov}(D, \epsilon) \neq 0$ — treatment is correlated with the error term (which contains the unobserved confounder). But $\hat{D}$ is a function only of $Z$ and $X$, both of which are exogenous. So $\text{Cov}(\hat{D}, \epsilon) = 0$, and OLS on the second stage is consistent.

To see this more concretely, decompose $D$ into its fitted value and residual: $D_i = \hat{D}_i + \hat{v}_i$. The fitted component $\hat{D}_i$ is the "good" variation — the part predicted by the exogenous instrument. The residual $\hat{v}_i$ is the "bad" variation — the part driven by unobserved confounders like patience. By substituting $\hat{D}$ for $D$ in the second stage, we use only the good variation and throw away the bad. This is sometimes described as IV "purifying" the treatment variable by stripping out the endogenous component.

An equivalent perspective comes from the **control function** approach. Instead of replacing $D$ with $\hat{D}$, you can include the first-stage residual $\hat{v}_i$ as an additional regressor in the outcome equation:

$$Y_i = \beta_0 + \beta_1 D_i + X_i'\beta_2 + \rho \hat{v}_i + \eta_i$$

The coefficient $\beta_1$ in this specification is numerically identical to the 2SLS estimate. Including $\hat{v}_i$ "controls for" the endogenous component of $D$, allowing $\beta_1$ to capture only the exogenous variation. The control function approach also provides a direct test of endogeneity: if $\hat{\rho} = 0$, then $D$ is exogenous and OLS is consistent. This is the **Hausman test** (or Durbin-Wu-Hausman test) for endogeneity.

### Including Covariates

Even when the instrument is randomly assigned, including covariates $X$ can be valuable for two reasons:

1. **Efficiency:** If covariates explain substantial variation in $Y$, including them reduces the residual variance and tightens confidence intervals.
2. **Conditional IV:** Sometimes the instrument is only valid *conditional* on covariates. For example, if the lottery probability varies by trainer level (higher-level trainers get more entries), then the lottery is only as-if random within level groups. Including trainer level as a covariate restores validity.

A critical rule: **any covariate included in the second stage must also be included in the first stage.** If you control for trainer level in the outcome equation, you must also control for it in the first-stage regression. Omitting it from the first stage would contaminate $\hat{D}$ with level-related variation that is not instrumented.

### Overidentification: Multiple Instruments

Sometimes you have more instruments than endogenous variables. Suppose the Safari Zone runs *two* lotteries — a weekly drawing ($Z_1$) and a monthly grand prize ($Z_2$). Both are valid instruments for attendance. With two instruments and one endogenous variable, the model is **overidentified**.

The first stage becomes:

$$D_i = \pi_0 + \pi_1 Z_{1i} + \pi_2 Z_{2i} + X_i'\pi_3 + v_i$$

Overidentification brings two advantages:

1. **Efficiency:** More instruments generally yield more precise estimates (tighter standard errors) because they capture more exogenous variation in $D$.
2. **Testability:** With multiple instruments, you can partially test the exclusion restriction using the **Sargan-Hansen J test**. The null hypothesis is that all instruments are valid. Rejection suggests at least one instrument violates the exclusion restriction. However, the test has limited power and cannot identify *which* instrument is invalid.

> **Professor Oak Explains: The J Test's Limitations**
>
> "The Sargan-Hansen J test is useful but imperfect. It tests whether all your instruments agree on the causal effect. If they do, it fails to reject — but this does not prove validity. All instruments could be invalid in the same way, yielding the same biased estimate. The J test catches disagreement, not invalidity per se. It is a necessary condition, not a sufficient one."

### Standard Errors: A Critical Warning

A common pitfall: if you manually run OLS in the first stage, save $\hat{D}$, and then run OLS in the second stage, the coefficient $\hat{\beta}_1$ will be correct, but the **standard errors will be wrong**. The naive second-stage OLS standard errors fail to account for the fact that $\hat{D}$ is itself an estimate (with sampling uncertainty from the first stage). Proper 2SLS standard errors are larger than the naive ones — they incorporate the estimation error from both stages.

Always use a dedicated 2SLS procedure (such as `linearmodels.IV2SLS` in Python or `ivreg` in R) that computes correct standard errors automatically.

### Worked Example: Full 2SLS with Safari Zone Data

Using the `safari_zone_lottery.csv` dataset with 500 trainers, we include trainer level and number of badges as covariates:

**First stage:**

$$D_i = -0.15 + 0.43 \cdot Z_i + 0.02 \cdot \text{Level}_i + 0.05 \cdot \text{Badges}_i + v_i$$

| Variable | Coefficient | Std. Error | $t$-statistic | $p$-value |
|---|---|---|---|---|
| $Z$ (Lottery) | 0.430 | 0.038 | 11.32 | < 0.001 |
| Level | 0.021 | 0.005 | 4.20 | < 0.001 |
| Badges | 0.048 | 0.019 | 2.53 | 0.012 |
| Constant | $-0.152$ | 0.071 | $-2.14$ | 0.033 |

The first-stage F-statistic on $Z$ is $11.32^2 = 128.1$, well above the critical threshold of 10 (more on this shortly).

**Second stage:**

$$Y_i = 0.22 + 0.191 \cdot \hat{D}_i + 0.008 \cdot \text{Level}_i + 0.031 \cdot \text{Badges}_i + \epsilon_i$$

| Variable | Coefficient | 2SLS Std. Error | $t$-statistic | $p$-value |
|---|---|---|---|---|
| $\hat{D}$ (Safari attendance) | 0.191 | 0.049 | 3.90 | < 0.001 |
| Level | 0.008 | 0.004 | 2.00 | 0.046 |
| Badges | 0.031 | 0.016 | 1.94 | 0.053 |
| Constant | 0.220 | 0.062 | 3.55 | < 0.001 |

The 2SLS estimate is $\hat{\tau}_{2SLS} = 0.191$ — virtually identical to the Wald estimate of 0.190, as expected when covariates are included in a well-specified model. Safari Zone attendance causes a 19.1-percentage-point increase in win rate, after removing the bias from unobserved patience.

---

## 6.3 Instrument Validity and Diagnostics

The power of IV comes with a price: the estimates are only as good as the instrument. This section covers the diagnostic toolkit every researcher must apply before trusting an IV estimate.

### Weak Instruments

An instrument is **weak** if it has only a small effect on the treatment — that is, if the first-stage relationship between $Z$ and $D$ is statistically significant but practically small. Weak instruments cause two severe problems:

1. **Bias:** The 2SLS estimator is biased toward the OLS estimate in finite samples. With a weak instrument, 2SLS can be nearly as biased as naive OLS — defeating the entire purpose of IV.
2. **Size distortion:** Standard confidence intervals and hypothesis tests based on normal approximations become unreliable. Confidence intervals may be far too narrow, leading to false rejections.

> **Definition 6.3 (Stock and Yogo, 2005, Rule of Thumb).** An instrument is considered sufficiently strong if the first-stage F-statistic exceeds 10. For a single endogenous regressor with a single instrument, this corresponds to a first-stage $t$-statistic exceeding approximately 3.16.

In our Safari Zone example, the first-stage F-statistic was 128.1 — well above 10. The lottery is a strong instrument.

But what if you were using a different instrument — say, distance from a trainer's home to the Safari Zone? If trainers who live closer are only slightly more likely to attend, the first-stage F might be, say, 4.2. With such a weak instrument, the 2SLS estimate would be unreliable.

To understand the finite-sample bias intuitively, recall that the Wald estimator is a *ratio*: reduced form divided by first stage. When the first stage is near zero (a weak instrument), you are dividing by a small and noisy number. Small estimation errors in the denominator get amplified dramatically, pushing the ratio toward the OLS estimate. In the extreme case of a completely irrelevant instrument (first stage exactly zero), the IV estimator is undefined — you would be dividing by zero.

The Stock and Yogo (2005) framework provides precise critical values for the first-stage F-statistic based on two criteria: (1) the maximum relative bias of 2SLS relative to OLS that the researcher is willing to tolerate, and (2) the maximum size distortion of the Wald test that is acceptable. The F > 10 rule of thumb corresponds roughly to ensuring that the 2SLS bias is no more than 10% of the OLS bias. For stricter standards (e.g., 5% bias), higher F-statistics are required.

Lee, McCrary, Moreira, and Porter (2022) have recently proposed a new framework for weak IV inference that conditions on the first-stage F-statistic directly, providing valid confidence intervals for any value of the first stage — not just values above 10. Their `tF` procedure is an attractive alternative when the researcher is concerned about weak instruments but wants to use the 2SLS framework.

**Anderson-Rubin confidence sets** provide a solution for weak instruments. Unlike standard Wald-based confidence intervals, the Anderson-Rubin (AR) test is valid regardless of instrument strength. It inverts a test of the reduced-form hypothesis to construct a confidence set for the causal parameter. When the instrument is strong, the AR confidence set closely matches the standard 2SLS interval. When the instrument is weak, the AR set may be much wider (or even unbounded), honestly reflecting the true uncertainty.

### The Exclusion Restriction: Untestable and Unforgiving

The exclusion restriction — that $Z$ affects $Y$ only through $D$ — is the Achilles' heel of instrumental variables. It cannot be tested with data. No statistical procedure can determine whether the lottery has a direct effect on battle performance that bypasses the Safari Zone.

Consider a potential violation: **What if lottery winners feel lucky, and this psychological boost makes them fight more boldly and win more battles — independent of whether they actually attend the Safari Zone?**

If this "luck effect" exists, the reduced form captures both the indirect effect (through attendance) and the direct effect (through confidence). The Wald estimator becomes:

$$\frac{E[Y | Z=1] - E[Y | Z=0]}{E[D | Z=1] - E[D | Z=0]} = \tau + \frac{\text{direct effect of } Z \text{ on } Y}{\text{first stage}}$$

The IV estimate is biased upward by the ratio of the direct effect to the first stage. If the direct "luck" effect is small relative to the first stage, the bias is small. But you cannot know this from the data.

> **Blue's Mistake: "My Instrument Is Fine Because It's Significant"**
>
> Blue claims he has found a great instrument: whether a trainer owns a Fishing Rod. "Fishing Rod owners are more likely to visit the Safari Zone — the first stage is super strong! And it's clearly relevant. So IV is valid."
>
> But does owning a Fishing Rod satisfy the exclusion restriction? Trainers who own Fishing Rods are likely outdoorsy, patient, and experienced — all traits that directly affect battle performance. The Fishing Rod is correlated with unobserved confounders, so the "independence" assumption fails. A strong first stage does not make an instrument valid. The exclusion restriction is the binding constraint, and no amount of statistical significance can substitute for a convincing argument that the instrument only affects the outcome through the treatment.

### Monotonicity and the Absence of Defiers

A fourth assumption, not always listed among the "big three," is critical for the LATE interpretation (Section 6.4):

> **Definition 6.4 (Monotonicity).** For all individuals $i$:
>
> $$D_i(1) \geq D_i(0)$$
>
> That is, winning the lottery weakly increases attendance for every trainer. No one who would attend without winning the lottery would refuse to attend *because* they won.

Monotonicity rules out **defiers** — perverse individuals who do the opposite of what the instrument encourages. In the Safari Zone context, a defier would be someone who thinks, "I won a free pass? That's too mainstream. I refuse to go now." While such behavior is logically possible, it is behaviorally implausible in most settings, and monotonicity is usually considered a mild assumption.

### Partial Identification Under Weaker Assumptions

If you are unwilling to assume the exclusion restriction holds exactly, you can still obtain **bounds** on the causal effect. Nevo and Rosen (2012) show that if you know the *direction* of the exclusion restriction violation (e.g., the direct effect of $Z$ on $Y$ is positive), you can tighten the bounds substantially. Conley, Hansen, and Rossi (2012) propose a framework where the exclusion restriction holds "approximately" — the direct effect of $Z$ on $Y$ is small but not exactly zero — and derive confidence intervals that incorporate this uncertainty.

These partial identification approaches trade precision for honesty. They acknowledge that the exclusion restriction is an assumption, not a fact, and they show how sensitive the conclusions are to violations.

---

## 6.4 LATE and the Complier Taxonomy

The IV estimate does not recover the average treatment effect for the entire population. It recovers the effect for a very specific subgroup. Understanding which subgroup — and why — is essential for interpreting IV results correctly.

### Four Types of Trainers

When we have a binary instrument $Z$ (lottery win/loss) and a binary treatment $D$ (attend/not attend), each trainer has two potential treatment values: $D_i(1)$ (what they would do if they won the lottery) and $D_i(0)$ (what they would do if they lost). This creates a 2 $\times$ 2 classification:

> **Definition 6.5 (Compliance Types).** Based on potential treatments $D_i(1)$ and $D_i(0)$:
>
> | Type | $D_i(0)$ | $D_i(1)$ | Behavior |
> |---|---|---|---|
> | **Complier** | 0 | 1 | Attends *only if* wins lottery |
> | **Always-Taker** | 1 | 1 | Attends *regardless* of lottery |
> | **Never-Taker** | 0 | 0 | Never attends regardless |
> | **Defier** | 1 | 0 | Attends only if *loses* lottery |

Let us put faces to these types in Fuchsia City.

**Compliers** are trainers who would not pay the 500-Pokedollar admission on their own but will happily go if it is free. The lottery *changes their behavior*. These are the trainers for whom the instrument makes a difference.

**Always-Takers** are wealthy or devoted trainers who attend the Safari Zone every week regardless. They buy their own ticket even if they lose the lottery. The lottery does not change their behavior — they attend either way.

**Never-Takers** are trainers who have no interest in the Safari Zone. Even a free pass does not entice them — maybe they find it boring, or they are too busy training at the Fuchsia Gym. The lottery does not change their behavior — they stay away either way.

**Defiers** would be trainers who attend when they lose but refuse to attend when they win. Under the monotonicity assumption, we rule out this group. (And indeed, it is hard to imagine why anyone would behave this way with a free Safari Zone pass.)

A crucial observation: we can never directly observe any individual's type. We observe $Z_i$ and $D_i$ for each trainer, but this only tells us:

- If $Z_i = 1$ and $D_i = 1$: the trainer is either a Complier or an Always-Taker.
- If $Z_i = 1$ and $D_i = 0$: the trainer is a Never-Taker.
- If $Z_i = 0$ and $D_i = 1$: the trainer is an Always-Taker.
- If $Z_i = 0$ and $D_i = 0$: the trainer is either a Complier or a Never-Taker.

We can identify Never-Takers (among winners) and Always-Takers (among losers) individually, but we can never point to a single person and say with certainty "this person is a Complier."

### The Local Average Treatment Effect (LATE)

The IV/Wald estimator recovers the average treatment effect *for Compliers only*:

> **Definition 6.6 (Local Average Treatment Effect).** Under the assumptions of relevance, independence, exclusion restriction, and monotonicity:
>
> $$\hat{\tau}_{IV} \xrightarrow{p} \text{LATE} = E[Y_i(1) - Y_i(0) \mid \text{Complier}]$$
>
> The IV estimate is the causal effect of treatment for the subpopulation whose treatment status is changed by the instrument.

This is the landmark result of Imbens and Angrist (1994). It tells us precisely what IV identifies and for whom.

### Why LATE $\neq$ ATE

The LATE is a *local* effect — local to the complier subpopulation. It need not equal the average treatment effect for the whole population, the effect for always-takers, or the effect for never-takers.

Consider why compliers might differ from the general population in the Safari Zone setting. Compliers are trainers on the margin: interested enough to attend if free but not willing to pay. These are likely mid-level trainers — not the most dedicated (who are always-takers) and not the least interested (who are never-takers). The effect of Safari Zone training on these marginal trainers may differ from its effect on devoted trainers who attend regardless.

If the treatment effect is *homogeneous* — the same for everyone — then LATE = ATE, and this distinction is moot. But with heterogeneous treatment effects, the distinction matters greatly. A LATE of 19 percentage points for compliers does not mean the ATE is 19 percentage points for the entire population.

This also means that **different instruments identify different LATEs**. Suppose a second instrument — a Pokedollar rebate coupon — also affects Safari Zone attendance. The compliers for the coupon (trainers who attend because of the rebate but would not otherwise) are a different subpopulation than the compliers for the lottery (trainers who attend because of the free pass). If the treatment effect is heterogeneous, these two instruments will produce different IV estimates — not because one is "wrong," but because they identify effects for different groups. This is not a bug; it is a feature of the LATE framework. But it does mean that comparing IV estimates across studies using different instruments requires caution.

Angrist and Fernandez-Val (2013) provide methods for extrapolating from the LATE to broader populations under additional assumptions about how the treatment effect varies with observable characteristics. Mogstad, Santos, and Torgovitsky (2018) develop a more general framework for using multiple instruments to learn about the distribution of treatment effects across compliance types.

> **Professor Oak Explains: When LATE Is What You Want**
>
> "LATE is often dismissed as a 'second-best' estimand — people want the ATE but settle for the LATE. But in many policy contexts, the LATE is exactly the right quantity. If the Fuchsia City Warden is considering making the Safari Zone free for everyone, the relevant question is: how much would *marginal* trainers benefit? These are precisely the compliers — the trainers whose behavior would be changed by the policy. Always-takers already attend, and never-takers will not attend even if it is free. The compliers are the policy-relevant population."

### Characterizing Compliers

Although we cannot identify individual compliers, we can describe their characteristics as a group. Abadie (2003) showed that you can estimate the distribution of observed covariates among compliers using a reweighting approach. For any covariate $X$:

$$E[X | \text{Complier}] = \frac{E[X \cdot D | Z=1] - E[X \cdot D | Z=0]}{E[D | Z=1] - E[D | Z=0]}$$

In our data, suppose we compute:

| Covariate | Population Mean | Complier Mean |
|---|---|---|
| Trainer Level | 38.2 | 33.7 |
| Badges | 5.1 | 4.4 |
| Party Size | 4.8 | 4.2 |

Compliers tend to be somewhat lower-level trainers with fewer badges and smaller parties — consistent with the "marginal trainer" interpretation.

### The ITT-LATE Connection

The relationship between the intent-to-treat effect and the LATE provides useful intuition and connects back to the experimental design ideas from Chapter 2:

$$\text{ITT} = \text{LATE} \times P(\text{Complier})$$

The ITT is the "diluted" version of the LATE — diluted by the fraction of the population that are compliers. In our example:

$$0.08 = 0.19 \times 0.42$$

The ITT of 8 percentage points equals the LATE of 19 percentage points times the compliance rate of 42%. This is why we divide the ITT by the first stage to recover the LATE: we are "undiluting" the effect.

---

# Part II: Regression Discontinuity (Cinnabar Island)

*You take the ferry from Fuchsia City to Cinnabar Island. The volcanic island is famous for its research lab, where scientists study Pokemon evolution. A particularly interesting phenomenon catches your eye: Pokemon with a happiness score of 220 or above evolve into a stronger form, while those below 220 remain unevolved. This sharp threshold creates a natural experiment waiting to be exploited.*

---

## 6.5 Sharp Regression Discontinuity Design

### The Setting

On Cinnabar Island, researchers have assembled the `happiness_evolution.csv` dataset tracking Pokemon and their trainers. Each Pokemon has a **happiness score** — a continuous measure from 0 to 255 based on time spent with the trainer, battles fought, items used, and other factors. The game mechanics dictate that when a Pokemon's happiness reaches 220, it evolves.

Let $X_i$ denote the happiness score (the **running variable** or **forcing variable**), $c = 220$ the cutoff, and $D_i$ the treatment (evolution):

$$D_i = \begin{cases} 1 & \text{if } X_i \geq 220 \\ 0 & \text{if } X_i < 220 \end{cases}$$

The outcome $Y_i$ is the Pokemon's battle performance after evolution (or non-evolution), measured as a standardized combat power index.

The question: does evolution *cause* improved battle performance? Or do Pokemon that are about to evolve already have high battle stats simply because their trainers have invested heavily in them?

This is another instance of selection bias. Pokemon with high happiness have dedicated trainers who invest in every aspect of their Pokemon's development — not just happiness, but also training, move selection, and strategic battle preparation. Simply comparing evolved to unevolved Pokemon confounds the effect of evolution itself with the effect of having a dedicated trainer. We need a design that isolates the causal effect of evolution from the selection effect of trainer quality.

### The Identification Idea

The RDD identification strategy is simple and elegant: **compare Pokemon just above the cutoff to Pokemon just below it.**

A Pokemon with a happiness score of 221 evolved. A Pokemon with a happiness score of 219 did not. But these two Pokemon are essentially identical in every other respect — their trainers invested almost the same amount of effort, they have nearly the same experience, and they differ by a mere 2 points on a 0-255 scale. Yet one evolved and the other did not.

The key assumption is that all factors other than treatment vary **smoothly** (continuously) at the cutoff. There is no reason to expect a sudden jump in trainer skill, Pokemon genetics, or any other determinant of battle performance at exactly 220. The only thing that jumps at 220 is evolution status.

> **Definition 6.7 (Sharp RDD Estimand).** The causal effect of treatment at the cutoff is:
>
> $$\tau_{RDD} = \lim_{x \downarrow c} E[Y_i | X_i = x] - \lim_{x \uparrow c} E[Y_i | X_i = x] = E[Y_i(1) - Y_i(0) | X_i = c]$$
>
> The RDD estimates the average treatment effect for units *at the cutoff* — those with $X_i = c$.

This is a *local* estimate, just like the LATE from IV. It applies to Pokemon right at the boundary of evolution. Pokemon with happiness scores of 100 or 250 are far from the cutoff, and the RDD tells us nothing about the effect of evolution for them.

The formal identification relies on a **continuity assumption**: the conditional expectation functions $E[Y(1) | X = x]$ and $E[Y(0) | X = x]$ are both continuous at $x = c$. This means that in the absence of treatment, there would be no jump in outcomes at the cutoff. The only reason we observe a jump in $E[Y | X = x]$ at $c$ is because treatment switches on at that point. Formally:

$$\tau_{RDD} = \lim_{x \downarrow c} E[Y | X = x] - \lim_{x \uparrow c} E[Y | X = x]$$

$$= \lim_{x \downarrow c} E[Y(1) | X = x] - \lim_{x \uparrow c} E[Y(0) | X = x]$$

$$= E[Y(1) | X = c] - E[Y(0) | X = c] \quad \text{(by continuity)}$$

$$= E[Y(1) - Y(0) | X = c]$$

This derivation, due to Hahn, Todd, and van der Klaauw (2001), shows that the RDD identifies the treatment effect at the cutoff under the continuity assumption alone — no functional form restrictions, no model for selection, no conditional independence.

### The Local Randomization Interpretation

Near the cutoff, treatment assignment is "as good as random." A Pokemon with a happiness score of 219 versus 221 is separated by such a tiny margin that the variation is essentially noise — the result of one extra pat on the head or one fewer potion used. This local randomization perspective makes the RDD especially credible: near the cutoff, it mimics a randomized experiment.

This interpretation requires that units cannot *precisely manipulate* the running variable to be just above or below the cutoff. If trainers could set their Pokemon's happiness to exactly 221 to guarantee evolution, the "as good as random" argument collapses. We will return to this concern in Section 6.7 on diagnostics.

### Estimation: Local Linear Regression

The most common approach to estimating the RDD effect is **local linear regression**: fit separate linear regressions on each side of the cutoff using only observations within a bandwidth $h$ of the cutoff.

For observations with $X_i \in [c - h, c)$ (below the cutoff):

$$Y_i = \alpha_l + \beta_l (X_i - c) + \epsilon_i^l$$

For observations with $X_i \in [c, c + h]$ (above the cutoff):

$$Y_i = \alpha_r + \beta_r (X_i - c) + \epsilon_i^r$$

The RDD estimate is the difference in intercepts:

$$\hat{\tau}_{RDD} = \hat{\alpha}_r - \hat{\alpha}_l$$

This estimates the jump in the conditional expectation function at the cutoff.

Why *local linear* and not global polynomial? Global polynomial regressions (fitting a single high-order polynomial across the entire range of $X$) are seductive but dangerous. Gelman and Imbens (2019) argue convincingly that high-order global polynomials are sensitive to observations far from the cutoff, can produce wild extrapolations, and generate confidence intervals with poor coverage. For example, fitting a fourth-degree polynomial to our happiness-performance data would allow observations with happiness scores of 150 to influence the estimated treatment effect at 220 — even though those observations are 70 points away from the cutoff and tell us almost nothing about the local behavior near the threshold.

Local linear regression avoids these problems by focusing only on data near the cutoff, where the linear approximation is most plausible. The key mathematical property is that local linear regression has a **boundary bias** that is of order $h^2$ (where $h$ is the bandwidth), while local constant (Nadaraya-Watson) regression has boundary bias of order $h$. This means local linear regression provides a better approximation at the cutoff — precisely where we need accuracy.

> **Blue's Mistake: "I'll Fit a Sixth-Degree Polynomial"**
>
> Blue decides to estimate the RDD by fitting a sixth-degree polynomial on each side of the cutoff using all the data. "More flexible is better, right? My $R^2$ is 0.94!" But his treatment effect estimate is 22.7 — nearly double the local linear estimate. The high-order polynomial is being pulled by a handful of influential observations with happiness scores near 150 and 255, creating Runge-phenomenon-like oscillations that distort the extrapolation to the cutoff. When he drops observations below 180 or above 250, his estimate changes dramatically. This sensitivity to faraway data is precisely why Gelman and Imbens recommend against high-order polynomials. Stick with local linear regression.

### Kernel Choice and Bandwidth

In practice, local linear regression is implemented using a **kernel function** $K(\cdot)$ that assigns weights to observations based on their distance from the cutoff. Common choices include:

- **Triangular kernel:** $K(u) = (1 - |u|) \cdot \mathbf{1}(|u| \leq 1)$ — gives the most weight to observations closest to the cutoff. This is optimal in a minimax mean-squared-error sense (Fan, 1992).
- **Uniform (rectangular) kernel:** $K(u) = \frac{1}{2} \cdot \mathbf{1}(|u| \leq 1)$ — gives equal weight to all observations within the bandwidth. Equivalent to unweighted local linear regression within the bandwidth window.
- **Epanechnikov kernel:** $K(u) = \frac{3}{4}(1 - u^2) \cdot \mathbf{1}(|u| \leq 1)$ — a smooth compromise.

The **bandwidth** $h$ controls the bias-variance tradeoff:

- **Small $h$:** Uses fewer observations near the cutoff. Low bias (the linear approximation is excellent over a narrow range) but high variance (few data points).
- **Large $h$:** Uses more observations further from the cutoff. Lower variance but higher bias (the linear approximation may be poor over a wide range).

Optimal bandwidth selection methods, such as those of Imbens and Kalyanaraman (2012) and Cattaneo, Idrobo, and Titiunik (2020), balance this tradeoff by minimizing mean squared error. The `rdrobust` package in R and Python implements these procedures. We will discuss optimal bandwidth selection further in Section 6.7.

### Worked Example: The Effect of Evolution on Battle Performance

Using the `happiness_evolution.csv` dataset with 800 Pokemon, we estimate the effect of evolution on the standardized combat power index.

**Setup:**
- Running variable: Happiness score ($X$), ranging from 150 to 255
- Cutoff: $c = 220$
- Treatment: Evolution ($D = \mathbf{1}(X \geq 220)$)
- Outcome: Standardized combat power index ($Y$)
- Bandwidth: $h = 15$ (selected via Cattaneo-Idrobo-Titiunik optimal bandwidth selector)

**Observations within bandwidth:** 312 Pokemon with happiness scores in $[205, 235]$

**Left-side regression** ($X \in [205, 220)$, $n = 148$):

$$\hat{Y}_i = 52.3 + 0.41 \cdot (X_i - 220)$$

At $X = 220$: predicted $Y = 52.3$

**Right-side regression** ($X \in [220, 235]$, $n = 164$):

$$\hat{Y}_i = 63.8 + 0.38 \cdot (X_i - 220)$$

At $X = 220$: predicted $Y = 63.8$

**RDD estimate:**

$$\hat{\tau}_{RDD} = 63.8 - 52.3 = 11.5$$

with a robust standard error of 3.2, yielding a 95% confidence interval of $[5.2, 17.8]$.

Evolution causes an **11.5-point increase** in the standardized combat power index for Pokemon at the happiness threshold of 220. This is a substantial and statistically significant effect.

> **Professor Oak Explains: What the RDD Graph Shows**
>
> "The classic RDD visualization shows a scatter plot of the outcome against the running variable, with a vertical line at the cutoff. You should see a clear *jump* in the outcome at the cutoff — the treatment effect. On either side of the cutoff, the relationship between happiness and combat power should be smooth and continuous. The discontinuity at the cutoff is the causal effect.
>
> "If you see a smooth curve with no jump, there is no treatment effect. If you see a jump but the data are noisy, the treatment effect is uncertain. If you see jumps at places *other* than the cutoff, something may be wrong with the design."

---

## 6.6 Fuzzy Regression Discontinuity Design

### When the Cutoff Is Not Sharp

In the sharp RDD, crossing the threshold deterministically assigns treatment: every Pokemon at or above 220 evolves, and every Pokemon below 220 does not. But in practice, the world is rarely so clean.

On Cinnabar Island, some trainers **press the B button** during the evolution animation, canceling the evolution. They might prefer the unevolved form's aesthetic, its moveset, or its type. This means that some Pokemon above the happiness threshold of 220 *do not evolve*, even though they are eligible.

Formally, let $D_i$ now denote actual evolution status. In the **fuzzy RDD**:

$$\lim_{x \downarrow c} E[D | X = x] - \lim_{x \uparrow c} E[D | X = x] = \kappa, \quad 0 < \kappa < 1$$

The probability of treatment *jumps* at the cutoff but does not go from 0 to 1. In our data, suppose:

- Among Pokemon just above 220: 82% evolved ($D = 1$)
- Among Pokemon just below 220: 0% evolved ($D = 0$, no one below the threshold can evolve)

The jump in treatment probability is $\kappa = 0.82 - 0.00 = 0.82$.

### Fuzzy RDD as Instrumental Variables

The fuzzy RDD is conceptually identical to instrumental variables, where the instrument is **whether the running variable exceeds the cutoff**:

$$Z_i = \mathbf{1}(X_i \geq c)$$

This indicator $Z_i$ serves as an instrument for actual treatment $D_i$. The three IV assumptions hold in the RDD context:

1. **Relevance:** Crossing the cutoff increases the probability of treatment (from 0% to 82% in our example).
2. **Independence:** Near the cutoff, being just above or below is "as good as random" — the running variable's position near the cutoff is essentially noise.
3. **Exclusion restriction:** Crossing the cutoff affects outcomes *only through* its effect on treatment (evolution). The cutoff itself has no direct effect on battle performance.

The **fuzzy RDD estimand** is the ratio of the jump in outcomes to the jump in treatment at the cutoff:

> **Definition 6.8 (Fuzzy RDD Estimand).** The fuzzy RDD estimate is:
>
> $$\tau_{FRDD} = \frac{\lim_{x \downarrow c} E[Y | X = x] - \lim_{x \uparrow c} E[Y | X = x]}{\lim_{x \downarrow c} E[D | X = x] - \lim_{x \uparrow c} E[D | X = x]}$$
>
> This is exactly the Wald estimator applied locally at the discontinuity.

### Connection to 2SLS

The fuzzy RDD can be estimated via 2SLS using only observations within the bandwidth:

**First stage:**

$$D_i = \pi_0 + \pi_1 \cdot \mathbf{1}(X_i \geq c) + \pi_2 \cdot (X_i - c) + \pi_3 \cdot \mathbf{1}(X_i \geq c) \cdot (X_i - c) + v_i$$

**Second stage:**

$$Y_i = \beta_0 + \beta_1 \hat{D}_i + \beta_2 \cdot (X_i - c) + \beta_3 \cdot \mathbf{1}(X_i \geq c) \cdot (X_i - c) + \epsilon_i$$

The coefficient $\hat{\beta}_1$ is the fuzzy RDD estimate. Note the inclusion of the running variable $(X_i - c)$ and its interaction with the cutoff indicator — these allow separate slopes on each side of the cutoff, as in the sharp RDD.

### The Complier Interpretation in Fuzzy RDD

Just as IV recovers a LATE, the fuzzy RDD recovers the treatment effect for **compliers at the cutoff** — Pokemon whose evolution status is changed by crossing the threshold. These are the Pokemon that *would* evolve if above 220 but *would not* (could not) if below. The B-button pressers are the non-compliers — they are above the threshold but refuse treatment (evolution).

In the language of the complier taxonomy from Section 6.4:
- **Compliers:** Pokemon that evolve when above 220 and would not evolve if below. These are the "normal" cases — the game triggers evolution, and the trainer allows it.
- **Never-Takers (B-button pressers):** Pokemon whose trainers cancel evolution even when above 220. They are treated (crossing the threshold) but refuse the actual treatment (evolution).
- **Always-Takers:** In principle, these would be Pokemon that evolve even below 220, which is impossible by game mechanics. So in this one-sided fuzzy design, there are no always-takers below the cutoff.
- **Defiers:** Ruled out by monotonicity — no Pokemon evolves *only when below* the threshold.

The fuzzy RDD LATE is the effect of evolution for the compliers at the cutoff: trainers who allow evolution to proceed when the happiness threshold is crossed. This is a natural and policy-relevant quantity — it tells us what evolution does for the "typical" Pokemon that evolves at the margin.

### Worked Example: Fuzzy RDD with Happiness Evolution Data

Using the same `happiness_evolution.csv` dataset, but now accounting for B-button cancellations:

**Jump in outcomes at cutoff:**

$$\lim_{x \downarrow 220} E[Y | X = x] - \lim_{x \uparrow 220} E[Y | X = x] = 62.1 - 52.3 = 9.8$$

**Jump in treatment at cutoff:**

$$\lim_{x \downarrow 220} E[D | X = x] - \lim_{x \uparrow 220} E[D | X = x] = 0.82 - 0.00 = 0.82$$

**Fuzzy RDD estimate:**

$$\hat{\tau}_{FRDD} = \frac{9.8}{0.82} = 11.95$$

The fuzzy RDD estimate is 11.95 — slightly larger than the sharp RDD estimate of 11.5. This makes sense: the sharp RDD "dilutes" the effect by averaging over both evolved Pokemon and B-button non-compliers above the threshold. The fuzzy RDD corrects for this dilution by dividing by the compliance rate.

> **Blue's Mistake: "Just Compare Above vs. Below"**
>
> Blue looks at the happiness evolution data and says, "Easy! Pokemon above 220 have an average combat power of 61.5, and those below average 48.2. The effect of evolution is $61.5 - 48.2 = 13.3$ points."
>
> Blue is committing two errors. First, he is comparing *all* Pokemon above and below the cutoff, not just those near it. Pokemon with happiness of 250 are very different from those with happiness of 180 — they have more experienced trainers, more battles, more investment. The RDD uses only observations near the cutoff to ensure comparability. Second, he is ignoring the fuzzy nature of the design — not all Pokemon above 220 actually evolved. The naive comparison conflates the effect of evolution with the effect of happiness itself.

---

## 6.7 RDD Diagnostics

A well-executed RDD is among the most credible quasi-experimental designs. But this credibility rests on assumptions that must be carefully validated. This section presents the essential diagnostic checks.

### McCrary Density Test: Checking for Manipulation

The most important threat to RDD validity is **manipulation of the running variable**. If trainers can precisely control their Pokemon's happiness to land just above 220, then the Pokemon right above the cutoff are not comparable to those right below — they are systematically different (their trainers are more skilled, more strategic, more invested).

The **McCrary (2008) density test** checks for manipulation by examining whether the density of the running variable is continuous at the cutoff. Under no manipulation, we expect approximately equal numbers of Pokemon on both sides of 220. If trainers are gaming the threshold, we would see a **bunching** — an excess mass of observations just above 220 and a corresponding hollow just below.

Formally, the test estimates the density of $X$ separately on each side of the cutoff and tests for a discontinuity:

$$H_0: \lim_{x \downarrow c} f(x) = \lim_{x \uparrow c} f(x) \qquad H_1: \lim_{x \downarrow c} f(x) \neq \lim_{x \uparrow c} f(x)$$

To implement the test visually, plot a histogram of the happiness score with fine bins near the cutoff. If you see a smooth, continuous distribution, manipulation is unlikely. If you see a spike just above 220 or a dip just below, there is cause for concern.

In our data, the histogram shows a roughly uniform distribution of happiness scores between 200 and 240, with no visible bunching at 220. The McCrary test statistic is $-0.08$ with a $p$-value of $0.64$ — we fail to reject the null of no manipulation. This is reassuring.

The McCrary test works by estimating the density of $X$ on each side of the cutoff using local polynomial density estimation, then computing the log difference in the estimated densities at the cutoff. Under the null of no manipulation, this log difference is asymptotically normal. Cattaneo, Jansson, and Ma (2020) provide an updated version of the density test (`rddensity`) with improved finite-sample properties and automatic bandwidth selection.

It is worth noting what the McCrary test can and cannot tell you. It can detect *precise* manipulation — trainers pushing their Pokemon's happiness to exactly 220 or just above. But it cannot detect *imprecise* manipulation — trainers generally trying to increase happiness without precise control over the exact score. If all trainers are trying to make their Pokemon happier (a reasonable assumption), this does not threaten the RDD as long as they cannot precisely target the 220 threshold.

> **Professor Oak Explains: When Manipulation Is Plausible**
>
> "Not all running variables are equally susceptible to manipulation. Happiness scores in Pokemon games are a complex function of many inputs — walking steps, using items, winning battles, leveling up — and they are not displayed to trainers as a precise number. This makes precise manipulation difficult.
>
> "Contrast this with settings where the running variable is self-reported (income for benefit eligibility) or precisely known to the individual (test scores for program entry). In those cases, manipulation is a serious concern, and the McCrary test becomes essential. If the density test rejects, the RDD may not be credible."

### Placebo Tests: Covariate Balance at the Cutoff

The key assumption of RDD is that all factors other than treatment vary smoothly at the cutoff. We can partially test this by checking whether **pre-treatment covariates** show discontinuities at the cutoff. If the design is valid, covariates that are determined before the running variable reaches the cutoff should be continuous through it.

For each covariate $W$ (e.g., Pokemon level, base attack, base defense, base speed), run the RDD with $W$ as the outcome:

$$\hat{\delta}_W = \lim_{x \downarrow c} E[W | X = x] - \lim_{x \uparrow c} E[W | X = x]$$

If the design is valid, $\hat{\delta}_W \approx 0$ for all pre-treatment covariates. A statistically significant discontinuity in a covariate suggests that something other than the treatment changes at the cutoff — a red flag.

In our data:

| Covariate | Estimated Discontinuity | Std. Error | $p$-value |
|---|---|---|---|
| Level | $-0.3$ | 1.1 | 0.78 |
| Base Attack | 0.8 | 1.5 | 0.59 |
| Base Defense | $-0.5$ | 1.4 | 0.72 |
| Base Speed | 0.2 | 1.3 | 0.88 |

None of the covariates show a significant discontinuity at 220. This is consistent with the identifying assumption that all factors other than evolution are smooth through the cutoff.

### Bandwidth Sensitivity

Because the RDD estimate depends on the choice of bandwidth $h$, it is essential to show that the results are **robust to different bandwidths**. If the estimate changes dramatically as you widen or narrow the bandwidth, this raises concerns about the specification.

Good practice is to present the estimate for a range of bandwidths: half the optimal bandwidth, the optimal bandwidth, one-and-a-half times the optimal, and twice the optimal:

| Bandwidth | $n$ within window | $\hat{\tau}_{RDD}$ | Std. Error | 95% CI |
|---|---|---|---|---|
| $h = 8$ | 158 | 12.8 | 4.7 | $[3.6, 22.0]$ |
| $h = 12$ | 247 | 11.9 | 3.6 | $[4.8, 19.0]$ |
| $h = 15$ (optimal) | 312 | 11.5 | 3.2 | $[5.2, 17.8]$ |
| $h = 20$ | 402 | 10.8 | 2.8 | $[5.3, 16.3]$ |
| $h = 30$ | 548 | 9.6 | 2.4 | $[4.9, 14.3]$ |

The estimate ranges from 9.6 to 12.8, with all confidence intervals overlapping. The point estimate decreases slightly as the bandwidth increases (because the linear approximation becomes less accurate at wider bandwidths), but the estimates are reasonably stable. This is reassuring.

### Donut Hole RDD

If there is concern about manipulation *very close* to the cutoff, a **donut hole RDD** excludes observations within a small window around the cutoff. For example, exclude Pokemon with happiness scores in $[218, 222]$ and estimate the RDD using the remaining observations within the bandwidth.

If manipulation affects only the observations immediately adjacent to the cutoff, the donut hole RDD removes these contaminated observations while still estimating the discontinuity. In our data, the donut hole estimate (excluding $[218, 222]$) is $11.2$ (SE $= 3.5$), very close to the baseline estimate of $11.5$.

### Optimal Bandwidth Selection

Cattaneo, Idrobo, and Titiunik (2020) provide the modern standard for bandwidth selection in RDD. Their approach, implemented in the `rdrobust` package, minimizes the mean squared error of the RDD estimator by balancing bias and variance. The procedure:

1. Estimates the second derivative of the conditional expectation function to quantify the bias from the linear approximation.
2. Estimates the variance of the local linear estimator.
3. Selects the bandwidth $h^*$ that minimizes the asymptotic MSE.
4. Provides **bias-corrected confidence intervals** that account for the remaining bias at the optimal bandwidth.

The bias-corrected confidence intervals from `rdrobust` are generally wider than conventional ones because they honestly account for the approximation error inherent in the local linear specification. These are the intervals that should be reported in applied work.

> **Blue's Mistake: "I'll Just Pick the Bandwidth That Gives the Best Result"**
>
> Blue runs the RDD with 15 different bandwidths and reports only the one that gives the largest and most significant estimate. "Look, with a bandwidth of 7, the effect is 14.8 with a $p$-value of 0.003! Very significant!"
>
> This is cherry-picking — a form of $p$-hacking. The bandwidth should be chosen by a principled, data-driven procedure *before* looking at the results, or the full range of estimates should be reported transparently. Cattaneo, Idrobo, and Titiunik's optimal bandwidth selector provides a pre-committed choice that balances bias and variance without reference to the treatment effect estimate. Always report results for the optimal bandwidth and show sensitivity to alternative choices.

---

## Brief Mentions: Extensions and Related Designs

### Shift-Share (Bartik) Instruments

The shift-share instrument, popularized by Bartik (1991), is a widely used IV strategy in economics. The idea is to construct an instrument that combines aggregate-level "shifts" (changes) with unit-level "shares" (exposure). The instrument for unit $i$ takes the form:

$$B_i = \sum_k s_{ik} \cdot g_k$$

where $s_{ik}$ is unit $i$'s share in category $k$ and $g_k$ is the aggregate change in category $k$.

In the Kanto context, imagine constructing an instrument for changes in local Gym difficulty. Each city has a different composition of trainer types (share of Water-type specialists, Fire-type specialists, etc.). Region-wide changes in the availability of type-specific TMs differentially affect cities depending on their trainer composition. The Bartik instrument would be:

$$B_{\text{city}} = \sum_{\text{type}} (\text{share of type in city}) \times (\text{region-wide change in type-specific TM availability})$$

Recent work by Goldsmith-Pinkham, Sorkin, and Swift (2020) and Borusyak, Hull, and Jaravel (2022) has clarified the identification assumptions underlying Bartik instruments, showing that identification can come either from the exogeneity of shares (the GPSS approach) or the exogeneity of shifts (the BHJ approach), with different implications for which confounders must be addressed.

### Regression Discontinuity in Time (RDiT)

When the running variable is *time* rather than a continuous score, the design is called **Regression Discontinuity in Time** (Hausman and Rapson, 2018). For example, if the Pokemon League changed its battle rules on a specific date, one could compare battle outcomes just before and just after the policy change, using date as the running variable.

RDiT requires the same continuity assumptions as standard RDD — all factors other than the policy change must vary smoothly across the implementation date. But time series data present additional challenges: seasonality (battle performance may vary by day of the week or month of the year), trends (trainers may be improving over time regardless of the policy), and autocorrelation (outcomes in adjacent time periods are correlated). These features make the continuity assumption harder to defend and require more careful specification than in a standard cross-sectional RDD.

RDiT is related to but distinct from difference-in-differences (Chapter 7). DiD exploits variation across both time and units, requiring parallel trends. RDiT exploits only the temporal discontinuity, requiring continuity at the cutoff. The two designs answer different questions and require different assumptions.

---

## Chapter Summary

### Part I: Instrumental Variables

- **Unobserved confounding** cannot be addressed by regression, matching, or propensity scores. When important confounders are unmeasured, these methods fail.
- An **instrumental variable** $Z$ provides an alternative route to causal identification. It must satisfy three assumptions: relevance ($Z$ affects $D$), independence ($Z$ is as-if random), and the exclusion restriction ($Z$ affects $Y$ only through $D$).
- The **Wald estimator** $\hat{\tau}_{IV} = \frac{E[Y|Z=1] - E[Y|Z=0]}{E[D|Z=1] - E[D|Z=0]}$ is the ratio of the reduced-form effect to the first-stage effect.
- **Two-Stage Least Squares (2SLS)** generalizes IV to include covariates, continuous variables, and multiple instruments.
- The **exclusion restriction** is untestable and is the primary vulnerability of any IV design.
- **Weak instruments** (first-stage $F < 10$) cause bias and unreliable inference. Anderson-Rubin confidence sets provide a weak-instrument-robust alternative.
- IV recovers the **Local Average Treatment Effect (LATE)** — the causal effect for *compliers*, the subpopulation whose treatment is changed by the instrument.
- The four compliance types are Compliers, Always-Takers, Never-Takers, and Defiers (ruled out by monotonicity).

### Part II: Regression Discontinuity

- **Sharp RDD** exploits a deterministic treatment assignment rule based on a continuous running variable crossing a cutoff.
- The key assumption is that all factors other than treatment are **continuous at the cutoff** — ensuring that units just above and below the cutoff are comparable.
- **Local linear regression** with optimal bandwidth is the recommended estimation strategy. Avoid global polynomials.
- **Fuzzy RDD** arises when crossing the cutoff increases the *probability* of treatment without determining it completely. Fuzzy RDD is equivalent to IV at the discontinuity.
- **McCrary density tests** check for manipulation of the running variable. Bunching at the cutoff invalidates the design.
- **Placebo tests** on pre-treatment covariates verify that no other discontinuity exists at the cutoff.
- **Bandwidth sensitivity** analysis and **bias-corrected confidence intervals** (via `rdrobust`) ensure robust inference.

---

## Professor Oak's Review Questions

1. **IV Conceptual:** Explain why the exclusion restriction cannot be tested with data. Give an example of a plausible violation of the exclusion restriction in the Safari Zone lottery setting that would bias the IV estimate upward.

2. **IV Technical:** Suppose you have two instruments for Safari Zone attendance: the lottery ($Z_1$) and a Pokedollar rebate coupon ($Z_2$). The first-stage F-statistics are 85.3 and 6.2, respectively. Which instrument raises concerns about weak instrument bias? What diagnostic would you use to obtain reliable inference with the weaker instrument?

3. **IV Interpretation:** A researcher estimates that the LATE of Safari Zone training on win rate is 19 percentage points. A policymaker wants to know the effect of making the Safari Zone free for *all* trainers. Under what conditions would the LATE be a good estimate of the policy-relevant treatment effect? Under what conditions might it be misleading?

4. **RDD Conceptual:** Why is the McCrary density test important for the credibility of an RDD? Describe a scenario in the happiness evolution setting where the test might reject, and explain what this would imply for the causal estimate.

5. **RDD Technical:** A researcher estimates a sharp RDD with optimal bandwidth $h = 15$ and finds a significant effect of evolution on combat power. She then tries bandwidths of 8, 12, 20, and 30, and finds that the effect is significant for $h = 15$ and $h = 20$ but not for $h = 8$ or $h = 30$. Should she be concerned? Explain.

6. **RDD vs. IV:** Both fuzzy RDD and standard IV use the Wald estimator structure. What is the key difference in the source of identifying variation? Why is the fuzzy RDD often considered more credible than a typical IV design?

---

## Trainer Challenge Exercises

### Exercise 1: Compute the Wald Estimate

The following table summarizes data from a Safari Zone lottery:

| | Winners ($Z = 1$) | Losers ($Z = 0$) |
|---|---|---|
| $n$ | 150 | 350 |
| Mean attendance ($\bar{D}$) | 0.80 | 0.25 |
| Mean win rate ($\bar{Y}$) | 0.62 | 0.51 |

(a) Compute the first-stage effect.
(b) Compute the reduced-form (ITT) effect.
(c) Compute the Wald IV estimate.
(d) What is the estimated compliance rate? Interpret this number in context.
(e) Using the ITT-LATE relationship, verify that $\text{ITT} = \text{LATE} \times P(\text{Complier})$.

### Exercise 2: Assess Instrument Strength

A researcher proposes using "distance from a trainer's home to the nearest Safari Zone entrance" as an instrument for Safari Zone attendance. The first-stage regression yields:

$$D_i = 0.65 - 0.008 \cdot \text{Distance}_i + \hat{v}_i$$

with a first-stage F-statistic of 7.3.

(a) According to the Stock-Yogo rule of thumb, is this instrument sufficiently strong?
(b) Describe two problems that arise from using a weak instrument.
(c) Propose a diagnostic that provides valid inference even with a weak instrument.
(d) Separately from strength, evaluate whether "distance to Safari Zone" is likely to satisfy the exclusion restriction. What potential violations might arise?

### Exercise 3: Estimate a Sharp RDD

Using the following data from the `happiness_evolution.csv` dataset (showing mean combat power for bins of happiness score), estimate the sharp RDD effect of evolution on combat power:

| Happiness bin | Midpoint | Mean $Y$ | $n$ |
|---|---|---|---|
| [205, 210) | 207.5 | 49.1 | 38 |
| [210, 215) | 212.5 | 50.8 | 42 |
| [215, 220) | 217.5 | 52.6 | 45 |
| [220, 225) | 222.5 | 64.1 | 48 |
| [225, 230) | 227.5 | 65.3 | 44 |
| [230, 235) | 232.5 | 66.8 | 40 |

(a) Fit separate linear regressions for the three bins below and above the cutoff of 220.
(b) Extrapolate each regression to the cutoff ($X = 220$) and compute the RDD estimate.
(c) Plot the data and your fitted lines (sketch or software).
(d) What assumption is required for this estimate to be causal? How would you test it?

### Exercise 4: Conceptual McCrary Test

Suppose you are studying the effect of a new TM move on Pokemon battle performance. The TM is available only to Pokemon whose trainer has at least 1000 hours of gameplay, and trainers can see their hour count on their Trainer Card.

(a) Explain why you might be concerned about manipulation of the running variable in this setting.
(b) Describe what a McCrary density test would look like if manipulation were occurring. Sketch the expected histogram shape.
(c) Propose two additional diagnostic checks (beyond the McCrary test) that would strengthen or weaken the case for a valid RDD.
(d) If the McCrary test rejects, does this definitively invalidate the RDD? What alternatives might you consider?

---

## Further Reading

- **Angrist, J. D., Imbens, G. W., & Rubin, D. B. (1996).** "Identification of Causal Effects Using Instrumental Variables." *Journal of the American Statistical Association*, 91(434), 444-455. *The foundational paper establishing LATE and the complier framework.*

- **Imbens, G. W. & Angrist, J. D. (1994).** "Identification and Estimation of Local Average Treatment Effects." *Econometrica*, 62(2), 467-475. *Introduces the LATE theorem and the monotonicity condition.*

- **Stock, J. H. & Yogo, M. (2005).** "Testing for Weak Instruments in Linear IV Regression." In *Identification and Inference for Econometric Models: Essays in Honor of Thomas Rothenberg*, 80-108. *The definitive treatment of weak instrument diagnostics and the F > 10 rule.*

- **Lee, D. S. & Lemieux, T. (2010).** "Regression Discontinuity Designs in Economics." *Journal of Economic Literature*, 48(2), 281-355. *A comprehensive practical guide to RDD covering sharp, fuzzy, and kink designs.*

- **Cattaneo, M. D., Idrobo, N., & Titiunik, R. (2020).** *A Practical Introduction to Regression Discontinuity Designs: Foundations.* Cambridge University Press. *The modern standard reference for RDD estimation, bandwidth selection, and inference.*

- **Hahn, J., Todd, P., & van der Klaauw, W. (2001).** "Identification and Estimation of Treatment Effects with a Regression-Discontinuity Design." *Econometrica*, 69(1), 201-209. *The formal identification result for RDD using the continuity of conditional expectations.*

- **McCrary, J. (2008).** "Manipulation of the Running Variable in the Regression Discontinuity Design: A Density Test." *Journal of Econometrics*, 142(2), 698-714. *Introduces the density test for checking manipulation in RDD.*

- **Gelman, A. & Imbens, G. W. (2019).** "Why High-Order Polynomials Should Not Be Used in Regression Discontinuity Designs." *Journal of Business & Economic Statistics*, 37(3), 447-456. *A cautionary note against global polynomial specifications in RDD.*

---

## Badges Earned

> **Soul Badge** (Fuchsia City Gym)
> *Awarded for mastering Instrumental Variables — using exogenous variation to identify causal effects when unobserved confounders block the backdoor path. You have learned the Wald estimator, 2SLS, the LATE theorem, and the art of defending the exclusion restriction.*

> **Volcano Badge** (Cinnabar Island Gym)
> *Awarded for mastering Regression Discontinuity Designs — exploiting sharp and fuzzy thresholds to estimate causal effects at the boundary. You have learned local linear regression, the McCrary density test, bandwidth sensitivity analysis, and the connection between fuzzy RDD and IV.*

With six badges in hand, you are nearing the end of your Kanto journey. Two more Gyms remain. The next will test everything you have learned — and introduce the most powerful quasi-experimental design of all.

---

## Next Chapter Preview

> *Saffron City is in crisis. Team Rocket has invaded, and a mysterious new TM is being released city by city. The staggered rollout creates a natural experiment — if you know how to analyze it. But beware: the naive two-way fixed effects estimator that Blue relies on hides a treacherous bias when treatment timing varies. You will need difference-in-differences, synthetic control, and the modern tools of Callaway-Sant'Anna and Goodman-Bacon to unravel the truth. The Marsh Badge awaits.*
