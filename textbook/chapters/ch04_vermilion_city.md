# Chapter 4: Vermilion City — Matching & Subclassification

<!-- FIG-CH04-ELECMONS -->
<div style="display:flex; gap:18px; flex-wrap:wrap; justify-content:center; align-items:flex-end; margin:1.25em auto;">
<figure style="margin:0; text-align:center;">
<img src="../../assets/sprites/front/25.png" alt="Pikachu" style="width:105px; display:block; margin:0 auto; image-rendering: pixelated;">
<figcaption style="font-size:0.8em;">#025 Pikachu</figcaption>
</figure>
<figure style="margin:0; text-align:center;">
<img src="../../assets/sprites/front/26.png" alt="Raichu" style="width:105px; display:block; margin:0 auto; image-rendering: pixelated;">
<figcaption style="font-size:0.8em;">#026 Raichu</figcaption>
</figure>
<figure style="margin:0; text-align:center;">
<img src="../../assets/sprites/front/100.png" alt="Voltorb" style="width:105px; display:block; margin:0 auto; image-rendering: pixelated;">
<figcaption style="font-size:0.8em;">#100 Voltorb</figcaption>
</figure>
</div>
<p style="text-align:center; font-size:0.85em; color:#666; font-style:italic; margin:0.25em 0 1em;">Vermilion's Electric-type roster — treatment groups we'll try to match.</p>


<!-- FIG-CH04-ELEC -->
<figure style="margin:1em auto; max-width:110px; text-align:center;">
<img src="../../assets/sprites/types/electric.png" alt="Electric-type — Lt. Surge's specialty" style="width:90px; display:block; margin:0 auto;">
<figcaption style="font-size:0.85em;">Electric-type — Lt. Surge's specialty</figcaption>
</figure>


<!-- FIG-CH04-SURGE -->
<figure style="margin:1.5em auto; max-width:160px; text-align:center;">
<img src="../../assets/characters/surge.png" alt="Lt. Surge, Vermilion Gym Leader" style="width:140px; display:block; margin:0 auto; image-rendering: pixelated;">
<figcaption style="font-size:0.85em;">Lt. Surge, Vermilion Gym Leader</figcaption>
</figure>


> *"The best trainers don't just fight hard — they find the right opponent to learn from."*
> — Lt. Surge, Vermilion City Gym Leader

The S.S. Anne sits in Vermilion Harbor, its hull gleaming under the Kanto sun. Four hundred trainers have disembarked after a weeklong cruise, and among them a fierce debate has broken out: does Lt. Surge's "Thunder Training" program actually make trainers better at the Vermilion Gym? Some passengers completed the program during the cruise; others spent their time at the buffet, the pool, or the onboard Pokemon Center. Now, with the Gym battle looming, we have the perfect observational study.

In Chapter 3, we learned to draw DAGs and identify which variables confound the relationship between a treatment and an outcome. But identifying confounders is only half the battle. We now need a *strategy* for adjusting for those confounders so that we can isolate the causal effect of Thunder Training on Gym performance. This chapter introduces the oldest and most intuitive family of such strategies: **matching**.

The logic is beautifully simple. If we want to know whether Thunder Training helps, we should compare a trained trainer to an untrained trainer who is *otherwise identical* — the same number of badges, the same team level, the same battle experience. If the trained trainer still performs better, we can attribute the difference to the training itself. The challenge, as we will see, is that "otherwise identical" is far harder to achieve than it sounds.

---

## 4.1 The Intuition Behind Matching

### The S.S. Anne Passenger Manifest

Let us formalize the setting. We observe $n = 400$ trainers who disembarked from the S.S. Anne. For each trainer $i$, we record the following:

- $D_i \in \{0, 1\}$: whether trainer $i$ completed Thunder Training ($D_i = 1$) or not ($D_i = 0$).
- $Y_i$: performance score at the Vermilion Gym (0-100 scale, combining damage dealt, Pokemon remaining, and time to victory or defeat).
- $X_i$: a vector of pre-treatment covariates, including:

| Variable | Description | Range |
|----------|-------------|-------|
| `badges` | Number of Gym badges earned before Vermilion | 0-7 |
| `team_level` | Average level of the trainer's six Pokemon | 10-55 |
| `battle_exp` | Total battles fought (career) | 5-500 |
| `strategy_score` | Score on a tactical reasoning assessment | 0-100 |
| `electric_knowledge` | Prior knowledge of Electric-type matchups | 0-10 |
| `pokedex_count` | Number of species registered in Pokedex | 5-151 |
| `has_ground_type` | Whether the team includes a Ground-type Pokemon | 0 or 1 |
| `items_carried` | Number of healing/battle items in the bag | 0-20 |
| `hours_training` | Hours spent training Pokemon in the past month | 0-200 |
| `cruise_day_joined` | Day of the cruise when training began (1-7, or 0 if untreated) | 0-7 |

Of the 400 trainers, 160 completed Thunder Training ($D = 1$) and 240 did not ($D = 0$). A naive comparison of group means yields:

$$\bar{Y}_1 - \bar{Y}_0 = 72.4 - 58.1 = 14.3 \text{ points}$$

Thunder Training graduates scored, on average, 14.3 points higher at the Vermilion Gym. Case closed?

### Why Simple Comparison Fails

Not remotely. Consider the covariate means by treatment group:

| Covariate | Thunder Training ($D=1$) | No Training ($D=0$) | Difference |
|-----------|:------------------------:|:--------------------:|:----------:|
| `badges` | 3.8 | 2.1 | +1.7 |
| `team_level` | 34.2 | 25.6 | +8.6 |
| `battle_exp` | 187.3 | 98.4 | +88.9 |
| `strategy_score` | 68.5 | 52.3 | +16.2 |
| `electric_knowledge` | 6.2 | 3.8 | +2.4 |
| `has_ground_type` | 0.71 | 0.43 | +0.28 |

The trainers who chose Thunder Training were *already better*. They had more badges, higher-level Pokemon, more battle experience, and greater strategic sophistication. The 14.3-point raw difference confounds the causal effect of Thunder Training with these pre-existing advantages.

In the language of potential outcomes from Chapter 1, the problem is *selection bias*:

$$\bar{Y}_1 - \bar{Y}_0 = \underbrace{\mathbb{E}[Y_i(1) - Y_i(0) \mid D_i = 1]}_{\text{ATT}} + \underbrace{\mathbb{E}[Y_i(0) \mid D_i = 1] - \mathbb{E}[Y_i(0) \mid D_i = 0]}_{\text{Selection bias}}$$

The second term — selection bias — reflects the fact that Thunder Training participants would have performed better *even without the training*, simply because they are more skilled. Our goal is to eliminate this term.

### The Matching Idea

Matching attacks selection bias with a beautifully direct strategy: for each treated trainer, find an untreated trainer with the same covariates. If trainer $i$ completed Thunder Training, has 4 badges, a team level of 32, and 150 career battles, we search the control group for trainer $j$ who also has 4 badges, a team level of 32, and 150 career battles — but who skipped the training. The difference $Y_i - Y_j$ estimates the individual treatment effect for someone with those characteristics, and the average across all matched pairs estimates the **Average Treatment Effect on the Treated (ATT)**:

$$\widehat{\text{ATT}} = \frac{1}{n_1} \sum_{i: D_i = 1} \left( Y_i - Y_{j(i)} \right)$$

where $j(i)$ denotes the matched control unit for treated unit $i$, and $n_1$ is the number of treated units.

The logic is identical to the ideal experiment we cannot run. In an RCT, randomization ensures that treated and control groups are comparable on all covariates, both observed and unobserved. Matching tries to *construct* a comparison group that resembles the treated group on observed covariates. If we succeed, and if there are no unobserved confounders (the "conditional ignorability" assumption from Chapter 3), then the matched comparison is as good as a randomized experiment.

> **Blue's Mistake: The Lazy Comparison**
>
> Blue bursts into the Vermilion Pokemon Center waving a printout. "I computed the average Gym score for Thunder Training graduates and non-participants," he announces. "The difference is 14.3 points! Thunder Training is *incredible*!"
>
> Red shakes his head. "Blue, the graduates already had more badges and higher-level Pokemon. You're comparing Dragonite trainers to Rattata trainers and crediting the difference to a one-week course."
>
> Blue's mistake is the most fundamental error in observational causal inference: treating an associational comparison as a causal one. Without adjusting for confounders, the raw mean difference is a biased estimate of the causal effect. Blue is, quite literally, comparing apples to oranges — and then concluding that apples taste better because they're apples.
>
> To his credit, Blue *did* collect the right data. His mistake is in the analysis, not the measurement. As we will see, matching provides a principled way to use that data correctly.

