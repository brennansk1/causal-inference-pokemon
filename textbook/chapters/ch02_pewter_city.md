# Chapter 2: Pewter City — Randomized Experiments

<!-- FIG-CH02-ONIX -->
<figure style="margin:1.5em auto; max-width:180px; text-align:center;">
<img src="../../assets/sprites/front/95.png" alt="Onix" style="width:160px; display:block; margin:0 auto; image-rendering: pixelated;">
<figcaption style="font-size:0.85em;"><strong>#095 Onix</strong></figcaption>
</figure>


<!-- FIG-CH02-ROCKTYPE -->
<figure style="margin:1em auto; max-width:110px; text-align:center;">
<img src="../../assets/sprites/types/rock.png" alt="Rock-type — Brock's specialty" style="width:90px; display:block; margin:0 auto;">
<figcaption style="font-size:0.85em;">Rock-type — Brock's specialty</figcaption>
</figure>


<!-- FIG-CH02-BROCK -->
<figure style="margin:1.5em auto; max-width:160px; text-align:center;">
<img src="../../assets/characters/brock.png" alt="Brock, Pewter Gym Leader" style="width:140px; display:block; margin:0 auto; image-rendering: pixelated;">
<figcaption style="font-size:0.85em;">Brock, Pewter Gym Leader</figcaption>
</figure>


> *"The best time to plant a tree was twenty years ago. The best way to test a supplement is a randomized experiment."*
> — Professor Oak, Kanto Regional Laboratory

---

You have arrived in Pewter City. The rocky terrain gives way to a modest settlement built around the famous Pewter City Gym, home to Brock, the Rock-type specialist. But before you challenge Brock, there is a scientific dispute to settle — one that will teach you why the randomized controlled trial is the gold standard of causal inference.

At the Pewter City Pokemon Center, Nurse Joy has had enough. For weeks, trainers have been filing in after their battles with Brock, some triumphant, others carrying fainted Pokemon. And all of them — winners and losers alike — have an opinion about **Pewter Protein**, a new supplement rumored to boost a Pokemon's Attack stat before battle.

"It definitely works," says one trainer, flexing his Machop's arm. "My Charmander hit 20% harder after one dose!"

"It's a scam," says another, nursing a wounded Pidgey. "I took it and Brock's Onix still destroyed me."

Nurse Joy has data — she has been recording outcomes for every trainer who walks through her doors — but the data is hopelessly confounded. Trainers who *choose* to buy Pewter Protein tend to be wealthier, more experienced, and more likely to have Pokemon with type advantages against Rock. Are they winning because of the Protein, or because they were going to win anyway?

Enter Professor Oak, who arrives in Pewter City for a research consultation.

"Nurse Joy," he says, adjusting his lab coat, "you don't need more data. You need *better* data. You need a **randomized controlled trial**."

---

## 2.1 Why Randomization Works

### The Coin Flip That Changes Everything

Professor Oak hands Nurse Joy a simple Poke-coin — Magikarp on one side, Gyarados on the other. "For the next 200 trainers who register for a Brock challenge," he instructs, "flip this coin. Magikarp: the trainer gets the real Pewter Protein. Gyarados: they get an identical-looking Placebo Berry — same size, same color, same taste, but no active ingredient. Don't tell them which one they received."

Nurse Joy is skeptical. "That's it? A coin flip decides who gets what?"

"That," Professor Oak replies, "is the most powerful tool in all of causal inference."

### Independence of Potential Outcomes and Treatment

Recall from Chapter 1 that every trainer $i$ has two **potential outcomes**: $Y_i(1)$, the outcome they would experience if they received Pewter Protein (treatment), and $Y_i(0)$, the outcome under the Placebo Berry (control). The individual causal effect is $\tau_i = Y_i(1) - Y_i(0)$, and the **Average Treatment Effect (ATE)** is:

$$\tau = E[Y_i(1) - Y_i(0)] = E[Y_i(1)] - E[Y_i(0)]$$

The **fundamental problem of causal inference** (Holland, 1986) tells us we can never observe both $Y_i(1)$ and $Y_i(0)$ for the same trainer. We only see the outcome corresponding to the treatment actually received:

$$Y_i = D_i \cdot Y_i(1) + (1 - D_i) \cdot Y_i(0)$$

where $D_i \in \{0, 1\}$ is the treatment indicator.

The question is: when we compare the average outcomes of treated trainers to control trainers, does this comparison identify the ATE? From Chapter 1, we know the naive comparison gives us:

$$E[Y_i \mid D_i = 1] - E[Y_i \mid D_i = 0] = \underbrace{E[Y_i(1) - Y_i(0) \mid D_i = 1]}_{\text{ATT}} + \underbrace{E[Y_i(0) \mid D_i = 1] - E[Y_i(0) \mid D_i = 0]}_{\text{Selection Bias}}$$

When trainers **self-select** into treatment — buying Protein of their own volition — the selection bias term is generally nonzero. But under random assignment, something remarkable happens.

> **Definition 2.1 (Random Assignment).** Treatment $D_i$ is said to be *randomly assigned* if the treatment indicator is statistically independent of the potential outcomes:
>
> $$(Y_i(0), Y_i(1)) \perp\!\!\!\perp D_i$$
>
> This means the joint distribution of potential outcomes is the same in the treatment and control groups.

When this independence condition holds, the selection bias vanishes:

$$E[Y_i(0) \mid D_i = 1] - E[Y_i(0) \mid D_i = 0] = E[Y_i(0)] - E[Y_i(0)] = 0$$

And therefore:

$$E[Y_i \mid D_i = 1] - E[Y_i \mid D_i = 0] = E[Y_i(1)] - E[Y_i(0)] = \tau$$

The simple difference in group means identifies the ATE. No regression. No fancy adjustment. Just a coin flip and a subtraction.

### Balancing Observed AND Unobserved Confounders