### What Matching Requires

For matching to yield a valid causal estimate, we need two key assumptions (which we formalized as DAG criteria in Chapter 3):

1. **Conditional Ignorability (Unconfoundedness):** $Y(0), Y(1) \perp D \mid X$. Given the observed covariates, treatment assignment is as good as random. There are no unobserved confounders.

2. **Overlap (Common Support):** $0 < P(D = 1 \mid X = x) < 1$ for all $x$ in the support of $X$. For every combination of covariate values observed among the treated, there exists at least some probability of finding a control unit with the same values.

If both assumptions hold, matching on $X$ eliminates selection bias completely. The question is *how* to match. The next several sections explore increasingly sophisticated answers.

---

## 4.2 Exact Matching and Coarsened Exact Matching (CEM)

### Exact Matching: The Gold Standard in Theory

The most straightforward approach to matching is **exact matching**: for each treated unit, find a control unit with *exactly the same values* on every covariate. If treated trainer $i$ has $X_i = (4 \text{ badges}, 32 \text{ team level}, 150 \text{ battles}, 68 \text{ strategy}, \ldots)$, we require control trainer $j$ to have $X_j = (4, 32, 150, 68, \ldots)$ identically.

> **Definition 4.1 (Exact Matching).** A matched pair $(i, j)$ is an *exact match* if $X_i = X_j$, where $i$ is a treated unit and $j$ is a control unit. The exact matching estimator of the ATT is:
>
> $$\widehat{\text{ATT}}_{\text{exact}} = \frac{1}{n_1} \sum_{i: D_i = 1} \left( Y_i - \bar{Y}_{0, \mathcal{M}(i)} \right)$$
>
> where $\mathcal{M}(i) = \{j : D_j = 0, X_j = X_i\}$ is the set of exact matches for treated unit $i$, and $\bar{Y}_{0, \mathcal{M}(i)}$ is the average outcome among those matches.

Exact matching has an obvious appeal: if we find exact matches, there is zero covariate imbalance within matched sets, and the estimator is unbiased under conditional ignorability. But there is a fatal practical problem.

### The Curse of Dimensionality

Consider our S.S. Anne data. We have 10 covariates, many of which are continuous or take many discrete values. Even if we discretize `team_level` into just 10 bins, `battle_exp` into 10 bins, `strategy_score` into 10 bins, and so on, the covariate space contains:

$$8 \times 10 \times 10 \times 10 \times 11 \times 147 \times 2 \times 21 \times 10 \times 8 \approx 2.7 \times 10^{10} \text{ cells}$$

With only 400 trainers, the vast majority of these cells are empty. Finding a control trainer who matches a treated trainer on *all* covariates simultaneously is virtually impossible. In practice, exact matching with more than 3-4 discrete covariates produces very few matches, leaving most treated units unmatched and the analysis severely underpowered.

This is the **curse of dimensionality**: as the number of covariates grows, the volume of the covariate space explodes exponentially, and the data become extremely sparse.

### Coarsened Exact Matching (CEM)

Iacus, King, and Porro (2012) proposed an elegant compromise: **Coarsened Exact Matching (CEM)**. The idea is to *coarsen* each covariate into a small number of bins, then perform exact matching on the coarsened values.

> **Definition 4.2 (Coarsened Exact Matching).** Let $\tilde{X}_k$ denote the coarsened version of covariate $X_k$, obtained by mapping continuous values into discrete bins. CEM proceeds as follows:
>
> 1. **Coarsen** each covariate: define bins for each $X_k$.
> 2. **Exact match** on the coarsened covariates: place all units into strata defined by unique combinations of $(\tilde{X}_1, \tilde{X}_2, \ldots, \tilde{X}_K)$.
> 3. **Prune** any stratum that does not contain at least one treated and one control unit.
> 4. **Weight** remaining units within each stratum to account for different numbers of treated and control units.

**Worked Example.** Suppose we coarsen three key covariates as follows:

| Covariate | Original Range | Coarsened Bins |
|-----------|---------------|----------------|
| `badges` | 0-7 | {0-2: Low, 3-5: Mid, 6-7: High} |
| `team_level` | 10-55 | {10-25: Low, 26-40: Mid, 41-55: High} |
| `has_ground_type` | 0, 1 | {0: No, 1: Yes} |

This creates $3 \times 3 \times 2 = 18$ strata. Consider four of them:

| Stratum | Badges | Team Level | Ground? | Treated ($n_1$) | Control ($n_0$) | Status |
|:-------:|:------:|:----------:|:-------:|:----------------:|:----------------:|:------:|
| A | Low | Low | No | 3 | 28 | Matched |
| B | Mid | Mid | Yes | 22 | 15 | Matched |
| C | High | High | Yes | 18 | 2 | Matched |
| D | High | High | No | 8 | 0 | **Pruned** |

Stratum D is pruned because it contains no control units — these 8 treated trainers cannot be matched and are excluded from the analysis. Within surviving strata, we assign weights to ensure that the treated-to-control ratio is balanced.

For stratum $s$ with $n_{1s}$ treated units and $n_{0s}$ control units, each control unit receives weight:

$$w_s = \frac{n_{1s} / n_1}{n_{0s} / n_0}$$

where $n_1$ and $n_0$ are the total treated and control counts across all matched strata.

The CEM estimate of the ATT within stratum B, for example, would be:

$$\widehat{\text{ATT}}_B = \bar{Y}_{1,B} - \bar{Y}_{0,B}$$

and the overall ATT is the weighted average across strata:

$$\widehat{\text{ATT}}_{\text{CEM}} = \sum_{s} \frac{n_{1s}}{n_1^{\text{matched}}} \widehat{\text{ATT}}_s$$

### The Coarsening Tradeoff

CEM introduces a fundamental tradeoff:

- **More coarsening** (fewer, wider bins): more matches are found, but units within a stratum may differ substantially on the original covariates. The matching is less precise, introducing potential bias.
- **Less coarsening** (more, narrower bins): matches are more precise, but fewer strata survive pruning, and more treated units are discarded. The analysis may become underpowered.

The researcher must navigate this tradeoff thoughtfully. CEM's key advantage is its *transparency*: the researcher chooses the coarsening explicitly and can evaluate the resulting covariate balance directly. There is no hidden model dependence — the tradeoffs are visible.

> **Professor Oak Explains: Why CEM Is a "Method of Monotone Imbalance Bounding"**
>
> "CEM has a remarkable theoretical property," Professor Oak notes, adjusting his glasses. "The maximum imbalance between treated and control groups is *bounded* by the coarsening the researcher chooses. If you coarsen `team_level` into bins of width 10, you know that any matched treated-control pair differs by at most 10 levels on that variable. This bound holds regardless of the data — it is set *ex ante* by the researcher."
>
> "Compare this to other matching methods where the degree of imbalance is discovered only *after* matching and depends on the data in complex ways. CEM lets you choose your acceptable imbalance *first* and then find matches that satisfy it. That is a powerful guarantee."

---

## 4.3 Distance-Based Matching