Why does this work so powerfully? Because the coin doesn't know anything about the trainer. It doesn't know whether they have a Water-type Pokemon (which would be devastating against Brock's Rock-types). It doesn't know their experience level, their number of gym badges, or their secret training regimen in Mt. Moon. It doesn't even know things that *we* can never measure — like the trainer's natural battle instinct, their Pokemon's hidden Individual Values (IVs), or whether they had a good night's sleep.

By assigning treatment entirely at random, we ensure that — **in expectation** — the treatment and control groups are identical on every dimension, observed and unobserved alike. This is worth pausing on, because no other method in this textbook achieves this. Every observational method we will encounter in Chapters 3 through 7 can only address *observed* confounders (or confounders with specific structural properties). Randomization handles them all.

> **Professor Oak Explains: Why "In Expectation" Matters**
>
> Randomization does not guarantee that the treatment and control groups are *perfectly* balanced in any given experiment. If you flip 200 coins, you might get 105 heads and 95 tails. By chance, the treatment group might have slightly more Water-type trainers. But the *expected* distribution is balanced, and with a large enough sample, deviations from balance become small and quantifiable. We will make this precise in Section 2.3 when we discuss variance estimation.

### Unbiasedness of the Difference-in-Means Estimator

Let us prove this formally. We have $n$ trainers, of whom $n_1$ are randomly assigned to treatment and $n_0 = n - n_1$ to control. The **difference-in-means estimator** is:

$$\hat{\tau}^{DM} = \bar{Y}_1 - \bar{Y}_0 = \frac{1}{n_1}\sum_{i: D_i = 1} Y_i - \frac{1}{n_0}\sum_{i: D_i = 0} Y_i$$

Under random assignment:

$$E[\bar{Y}_1] = E\left[\frac{1}{n_1}\sum_{i: D_i=1} Y_i\right] = E[Y_i \mid D_i = 1] = E[Y_i(1) \mid D_i = 1] = E[Y_i(1)]$$

where the last equality uses $(Y_i(0), Y_i(1)) \perp\!\!\!\perp D_i$. By the same logic:

$$E[\bar{Y}_0] = E[Y_i(0)]$$

Therefore:

$$E[\hat{\tau}^{DM}] = E[\bar{Y}_1 - \bar{Y}_0] = E[Y_i(1)] - E[Y_i(0)] = \tau$$

The difference-in-means estimator is **unbiased** for the ATE under random assignment. This is the foundational result of experimental causal inference, articulated in various forms by Fisher (1935), Neyman (1923/1990), and formalized in the modern potential outcomes framework by Rubin (1974).

### The Pewter Protein Balance Table

Nurse Joy runs the trial. Two hundred trainers walk through the doors, each receiving their coin-flip assignment. After enrollment is complete, she compiles a **balance table** — a comparison of pre-treatment characteristics across the two groups — to check whether randomization achieved approximate balance.

| Characteristic | Protein ($n_1 = 102$) | Placebo ($n_0 = 98$) | Difference | p-value |
|---|---|---|---|---|
| Mean trainer level | 14.8 | 14.3 | 0.5 | 0.52 |
| % with Water-type Pokemon | 28.4% | 26.5% | 1.9 pp | 0.76 |
| % with Grass-type Pokemon | 15.7% | 17.3% | -1.6 pp | 0.74 |
| Mean # of Pokemon on team | 3.8 | 3.9 | -0.1 | 0.67 |
| Mean prior gym badges | 0.9 | 0.8 | 0.1 | 0.41 |
| % first-time challengers | 61.8% | 64.3% | -2.5 pp | 0.71 |
| Mean Pokemon avg. level | 13.2 | 12.9 | 0.3 | 0.59 |

**Table 2.1:** Balance table for the Pewter Protein RCT. No statistically significant differences at $\alpha = 0.05$, consistent with successful randomization. (pp = percentage points.)

None of the p-values are close to significance. The groups look comparable. Of course, even if one or two covariates showed a significant imbalance by chance (which happens roughly 5% of the time per test at $\alpha = 0.05$), this would not invalidate the experiment — it is expected under the null of successful randomization.

### Blue's Mistake: Self-Selection is Not Randomization

Right as Nurse Joy is reviewing her balance table, Blue strides into the Pokemon Center, arms full of shopping bags.

> **Blue's Mistake: "I Don't Need an Experiment"**
>
> "Hey losers," Blue announces, dumping 50 boxes of Pewter Protein on the counter. "I already KNOW this stuff works. I've been using it for a week and my Squirtle is destroying everything. I don't need some nerdy experiment to tell me what's obvious."
>
> Professor Oak sighs. "Blue, you chose to buy Protein because you're wealthy, experienced, and already have a Water-type starter — the perfect counter to Brock's Rock-types. Trainers like you *would have won anyway*. Your personal experience tells us nothing about whether the Protein itself had any effect."
>
> Blue's data illustrates **self-selection bias** perfectly. Among trainers who voluntarily purchase Pewter Protein, the win rate against Brock is 78%. Among those who don't, it's 45%. But this 33 percentage point gap is a mix of the true causal effect of Protein and the fact that Protein buyers are stronger trainers to begin with.
>
> Nurse Joy's RCT tells a different story. In the randomized trial, the win rate is 52% in the Protein group and 43% in the Placebo group — a 9 percentage point difference. The true effect of Pewter Protein exists, but it's much smaller than Blue's naive comparison suggests.

The gap between Blue's estimate (33 pp) and the experimental estimate (9 pp) — a difference of 24 percentage points — is pure selection bias. This is the danger of drawing causal conclusions from observational data without proper adjustment, a theme we will return to throughout this textbook.

---

## 2.2 Experimental Design

A randomized experiment does not design itself. The coin flip is the heart of the method, but an enormous amount of thought must go into the architecture surrounding that flip. In this section, we walk through the key design decisions that Professor Oak and Nurse Joy faced when planning the Pewter Protein RCT.

### Precise Treatment Definition

A vague treatment yields vague conclusions. "Pewter Protein" could mean many things — different doses, different timings, different formulations. The treatment must be defined with surgical precision.

> **Definition 2.2 (Treatment Protocol).** The treatment in the Pewter Protein RCT is defined as:
>
> - **Treatment arm:** Exactly one tablet of Pewter Protein (10 mg, Lot #151, manufactured by Silph Co.) administered orally with 200 mL water, exactly 60 minutes before the trainer's scheduled Brock battle.
> - **Control arm:** Exactly one Placebo Berry tablet, identical in size (8 mm diameter), color (pale blue), weight (0.5 g), and taste (mild Oran Berry flavor), administered under the same conditions.
> - **Administration:** By Nurse Joy, in a private room at the Pewter City Pokemon Center, following a standardized script.

This precision serves multiple purposes. First, it ensures replicability — another researcher in Cerulean City could run the same experiment with the same treatment. Second, it anchors the causal estimand: we are estimating the effect of *this specific intervention*, not "supplements in general." Third, it supports blinding: trainers cannot distinguish treatment from control by appearance, taste, or administration context.

### Outcome Definition

Brock battles yield multiple potential outcomes, each measuring something different:

| Outcome | Type | Definition | Pros | Cons |
|---|---|---|---|---|
| Beat Brock (yes/no) | Binary | Trainer's team reduces all of Brock's Pokemon to 0 HP | Clear, meaningful | Loses granularity |
| Total damage dealt | Continuous | Sum of HP damage dealt to Brock's Pokemon across all turns | Granular, high power | May be noisy |
| Turns to win | Count/Time-to-event | Number of battle turns until victory (censored if trainer loses) | Captures efficiency | Requires handling censoring |
| Pokemon remaining | Count | Number of trainer's Pokemon still standing at battle's end | Measures dominance | Bounded, discrete |

**Table 2.2:** Candidate outcome measures for the Pewter Protein RCT.

Nurse Joy selects **total damage dealt** (continuous) as the primary outcome and **beat Brock** (binary) as a pre-registered secondary outcome. The continuous measure provides more statistical power (we can detect smaller effects), while the binary measure is the outcome trainers actually care about.

The choice of primary vs. secondary outcomes must be **pre-registered** — declared before the data are analyzed. This prevents the researcher from running multiple analyses and cherry-picking the most favorable result, a practice known as *p-hacking* or *specification searching*.

### Power Analysis

Before enrolling a single trainer, Professor Oak insists on a **power analysis** to determine whether 200 trainers is enough to detect a meaningful effect.

Statistical power is the probability of correctly rejecting the null hypothesis when the treatment effect is real. For a two-sample test comparing means, the required sample size per group is approximately:

$$n_{\text{per group}} = \frac{(z_{\alpha/2} + z_{\beta})^2 (\sigma_1^2 + \sigma_0^2)}{(\mu_1 - \mu_0)^2}$$

where:
- $z_{\alpha/2}$ is the critical value for a two-sided test at significance level $\alpha$
- $z_{\beta}$ is the critical value corresponding to the desired power $1 - \beta$
- $\sigma_1^2, \sigma_0^2$ are the variances of the outcome in the treatment and control groups
- $\mu_1 - \mu_0$ is the **minimum detectable effect** (MDE) — the smallest effect we want to be able to detect

Professor Oak's assumptions, based on pilot data from Viridian City:

- Significance level: $\alpha = 0.05$, so $z_{\alpha/2} = 1.96$
- Power: $1 - \beta = 0.80$, so $z_{\beta} = 0.842$
- Standard deviation of damage dealt in both groups: $\sigma_1 = \sigma_0 = 35$ HP
- Minimum detectable effect: $\mu_1 - \mu_0 = 15$ HP of additional damage

Plugging in:

$$n_{\text{per group}} = \frac{(1.96 + 0.842)^2 (35^2 + 35^2)}{15^2} = \frac{(2.802)^2 (2450)}{225} = \frac{7.851 \times 2450}{225} = \frac{19{,}235}{225} \approx 85.5$$

Rounding up, we need approximately **86 trainers per group**, or 172 total. Professor Oak rounds up to 200 to provide a buffer for attrition and to increase power slightly. With $n = 200$ (100 per group), the actual power is approximately 87%.

> **Professor Oak Explains: Effect Sizes and Practical Significance**
>
> "A power analysis forces you to think about what effect size would be *meaningful*. If Pewter Protein only adds 2 HP of damage — less than a single Scratch attack — no trainer would care, even if it were statistically significant. We powered this study to detect a 15 HP difference because that's roughly the damage from one extra Tackle, which could plausibly swing a close battle. Always think about practical significance, not just statistical significance."

### Blocking and Stratified Randomization

Pure coin-flip randomization is simple and valid, but it can be made more efficient. Nurse Joy notices that having a Water-type or Grass-type Pokemon (which are super-effective against Brock's Rock-types) is the single strongest predictor of battle performance. If, by chance, more Water-type trainers ended up in the treatment group, the estimate would be noisier than necessary.

**Stratified (block) randomization** addresses this. Instead of one big randomization, we randomize *within strata*:

> **Definition 2.3 (Stratified Randomization).** Divide the sample into $K$ strata based on pre-treatment covariates. Within each stratum $k$, independently randomly assign a fixed number of units to treatment and control.

For the Pewter Protein RCT, Nurse Joy creates two blocks:

| Block | Definition | $n$ | Assigned to Protein | Assigned to Placebo |
|---|---|---|---|---|
| A: Type advantage | Trainer has $\geq 1$ Water or Grass-type Pokemon | 78 | 39 | 39 |
| B: No type advantage | Trainer has no Water or Grass-type Pokemon | 122 | 61 | 61 |
| **Total** | | **200** | **100** | **100** |

**Table 2.3:** Stratified randomization scheme for the Pewter Protein RCT.

Within each block, treatment and control are *exactly* balanced on the blocking variable. This eliminates one source of sampling variability, improving precision — especially when the blocking variable is strongly predictive of the outcome. The efficiency gain from blocking is proportional to the $R^2$ between the blocking variable and the outcome (see Gerber & Green, 2012, Chapter 4).

Importantly, stratified randomization preserves the independence condition $(Y_i(0), Y_i(1)) \perp\!\!\!\perp D_i \mid X_i$ within each stratum, and the overall ATE can be estimated as a weighted average of within-stratum effects:

$$\hat{\tau}_{\text{stratified}} = \sum_{k=1}^{K} \frac{n_k}{n} \hat{\tau}_k$$

where $\hat{\tau}_k = \bar{Y}_{1k} - \bar{Y}_{0k}$ is the difference in means within stratum $k$.

### Cluster Randomization

What if randomizing individual trainers is logistically impossible? Suppose the Kanto Pokemon League wants to test Pewter Protein across the entire region. It might be easier to randomize at the level of **Pokemon Centers**: all trainers at certain Centers receive Protein, all trainers at others receive Placebo.

This is **cluster randomization**, and it introduces complications:

> **Definition 2.4 (Cluster Randomized Trial).** Units are grouped into clusters (e.g., Pokemon Centers, towns, training schools). Entire clusters, rather than individual units, are randomly assigned to treatment or control.

The primary cost of cluster randomization is a loss of statistical power. Trainers within the same Pokemon Center are likely more similar to each other (they trained in the same area, faced similar wild Pokemon, may know each other) than trainers across Centers. This **intra-cluster correlation (ICC)** means that adding more trainers within a cluster provides diminishing returns. The effective sample size is:

$$n_{\text{effective}} = \frac{n}{1 + (m - 1)\rho}$$

where $n$ is the total sample size, $m$ is the average cluster size, and $\rho$ is the ICC. If $\rho = 0.05$ and each of 10 Pokemon Centers has 20 trainers ($n = 200$, $m = 20$), the effective sample size is only $200 / (1 + 19 \times 0.05) = 200 / 1.95 \approx 103$ — nearly half the nominal sample.

For the Pewter Protein RCT, individual randomization is feasible (every trainer visits the same Pokemon Center in Pewter City), so Nurse Joy and Professor Oak wisely avoid the power loss of clustering.

### Blinding

Blinding prevents **expectation effects** — changes in behavior caused by knowing one's treatment status rather than by the treatment itself.

| Blinding Level | Who is Blinded | Pewter Protein Implementation |
|---|---|---|
| **Single-blind** | Trainers don't know which tablet they received | Protein and Placebo look, taste, and smell identical |
| **Double-blind** | Trainers AND Brock don't know treatment status | Brock battles all challengers identically; no access to assignment records |
| **Triple-blind** | Trainers, Brock, AND Nurse Joy (analyst) | An independent statistician (Prof. Oak's assistant) analyzes coded data |

**Table 2.4:** Blinding levels in the Pewter Protein RCT.

The Pewter Protein RCT implements **double-blinding**. Trainers cannot tell which tablet they received. Brock, for his part, battles every challenger with the same team (Geodude and Onix) using the same strategy, and has no idea which trainers received Protein. Nurse Joy records outcomes but does not analyze the data until the trial is complete — and even then, treatment codes are not unblinded until after the primary analysis is locked.

### Design Summary

| Design Element | Decision | Rationale |
|---|---|---|
| Population | Trainers registering to challenge Brock at Pewter Gym | Defined, accessible population |
| Sample size | $n = 200$ (100 per arm) | 87% power to detect 15 HP MDE |
| Treatment | 10 mg Pewter Protein tablet | Standardized dose and formulation |
| Control | Placebo Berry tablet | Indistinguishable from treatment |
| Randomization | Stratified by type-advantage (2 blocks) | Improves precision |
| Primary outcome | Total damage dealt (HP) | Continuous, high power |
| Secondary outcome | Beat Brock (yes/no) | Binary, practically meaningful |
| Blinding | Double-blind | Prevents expectation effects |
| Analysis plan | Pre-registered difference-in-means | Prevents p-hacking |
| Ethics | Approved by Kanto Pokemon League IRB | Equipoise: genuine uncertainty about Protein efficacy |

**Table 2.5:** Summary of the Pewter Protein RCT design.

---

## 2.3 Estimands and Estimators

With the experiment designed and the data collected, we turn to the question of estimation. What exactly are we estimating, and how?

> **Notation at a Glance: The Symbols You'll See in This Section**
>
> The next few pages throw a lot of Greek letters at you. Here is what each one *means*, in plain English, before we use them in formulas.
>
> | Symbol | Plain-English reading |
> |:---|:---|
> | $n_1, n_0$ | How many trainers are in the treatment group ($n_1$) and the control group ($n_0$). |
> | $\bar{Y}_1, \bar{Y}_0$ | The group *averages* — the mean outcome in the treatment and control groups. |
> | $\hat{\tau} = \bar{Y}_1 - \bar{Y}_0$ | Our point estimate of the treatment effect: just the difference of the two group means. The hat ( $\hat{\;}$ ) means "estimated from data." |
> | $s_1^2, s_0^2$ | The *sample* variance in each group. Measures how spread out the outcomes are. |
> | $\sigma_1^2, \sigma_0^2$ | The *true* (population) variances. Greek letters = truth; Latin letters with hats = estimates. |
> | $\widehat{SE}$ | The standard error of $\hat{\tau}$ — how much our estimate would wiggle if we re-ran the same experiment. |
> | $\alpha$ | The *significance level* of a test (conventionally 0.05). "How often do we tolerate a false alarm?" |
> | $1 - \beta$ | The *power* of a test (conventionally 0.80). "How often do we catch a real effect?" |
> | $z_{\alpha/2}, z_{\beta}$ | Just lookup values from the normal curve — 1.96 and 0.842 for $\alpha = 0.05, \beta = 0.20$. |
> | $\mu_1 - \mu_0$ | The *effect size* we care about — the smallest difference worth detecting. |
> | $\rho$ | Intra-cluster correlation: "how similar are units in the same cluster?" |
> | $\epsilon_i$ | The unexplained leftover — the part of trainer $i$'s outcome no variable in the model accounts for. |
>
> The rule of thumb: Greek letters ($\mu, \sigma, \tau, \alpha, \beta$) are usually *unknown truths*. Latin letters with hats ($\hat{\tau}, \hat{\mu}, s$) are what we *compute* from data to estimate them.

### Estimands: ATE, ATT, and ATC

Recall from Chapter 1 the three core causal estimands:

$$\text{ATE} = E[Y_i(1) - Y_i(0)]$$

$$\text{ATT} = E[Y_i(1) - Y_i(0) \mid D_i = 1]$$

$$\text{ATC} = E[Y_i(1) - Y_i(0) \mid D_i = 0]$$

In an observational study, these can differ — the effect of Protein may be different for trainers who choose to take it (ATT) vs. those who do not (ATC). But under random assignment, treatment status is independent of potential outcomes, so:

$$\text{ATT} = E[Y_i(1) - Y_i(0) \mid D_i = 1] = E[Y_i(1) - Y_i(0)] = \text{ATE}$$

and similarly $\text{ATC} = \text{ATE}$. All three estimands coincide. This is a major simplification: in an RCT, we don't need to worry about which estimand we're targeting. The simple difference in means estimates all of them.

### Neyman's Repeated Sampling Framework

Jerzy Neyman, in his foundational 1923 paper (translated to English in 1990), provided the inferential framework that most applied researchers use today. The key idea: treat the observed data as one realization of all possible random assignments, and derive the sampling distribution of the estimator over these hypothetical repetitions.

For a completely randomized experiment with $n_1$ treated and $n_0$ control units, the difference-in-means estimator $\hat{\tau} = \bar{Y}_1 - \bar{Y}_0$ is unbiased (as shown in Section 2.1), and its variance under repeated sampling is:

$$\text{Var}(\hat{\tau}) = \frac{\sigma_1^2}{n_1} + \frac{\sigma_0^2}{n_0} - \frac{\sigma_{\tau}^2}{n}$$

where $\sigma_1^2 = \text{Var}(Y_i(1))$, $\sigma_0^2 = \text{Var}(Y_i(0))$, and $\sigma_{\tau}^2 = \text{Var}(\tau_i) = \text{Var}(Y_i(1) - Y_i(0))$ is the variance of the individual treatment effects.

The last term, $\sigma_{\tau}^2 / n$, is non-negative and generally unknown (it depends on the joint distribution of $Y_i(1)$ and $Y_i(0)$, which we never observe). Dropping it gives us a **conservative** variance estimator:

$$\hat{V}[\hat{\tau}] = \frac{s_1^2}{n_1} + \frac{s_0^2}{n_0}$$

where $s_1^2 = \frac{1}{n_1 - 1}\sum_{i: D_i = 1}(Y_i - \bar{Y}_1)^2$ and $s_0^2 = \frac{1}{n_0 - 1}\sum_{i: D_i = 0}(Y_i - \bar{Y}_0)^2$ are the sample variances in each group.

> **Definition 2.5 (Neyman Variance Estimator).** The conservative estimator of the variance of $\hat{\tau}$ under complete randomization is:
>
> $$\hat{V}[\hat{\tau}] = \frac{s_1^2}{n_1} + \frac{s_0^2}{n_0}$$
>
> This is conservative in the sense that $E[\hat{V}] \geq \text{Var}(\hat{\tau})$, with equality when $\tau_i = \tau$ for all $i$ (constant treatment effect). The standard error is $\widehat{SE} = \sqrt{\hat{V}[\hat{\tau}]}$.

This is precisely the familiar two-sample $t$-test variance formula. Neyman's contribution was showing that it is valid for inference about causal effects under the randomization distribution, without requiring any assumptions about a superpopulation or distributional form.

### Confidence Intervals and Hypothesis Testing

With the point estimate and standard error in hand, we construct a 95% confidence interval:

$$\hat{\tau} \pm 1.96 \times \widehat{SE}$$

and test the null hypothesis $H_0: \tau = 0$ using the test statistic:

$$t = \frac{\hat{\tau}}{\widehat{SE}}$$

Under the null, this is approximately standard normal for large samples (or follows a $t$-distribution with degrees of freedom given by the Welch-Satterthwaite approximation for finite samples).

### Worked Example: The Pewter Protein Results

Nurse Joy collects the data. Here are the summary statistics:

| Group | $n$ | Mean damage (HP) | SD (HP) |
|---|---|---|---|
| Protein (treatment) | 100 | 142.7 | 36.2 |
| Placebo (control) | 100 | 128.4 | 33.8 |

**Step 1: Point estimate.**

$$\hat{\tau} = \bar{Y}_1 - \bar{Y}_0 = 142.7 - 128.4 = 14.3 \text{ HP}$$

**Step 2: Standard error.**

$$\widehat{SE} = \sqrt{\frac{s_1^2}{n_1} + \frac{s_0^2}{n_0}} = \sqrt{\frac{36.2^2}{100} + \frac{33.8^2}{100}} = \sqrt{\frac{1310.44}{100} + \frac{1142.44}{100}} = \sqrt{13.10 + 11.42} = \sqrt{24.53} = 4.95$$

**Step 3: 95% Confidence interval.**

$$14.3 \pm 1.96 \times 4.95 = 14.3 \pm 9.7 = [4.6, 24.0]$$

**Step 4: Test statistic and p-value.**

$$t = \frac{14.3}{4.95} = 2.89$$

The two-sided p-value is $p = 0.004$. At $\alpha = 0.05$, we reject the null hypothesis of no treatment effect.

**Interpretation:** Pewter Protein increases the total damage dealt to Brock's Pokemon by an estimated 14.3 HP (95% CI: 4.6 to 24.0). This is statistically significant ($p = 0.004$) and practically meaningful — 14.3 HP is roughly equivalent to one additional Tackle attack, which could turn a close loss into a win.

For the secondary binary outcome (beat Brock), the treatment group win rate is 52% vs. 43% in the control group, a difference of 9 percentage points (95% CI: -1.8 to 19.8 pp, $p = 0.10$). The binary outcome is less precisely estimated because binary variables carry less information than continuous ones — a lesson in why the choice of outcome measure affects power.

### Regression Adjustment: Lin (2013)

Can we do better than the simple difference in means? **Yes** — without sacrificing the unbiasedness guarantee of randomization.

Lin (2013) proposed the following regression specification for estimating treatment effects in experiments with covariate adjustment:

$$Y_i = \alpha + \tau D_i + \beta X_i + \gamma D_i(X_i - \bar{X}) + \epsilon_i$$

where $X_i$ is a vector of pre-treatment covariates, centered by subtracting the overall mean $\bar{X}$. The OLS estimate of $\tau$ in this regression has two important properties:

1. It is **consistent** for the ATE regardless of whether the linear model is correctly specified.
2. It is **at least as precise** as the unadjusted difference-in-means (asymptotically), and strictly more precise when the covariates predict the outcome.

The interaction term $D_i(X_i - \bar{X})$ is critical — it allows the relationship between covariates and outcome to differ across treatment and control groups. Without it, misspecification of the covariate-outcome relationship can actually introduce bias (Freedman, 2008). Lin's specification is robust to this concern.

For the Pewter Protein trial, Nurse Joy includes the covariates from the balance table: trainer level, number of Pokemon, indicator for Water/Grass-type Pokemon, and prior gym badges. The regression-adjusted estimate is:

$$\hat{\tau}_{\text{adj}} = 14.8 \text{ HP}, \quad \widehat{SE}_{\text{adj}} = 3.91$$

The point estimate barely changes (14.8 vs. 14.3 — reassuring, since large changes would suggest imbalance), but the standard error shrinks from 4.95 to 3.91, a 21% reduction. The 95% CI narrows to $[7.1, 22.5]$, and the p-value drops to $p = 0.0002$.

> **Professor Oak Explains: Why Covariate Adjustment Helps but Doesn't Bias**
>
> "Here is the key insight: in a randomized experiment, covariate adjustment cannot *introduce* bias (the covariates are balanced in expectation), but it *can* reduce variance by explaining outcome variation that is unrelated to treatment. Think of it as noise reduction. The type of Pokemon a trainer has strongly predicts damage dealt, but since randomization balanced this variable across groups, including it in the model just soaks up residual variation, leaving a cleaner estimate of the treatment effect."

---

## 2.4 SUTVA: The Stable Unit Treatment Value Assumption

Every result derived so far — from the unbiasedness of difference-in-means to the validity of confidence intervals — rests on an assumption so fundamental that it often goes unstated. It is called **SUTVA**, and violating it can unravel the entire inferential framework.

> **Definition 2.6 (Stable Unit Treatment Value Assumption — SUTVA).** The potential outcomes for unit $i$ depend only on the treatment assigned to unit $i$, and not on the treatments assigned to other units. Furthermore, there is only one version of each treatment level. Formally:
>
> 1. **No interference:** $Y_i(D_1, D_2, \ldots, D_n) = Y_i(D_i)$ for all $i$. Unit $i$'s outcome depends only on its own treatment, not on the treatment status of any other unit.
>
> 2. **No hidden variations of treatment:** For all $i$, $Y_i(1)$ is a single, well-defined value — there is only one "version" of treatment.

### No Interference

SUTVA's first component requires that one trainer's treatment status does not affect another trainer's outcome. In the Pewter Protein trial, this seems plausible at first glance — each trainer battles Brock independently.

But consider violations:

**Sharing.** What if trainers in the Pokemon Center lobby share their tablets? "Hey, I got two of these blue things — want one?" If a control trainer receives half a Protein tablet from a treated trainer, both of their potential outcomes are distorted. The control trainer's $Y_i(0)$ is no longer their true untreated outcome.

**Information spillover.** Suppose trainers wait in a common area before their battles. A trainer who just won on Protein might tell the next trainer, "The Protein works — use Ember on Geodude first, then switch to your Water-type for Onix." Now the control trainer's strategy has been influenced by the treated trainer's experience, even without receiving the treatment.

**Brock's adaptation.** If Brock notices that Protein trainers hit harder and adjusts his strategy (e.g., using more Potions), then later trainers face a different version of Brock — one whose behavior has been influenced by earlier trainers' treatment status.

To mitigate interference, Nurse Joy schedules trainers at staggered times, prevents them from interacting in the waiting area, and ensures Brock follows a fixed battle script.

### No Hidden Variations of Treatment

SUTVA's second component requires that "Pewter Protein" means the same thing for every treated trainer. Violations include:

**Storage degradation.** Suppose some Protein tablets were stored in a hot stockroom and lost potency, while others were properly refrigerated. Now there are effectively two versions of treatment: full-strength Protein and degraded Protein. The potential outcome $Y_i(1)$ is no longer well-defined — it depends on *which* Protein the trainer received.

**Dosing variation.** If some trainers accidentally receive 8 mg instead of 10 mg (e.g., tablets from a faulty production batch), treatment is not uniform across the treated group.

**Trading.** In perhaps the most colorful SUTVA violation imaginable, suppose a treated and control trainer meet in the Pokemon Center lobby, discover their assignments, and *swap tablets*. The treated trainer now has the Placebo, the control trainer has the Protein, and the recorded treatment assignments are wrong for both. This is a form of noncompliance that simultaneously violates both SUTVA components.

Professor Oak addresses these threats through strict standardization: all Protein tablets come from the same lot, stored under controlled conditions, administered by Nurse Joy personally. Trainers are instructed not to share, trade, or discuss their tablets. The protocol isn't perfect — no protocol ever is — but it minimizes SUTVA violations to a manageable level.

> **Blue's Mistake: Ignoring Interference**
>
> Blue, of course, doesn't care about SUTVA. He shares his Protein with three friends, tells everyone in the Pokemon Center about his strategy for beating Brock, and loudly announces which trainers are in the treatment group. "Experiments are for nerds — I'm just helping people out!" Every violation of SUTVA that Nurse Joy carefully prevented, Blue happily introduces.

---

## 2.5 Internal vs. External Validity

An experiment can succeed in answering the question it asks (high internal validity) while failing to answer the question we actually care about (low external validity). These two dimensions of validity are often in tension, and understanding the tradeoff is essential for interpreting experimental results.

### Internal Validity

**Internal validity** asks: did the experiment correctly identify the causal effect of Pewter Protein *in this study population, under these conditions?*

Threats to internal validity include:

**Noncompliance.** Some trainers assigned to Protein refuse to take the tablet (perhaps they're suspicious of supplements). Some trainers assigned to Placebo obtain Protein elsewhere (perhaps from Blue, who is handing them out in the lobby). If we analyze based on what trainers *actually took* rather than what they were *assigned*, we reintroduce selection bias — the very problem randomization was designed to solve. We address this in Section 2.7.

**Attrition.** Trainers who lose to Brock badly — their entire team fainted in three turns — may be too embarrassed to report back to Nurse Joy. If attrition is related to treatment status (e.g., Protein trainers who lose feel worse because they "should have" won), the remaining sample is no longer balanced, and our estimate is biased. Formally, attrition means our observed outcome $Y_i$ is missing for some units, and if missingness depends on potential outcomes, we have a problem.

**Contamination.** Control group trainers learn about Protein from treated trainers and modify their behavior — perhaps they train harder to compensate for not having the supplement. This dilutes the treatment effect toward zero.

**Hawthorne effect.** Trainers in both groups may battle harder simply because they know they're in a study. If the Hawthorne effect is equal across groups, it doesn't bias the treatment effect estimate (both groups are equally affected). But if being told "you might have received a powerful supplement" motivates Protein trainers more than Placebo trainers — a form of placebo effect — the estimated effect is a composite of the pharmacological effect of Protein and the psychological effect of believing you have an advantage. Double-blinding mitigates this.

### External Validity

**External validity** asks: does the result generalize beyond this specific experiment?

Nurse Joy has convincingly shown that Pewter Protein boosts damage against Brock's Rock-type Pokemon in Pewter City. But consider:

**Different gym types.** Brock uses Geodude and Onix, both Rock/Ground types with specific weaknesses. Pewter Protein might boost physical Attack stats, which is exactly what you need against Rock-types with high Defense but exploitable weaknesses. Against Misty's Water-types in Cerulean City, the optimal strategy might rely on Special Attack instead. Would Protein help there?

**Different populations.** Pewter City trainers are typically early in their journey — low-level Pokemon, small teams, limited battle experience. Would Protein have the same effect on experienced trainers with Level 50 Pokemon challenging the Elite Four? There might be ceiling effects (experienced Pokemon already hit the damage cap) or floor effects (novice Pokemon can't absorb the Protein's benefits).

**Different contexts.** The Pewter Gym is an indoor arena with controlled conditions. Would Protein work the same in a wild Pokemon encounter, where terrain, weather, and surprise play a role? What about double battles, where strategy and team synergy matter more than individual stats?

**Dosing and timing.** The trial tested exactly 10 mg, 60 minutes before battle. Would 5 mg work? Would 20 mg work better, or cause side effects? What about taking it 2 hours before, or 10 minutes before?

### The Tradeoff

Internal and external validity often pull in opposite directions. The tighter you control an experiment — standardized dose, controlled setting, homogeneous population, strict protocol — the higher the internal validity but the narrower the generalizability.

A loose, "pragmatic" trial that enrolled all trainers across Kanto, let them take Protein whenever they wanted, and measured outcomes across all gym types would have higher external validity but would sacrifice internal validity to noncompliance, interference, and treatment variation.

The standard scientific approach is to establish internal validity first — prove the effect exists under controlled conditions — and then investigate generalizability through **replication** across different contexts. Nurse Joy's Pewter City trial is the first step. Future trials in Cerulean City, Vermilion City, and beyond will map the boundaries of the effect.

> **Professor Oak Explains: Transportability**
>
> "The question of whether a causal effect 'transports' from one setting to another is not just a matter of hand-waving. Pearl and Bareinboim (2014) developed a formal theory of **transportability**, which uses DAGs to identify exactly which conditions must hold for an experimental result to generalize from a source population to a target population. We'll touch on this in Chapter 8. For now, the lesson is: be precise about what population your experiment represents."

---

## 2.6 Randomization Inference

Everything in Section 2.3 relied on Neyman's framework, which treats the observed data as a draw from a hypothetical superpopulation and derives the sampling distribution over repeated experiments. There is an older, and in some ways more elegant, approach to inference in randomized experiments: **Fisher's randomization inference** (also called **permutation inference**).

### Fisher's Sharp Null Hypothesis

> **Definition 2.7 (Fisher's Sharp Null).** The sharp null hypothesis of no treatment effect states:
>
> $$H_0^F: Y_i(1) = Y_i(0) \quad \text{for all } i = 1, \ldots, n$$
>
> Under this hypothesis, the treatment has absolutely no effect on any unit. This is "sharp" because it specifies both potential outcomes for every unit, not just a population average.

The sharp null is stronger than Neyman's null ($H_0^N: E[Y_i(1)] - E[Y_i(0)] = 0$), which allows individual effects to be nonzero as long as they average to zero. Under the sharp null, every individual treatment effect is exactly zero: $\tau_i = 0$ for all $i$.

### The Permutation Distribution

Here is the key insight that makes Fisher's approach so powerful: **under the sharp null, all potential outcomes are observed.** If $Y_i(1) = Y_i(0)$ for every trainer, then regardless of whether trainer $i$ was assigned to treatment or control, they would have produced the same outcome. The observed outcome $Y_i$ equals both $Y_i(1)$ and $Y_i(0)$.

This means we can compute what the test statistic *would have been* under every possible random assignment, because the outcomes are fixed — only the assignment changes. The collection of these hypothetical test statistics is the **randomization distribution** (or permutation distribution).

The algorithm is:

1. Compute the observed test statistic $T^{\text{obs}}$ (e.g., the difference in means) from the actual data.
2. List all $\binom{n}{n_1}$ possible ways to assign $n_1$ units to treatment from $n$ total.
3. For each possible assignment $\mathbf{d}^{(j)}$, compute the test statistic $T^{(j)}$ using the *same outcomes* but the *reassigned treatment labels*.
4. The **Fisher exact p-value** is the fraction of permutations where the test statistic is at least as extreme as the observed value:

$$p_{\text{Fisher}} = \frac{\#\{j : |T^{(j)}| \geq |T^{\text{obs}}|\}}{\binom{n}{n_1}}$$

For large experiments, enumerating all $\binom{n}{n_1}$ permutations is computationally infeasible ($\binom{200}{100} \approx 9 \times 10^{58}$). In practice, we approximate the permutation distribution by drawing a large number of random permutations (e.g., 10,000 or 100,000).

### Worked Example: A Small Pewter Protein Trial

To illustrate the full permutation distribution, consider a miniature version of the trial with $n = 10$ trainers, $n_1 = 5$ assigned to Protein and $n_0 = 5$ to Placebo.

| Trainer | Treatment ($D_i$) | Damage Dealt ($Y_i$) |
|---|---|---|
| Ash | 1 (Protein) | 155 |
| Misty | 1 (Protein) | 180 |
| Brock Jr. | 1 (Protein) | 130 |
| Gary | 1 (Protein) | 145 |
| Leaf | 1 (Protein) | 160 |
| Jessie | 0 (Placebo) | 120 |
| James | 0 (Placebo) | 135 |
| Ritchie | 0 (Placebo) | 110 |
| Duplica | 0 (Placebo) | 140 |
| Todd | 0 (Placebo) | 125 |

**Observed test statistic:**

$$T^{\text{obs}} = \bar{Y}_1 - \bar{Y}_0 = \frac{155 + 180 + 130 + 145 + 160}{5} - \frac{120 + 135 + 110 + 140 + 125}{5} = 154 - 126 = 28$$

Under the sharp null, every trainer's outcome is fixed regardless of assignment. There are $\binom{10}{5} = 252$ possible assignments. For each, we compute the difference in means between the (hypothetically) treated and control groups.

For instance, one alternative assignment might place {Ash, Misty, Jessie, James, Ritchie} in treatment and {Brock Jr., Gary, Leaf, Duplica, Todd} in control. The test statistic would be:

$$T = \frac{155 + 180 + 120 + 135 + 110}{5} - \frac{130 + 145 + 160 + 140 + 125}{5} = 140 - 140 = 0$$

We compute all 252 such statistics and form the permutation distribution.

> **Figure 2.1 (Description):** A histogram of the 252 values of the difference-in-means test statistic under all possible random assignments of 5 out of 10 trainers to treatment. The distribution is approximately bell-shaped, centered at zero, with most values between -30 and +30. The observed statistic of $T^{\text{obs}} = 28$ is marked with a dashed red vertical line in the right tail. Very few permutations yield a test statistic as large or larger than 28 in absolute value, suggesting the result is unlikely under the sharp null.

Computing the exact Fisher p-value: of the 252 permutations, suppose 18 yield $|T^{(j)}| \geq 28$. Then:

$$p_{\text{Fisher}} = \frac{18}{252} = 0.071$$

At $\alpha = 0.05$, we would not reject the sharp null in this small sample — but the result is suggestive, and the full $n = 200$ trial (Section 2.3) confirms the effect.

### Fisher vs. Neyman

The Fisher and Neyman frameworks differ in philosophy and practice:

| Feature | Fisher (Randomization Inference) | Neyman (Repeated Sampling) |
|---|---|---|
| Null hypothesis | Sharp: $Y_i(1) = Y_i(0)$ for all $i$ | Weak: $E[Y_i(1)] - E[Y_i(0)] = 0$ |
| Inference basis | Permutation distribution over all possible random assignments | Sampling distribution over hypothetical repetitions |
| Assumption | SUTVA + random assignment | SUTVA + random assignment |
| Requires | No distributional assumptions | Large-sample normality (for $t$-test) |
| Focus | Testing (p-value) | Estimation (point estimate + CI) |
| Finite sample | Exact p-values | Approximate (conservative) |

**Table 2.6:** Comparison of Fisher and Neyman inferential frameworks.

In practice, both approaches typically yield similar conclusions. Neyman's framework is more useful for estimation (it provides point estimates and confidence intervals), while Fisher's is attractive for exact inference in small samples and for its elegant conceptual simplicity. Modern applied work often uses Neyman's framework for primary analysis and reports randomization inference as a robustness check.

> **Professor Oak Explains: The Intellectual Rivalry**
>
> "Fisher and Neyman famously disagreed about the foundations of statistical inference — their debates in the 1930s were legendary and sometimes acrimonious. Fisher emphasized testing and fiducial probability; Neyman emphasized estimation and confidence intervals. Both contributed indispensable ideas to experimental statistics, and modern practice draws from both traditions. In causal inference, Rubin (1974) and Holland (1986) synthesized these traditions within the potential outcomes framework. For the definitive modern treatment, see Imbens and Rubin (2015)."

---

## 2.7 Practical Complications

The theoretical elegance of randomized experiments meets the messy reality of the Pokemon world. In this section, we discuss the most common practical complications and how to handle them.

### Noncompliance

In an ideal experiment, every trainer takes the assigned treatment. In reality, compliance is imperfect.

**One-sided noncompliance:** Some trainers assigned to Protein refuse to take the tablet. Perhaps they're skeptical, or they feel sick that day, or they're philosophically opposed to supplements. But no control trainer can access Protein (because it's not available outside the trial). This is "one-sided" noncompliance — deviation occurs only in the treatment group.

**Two-sided noncompliance:** In the Pewter Protein trial, two-sided noncompliance arises because Blue is handing out Protein in the lobby. Some control trainers sneak Protein, and some treatment trainers — perhaps influenced by Blue's skeptics — throw their tablets away. Now compliance is imperfect in both directions.

The temptation is to analyze based on **actual treatment received** rather than *assigned* treatment. This is a grave error — it reintroduces selection bias. Trainers who comply with their assignment may differ systematically from those who don't. If we compare "Protein takers" to "non-takers" regardless of assignment, we are back in the observational world.

### Intent-to-Treat Analysis

The standard solution is **Intent-to-Treat (ITT)** analysis: analyze every trainer according to their *assigned* treatment, regardless of compliance.

> **Definition 2.8 (Intent-to-Treat).** The ITT estimand is the causal effect of being *assigned* to treatment, regardless of whether the treatment was actually received:
>
> $$\text{ITT} = E[Y_i \mid Z_i = 1] - E[Y_i \mid Z_i = 0]$$
>
> where $Z_i$ is the treatment assignment (instrument) and $D_i$ is the actual treatment received.

The ITT preserves the integrity of randomization — since assignment $Z_i$ is random, the ITT comparison is unbiased for the effect of *assignment*. However, it generally underestimates the effect of *treatment* itself, because some assigned trainers didn't actually take Protein. The ITT is sometimes called a "diluted" treatment effect.

In the Pewter Protein trial, suppose 12 of 100 trainers assigned to Protein refused to take it, and 5 of 100 control trainers obtained Protein from Blue. The ITT analysis still compares the 100 assigned-Protein trainers (88 of whom actually took it) against the 100 assigned-Placebo trainers (5 of whom actually took Protein). The ITT estimate will be attenuated relative to the true effect of actually consuming Protein.

### Preview: Instrumental Variables and LATE

Can we recover the effect of actually taking Protein, despite noncompliance? **Yes** — using the randomized assignment as an **instrumental variable**. This is the LATE (Local Average Treatment Effect) framework of Imbens and Angrist (1994):

$$\text{LATE} = \frac{\text{ITT}}{\text{Compliance Rate}} = \frac{E[Y_i \mid Z_i = 1] - E[Y_i \mid Z_i = 0]}{E[D_i \mid Z_i = 1] - E[D_i \mid Z_i = 0]}$$

This ratio — known as the **Wald estimator** — identifies the causal effect of Protein for **compliers**, the subpopulation of trainers who take Protein when assigned to it and don't take it when assigned to control. We will develop this machinery fully in Chapter 6 (Fuchsia City & Cinnabar Island: Instrumental Variables).

### Attrition

When trainers drop out of the study before outcomes are recorded, the remaining sample may no longer be balanced — even if the original randomization was perfect.

In the Pewter Protein trial, suppose 8 trainers in the Placebo group who lost badly to Brock leave without reporting their results, while only 2 trainers in the Protein group do the same. The remaining data overrepresent trainers who performed well (especially in the control group), biasing the estimated treatment effect downward.

When attrition rates differ across groups, **Lee (2009) bounds** provide a principled approach: trim the group with lower attrition to match the attrition rate of the other group, and report best-case and worst-case effect estimates. If even the worst-case bound excludes zero, the result is robust to attrition.

In practice, the best defense is prevention: Nurse Joy stations an assistant at the gym exit to record outcomes for *every* trainer, win or lose.

### Hawthorne Effect

The Hawthorne effect — named after a famous series of experiments at the Hawthorne Works factory in the 1920s — refers to behavior changes caused by the awareness of being observed or studied, rather than by the treatment itself.

In the Pewter Protein trial, trainers who know they're in a study might battle more carefully, use items more strategically, or try harder than they normally would. If this elevated effort is symmetric across treatment and control (both groups try equally hard), it inflates *both* group means but doesn't bias the treatment-control comparison. The estimated effect of Protein remains valid, but it applies to a population of trainers who are "trying their hardest" — which may differ from real-world conditions where trainers battle casually.

If the Hawthorne effect is asymmetric — for example, trainers in the Protein group try harder because they believe they have an advantage — it becomes a confound. Double-blinding is the primary defense.

### Ethical Considerations

Is it ethical to withhold a potentially beneficial treatment from control trainers? The Pewter Protein trial is justifiable because of **clinical equipoise**: before the trial, there is genuine uncertainty about whether Protein works. If we already knew it worked, randomizing some trainers to Placebo would be denying them a benefit. But we don't know — that's why we're running the experiment.

Additional ethical safeguards in the Pewter Protein RCT:

- **Informed consent:** Trainers are told they will receive *either* Protein or Placebo, and that the goal is to determine whether Protein works. They consent to this uncertainty.
- **No harm:** The Placebo Berry is inert; it doesn't make anyone worse off than they would be without the study. Losing to Brock is disappointing but not dangerous — Nurse Joy heals all Pokemon for free.
- **Data monitoring:** If interim results showed that Protein was causing serious Pokemon health issues, the trial would be stopped immediately.
- **Post-trial access:** After the trial concludes, if Protein is shown to be effective, all control trainers are offered free Protein before their next gym challenge.

---

## Chapter Summary

<!-- FIG-CH02-BADGE -->
<figure style="text-align:center; margin:1.5em auto;">
<img src="../../assets/badges/boulder_badge.png" alt="Boulder Badge" style="width:140px; display:block; margin:0 auto;">
<figcaption><strong>Boulder Badge earned!</strong></figcaption>
</figure>


This chapter has covered the theory and practice of randomized controlled trials, the gold standard of causal inference. Here are the key takeaways:

- **Randomization creates independence** between treatment assignment and potential outcomes: $(Y_i(0), Y_i(1)) \perp\!\!\!\perp D_i$. This eliminates selection bias and balances both observed and unobserved confounders in expectation.

- **The difference-in-means estimator** $\hat{\tau} = \bar{Y}_1 - \bar{Y}_0$ is **unbiased** for the ATE under random assignment. No modeling assumptions are required.

- **Experimental design** matters enormously: precise treatment definition, outcome selection, power analysis, stratified randomization, and blinding all improve the quality of the experiment.

- **Under randomization, ATE = ATT = ATC.** The distinction between estimands, which will be crucial in observational settings, collapses in an experiment.

- **Neyman's framework** provides variance estimation ($\hat{V}[\hat{\tau}] = s_1^2/n_1 + s_0^2/n_0$), confidence intervals, and hypothesis tests based on repeated sampling.

- **Regression adjustment** (Lin, 2013) can improve precision by absorbing residual outcome variation, without introducing bias, as long as the specification includes treatment-covariate interactions.

- **SUTVA** — the Stable Unit Treatment Value Assumption — requires no interference between units and no hidden treatment variations. Violations undermine the entire potential outcomes framework.

- **Internal validity** (did the experiment work as designed?) and **external validity** (do the results generalize?) are both important but often trade off against each other.

- **Randomization inference** (Fisher) provides exact p-values by computing the test statistic under all possible random assignments, exploiting the sharp null to treat all potential outcomes as known.

- **Practical complications** — noncompliance, attrition, Hawthorne effects — require careful handling. The ITT analysis preserves the benefits of randomization; IV/LATE (Chapter 6) recovers the effect on compliers.

---

## Professor Oak's Review Questions

1. **Conceptual.** Explain in your own words why randomization balances unobserved confounders. Why can't any observational method achieve this?

2. **Mathematical.** In the Pewter Protein RCT, the difference-in-means estimate is $\hat{\tau} = 14.3$ HP with $\widehat{SE} = 4.95$. Suppose we had used a one-sided test ($H_A: \tau > 0$) instead of a two-sided test. What would the p-value be? Would your conclusion change?

3. **Design.** Nurse Joy is planning a follow-up trial to test whether Pewter Protein also works against Misty's Water-type Pokemon. She expects a smaller effect (MDE = 10 HP) because Attack boosts are less relevant against Water-types. How many trainers does she need per group, assuming the same variance ($\sigma = 35$) and 80% power?

4. **SUTVA.** Give a realistic example of a SUTVA violation in the Pewter Protein trial that is NOT mentioned in this chapter. Explain how it would bias the estimated treatment effect and propose a solution.

5. **Fisher vs. Neyman.** In the small-sample worked example (Section 2.6), the Fisher p-value was 0.071 and we did not reject at $\alpha = 0.05$. Using Neyman's framework on the same 10 trainers, compute the difference-in-means, standard error, and 95% confidence interval. Does the confidence interval include zero? Are the two frameworks telling the same story?

6. **External Validity.** A researcher reads about the Pewter Protein trial and concludes: "Pewter Protein works. We should distribute it to all trainers in Kanto before every gym battle." Identify at least three reasons why this conclusion may be premature.

---

## Trainer Challenge Exercises

### Exercise 2.1: Balance Check Simulation

Using a programming language of your choice (Python or R recommended), simulate a completely randomized experiment with $n = 200$ trainers. Generate 10 pre-treatment covariates from standard normal distributions (independent of treatment). Assign 100 trainers to treatment and 100 to control. For each covariate, compute the two-sample $t$-test p-value. Repeat the entire experiment 1,000 times. What fraction of simulations have at least one covariate with $p < 0.05$? What does this tell you about interpreting balance tables?

### Exercise 2.2: Power Analysis

A researcher at the Celadon City Game Corner wants to test whether a new TM (Technical Machine) improves Pokemon battle performance. She expects the TM to increase damage by 8 HP, with standard deviations of 25 HP in both groups. Using the formula from Section 2.2, compute the required sample size per group for: (a) 80% power, (b) 90% power, (c) 95% power. Plot the required sample size as a function of power for $1 - \beta \in [0.5, 0.99]$. What happens to sample size requirements as you demand higher power?

### Exercise 2.3: Randomization Inference by Hand

Consider the following data from 8 trainers in a mini-experiment:

| Trainer | Assignment | Damage |
|---|---|---|
| A | Protein | 150 |
| B | Protein | 130 |
| C | Protein | 170 |
| D | Protein | 140 |
| E | Placebo | 120 |
| F | Placebo | 110 |
| G | Placebo | 145 |
| H | Placebo | 130 |

(a) Compute the observed difference-in-means test statistic.
(b) Under the sharp null, enumerate all $\binom{8}{4} = 70$ possible assignments of 4 trainers to treatment. For each, compute the difference-in-means.
(c) Plot the permutation distribution and mark the observed statistic.
(d) Compute the two-sided Fisher exact p-value. What do you conclude?

### Exercise 2.4: Noncompliance and ITT vs. Per-Protocol

In the Pewter Protein trial, suppose the following compliance data are observed:

| Assigned Group | Actually Took Protein | Actually Took Placebo | $n$ |
|---|---|---|---|
| Protein | 85 | 15 | 100 |
| Placebo | 8 | 92 | 100 |

The mean outcomes are: Protein group (as assigned) = 142.7 HP, Placebo group (as assigned) = 128.4 HP, Actual Protein takers (regardless of assignment) = 144.2 HP, Actual Placebo takers (regardless of assignment) = 126.8 HP.

(a) Compute the ITT estimate and explain what it estimates.
(b) Compute the naive "per-protocol" estimate (comparing actual takers vs. non-takers) and explain why it may be biased.
(c) Using the Wald estimator, compute the LATE. What population does this estimate apply to?
(d) Why is the LATE larger in magnitude than the ITT?

---

## Further Reading

- **Fisher, R.A.** (1935). *The Design of Experiments.* Edinburgh: Oliver and Boyd. The foundational text on randomized experiments and permutation inference.

- **Neyman, J.** (1923/1990). "On the Application of Probability Theory to Agricultural Experiments." Translated and republished in *Statistical Science*, 5(4), 465-472. The original articulation of potential outcomes and the repeated-sampling framework for experimental inference.

- **Rubin, D.B.** (1974). "Estimating Causal Effects of Treatments in Randomized and Nonrandomized Studies." *Journal of Educational Psychology*, 66(5), 688-701. The paper that formalized the potential outcomes framework and connected it to randomization.

- **Holland, P.W.** (1986). "Statistics and Causal Inference." *Journal of the American Statistical Association*, 81(396), 945-960. The classic paper stating the "fundamental problem of causal inference" and surveying the Rubin causal model.

- **Lin, W.** (2013). "Agnostic Notes on Regression Adjustments to Experimental Data: Reexamining Freedman's Critique." *Annals of Applied Statistics*, 7(1), 295-318. The definitive treatment of regression adjustment in randomized experiments.

- **Gerber, A.S. & Green, D.P.** (2012). *Field Experiments: Design, Analysis, and Interpretation.* New York: W.W. Norton. An excellent applied textbook on experimental design with extensive coverage of randomization inference, blocking, and noncompliance.

- **Athey, S. & Imbens, G.W.** (2017). "The Econometrics of Randomized Experiments." In *Handbook of Economic Field Experiments*, Vol. 1, 73-140. A modern survey of the econometric theory of randomized experiments, covering design, analysis, and extensions.

- **Imbens, G.W. & Rubin, D.B.** (2015). *Causal Inference for Statistics, Social, and Biomedical Sciences.* Cambridge University Press. The comprehensive graduate-level reference for the potential outcomes approach to causal inference.

---

## Skills to Practice in the Notebook

The notebook `notebooks/ch02_pewter_city.ipynb` is where RCT theory becomes a workable analysis pipeline. Before you claim the Boulder Badge, you should be able to do each of the following end-to-end in code:

1. **Simulate a completely randomized experiment.** Given $n$ trainers and known potential outcomes, flip a coin to assign treatment, compute $\hat{\tau} = \bar{Y}_1 - \bar{Y}_0$, and verify empirically that averaging $\hat{\tau}$ over many randomizations recovers the true ATE. This is the core "randomization makes naive estimators unbiased" demo.

2. **Build a balance table.** Using the Pewter Protein dataset (or a simulated one), compute the standardized mean difference (or two-sample $t$-test) for each pre-treatment covariate across treatment and control. Know what "balanced" looks like and be able to flag a covariate that is not.

3. **Run a power analysis.** Given $\alpha$, desired power $1-\beta$, outcome standard deviation $\sigma$, and minimum detectable effect (MDE), compute the required sample size per group. Then flip it around: given a fixed $n$, what MDE can you detect? Both directions matter.

4. **Compute a Neyman standard error and CI by hand (in code).** From raw group means and sample variances, build $\widehat{SE}$, a 95% confidence interval, and the two-sided p-value. Do *not* rely on a canned `ttest_ind` call — write the formula yourself at least once. Then cross-check against `scipy.stats.ttest_ind`.

5. **Do a Lin (2013) regression adjustment.** Fit `Y ~ D + (X - mean(X)) + D:(X - mean(X))`. Confirm the treatment coefficient is close to the unadjusted estimate but the standard error shrinks when $X$ predicts $Y$. Be able to explain in one sentence why this adjustment doesn't bias the estimate.

6. **Run Fisher randomization inference.** For a small dataset, enumerate (or sample) the permutation distribution of $\hat{\tau}$ under the sharp null, compute the exact p-value, and plot the distribution with the observed statistic marked.

7. **Complete the Trainer Challenge Exercises.**
   - **Exercise 2.1:** Balance-check simulation — what fraction of 1,000 random experiments show at least one covariate with $p < 0.05$ by chance?
   - **Exercise 2.2:** Power curve — plot sample size vs. power for $1-\beta \in [0.5, 0.99]$.
   - **Exercise 2.3:** Randomization inference by hand on the 8-trainer mini-dataset.
   - **Exercise 2.4:** ITT vs. per-protocol vs. LATE on the non-compliance table.

By the end, "run an RCT" should feel like 30 lines of pandas, not a mystery.

---

## Check Your Understanding

Walk through these before challenging Brock. If anything feels shaky, revisit that section — the rest of the book leans hard on Chapter 2's intuition about randomization.

**Questions you should be able to answer out loud, without notes:**

- Why does random assignment make the naive difference-in-means an *unbiased* estimate of the ATE? Which term in the selection-bias decomposition does it kill?
- State the independence condition $(Y_i(0), Y_i(1)) \perp\!\!\!\perp D_i$ and explain what it means in plain English about "the type of trainer who is treated."
- Why does randomization balance unobserved confounders, not just observed ones? Can any purely observational method do the same?
- Write the Neyman variance estimator $\hat{V}[\hat{\tau}] = s_1^2/n_1 + s_0^2/n_0$ and explain why it is *conservative* (i.e., why the "true" variance is generally smaller).
- What is the difference between $\sigma_1^2$, $s_1^2$, and $\widehat{SE}$? When do you use each?
- In an RCT, why do ATE, ATT, and ATC all coincide?
- What is statistical power, and what four inputs determine it? If you double the MDE, what happens to the required sample size?
- Why does stratified (block) randomization reduce variance? When does it *not* help?
- Explain SUTVA in two bullet points (no interference, no hidden variations) and give a concrete Pewter-Protein way each part could fail.
- Compare Fisher's sharp null and Neyman's average-effect null. Which test assumes constant effects across units? Which one gives exact p-values in finite samples?
- What does ITT estimate? What does per-protocol estimate? Why is the per-protocol estimate biased under noncompliance?

**Tasks you should be able to perform in code:**

- Randomly assign treatment to $n$ units and compute $\hat{\tau}$, $\widehat{SE}$, 95% CI, and a two-sided p-value — using both your own formula and `scipy`.
- Build a balance table showing the standardized mean difference for every covariate in a dataset.
- Compute required sample size from $(\alpha, 1-\beta, \sigma, \text{MDE})$ and plot the sample-size–vs–power curve.
- Fit a Lin (2013) regression with centered covariates and the treatment-covariate interaction, and compare its SE to the unadjusted SE.
- Run a permutation test: enumerate (or sample) treatment assignments, compute $\hat{\tau}$ under each, and compute the exact Fisher p-value.
- Given a noncompliance table (assigned vs. took), compute the ITT estimate and the Wald/LATE estimate.

If you can explain the answers *and* run the code without a cheat-sheet, you have truly earned the Boulder Badge.

---

## Badge Earned

> **You've earned the Boulder Badge!** You now understand how randomization eliminates confounding, why the difference-in-means estimator is unbiased under random assignment, and how to design, analyze, and interpret a randomized controlled trial. You've seen both Neyman's repeated sampling framework and Fisher's randomization inference, and you know how to handle the practical complications — noncompliance, attrition, and SUTVA violations — that arise in real experiments. Brock would be proud.

---

## Next: Route 3

*The path east from Pewter City winds through Route 3 and the dark tunnels of Mt. Moon. On the other side lies Cerulean City, where the Water-type gym leader Misty has been collecting mountains of observational battle data. Unlike Nurse Joy, Misty has no ability to randomize — she can only observe trainers as they come. How can she draw causal conclusions from this messy, non-experimental data? The answer involves directed acyclic graphs, the backdoor criterion, and the art of conditioning. Turn the page to Chapter 3: Cerulean City — Observational Studies & DAGs.*