> **Notation at a Glance: Matching and Propensity Scores**
>
> The matching literature has a lot of decorated $X$'s and scripty $\mathcal{M}$'s. Here is the plain-English decoder.
>
> | Symbol | Plain-English reading |
> |:---|:---|
> | $X_i$ | The vector of covariates for trainer $i$ — e.g., `[badges, team_level, experience]`. |
> | $X_i - X_j$ | How far apart two trainers are on each covariate, coordinate by coordinate. |
> | $\Sigma$ | The covariance matrix of $X$ in the full sample — encodes "how much each covariate varies" and "which pairs move together." |
> | $\Sigma^{-1}$ | Its inverse — used to *rescale* differences so every covariate matters on a comparable footing. |
> | $d_M(X_i, X_j)$ | Mahalanobis distance — how "similar" trainers $i$ and $j$ are, after rescaling. Small = good match. |
> | $e(X_i) = P(D_i = 1 \mid X_i)$ | The **propensity score** — the probability that a trainer with covariates $X_i$ ends up treated. A single number summarizing $X_i$'s effect on assignment. |
> | $e(X_i) = 0.5$ | "Given this trainer's covariates, treatment is a coin flip." The sweet spot for matching. |
> | $e(X_i) \approx 0$ or $1$ | "Essentially never/always treated" — these units hurt positivity and should be flagged. |
> | $\mathcal{M}(i)$ | The set of control units that trainer $i$ can be matched to (after applying a caliper). |
> | caliper $c$ | Maximum distance allowed for a match. Tighter $c$ → better matches, smaller sample. |
> | $w_i$ | Weight assigned to observation $i$ (e.g., 1 for matched, 0 for discarded; or a subclass weight). |
> | ATT | Average Treatment effect on the Treated — the estimand matching typically targets. |
> | SMD | Standardized Mean Difference — the balance diagnostic: $|\bar{X}_T - \bar{X}_C| / s_{\text{pooled}}$. Target < 0.1. |
>
> Keep in mind: the propensity score $e(X)$ is *not* a prediction we care about. It is a **balancing score** — a tool for making treated and control groups look alike. Its accuracy matters less than the balance it produces.

Exact matching (even coarsened) becomes unwieldy as the number of covariates grows. An alternative is to define a *distance metric* between units and match each treated unit to its nearest control neighbor in the covariate space.

### Mahalanobis Distance

The most common distance metric for matching is the **Mahalanobis distance**, which accounts for the variance and correlation structure of the covariates:

> **Definition 4.3 (Mahalanobis Distance).** The Mahalanobis distance between two covariate vectors $X_i$ and $X_j$ is:
>
> $$d_M(X_i, X_j) = \sqrt{(X_i - X_j)^T \Sigma^{-1} (X_i - X_j)}$$
>
> where $\Sigma$ is the sample covariance matrix of $X$ (typically computed from the full sample or the control group).

The Mahalanobis distance generalizes Euclidean distance by "standardizing" the covariates. If two covariates are measured on very different scales — `battle_exp` ranges from 5 to 500, while `badges` ranges from 0 to 7 — Euclidean distance would be dominated by `battle_exp`. The Mahalanobis distance rescales by the inverse covariance matrix, giving each covariate appropriate weight and accounting for correlations between covariates.

**Worked Example.** Consider two treated trainers and three potential control matches, using only two covariates for illustration: `badges` ($X_1$) and `team_level` ($X_2$).

| Trainer | Type | Badges ($X_1$) | Team Level ($X_2$) |
|---------|------|:---:|:---:|
| Alice | Treated | 4 | 32 |
| Bob | Control | 4 | 30 |
| Carol | Control | 3 | 35 |
| Dan | Control | 5 | 28 |

Suppose the sample covariance matrix (from all 400 trainers) is:

$$\Sigma = \begin{pmatrix} 3.2 & 4.5 \\ 4.5 & 64.0 \end{pmatrix}, \quad \Sigma^{-1} = \begin{pmatrix} 0.366 & -0.026 \\ -0.026 & 0.018 \end{pmatrix}$$

The Mahalanobis distance from Alice to each control is:

**Alice to Bob:** $\Delta X = (0, 2)$

$$d_M = \sqrt{(0, 2) \begin{pmatrix} 0.366 & -0.026 \\ -0.026 & 0.018 \end{pmatrix} \begin{pmatrix} 0 \\ 2 \end{pmatrix}} = \sqrt{(0, 2) \begin{pmatrix} -0.052 \\ 0.036 \end{pmatrix}} = \sqrt{0.072} = 0.268$$

**Alice to Carol:** $\Delta X = (-1, 3)$

$$d_M = \sqrt{(-1, 3) \begin{pmatrix} 0.366 & -0.026 \\ -0.026 & 0.018 \end{pmatrix} \begin{pmatrix} -1 \\ 3 \end{pmatrix}} = \sqrt{(-1, 3) \begin{pmatrix} -0.444 \\ 0.080 \end{pmatrix}} = \sqrt{0.444 + 0.240} = \sqrt{0.684} = 0.827$$

**Alice to Dan:** $\Delta X = (1, -4)$

$$d_M = \sqrt{(1, -4) \begin{pmatrix} 0.366 & -0.026 \\ -0.026 & 0.018 \end{pmatrix} \begin{pmatrix} 1 \\ -4 \end{pmatrix}} = \sqrt{(1, -4) \begin{pmatrix} 0.470 \\ -0.098 \end{pmatrix}} = \sqrt{0.470 + 0.392} = \sqrt{0.862} = 0.929$$

Bob is the nearest neighbor ($d_M = 0.268$), which makes intuitive sense: he matches Alice on badges exactly and is very close on team level.

### Nearest-Neighbor Matching

**1:1 matching** pairs each treated unit with its single closest control unit. **$k$:1 matching** pairs each treated unit with its $k$ nearest controls, using the average of their outcomes as the imputed counterfactual.

A key choice is **with or without replacement**:

- **Without replacement:** Each control unit can be matched to at most one treated unit. This avoids using the same control observation multiple times, but may force poor matches if the pool of unmatched controls shrinks. The order in which treated units are matched matters, introducing some arbitrariness.
- **With replacement:** Each control unit can serve as a match for multiple treated units. This generally produces better matches (the best control is always available), but reduces the effective sample size because some control observations receive heavy weight.

### Caliper Matching

A **caliper** imposes a maximum acceptable distance: if no control unit is within the caliper radius of a treated unit, that treated unit goes unmatched.

> **Definition 4.4 (Caliper Matching).** Given a caliper width $c > 0$, the match set for treated unit $i$ is:
>
> $$\mathcal{M}(i) = \{j : D_j = 0, \; d(X_i, X_j) \leq c\}$$
>
> If $\mathcal{M}(i) = \emptyset$, unit $i$ is discarded.

The caliper introduces a **bias-variance tradeoff**:

- **Tight caliper** ($c$ small): matches are excellent (low bias), but many treated units are unmatched, reducing sample size and increasing variance. The estimand shifts toward the ATT among *matchable* treated units, which may differ from the overall ATT.
- **Loose caliper** ($c$ large): most treated units are matched (low variance), but some matches are poor (higher bias).

A common rule of thumb, due to Austin (2011), is to set the caliper at 0.2 standard deviations of the logit of the propensity score.

> **Professor Oak Explains: Which Distance Metric?**
>
> "When you have a small number of continuous covariates — say, five or fewer — Mahalanobis distance matching works very well," Professor Oak advises. "It handles scale differences and correlations naturally. However, as the dimension grows, Mahalanobis distance can degrade because the inverse covariance matrix becomes unstable, and the notion of 'nearest neighbor' becomes less meaningful in high-dimensional space."
>
> "For higher-dimensional problems, the propensity score — which we will encounter in the next section — collapses all covariates into a single dimension. This is its great power, and also, as we shall see, the source of some controversy."

---

## 4.4 The Propensity Score

### Motivation: The Dimensionality Problem Revisited

Matching on many covariates simultaneously is difficult. With $K$ covariates, we are searching for neighbors in $K$-dimensional space, and the curse of dimensionality makes close neighbors increasingly rare. What if we could reduce the problem to matching on a *single number* that summarizes all the relevant information in $X$?

This is precisely what the **propensity score** achieves.

> **Definition 4.5 (Propensity Score).** The propensity score is the conditional probability of receiving treatment given the observed covariates:
>
> $$e(X_i) = P(D_i = 1 \mid X_i)$$
>
> For the S.S. Anne study, $e(X_i)$ is the probability that trainer $i$ completed Thunder Training, given their badges, team level, battle experience, and other observed characteristics.

### The Rosenbaum-Rubin Theorem

The propensity score's power comes from a remarkable theorem proved by Rosenbaum and Rubin (1983):

> **Theorem 4.1 (Propensity Score Theorem, Rosenbaum & Rubin, 1983).** If treatment assignment is strongly ignorable given $X$ — that is, $Y(0), Y(1) \perp D \mid X$ and $0 < e(X) < 1$ — then treatment assignment is also strongly ignorable given the propensity score alone:
>
> $$Y(0), Y(1) \perp D \mid e(X)$$

This theorem says that if conditioning on the full covariate vector $X$ is sufficient to eliminate confounding, then conditioning on the scalar $e(X)$ is *also* sufficient. We can collapse ten covariates into one number without losing any information relevant to confounding.

### Proof Sketch: The Balancing Property

The theorem rests on a key property: the propensity score *balances* the covariates between treated and control groups.

> **Lemma 4.1 (Balancing Property).** $D \perp X \mid e(X)$. That is, within strata defined by the propensity score, the distribution of covariates is the same for treated and control units.

**Proof sketch.** For any measurable set $A$ in the covariate space:

$$P(X \in A \mid e(X) = p, D = 1) = P(X \in A \mid e(X) = p, D = 0)$$

To see why, note that:

$$P(D = 1 \mid X, e(X)) = P(D = 1 \mid X) = e(X)$$

The first equality holds because $e(X)$ is a function of $X$ (so conditioning on both $X$ and $e(X)$ is the same as conditioning on $X$). Therefore, within a group of units that all share the same propensity score $e(X) = p$, the treatment probability is $p$ for every unit regardless of their specific covariate values. This means treatment assignment within a propensity score stratum is effectively *random* with respect to $X$ — exactly the balancing property.

Now, if $Y(0), Y(1) \perp D \mid X$ and $D \perp X \mid e(X)$, it follows that $Y(0), Y(1) \perp D \mid e(X)$. Intuitively: conditioning on $e(X)$ makes $D$ independent of $X$, and conditioning on $X$ makes $D$ independent of potential outcomes, so conditioning on $e(X)$ suffices to make $D$ independent of potential outcomes.

### Estimating the Propensity Score

In practice, $e(X)$ is unknown and must be estimated from the data. The most common approach is **logistic regression**:

$$\log \frac{e(X_i)}{1 - e(X_i)} = \beta_0 + \beta_1 \cdot \text{badges}_i + \beta_2 \cdot \text{team\_level}_i + \beta_3 \cdot \text{battle\_exp}_i + \beta_4 \cdot \text{strategy\_score}_i + \cdots$$

For the S.S. Anne data, suppose we estimate the following model:

| Covariate | Coefficient ($\hat{\beta}$) | Std. Error | $z$-value | $p$-value |
|-----------|:---------------------------:|:----------:|:---------:|:---------:|
| Intercept | $-4.821$ | 0.612 | $-7.88$ | $<0.001$ |
| `badges` | $0.342$ | 0.078 | $4.38$ | $<0.001$ |
| `team_level` | $0.058$ | 0.014 | $4.14$ | $<0.001$ |
| `battle_exp` | $0.004$ | 0.001 | $3.12$ | $0.002$ |
| `strategy_score` | $0.031$ | 0.008 | $3.88$ | $<0.001$ |
| `electric_knowledge` | $0.189$ | 0.052 | $3.63$ | $<0.001$ |
| `has_ground_type` | $0.614$ | 0.198 | $3.10$ | $0.002$ |
| `items_carried` | $0.023$ | 0.031 | $0.74$ | $0.458$ |
| `hours_training` | $0.007$ | 0.003 | $2.33$ | $0.020$ |
| `pokedex_count` | $0.005$ | 0.003 | $1.67$ | $0.095$ |

**Interpretation.** Each additional badge increases the log-odds of participating in Thunder Training by 0.342 (equivalently, the odds ratio is $e^{0.342} \approx 1.41$). Having a Ground-type Pokemon increases the odds by a factor of $e^{0.614} \approx 1.85$, which makes sense: trainers who already have a type advantage against Electric types may be particularly interested in learning to exploit it.

For a specific trainer — say, Alice with 4 badges, team level 32, 150 battles, strategy score 68, electric knowledge 7, Ground-type present, 8 items, 45 hours training, and 62 Pokedex entries — the estimated propensity score is:

$$\hat{e}(X_{\text{Alice}}) = \text{logit}^{-1}(-4.821 + 0.342(4) + 0.058(32) + 0.004(150) + 0.031(68) + 0.189(7) + 0.614(1) + 0.023(8) + 0.007(45) + 0.005(62))$$

$$= \text{logit}^{-1}(-4.821 + 1.368 + 1.856 + 0.600 + 2.108 + 1.323 + 0.614 + 0.184 + 0.315 + 0.310)$$

$$= \text{logit}^{-1}(3.857) = \frac{1}{1 + e^{-3.857}} = 0.979$$

Alice is almost certainly a Thunder Training participant, which is consistent with her strong profile.

### Checking Overlap

Before using propensity scores for matching, we must verify the **overlap** (common support) assumption: the propensity score distributions for treated and control groups must overlap substantially. If there are regions where the propensity score is near 0 or 1, there are treated units with no comparable controls (or vice versa), and matching in those regions is unreliable.

A summary of the propensity score distribution in our S.S. Anne data:

| Statistic | Treated ($D=1$) | Control ($D=0$) |
|-----------|:---------------:|:---------------:|
| Min | 0.08 | 0.02 |
| Q1 | 0.35 | 0.12 |
| Median | 0.58 | 0.25 |
| Q3 | 0.78 | 0.42 |
| Max | 0.98 | 0.89 |

The distributions overlap in the range $[0.08, 0.89]$. Treated trainers with propensity scores above 0.89 have no comparable controls; these units are in the region of *non-overlap* and should be handled carefully (trimmed, or given a sensitivity analysis).

### What the Propensity Score Does and Does Not Do

The propensity score is a powerful tool, but it is essential to understand its limitations:

**What it does:**
- Balances *observed* covariates between treated and control groups.
- Reduces a multi-dimensional matching problem to a one-dimensional one.
- Enables consistent estimation of causal effects under the assumption that all confounders are observed.

**What it does NOT do:**
- Balance *unobserved* covariates. If a confounder is missing from the propensity score model, matching on the score does not adjust for it.
- Guarantee that the propensity score model is correctly specified. If the true model involves interactions or nonlinearities that the logistic regression omits, the estimated score may fail to balance covariates.
- Eliminate all sources of bias. The propensity score is only as good as the conditional ignorability assumption. If that assumption fails, no propensity score method can save us.

> **Blue's Mistake: "The Score Handles Everything"**
>
> Blue has heard about propensity scores and is excited. "So I just run a logistic regression, compute the score, and match on it? That handles all confounding?"
>
> "Only confounding from *observed* variables," Red corrects. "If there's a confounder you didn't include in your model — like natural talent or patience — the propensity score won't help."
>
> "But my model has an $R^2$ of 0.35! That's pretty good!"
>
> "The $R^2$ of your propensity score model is irrelevant to whether you've captured all confounders. A model that perfectly predicts treatment based on five variables still misses the sixth if you didn't include it. Propensity scores balance what you put in. They have no magical power over what you leave out."

---

## 4.5 Propensity Score Matching

### The Procedure

With estimated propensity scores in hand, we can match treated and control units on this single dimension:

> **Definition 4.6 (Propensity Score Matching).** For each treated unit $i$, find the control unit $j$ that minimizes $|\hat{e}(X_i) - \hat{e}(X_j)|$. The PSM estimator of the ATT is:
>
> $$\widehat{\text{ATT}}_{\text{PSM}} = \frac{1}{n_1} \sum_{i: D_i = 1} \left( Y_i - Y_{j(i)} \right)$$

As with Mahalanobis matching, we must choose:

1. **1:1 or $k$:1 matching**: More matches per treated unit reduces variance but may introduce worse matches.
2. **With or without replacement**: With replacement generally yields better matches but complicates variance estimation.
3. **Caliper**: A maximum allowable distance on the propensity score scale (commonly 0.2 SD of the logit propensity score).

### Greedy vs. Optimal Matching

**Greedy (nearest-neighbor) matching** proceeds sequentially: for each treated unit (in some order), find the closest available control. This is fast but can produce suboptimal pairings — the first treated unit may "steal" a control that would have been a better match for a later treated unit.

**Optimal matching** minimizes the total distance across all matched pairs simultaneously, solving a combinatorial optimization problem (typically a minimum-cost flow problem). This guarantees the globally best set of pairings but is computationally more expensive. For most datasets of moderate size, optimal matching is feasible and preferred.

### Worked Example

Let us trace through propensity score matching for a small subset of S.S. Anne passengers. Consider five treated and eight control trainers:

| Trainer | $D$ | $\hat{e}(X)$ | Gym Score ($Y$) |
|---------|:---:|:-------------:|:---------------:|
| T1 | 1 | 0.72 | 78 |
| T2 | 1 | 0.45 | 65 |
| T3 | 1 | 0.61 | 71 |
| T4 | 1 | 0.83 | 82 |
| T5 | 1 | 0.38 | 60 |
| C1 | 0 | 0.40 | 58 |
| C2 | 0 | 0.69 | 70 |
| C3 | 0 | 0.55 | 63 |
| C4 | 0 | 0.22 | 48 |
| C5 | 0 | 0.47 | 62 |
| C6 | 0 | 0.75 | 72 |
| C7 | 0 | 0.60 | 64 |
| C8 | 0 | 0.34 | 55 |

**1:1 nearest-neighbor matching without replacement:**

| Treated | $\hat{e}$ | Best Match | $\hat{e}$ (match) | $|\Delta \hat{e}|$ | $Y_T$ | $Y_C$ | $Y_T - Y_C$ |
|---------|:---------:|:----------:|:-----------------:|:-------------------:|:------:|:------:|:------------:|
| T1 | 0.72 | C6 | 0.75 | 0.03 | 78 | 72 | +6 |
| T2 | 0.45 | C5 | 0.47 | 0.02 | 65 | 62 | +3 |
| T3 | 0.61 | C7 | 0.60 | 0.01 | 71 | 64 | +7 |
| T4 | 0.83 | C2 | 0.69 | 0.14 | 82 | 70 | +12 |
| T5 | 0.38 | C1 | 0.40 | 0.02 | 60 | 58 | +2 |

$$\widehat{\text{ATT}} = \frac{6 + 3 + 7 + 12 + 2}{5} = \frac{30}{5} = 6.0$$

Note that T4's match (C2, $\hat{e} = 0.69$) is the weakest — the distance is 0.14. If we had used a caliper of 0.10, T4 would have gone unmatched, and the ATT would have been estimated from only 4 pairs:

$$\widehat{\text{ATT}}_{\text{caliper}} = \frac{6 + 3 + 7 + 2}{4} = 4.5$$

The choice of caliper thus affects both the estimate and the estimand (the population for which the ATT is estimated).

### The Abadie and Imbens Warning

Abadie and Imbens (2016) proved a cautionary result: propensity score matching can *increase* the distance between matched units on the original covariates, even when the propensity scores are close. Two trainers with $\hat{e} = 0.50$ might have arrived at that score via very different covariate profiles — one with many badges but low strategy, another with few badges but high strategy.

> **Definition 4.7 (The PSM Imbalance Risk, Abadie & Imbens, 2016).** Matching on the estimated propensity score does not generally minimize covariate imbalance. If the propensity score model is misspecified, PSM can increase the mean squared difference in covariates between matched pairs relative to the unmatched sample.

This result has led some methodologists — most notably King and Nielsen (2019) — to argue that propensity score matching should be used with caution, and that direct covariate matching (e.g., Mahalanobis distance, CEM) may be preferable when the number of covariates is manageable.

The practical recommendation: after propensity score matching, *always* check covariate balance (Section 4.7). If balance is poor, the propensity score model may need re-specification.

### Standard Error Estimation

Standard errors for matching estimators are subtle. The naive formula — treating matched pairs as independent — ignores two sources of uncertainty:

1. **Estimation of the propensity score.** The score is estimated, not known, and this estimation uncertainty should propagate into the standard error of the ATT.
2. **Matching with replacement.** When a control unit is used multiple times, the effective sample size is reduced, and observations are no longer independent.

Abadie and Imbens (2006) derived analytical standard errors for nearest-neighbor matching estimators that account for matching uncertainty. In practice, many analysts use **bootstrap** standard errors, though Abadie and Imbens (2008) showed that the standard bootstrap is not valid for nearest-neighbor matching without modification. The subsampling bootstrap or the analytical formula should be used instead.

---

## 4.6 Subclassification / Stratification

### The Idea

Instead of finding a single matched partner for each treated unit, **subclassification** (also called **stratification**) divides the propensity score into strata and computes the treatment effect *within* each stratum.

> **Definition 4.8 (Subclassification on the Propensity Score).** Divide the estimated propensity score into $S$ strata defined by cutpoints $c_0 < c_1 < \cdots < c_S$. Within stratum $s$, estimate the treatment effect as:
>
> $$\hat{\tau}_s = \bar{Y}_{1s} - \bar{Y}_{0s}$$
>
> The ATT is estimated as a weighted average:
>
> $$\widehat{\text{ATT}}_{\text{sub}} = \sum_{s=1}^{S} \frac{n_{1s}}{n_1} \hat{\tau}_s$$
>
> where $n_{1s}$ is the number of treated units in stratum $s$ and $n_1 = \sum_s n_{1s}$.

### Cochran's Rule of Five

A classical result due to Cochran (1968) provides practical guidance: subclassification into **five strata** based on a single confounding covariate removes approximately 90% of the bias due to that covariate. With the propensity score summarizing multiple covariates, five to ten strata are typically sufficient for substantial bias reduction.

### Worked Example

We divide the estimated propensity scores from our S.S. Anne data into five quintile-based strata:

| Stratum | $\hat{e}$ Range | Treated ($n_{1s}$) | Control ($n_{0s}$) | $\bar{Y}_{1s}$ | $\bar{Y}_{0s}$ | $\hat{\tau}_s$ |
|:-------:|:---------------:|:------------------:|:------------------:|:---------------:|:---------------:|:--------------:|
| 1 | [0.02, 0.20) | 8 | 72 | 52.3 | 47.1 | 5.2 |
| 2 | [0.20, 0.35) | 22 | 68 | 59.8 | 53.6 | 6.2 |
| 3 | [0.35, 0.55) | 38 | 52 | 66.4 | 60.1 | 6.3 |
| 4 | [0.55, 0.75) | 48 | 36 | 73.2 | 66.8 | 6.4 |
| 5 | [0.75, 0.98] | 44 | 12 | 80.5 | 73.3 | 7.2 |

The ATT estimate via subclassification:

$$\widehat{\text{ATT}}_{\text{sub}} = \frac{8}{160}(5.2) + \frac{22}{160}(6.2) + \frac{38}{160}(6.3) + \frac{48}{160}(6.4) + \frac{44}{160}(7.2)$$

$$= 0.050(5.2) + 0.138(6.2) + 0.238(6.3) + 0.300(6.4) + 0.275(7.2)$$

$$= 0.260 + 0.856 + 1.499 + 1.920 + 1.980 = 6.52$$

This estimate of 6.52 points is substantially smaller than the naive difference of 14.3 points, confirming that much of the raw gap was due to selection bias. The matching estimate of 6.0 from Section 4.5 is similar, providing reassuring convergence across methods.

### Advantages Over Matching

Subclassification has several practical advantages:

1. **No units are discarded.** Every treated and control unit appears in exactly one stratum (assuming overlap). This preserves the full sample, unlike matching with calipers which can discard treated units.
2. **Computational simplicity.** No optimization problem is required — just sorting and stratifying.
3. **Transparency.** The within-stratum comparisons are easy to inspect. If one stratum shows a wildly different treatment effect, it may signal model misspecification or effect heterogeneity.
4. **Variance estimation is straightforward.** Standard errors can be computed within each stratum using conventional formulas and combined using the delta method.

The main disadvantage is *residual confounding*: within each stratum, the propensity score is not perfectly constant, so some covariate imbalance may remain. Using more strata mitigates this but reduces the sample size per stratum.

---

## 4.7 Covariate Balance Assessment

Matching and subclassification aim to eliminate covariate imbalance between treated and control groups. The most important diagnostic step is to verify that they succeeded. Unlike regression, where model fit is assessed via residuals and $R^2$, matching quality is assessed via **covariate balance**.

### Standardized Mean Difference

The primary balance metric is the **Standardized Mean Difference (SMD)**:

> **Definition 4.9 (Standardized Mean Difference).** For covariate $X_k$, the SMD is:
>
> $$\text{SMD}_k = \frac{\bar{X}_{k,1} - \bar{X}_{k,0}}{\sqrt{(s_{k,1}^2 + s_{k,0}^2) / 2}}$$
>
> where $\bar{X}_{k,1}$ and $\bar{X}_{k,0}$ are the covariate means in the treated and matched control groups, and $s_{k,1}^2$ and $s_{k,0}^2$ are the corresponding variances.

The SMD expresses the group difference in standard deviation units, making it comparable across covariates measured on different scales. A widely used rule of thumb (Rosenbaum & Rubin, 1985; Austin, 2009):

- $|\text{SMD}| < 0.1$: **Good balance**. Negligible difference.
- $0.1 \leq |\text{SMD}| < 0.25$: **Moderate imbalance**. May warrant concern.
- $|\text{SMD}| \geq 0.25$: **Substantial imbalance**. The matching has failed to adequately balance this covariate.

### Variance Ratios

In addition to means, we should check that the *variances* of covariates are similar across groups. The **variance ratio** is:

$$\text{VR}_k = \frac{s_{k,1}^2}{s_{k,0}^2}$$

A ratio near 1.0 indicates balanced variances. Rubin (2001) recommends that variance ratios fall between 0.5 and 2.0. A variance ratio far from 1 suggests that matching has created groups with different distributional shapes, even if the means are balanced.

### Balance Table: Before and After Matching

The following table summarizes covariate balance for the S.S. Anne data before matching and after 1:1 propensity score matching:

| Covariate | Before Matching | | After Matching | |
|-----------|:---:|:---:|:---:|:---:|
| | SMD | VR | SMD | VR |
| `badges` | 0.85 | 1.12 | 0.04 | 0.98 |
| `team_level` | 0.91 | 0.87 | 0.06 | 1.03 |
| `battle_exp` | 0.78 | 1.45 | 0.08 | 1.11 |
| `strategy_score` | 0.82 | 0.93 | 0.05 | 0.97 |
| `electric_knowledge` | 0.72 | 1.08 | 0.03 | 1.01 |
| `has_ground_type` | 0.58 | — | 0.07 | — |
| `items_carried` | 0.21 | 1.22 | 0.02 | 1.04 |
| `hours_training` | 0.64 | 1.31 | 0.09 | 1.08 |
| `pokedex_count` | 0.43 | 0.91 | 0.06 | 0.99 |

Before matching, every covariate shows substantial imbalance (SMDs ranging from 0.21 to 0.91). After matching, all SMDs fall below 0.10 and all variance ratios are between 0.5 and 2.0. This is excellent balance.

### Love Plots

A **Love plot** (named after Thomas Love) is a horizontal dot plot that displays the SMD for each covariate, with markers for "before matching" and "after matching." Vertical reference lines are drawn at $\pm 0.1$ (or $\pm 0.25$) to indicate the balance threshold.

```
                         Love Plot: Covariate Balance
                 ─0.25          0.0          +0.25         +0.50         +0.75         +1.0
                   │              │              │              │              │              │
    badges         │          ●   │              │              │              │    ○         │
    team_level     │          ●   │              │              │              │     ○        │
    battle_exp     │           ●  │              │              │          ○   │              │
    strategy_score │          ●   │              │              │              │    ○         │
    elec_knowledge │         ●    │              │              │         ○    │              │
    has_ground     │           ●  │              │              │    ○         │              │
    items_carried  │          ●   │              │              │              │              │
                   │              │         ○    │              │              │              │
    hours_training │           ●  │              │              │       ○      │              │
    pokedex_count  │           ●  │              │         ○    │              │              │
                   │              │              │              │              │              │
                   └──────────────┼──────────────┘              
                            ● After    ○ Before
                            Dashed lines at ±0.1
```

In a proper graphical implementation (see the companion Jupyter notebook), the Love plot provides an immediate visual summary: all "after" markers should cluster near zero, while the "before" markers may be scattered far from zero.

### What to Do When Balance Is Poor

If matching fails to achieve adequate balance on one or more covariates, the analyst should:

1. **Re-specify the propensity score model.** Add interaction terms (e.g., `badges` $\times$ `team_level`), polynomial terms (e.g., `battle_exp`$^2$), or additional covariates that were initially excluded.

2. **Try a different matching method.** If propensity score matching produces poor balance, consider Mahalanobis distance matching, CEM, or a combination (e.g., Mahalanobis matching within propensity score calipers).

3. **Use a tighter caliper.** Reducing the caliper width forces closer matches but at the cost of losing some treated units.

4. **Increase the matching ratio.** Moving from 1:1 to $k$:1 matching can improve balance by averaging over multiple controls.

5. **Consider alternative estimators.** If matching proves difficult, inverse probability weighting (Chapter 5) or doubly robust estimation may be more appropriate.

> **Professor Oak Explains: Balance, Not Prediction**
>
> "A common misunderstanding is that the propensity score model should be evaluated by how well it *predicts* treatment assignment," Professor Oak cautions. "In fact, the goal is not prediction but *balance*. A model with a modest pseudo-$R^2$ but excellent covariate balance is preferable to one with a high pseudo-$R^2$ but residual imbalance."
>
> "This is why we assess matching quality through balance diagnostics — SMDs, variance ratios, Love plots — rather than model fit statistics. The propensity score is a *tool for balance*, not a prediction model. Its quality is judged entirely by whether it achieves balance."

---

## 4.8 Limitations of Matching

Matching is intuitive, transparent, and powerful. But like every method in causal inference, it rests on assumptions that may be violated. Understanding these limitations is essential for responsible application — and for knowing when to reach for other tools.

### The Critical Assumption: No Unobserved Confounders

Matching adjusts for *observed* covariates. The validity of matching-based causal estimates depends entirely on the **conditional ignorability** assumption:

$$Y(0), Y(1) \perp D \mid X$$

If there exists a confounder $U$ that affects both treatment and outcome but is not included in $X$, matching on $X$ alone does not eliminate the bias.

**The S.S. Anne Unmasking.** Suppose that two variables we *did not observe* also influence both Thunder Training participation and Gym performance:

- **Patience** ($U_1$): patient trainers are more likely to complete a week-long training program *and* more likely to persevere through a difficult Gym battle.
- **Natural Talent** ($U_2$): naturally talented trainers are drawn to intensive training *and* perform better in any battle, regardless of training.

The true causal DAG includes:

```
                badges ──────→ Thunder Training ──────→ Gym Score
                  ↑                  ↑                     ↑
              team_level        patience (U₁)        patience (U₁)
                  ↑                  ↑                     ↑
            battle_exp        nat. talent (U₂)      nat. talent (U₂)
                  ↑
          strategy_score
                  ↑
         electric_knowledge
```

Because $U_1$ and $U_2$ are unobserved, they do not appear in our propensity score model. Matching on observed covariates does not block the backdoor paths through $U_1$ and $U_2$. Our estimated ATT of approximately 6.0-6.5 points is *biased upward*: part of it reflects the advantage that patient, naturally talented trainers have even without Thunder Training.

If the true causal effect is, say, 4.0 points, then roughly 2.0-2.5 points of our estimate is residual confounding bias due to the unobserved variables. No amount of re-specifying the propensity score model or trying different matching algorithms can fix this — the problem is in the data, not the method.

### Positivity Violations

The **overlap** assumption requires that for every covariate pattern observed among the treated, there is a non-zero probability of being a control. In practice, this fails in predictable ways:

- **Structural violations:** Some trainers may *always* or *never* participate in Thunder Training given their characteristics. For example, trainers with zero badges and team level below 15 may never have been offered the program (selection by the cruise director). These trainers have $e(X) = 0$, and no matching can create comparisons for treated units in this region.

- **Random violations:** Even without structural reasons, small sample sizes can produce regions of covariate space where only treated or only control units are observed.

Positivity violations manifest as extreme propensity scores (near 0 or 1) and require the analyst to either trim the sample (restricting inference to the region of overlap) or use extrapolation-based methods (regression), which introduce model dependence.

### Model Dependence

Ho, Imai, King, and Stuart (2007) demonstrated that when matching is imperfect — when matched units still differ on covariates — the treatment effect estimate can be sensitive to how the researcher handles this residual imbalance. Different matching specifications (1:1 vs. 5:1, with vs. without replacement, different calipers) can yield different results.

This **model dependence** is not unique to matching — regression suffers from it too — but it means that analysts should report results across multiple reasonable specifications. If the conclusions are robust across specifications, we can be more confident. If they vary substantially, the evidence is weaker.

### From Matching to Stronger Designs

These limitations of matching are not reasons to abandon it. Matching remains one of the most transparent and interpretable methods for observational causal inference. But they motivate the tools we will develop in subsequent chapters:

- **Chapter 5 (Celadon City)** introduces **regression** and **inverse probability weighting** as alternatives to matching, and shows how combining them yields **doubly robust** estimators that are consistent if *either* the outcome model or the propensity score model is correctly specified.

- **Chapter 6 (Fuchsia & Cinnabar)** introduces **instrumental variables**, which can identify causal effects even in the presence of unobserved confounders — precisely the scenario where matching fails. The key is finding a variable that affects treatment but has no direct effect on the outcome.

- **Sensitivity analysis** techniques (which we will encounter along the way) allow us to ask: "How strong would an unobserved confounder have to be to overturn our conclusions?" If the answer is "implausibly strong," we can be more confident despite the theoretical vulnerability.

> **Professor Oak Explains: Matching Is a Design, Not Just an Estimator**
>
> "I want to emphasize something that many researchers overlook," Professor Oak says. "Matching is not just a statistical technique — it is a *research design*. When you match, you are constructing a comparison group that approximates what a randomized experiment would have produced. This is a design step, just as choosing your sample or your treatment is a design step."
>
> "The practical implication is that matching should be done *before* looking at outcomes. Assess covariate balance, iterate on the propensity score model, try different matching specifications — all without peeking at $Y$. Only after you are satisfied with the matched sample should you estimate the treatment effect. This separation of design and analysis protects against the temptation to choose the matching specification that gives the 'best' result."

---

## Chapter Summary

<!-- FIG-CH04-BADGE -->
<figure style="text-align:center; margin:1.5em auto;">
<img src="../../assets/badges/thunder_badge.png" alt="Thunder Badge" style="width:140px; display:block; margin:0 auto;">
<figcaption><strong>Thunder Badge earned!</strong></figcaption>
</figure>


In this chapter, we explored the family of matching methods for causal inference in observational studies, using the S.S. Anne Thunder Training study as our running example.

**Key concepts:**

1. **Matching intuition.** Compare treated units to untreated units that are similar on observed covariates. This approximates the comparison that a randomized experiment would provide.

2. **Exact and Coarsened Exact Matching.** Exact matching requires identical covariate values, which is infeasible in high dimensions. CEM coarsens covariates into bins and matches exactly on bins, offering a transparent bias-variance tradeoff.

3. **Distance-based matching.** The Mahalanobis distance accounts for covariate scaling and correlations. Nearest-neighbor matching (with or without replacement, with or without calipers) finds close matches in covariate space.

4. **The propensity score.** The probability of treatment given covariates, $e(X) = P(D=1|X)$. The Rosenbaum-Rubin theorem shows that conditioning on this scalar is sufficient to eliminate confounding from observed variables. Typically estimated via logistic regression.

5. **Propensity score matching.** Match treated and control units on estimated propensity scores. Computationally simple but may increase covariate imbalance if the score model is misspecified (Abadie & Imbens, 2016).

6. **Subclassification.** Divide the propensity score into strata, estimate effects within strata, and combine. Uses all observations and avoids discarding data.

7. **Covariate balance assessment.** Standardized mean differences, variance ratios, and Love plots are essential diagnostics. The goal of matching is balance, not prediction.

8. **Limitations.** Matching adjusts only for observed confounders. Unobserved confounders, positivity violations, and model dependence remain threats. These motivate the methods of subsequent chapters.

**The journey so far.** In Pallet Town, we learned the language of potential outcomes. In Pewter City, we saw that randomization solves the causal inference problem by design. In Cerulean City, we learned to identify confounders using DAGs. Here in Vermilion City, we took our first step toward *adjusting* for confounders in observational data — finding each trainer's twin. But the twin we found may not be as identical as we hoped. Hidden variables lurk beneath the surface, and our next challenges will equip us with more powerful tools to confront them.

---

## Professor Oak's Review Questions

1. **Conceptual.** Explain, in your own words, why the raw difference in Gym scores between Thunder Training graduates and non-participants ($\bar{Y}_1 - \bar{Y}_0 = 14.3$) is not a valid estimate of the causal effect of Thunder Training. Decompose this difference into the ATT and the selection bias term.

2. **Matching mechanics.** Suppose you have three covariates, each taking 5 possible values. How many cells does the exact matching table have? If you have 200 treated units and 300 control units, what fraction of cells do you expect to contain at least one treated *and* one control unit? What does this imply for the feasibility of exact matching?

3. **Propensity score theory.** State the balancing property of the propensity score. Why does this property imply that conditioning on $e(X)$ is sufficient for causal identification, even though $e(X)$ is a scalar summary of a vector $X$?

4. **Critical thinking.** Blue matches treated and control trainers on their propensity scores and finds that balance on `strategy_score` is poor (SMD = 0.32). He declares that the propensity score "doesn't work." What are three concrete steps he should take before abandoning the method?

5. **Assumptions.** Suppose an unobserved variable, `motivation`, influences both the decision to undertake Thunder Training and performance at the Vermilion Gym. Draw the DAG including this variable. Does matching on observed covariates block the backdoor path through `motivation`? What methods from later chapters might address this problem?

6. **Subclassification.** Cochran (1968) showed that five strata remove approximately 90% of bias from a single covariate. Does this guarantee vanish if the propensity score model is misspecified? Why or why not?

---

## Trainer Challenge Exercises

**Exercise 4.1: Computing Mahalanobis Distances**

Consider the following four trainers and two covariates:

| Trainer | Treatment | Badges ($X_1$) | Strategy ($X_2$) |
|---------|:---------:|:---:|:---:|
| Ash | 1 | 3 | 72 |
| Misty | 0 | 5 | 65 |
| Brock | 0 | 4 | 70 |
| Erika | 0 | 2 | 78 |

The covariance matrix is:

$$\Sigma = \begin{pmatrix} 1.5 & -3.0 \\ -3.0 & 28.0 \end{pmatrix}$$

(a) Compute $\Sigma^{-1}$.

(b) Compute the Mahalanobis distance from Ash to each control trainer (Misty, Brock, Erika).

(c) Which trainer is Ash's nearest neighbor? Is this the same trainer who would be selected by Euclidean distance?

(d) Explain intuitively why the Mahalanobis distance might differ from the Euclidean distance in this case.

---

**Exercise 4.2: Propensity Score Estimation and Matching**

A logistic regression for Thunder Training participation yields the following model:

$$\log \frac{e(X)}{1 - e(X)} = -3.5 + 0.40 \cdot \text{badges} + 0.05 \cdot \text{team\_level} + 0.25 \cdot \text{has\_ground}$$

Consider the following six trainers:

| Trainer | $D$ | Badges | Team Level | Has Ground | $Y$ |
|---------|:---:|:------:|:----------:|:----------:|:---:|
| A | 1 | 4 | 30 | 1 | 75 |
| B | 1 | 3 | 35 | 0 | 68 |
| C | 1 | 5 | 28 | 1 | 80 |
| D | 0 | 3 | 32 | 1 | 62 |
| E | 0 | 4 | 25 | 0 | 58 |
| F | 0 | 2 | 38 | 1 | 55 |

(a) Compute the estimated propensity score $\hat{e}(X)$ for each trainer.

(b) Perform 1:1 nearest-neighbor matching (without replacement) on the propensity score, matching each treated trainer to a control.

(c) Compute the matched ATT estimate.

(d) Assess covariate balance before and after matching by computing the SMD for each covariate. Does matching improve balance?

---

**Exercise 4.3: Subclassification**

Using the estimated propensity scores from the full S.S. Anne dataset (provided in the companion notebook), divide the sample into 5 strata based on quintiles of the propensity score distribution.

(a) Compute the number of treated and control units in each stratum. Are there any strata with very few treated or very few control units?

(b) Compute the within-stratum treatment effect $\hat{\tau}_s$ for each stratum.

(c) Compute the overall ATT using the subclassification formula. Compare this to the matching estimate from Section 4.5.

(d) Now divide the sample into 10 strata instead of 5. How does the ATT estimate change? What happens to the standard error?

---

**Exercise 4.4: Balance Table Construction**

Using the matched sample from Exercise 4.2 (or the full matched S.S. Anne sample from the companion notebook):

(a) Construct a complete balance table showing, for each covariate: the treated mean, the control mean, the SMD, and the variance ratio, both before and after matching.

(b) Create a Love plot visualizing the SMDs before and after matching.

(c) Identify any covariates with $|\text{SMD}| > 0.1$ after matching. For each such covariate, propose a modification to the propensity score model that might improve balance (e.g., adding an interaction term, a polynomial, or re-specifying the functional form).

---

## Further Reading

- **Rosenbaum, P. R. & Rubin, D. B. (1983).** "The Central Role of the Propensity Score in Observational Studies for Causal Effects." *Biometrika*, 70(1), 41-55. The foundational paper introducing the propensity score and proving the balancing theorem.

- **Iacus, S. M., King, G., & Porro, G. (2012).** "Causal Inference without Balance Checking: Coarsened Exact Matching." *Political Analysis*, 20(1), 1-24. Introduces CEM and the concept of monotone imbalance bounding.

- **Stuart, E. A. (2010).** "Matching Methods for Causal Inference: A Review and a Look Forward." *Statistical Science*, 25(1), 1-21. An excellent comprehensive review of matching methods.

- **Abadie, A. & Imbens, G. W. (2006).** "Large Sample Properties of Matching Estimators for Average Treatment Effects." *Econometrica*, 74(1), 235-267. Derives the asymptotic properties and standard errors of matching estimators.

- **Abadie, A. & Imbens, G. W. (2016).** "Matching on the Estimated Propensity Score." *Econometrica*, 84(2), 781-807. Shows that propensity score matching can increase covariate imbalance under misspecification.

- **Ho, D. E., Imai, K., King, G., & Stuart, E. A. (2007).** "Matching as Nonparametric Preprocessing for Reducing Model Dependence in Parametric Causal Inference." *Political Analysis*, 15(3), 199-236. Argues for matching as a preprocessing step to reduce model dependence in subsequent regression.

- **King, G. & Nielsen, R. (2019).** "Why Propensity Scores Should Not Be Used for Matching." *Political Analysis*, 27(4), 435-454. A provocative critique arguing that PSM can increase imbalance, approximates a random experiment poorly, and should be replaced by other methods.

- **Cochran, W. G. (1968).** "The Effectiveness of Adjustment by Subclassification in Removing Bias in Observational Studies." *Biometrics*, 24(2), 295-313. The classic result that five strata remove approximately 90% of bias.

- **Austin, P. C. (2011).** "An Introduction to Propensity Score Methods for Reducing the Effects of Confounding in Observational Studies." *Multivariate Behavioral Research*, 46(3), 399-424. An accessible introduction to propensity score methods for applied researchers.

---

## Skills to Practice in the Notebook

The notebook `notebooks/ch04_vermilion_city.ipynb` is where matching stops being a diagram and becomes an estimator. Complete each of the following to claim the Thunder Badge:

1. **Implement exact matching from scratch.** Given a dataset with a discrete covariate (e.g., hometown), pair each treated unit with controls that share the same value. Compute the matched ATT as the mean of within-pair differences. No library — do it in pandas first.

2. **Compute Mahalanobis distances and do 1:1 nearest-neighbor matching.** Use `scipy.spatial.distance.mahalanobis` (or your own implementation) to find the closest control for each treated unit on a small set of covariates. Then pair outcomes and compute $\hat{\tau}_{ATT}$. Do this both *with* and *without* replacement and compare.

3. **Estimate a propensity score.** Fit a logistic regression (or a gradient boosted classifier) for $P(D=1 \mid X)$. Plot overlap: histograms of $\hat{e}(X)$ for treated and control. Be able to *spot* positivity violations visually.

4. **Do propensity score matching with a caliper.** Match each treated unit to its nearest control within a caliper of $0.2 \times \text{SD}(\text{logit}(\hat{e}))$. Count how many treated units are dropped. Compute the caliper-matched ATT.

5. **Check balance before and after matching.** For every covariate, compute the standardized mean difference (SMD) in the raw data and in the matched sample. Plot a "love plot" (SMD before vs. after) and know what "success" looks like (all SMDs below 0.1).

6. **Run subclassification / stratification.** Split the sample into 5 propensity-score bins. Within each bin, compute a treated-vs-control difference. Combine bin-level estimates into an overall ATE and ATT using the appropriate weights. Compare against the matched estimate.

7. **Complete the Trainer Challenge Exercises.** The notebook walks you through: (a) rebuilding the Rosenbaum-Rubin balancing result in simulation, (b) showing how caliper width trades off bias vs. variance empirically, and (c) diagnosing a dataset where matching *fails* because positivity is violated.

---

## Check Your Understanding

Before challenging Lt. Surge, work through these. Matching is the foundation for Chapter 5's regression adjustment and the weighting methods in Chapter 6 — do not move forward with gaps.

**Questions you should be able to answer out loud, without notes:**

- Why do we match? What is the "counterfactual twin" intuition in one sentence?
- State the ignorability assumption $(Y_i(0), Y_i(1)) \perp\!\!\!\perp D_i \mid X_i$ and say precisely what matching assumes and does not assume.
- Why does the curse of dimensionality make exact matching on many covariates impractical?
- Define the Mahalanobis distance and explain in plain English what the $\Sigma^{-1}$ factor *does* (why not just Euclidean distance?).
- Define the propensity score $e(X) = P(D = 1 \mid X)$. Why is it a *balancing* score rather than a *prediction* score?
- State the Rosenbaum-Rubin theorem in one sentence. What's the practical payoff?
- What is positivity? Why do $e(X)$ values near 0 or 1 break matching?
- Compare matching with replacement and without replacement. When does each win?
- What does a caliper do, and what is the bias-variance tradeoff it controls?
- What is the standardized mean difference (SMD), and what threshold flags "acceptable balance"?
- Why does matching target the ATT rather than the ATE, and how would you adapt the method to estimate the ATE instead?
- Name three ways matching can fail even when the code runs cleanly. (Hidden bias, poor overlap, model misspecification of $e(X)$, etc.)

**Tasks you should be able to perform in code:**

- Fit a propensity score model, plot the overlap histogram, and flag units with $\hat{e}(X) < 0.05$ or $> 0.95$.
- Do 1:1 and $k$:1 nearest-neighbor matching (with and without replacement) using a Mahalanobis or propensity-score distance.
- Compute the ATT from a matched sample and get a valid (Abadie-Imbens) standard error — or at least a bootstrap one.
- Compute SMDs for every covariate, pre- and post-match, and draw the love plot.
- Run propensity-score subclassification with $K$ bins and aggregate to ATT and ATE.
- Spot and *report* a positivity violation in the data rather than silently ignoring it.

Do all this and the Thunder Badge is yours.

---

## Badge Earned: Thunder Badge

```
    ╔══════════════════════════════════════════════╗
    ║                                              ║
    ║            ⚡  THUNDER BADGE  ⚡              ║
    ║                                              ║
    ║   Awarded for mastering matching methods,    ║
    ║   propensity scores, and the art of finding  ║
    ║   each trainer's counterfactual twin.         ║
    ║                                              ║
    ║   Bearer understands:                        ║
    ║     • Exact, coarsened, and distance matching ║
    ║     • The Rosenbaum-Rubin balancing theorem   ║
    ║     • Propensity score estimation & matching  ║
    ║     • Subclassification / stratification      ║
    ║     • Covariate balance diagnostics           ║
    ║     • Limitations of selection on observables ║
    ║                                              ║
    ║          Lt. Surge, Vermilion City            ║
    ╚══════════════════════════════════════════════╝
```

---

## Next Stop: Celadon City

*Celadon City's Department Store has everything a trainer could want — potions, TMs, evolution stones, and an overwhelming number of choices. But who buys what, and why? When we observe trainers purchasing Rare Candies and later winning battles, how do we separate the effect of the candy from the wealth and experience that let them afford it in the first place? The answer will teach you about regression, inverse probability weighting, and the art of being doubly robust — building an estimator that works even when you get one of your models wrong. Grab your shopping list and your covariance matrix. The Celadon Department Store awaits...*
