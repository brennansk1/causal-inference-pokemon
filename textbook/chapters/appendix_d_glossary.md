# Appendix D: Glossary --- The Causal Pokedex

---

*Every trainer needs a Pokedex. Yours catalogs not Pokemon, but the concepts, estimators, assumptions, and threats that populate the world of causal inference. Each entry below follows a standard format --- like a Pokedex entry --- so you can look up what you need quickly. The entries are sorted alphabetically.*

---

## How to Read an Entry

| Field | Description |
|:---|:---|
| **Term** | The concept name |
| **Type** | Assumption, Estimand, Estimator, Design, Concept, or Threat |
| **Tier** | Foundational / Intermediate / Advanced / Frontier |
| **Rarity** | Common / Uncommon / Rare / Legendary |
| **Definition** | Formal 1--2 sentence definition |
| **Pokemon Analogy** | Brief Kanto-themed intuition |
| **First Appears** | Chapter reference in this textbook |

**Type key:**

- **Assumption** --- A condition required for identification or validity
- **Estimand** --- A quantity we want to estimate (the target)
- **Estimator** --- A statistical method/procedure that produces an estimate
- **Design** --- A research design or data structure
- **Concept** --- A foundational idea or building block
- **Threat** --- A source of bias or invalidity

---

## The Entries

---

### 1. AIPW / Doubly Robust Estimator

| | |
|:---|:---|
| **Type** | Estimator |
| **Tier** | Intermediate |
| **Rarity** | Uncommon |
| **Definition** | An estimator that combines an outcome regression model and a propensity score model. It is consistent if *either* model is correctly specified (hence "doubly robust"): $\hat{\tau}_{DR} = \frac{1}{n}\sum_{i} \left[\hat{\mu}_1(\mathbf{X}_i) - \hat{\mu}_0(\mathbf{X}_i) + \frac{D_i(Y_i - \hat{\mu}_1(\mathbf{X}_i))}{\hat{e}(\mathbf{X}_i)} - \frac{(1-D_i)(Y_i - \hat{\mu}_0(\mathbf{X}_i))}{1 - \hat{e}(\mathbf{X}_i)}\right]$. |
| **Pokemon Analogy** | Like having both a Fire-type and a Water-type on your team --- if one fails against a Gym Leader, the other covers. You get two chances to be right. |
| **First Appears** | Chapter 6 |

---

### 2. ATC (Average Treatment Effect on the Control)

| | |
|:---|:---|
| **Type** | Estimand |
| **Tier** | Intermediate |
| **Rarity** | Uncommon |
| **Definition** | The average causal effect of treatment among those who did *not* receive it: $\text{ATC} = E[Y(1) - Y(0) \mid D = 0]$. |
| **Pokemon Analogy** | How much would trainers who *didn't* use Exp. Share have benefited if they had? The hypothetical gain for the non-users. |
| **First Appears** | Chapter 2 |

---

### 3. ATE (Average Treatment Effect)

| | |
|:---|:---|
| **Type** | Estimand |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | The average causal effect of treatment across the entire population: $\text{ATE} = E[Y(1) - Y(0)]$. |
| **Pokemon Analogy** | If we could clone every trainer and give one clone Exp. Share and one none, the ATE is the average badge difference across all cloned pairs. |
| **First Appears** | Chapter 2 |

---

### 4. ATT (Average Treatment Effect on the Treated)

| | |
|:---|:---|
| **Type** | Estimand |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | The average causal effect of treatment among those who actually received treatment: $\text{ATT} = E[Y(1) - Y(0) \mid D = 1]$. |
| **Pokemon Analogy** | Among trainers who chose to use Exp. Share, how many extra badges did it actually give them, on average? |
| **First Appears** | Chapter 2 |

---

### 5. Backdoor Criterion

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | A set of variables $\mathbf{Z}$ satisfies the backdoor criterion relative to $(T, Y)$ if (i) no node in $\mathbf{Z}$ is a descendant of $T$, and (ii) $\mathbf{Z}$ blocks every path between $T$ and $Y$ that contains an arrow *into* $T$. Conditioning on such a set identifies the causal effect. |
| **Pokemon Analogy** | To see Exp. Share's true effect on badges, you must block all "backdoor" routes --- like the wealth pathway --- without accidentally blocking the causal route itself. |
| **First Appears** | Chapter 3 |

---

### 6. Bad Control

| | |
|:---|:---|
| **Type** | Threat |
| **Tier** | Intermediate |
| **Rarity** | Common |
| **Definition** | A variable that, when included in a regression or adjustment set, introduces or amplifies bias rather than reducing it. Common examples include mediators, colliders, and descendants of the outcome. |
| **Pokemon Analogy** | Controlling for `elite_four_attempted` when estimating the effect of strategy on badges is like judging a trainer's skill only among those who reached the Pokemon League --- you lose everyone who dropped out. |
| **First Appears** | Chapter 3 |

---

### 7. Blocking

| | |
|:---|:---|
| **Type** | Design |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | An experimental design strategy that groups units into homogeneous blocks before randomization, ensuring balance on key covariates within each block. |
| **Pokemon Analogy** | Before the Pokemon tournament draws, organizers separate trainers by experience level (blocks), then randomly assign opponents within each block so no experience group is systematically disadvantaged. |
| **First Appears** | Chapter 4 |

---

### 8. CATE (Conditional Average Treatment Effect)

| | |
|:---|:---|
| **Type** | Estimand |
| **Tier** | Intermediate |
| **Rarity** | Uncommon |
| **Definition** | The average treatment effect within a subgroup defined by covariate values: $\text{CATE}(\mathbf{x}) = E[Y(1) - Y(0) \mid \mathbf{X} = \mathbf{x}]$. |
| **Pokemon Analogy** | Exp. Share might help low-experience trainers more than veterans. The CATE tells you the effect *for trainers with 2 years of experience* or *for trainers from Cerulean City*. |
| **First Appears** | Chapter 10 |

---

### 9. Causal Discovery

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Frontier |
| **Rarity** | Rare |
| **Definition** | The task of learning the causal graph structure (which variables cause which) from observational data and assumptions, rather than specifying it a priori. Algorithms include PC, GES, and FCI. |
| **Pokemon Analogy** | Instead of Professor Oak telling you the Kanto DAG, you try to *infer* the causal structure by observing patterns in trainer data --- like discovering evolution chains by watching Pokemon in the wild. |
| **First Appears** | Chapter 12 |

---

### 10. Causal Forest

| | |
|:---|:---|
| **Type** | Estimator |
| **Tier** | Advanced |
| **Rarity** | Rare |
| **Definition** | A forest-based machine learning method for estimating heterogeneous treatment effects (CATEs). It modifies the random forest algorithm to split on treatment effect heterogeneity rather than prediction accuracy. |
| **Pokemon Analogy** | Like a Pokedex that does not just record one average stat for a species but tells you how the effect of a Rare Candy varies for each individual Pokemon based on its nature, level, and species. |
| **First Appears** | Chapter 10 |

---

### 11. Collider

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | A variable that is a common *effect* of two other variables: $A \to C \leftarrow B$. Conditioning on a collider (or its descendant) opens a spurious association between its parents. |
| **Pokemon Analogy** | `starter_type` is a collider of `wealth` and `trainer_experience` (both influence starter choice). If you study only Squirtle trainers, you create a spurious negative correlation between wealth and experience. |
| **First Appears** | Chapter 3 |

---

### 12. Confounder

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | A variable that causally affects both the treatment and the outcome, creating a non-causal (backdoor) path between them. Failing to adjust for a confounder leads to biased estimates. |
| **Pokemon Analogy** | `wealth` confounds the relationship between Exp. Share and badges: wealthy trainers are more likely to buy Exp. Share *and* earn more badges through other spending advantages. |
| **First Appears** | Chapter 1 |

---

### 13. Consistency

| | |
|:---|:---|
| **Type** | Assumption |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | The assumption that the observed outcome for a treated unit equals its potential outcome under treatment: if $D_i = d$, then $Y_i^{obs} = Y_i(d)$. This requires that "treatment" is well-defined and has a single version. |
| **Pokemon Analogy** | "Using Exp. Share" must mean the same thing for every trainer. If some trainers use a glitched Exp. Share that doubles XP, consistency is violated. |
| **First Appears** | Chapter 2 |

---

### 14. Counterfactual

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | The outcome a unit *would* have experienced under an alternative treatment. For a trainer who used Exp. Share, the counterfactual is their badge count had they *not* used it. Counterfactuals are fundamentally unobservable for any individual unit. |
| **Pokemon Analogy** | You chose Charmander. What *would* have happened if you had chosen Squirtle? You can never replay your journey with a different starter and the same random encounters. |
| **First Appears** | Chapter 1 |

---

### 15. d-Separation

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Intermediate |
| **Rarity** | Uncommon |
| **Definition** | A graphical criterion for determining whether two variables are conditionally independent given a set of other variables in a DAG. Two nodes $X$ and $Y$ are $d$-separated by a set $\mathbf{Z}$ if every path between them is blocked by $\mathbf{Z}$. |
| **Pokemon Analogy** | In the Kanto DAG, `patience` and `badges` are $d$-separated by `strategy_score` and `type_diversity` --- once you know a trainer's strategy and type diversity, knowing their patience tells you nothing more about badges (given the DAG). |
| **First Appears** | Chapter 3 |

---

### 16. DAG (Directed Acyclic Graph)

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | A graph with directed edges (arrows) and no cycles, used to represent causal relationships among variables. Each arrow $A \to B$ means $A$ is a direct cause of $B$. |
| **Pokemon Analogy** | Professor Oak's wall map showing how trainer attributes, items, and team stats cause badge outcomes. Arrows flow forward (training $\to$ badges $\to$ Elite Four), never backward. |
| **First Appears** | Chapter 3 |

---

### 17. Difference-in-Differences (DiD)

| | |
|:---|:---|
| **Type** | Design |
| **Tier** | Intermediate |
| **Rarity** | Common |
| **Definition** | A quasi-experimental design that estimates causal effects by comparing the change in outcomes over time between a treatment group and a control group: $\hat{\tau}_{DiD} = (\bar{Y}_{treat,post} - \bar{Y}_{treat,pre}) - (\bar{Y}_{ctrl,post} - \bar{Y}_{ctrl,pre})$. |
| **Pokemon Analogy** | When Team Rocket invades Saffron City, compare how trainer activity changed in Saffron (before vs. after invasion) relative to how it changed in Celadon (unaffected city) over the same period. |
| **First Appears** | Chapter 9 |

---

### 18. DML (Double/Debiased Machine Learning)

| | |
|:---|:---|
| **Type** | Estimator |
| **Tier** | Advanced |
| **Rarity** | Rare |
| **Definition** | A framework that uses machine learning to estimate nuisance parameters (propensity scores, outcome models) while using sample splitting and Neyman orthogonality to obtain valid inference for the causal parameter. |
| **Pokemon Analogy** | Like using a sophisticated team-building AI to handle the complex prediction tasks (which trainers use Exp. Share? what are their expected badges?) while a simple final calculation extracts the clean causal effect. |
| **First Appears** | Chapter 10 |

---

### 19. do-Operator

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Intermediate |
| **Rarity** | Uncommon |
| **Definition** | Pearl's notation for intervention. $P(Y \mid do(X = x))$ denotes the distribution of $Y$ when $X$ is *set* to value $x$ by external intervention, as opposed to merely *observing* $X = x$. The do-operator removes all arrows into $X$ in the DAG. |
| **Pokemon Analogy** | Observing that Squirtle trainers earn more badges is $P(\text{badges} \mid \text{starter} = \text{Squirtle})$. *Forcing* a random trainer to use Squirtle is $P(\text{badges} \mid do(\text{starter} = \text{Squirtle}))$. |
| **First Appears** | Chapter 1 |

---

### 20. E-value

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Advanced |
| **Rarity** | Uncommon |
| **Definition** | A measure of the minimum strength of association that an unmeasured confounder would need to have with both the treatment and the outcome to fully explain away an observed effect. Larger E-values indicate more robust findings. |
| **Pokemon Analogy** | If we estimate that Exp. Share gives +0.8 badges, the E-value tells us how powerful a hidden variable (like an unknown latent trait) would need to be to make that entire effect disappear. If it would need to be as strong as `natural_talent`, and we think no such variable exists, our finding is robust. |
| **First Appears** | Chapter 11 |

---

### 21. Event Study

| | |
|:---|:---|
| **Type** | Design |
| **Tier** | Intermediate |
| **Rarity** | Uncommon |
| **Definition** | A dynamic version of difference-in-differences that estimates treatment effects at each time period relative to the treatment onset. Pre-treatment coefficients serve as a test of parallel trends. |
| **Pokemon Analogy** | Plot the difference in trainer activity between invaded and non-invaded cities for each month before and after Team Rocket's arrival. The pre-invasion coefficients should be near zero if parallel trends holds. |
| **First Appears** | Chapter 9 |

---

### 22. Exclusion Restriction

| | |
|:---|:---|
| **Type** | Assumption |
| **Tier** | Intermediate |
| **Rarity** | Common |
| **Definition** | The assumption that an instrument $Z$ affects the outcome $Y$ *only through* the treatment $D$, not through any other channel: $Z \perp\!\!\!\perp Y \mid D$ (conditional on treatment). |
| **Pokemon Analogy** | The Safari Zone lottery (instrument) affects battle performance (outcome) *only* through Safari Zone access (treatment). If lottery winners also receive a cash prize that improves performance independently, the exclusion restriction fails. |
| **First Appears** | Chapter 7 |

---

### 23. Frontdoor Criterion

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Advanced |
| **Rarity** | Rare |
| **Definition** | An identification strategy for the causal effect of $X$ on $Y$ when there exists an unblocked confounder but a mediator $M$ that (i) is fully caused by $X$, (ii) blocks all directed paths from $X$ to $Y$, and (iii) has no unblocked backdoor from $M$ to $Y$ that does not go through $X$. |
| **Pokemon Analogy** | If we cannot observe `patience` (confounder between `safari_zone_visits` and `total_pokemon_caught`), but we can identify a mediator that captures all of the Safari Zone's effect on catches, the frontdoor criterion lets us recover the causal effect through the mediator. |
| **First Appears** | Chapter 3 |

---

### 24. g-formula

| | |
|:---|:---|
| **Type** | Estimator |
| **Tier** | Advanced |
| **Rarity** | Uncommon |
| **Definition** | Robins' generalization of standardization to time-varying treatments. It computes the causal effect by averaging the outcome model over the covariate distribution: $E[Y(d)] = \sum_{\mathbf{x}} E[Y \mid D=d, \mathbf{X}=\mathbf{x}] \, P(\mathbf{X}=\mathbf{x})$. |
| **Pokemon Analogy** | To estimate what would happen if *all* trainers used Exp. Share, take the average predicted badge count under Exp. Share use for each combination of trainer characteristics, then average over the population of characteristics. |
| **First Appears** | Chapter 11 |

---

### 25. Ignorability (Unconfoundedness)

| | |
|:---|:---|
| **Type** | Assumption |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | The assumption that, conditional on observed covariates $\mathbf{X}$, treatment assignment is independent of potential outcomes: $\{Y(0), Y(1)\} \perp\!\!\!\perp D \mid \mathbf{X}$. Also called "selection on observables" or "no unmeasured confounding." |
| **Pokemon Analogy** | Among trainers with the same wealth and experience, whether they used Exp. Share is essentially random (not driven by anything else that affects badges). All the confounders are in your dataset. |
| **First Appears** | Chapter 2 |

---

### 26. Instrumental Variable (IV)

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Intermediate |
| **Rarity** | Common |
| **Definition** | A variable $Z$ that (i) is correlated with the treatment $D$ (relevance), (ii) affects the outcome $Y$ only through $D$ (exclusion restriction), and (iii) is not confounded with $Y$ (independence/exogeneity). |
| **Pokemon Analogy** | The Safari Zone lottery is an instrument: winning the lottery (Z) affects whether you visit the Safari Zone (D), which affects your rare Pokemon collection (Y). Winning the lottery does not directly affect your collection except through actually visiting. |
| **First Appears** | Chapter 7 |

---

### 27. Interference

| | |
|:---|:---|
| **Type** | Threat |
| **Tier** | Advanced |
| **Rarity** | Uncommon |
| **Definition** | A violation of SUTVA that occurs when one unit's treatment affects another unit's outcome. In the presence of interference, the standard potential outcomes framework breaks down because $Y_i$ depends not just on $D_i$ but also on $D_j$ for $j \neq i$. |
| **Pokemon Analogy** | In double battles, your partner's strategy affects your outcome. If your partner uses a move that powers up your Pokemon, your treatment effect depends on their treatment --- interference. |
| **First Appears** | Chapter 11 |

---

### 28. IPW (Inverse Probability Weighting)

| | |
|:---|:---|
| **Type** | Estimator |
| **Tier** | Intermediate |
| **Rarity** | Common |
| **Definition** | An estimator that weights each observation by the inverse of its probability of receiving its actual treatment: $\hat{\tau}_{IPW} = \frac{1}{n}\sum_i \frac{D_i Y_i}{\hat{e}(\mathbf{X}_i)} - \frac{1}{n}\sum_i \frac{(1-D_i) Y_i}{1 - \hat{e}(\mathbf{X}_i)}$. Creates a pseudo-population where treatment is independent of covariates. |
| **Pokemon Analogy** | A wealthy, experienced trainer who uses Exp. Share is "expected" --- they get a low weight. A poor, inexperienced trainer who uses Exp. Share is "surprising" --- they get a high weight. Reweighting makes the groups comparable. |
| **First Appears** | Chapter 6 |

---

### 29. ITE (Individual Treatment Effect)

| | |
|:---|:---|
| **Type** | Estimand |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | The causal effect of treatment for a specific unit: $\tau_i = Y_i(1) - Y_i(0)$. Fundamentally unobservable because we can only see one potential outcome per unit (the Fundamental Problem of Causal Inference). |
| **Pokemon Analogy** | How many *more* badges would Trainer Red #4521 specifically earn with Exp. Share vs. without? We can never know for certain because Red cannot live the same journey twice. |
| **First Appears** | Chapter 2 |

---

### 30. LATE (Local Average Treatment Effect)

| | |
|:---|:---|
| **Type** | Estimand |
| **Tier** | Intermediate |
| **Rarity** | Common |
| **Definition** | The average treatment effect among *compliers* --- units whose treatment status is changed by the instrument: $\text{LATE} = E[Y(1) - Y(0) \mid \text{complier}] = \frac{E[Y \mid Z=1] - E[Y \mid Z=0]}{E[D \mid Z=1] - E[D \mid Z=0]}$. |
| **Pokemon Analogy** | The Safari Zone lottery effect applies specifically to trainers who visit *because* they won the lottery (compliers), not to those who would visit regardless (always-takers) or never visit (never-takers). |
| **First Appears** | Chapter 7 |

---

### 31. Matching

| | |
|:---|:---|
| **Type** | Estimator |
| **Tier** | Intermediate |
| **Rarity** | Common |
| **Definition** | A method that estimates causal effects by pairing treated units with similar control units based on observed covariates. The treatment effect is the average outcome difference within matched pairs. |
| **Pokemon Analogy** | For each trainer who used Exp. Share, find a "twin" --- a trainer with similar wealth, experience, and strategy score --- who did not use it. Compare their badge counts. |
| **First Appears** | Chapter 5 |

---

### 32. Mediator

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | A variable $M$ that lies on a causal path from treatment $T$ to outcome $Y$: $T \to M \to Y$. The mediator transmits (part of) the treatment's effect. |
| **Pokemon Analogy** | `team_level_avg` mediates the effect of `trainer_experience` on `badges`: more experience leads to higher team levels, which leads to more badges. |
| **First Appears** | Chapter 3 |

---

### 33. Mediation (NDE/NIE)

| | |
|:---|:---|
| **Type** | Estimand |
| **Tier** | Advanced |
| **Rarity** | Uncommon |
| **Definition** | Decomposition of a total effect into a Natural Direct Effect (NDE) --- the effect of treatment holding the mediator fixed --- and a Natural Indirect Effect (NIE) --- the effect operating through the mediator. Total effect $= $ NDE $+$ NIE. |
| **Pokemon Analogy** | Does `trainer_experience` improve badges directly (NDE: experience gives strategic intuition) or indirectly through leveling up the team (NIE: experience $\to$ `team_level_avg` $\to$ `badges`)? |
| **First Appears** | Chapter 11 |

---

### 34. MSM (Marginal Structural Model)

| | |
|:---|:---|
| **Type** | Estimator |
| **Tier** | Advanced |
| **Rarity** | Rare |
| **Definition** | A model for the potential outcomes as a function of treatment history, estimated using inverse probability of treatment weighting (IPTW) to handle time-varying confounding. |
| **Pokemon Analogy** | A trainer's item usage changes over time, and past badge counts affect future item choices. An MSM uses careful reweighting to estimate the effect of a full treatment sequence (e.g., Exp. Share in month 1, Rare Candy in month 2). |
| **First Appears** | Chapter 11 |

---

### 35. Outcome

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | The variable whose causal determinants we wish to understand. Denoted $Y$. |
| **Pokemon Analogy** | The number of `badges` earned, `elite_four_wins`, or `total_battles_won` --- whatever we are trying to explain or predict under intervention. |
| **First Appears** | Chapter 1 |

---

### 36. Overlap (Common Support)

| | |
|:---|:---|
| **Type** | Assumption |
| **Tier** | Intermediate |
| **Rarity** | Common |
| **Definition** | The requirement that for every combination of covariates, there is a positive probability of receiving either treatment condition: $0 < P(D = 1 \mid \mathbf{X} = \mathbf{x}) < 1$ for all $\mathbf{x}$. Also called common support or positivity. |
| **Pokemon Analogy** | For matching and IPW to work, there must be both Exp. Share users *and* non-users at every wealth and experience level. If all wealthy trainers use Exp. Share (no overlap), we cannot compare. |
| **First Appears** | Chapter 5 |

---

### 37. OVB (Omitted Variable Bias)

| | |
|:---|:---|
| **Type** | Threat |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | Bias in an estimated treatment effect that arises from failing to control for a confounder. The OVB formula for a simple regression is: $\text{Bias} = \gamma \times \delta$, where $\gamma$ is the effect of the omitted variable on the outcome and $\delta$ is the association between the omitted variable and the treatment. |
| **Pokemon Analogy** | If you regress badges on Exp. Share without controlling for wealth, the Exp. Share coefficient is inflated because wealth (omitted) positively affects both Exp. Share use ($\delta > 0$) and badges ($\gamma > 0$). |
| **First Appears** | Chapter 4 |

---

### 38. Parallel Trends

| | |
|:---|:---|
| **Type** | Assumption |
| **Tier** | Intermediate |
| **Rarity** | Common |
| **Definition** | The key identifying assumption of difference-in-differences: in the absence of treatment, the treated and control groups would have followed the same trend over time. $E[Y_t(0) - Y_{t-1}(0) \mid D=1] = E[Y_t(0) - Y_{t-1}(0) \mid D=0]$. |
| **Pokemon Analogy** | Before Team Rocket invaded Saffron, trainer activity in Saffron and Celadon was trending in the same direction. We assume that, without the invasion, they would have continued on the same path. |
| **First Appears** | Chapter 9 |

---

### 39. Partial Identification

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Advanced |
| **Rarity** | Rare |
| **Definition** | When assumptions are insufficient to point-identify a causal effect, partial identification provides bounds --- an interval that the true effect must lie within, given the data and maintained assumptions. |
| **Pokemon Analogy** | If we cannot observe `patience`, we may not be able to pin down the exact effect of Safari Zone visits on catches, but we can say "the effect is between 0.5 and 2.3 additional Pokemon per visit." |
| **First Appears** | Chapter 11 |

---

### 40. Positivity

| | |
|:---|:---|
| **Type** | Assumption |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | Identical to overlap. For all covariate strata, $P(D=1 \mid \mathbf{X}) > 0$ and $P(D=0 \mid \mathbf{X}) > 0$. Without positivity, the counterfactual outcome is unidentified for some subgroups. |
| **Pokemon Analogy** | If every trainer from Cinnabar Island uses Exp. Share (positivity violation), we have no basis for estimating what their badges would be without it. |
| **First Appears** | Chapter 2 |

---

### 41. Potential Outcomes

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | The pair of outcomes each unit would experience under treatment and control: $Y_i(1)$ and $Y_i(0)$. The Rubin Causal Model (RCM) defines causal effects as contrasts between potential outcomes. Only one is observed; the other is the counterfactual. |
| **Pokemon Analogy** | Trainer Ash has two potential badge counts: $Y_{Ash}(1) = 7$ badges with Exp. Share, $Y_{Ash}(0) = 5$ badges without. We observe one; the other exists only in a parallel universe. |
| **First Appears** | Chapter 2 |

---

### 42. Propensity Score

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Intermediate |
| **Rarity** | Common |
| **Definition** | The probability of receiving treatment given observed covariates: $e(\mathbf{x}) = P(D = 1 \mid \mathbf{X} = \mathbf{x})$. Rosenbaum and Rubin (1983) showed that conditioning on the propensity score is sufficient for removing confounding bias (given ignorability). |
| **Pokemon Analogy** | The propensity score is the probability that a trainer uses Exp. Share, given their wealth, experience, and other characteristics. Two trainers with the same propensity score are "equally likely" to have used Exp. Share, even if their individual covariates differ. |
| **First Appears** | Chapter 5 |

---

### 43. Randomization Inference (Fisher's Exact Test)

| | |
|:---|:---|
| **Type** | Estimator |
| **Tier** | Intermediate |
| **Rarity** | Uncommon |
| **Definition** | A permutation-based approach to hypothesis testing. Under the sharp null ($H_0: Y_i(1) = Y_i(0)$ for all $i$), the observed data are consistent with any assignment, so we compute the test statistic for all (or many sampled) permutations to obtain an exact $p$-value. |
| **Pokemon Analogy** | Under the null that Protein has no effect on Pokemon strength, shuffle the treatment labels across Pokemon 10,000 times. If the observed difference is larger than 95% of the permuted differences, reject the null. |
| **First Appears** | Chapter 4 |

---

### 44. RCT (Randomized Controlled Trial)

| | |
|:---|:---|
| **Type** | Design |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | An experimental design where units are randomly assigned to treatment or control. Randomization ensures that treatment is independent of all potential confounders (both measured and unmeasured), making the simple difference in means an unbiased estimator of the ATE. |
| **Pokemon Analogy** | The Pewter Protein RCT randomly assigns Protein supplements to Pokemon, eliminating confounders. We do not need to worry about which Pokemon would "choose" to take Protein --- assignment is by coin flip. |
| **First Appears** | Chapter 4 |

---

### 45. RDD, Fuzzy

| | |
|:---|:---|
| **Type** | Design |
| **Tier** | Advanced |
| **Rarity** | Uncommon |
| **Definition** | A regression discontinuity design where crossing the threshold *increases the probability* of treatment but does not guarantee it. Estimated via IV/2SLS using threshold crossing as an instrument for treatment. |
| **Pokemon Analogy** | When a Pokemon's happiness crosses 220, it is *more likely* to evolve but might not (e.g., the trainer might cancel). The jump in evolution probability at the cutoff identifies the effect. |
| **First Appears** | Chapter 8 |

---

### 46. RDD, Sharp

| | |
|:---|:---|
| **Type** | Design |
| **Tier** | Intermediate |
| **Rarity** | Common |
| **Definition** | A quasi-experimental design that exploits a known threshold: units just above the cutoff receive treatment, units just below do not. The causal effect is identified by the discontinuity in outcomes at the cutoff: $\tau_{RDD} = \lim_{r \downarrow c} E[Y \mid R=r] - \lim_{r \uparrow c} E[Y \mid R=r]$. |
| **Pokemon Analogy** | Pokemon with happiness $\geq 220$ evolve; those just below 220 do not. By comparing battle stats of Pokemon just above and just below the threshold, we identify the causal effect of evolution. |
| **First Appears** | Chapter 8 |

---

### 47. Rosenbaum Bounds

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Advanced |
| **Rarity** | Uncommon |
| **Definition** | A sensitivity analysis framework that asks: how much unmeasured confounding ($\Gamma$) would be required to change the study's conclusion? For a given $\Gamma$, it computes worst-case $p$-values and confidence intervals. |
| **Pokemon Analogy** | If a hidden trait $\Gamma = 2$ times as likely to drive Exp. Share use could explain away the effect, and you believe no such trait exists, your result is robust. If even $\Gamma = 1.1$ would nullify the finding, it is fragile. |
| **First Appears** | Chapter 11 |

---

### 48. Selection Bias

| | |
|:---|:---|
| **Type** | Threat |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | Bias arising from systematic differences between the treated and control groups that are related to the outcome. In the potential outcomes framework: $E[Y(0) \mid D=1] \neq E[Y(0) \mid D=0]$. |
| **Pokemon Analogy** | Trainers who *choose* to use Exp. Share are wealthier and more experienced than those who don't. Comparing their badge counts conflates the Exp. Share effect with pre-existing advantages. |
| **First Appears** | Chapter 2 |

---

### 49. Sensitivity Analysis

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Intermediate |
| **Rarity** | Common |
| **Definition** | A suite of methods for assessing how robust a causal conclusion is to violations of identifying assumptions (especially unmeasured confounding). Includes Rosenbaum bounds, E-values, and Cinelli-Hazlett partial $R^2$ approaches. |
| **Pokemon Analogy** | After estimating Exp. Share's effect, ask: "How strong would an unmeasured confounder need to be to destroy this result?" If the answer is "implausibly strong," the finding is robust. |
| **First Appears** | Chapter 11 |

---

### 50. Simpson's Paradox

| | |
|:---|:---|
| **Type** | Threat |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | A phenomenon where a trend that appears in aggregated data reverses or disappears when the data is disaggregated by a confounding variable. |
| **Pokemon Analogy** | Squirtle trainers have more badges overall, but *within* each wealth level, starter type makes no difference. The aggregate pattern is driven by wealthy trainers disproportionately choosing Squirtle. |
| **First Appears** | Chapter 1 |

---

### 51. Spillover

| | |
|:---|:---|
| **Type** | Threat |
| **Tier** | Advanced |
| **Rarity** | Uncommon |
| **Definition** | A specific form of interference where one unit's treatment affects nearby or connected units' outcomes. Violates SUTVA and the assumption that potential outcomes depend only on own treatment. |
| **Pokemon Analogy** | If a strong trainer at a Gym deters weaker trainers from challenging it, the strong trainer's treatment (training) "spills over" to affect others' badge-earning opportunities. |
| **First Appears** | Chapter 11 |

---

### 52. SUTVA (Stable Unit Treatment Value Assumption)

| | |
|:---|:---|
| **Type** | Assumption |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | The assumption that (i) there is no interference between units (one trainer's treatment does not affect another's outcome) and (ii) there is only one version of each treatment level (consistency). |
| **Pokemon Analogy** | Your badges depend only on *your* Exp. Share usage, not on whether your rival also uses it. And "using Exp. Share" means the same thing for everyone. |
| **First Appears** | Chapter 2 |

---

### 53. Survivorship Bias

| | |
|:---|:---|
| **Type** | Threat |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | A form of selection bias where only "surviving" units (those who passed some selection filter) are observed, creating a misleading picture of the full population. |
| **Pokemon Analogy** | If we only study trainers who reached the Elite Four, we miss everyone who quit. The survivors look uniformly strong, hiding the fact that many strategies failed along the way. |
| **First Appears** | Chapter 2 |

---

### 54. Synthetic Control

| | |
|:---|:---|
| **Type** | Estimator |
| **Tier** | Advanced |
| **Rarity** | Uncommon |
| **Definition** | A method for comparative case studies that constructs a weighted combination of control units to serve as a counterfactual for a single treated unit. The weights are chosen to match the treated unit's pre-treatment outcomes. |
| **Pokemon Analogy** | After Team Rocket invades Saffron City, build a "Synthetic Saffron" from a weighted combination of Celadon (40%), Vermilion (35%), and Cerulean (25%) that matched Saffron's pre-invasion trends. The post-invasion gap between real and synthetic Saffron is the causal effect. |
| **First Appears** | Chapter 9 |

---

### 55. TMLE (Targeted Minimum Loss-Based Estimation)

| | |
|:---|:---|
| **Type** | Estimator |
| **Tier** | Frontier |
| **Rarity** | Rare |
| **Definition** | A semiparametric estimation procedure that targets a specific causal parameter (e.g., ATE) by iteratively updating an initial outcome model estimate using a clever covariate derived from the propensity score. It is doubly robust and achieves semiparametric efficiency bounds. |
| **Pokemon Analogy** | TMLE is like a Mega Evolution for doubly robust estimation --- it starts with a standard estimate, then "evolves" it with a targeting step that focuses specifically on getting the causal effect right, even at the cost of overall prediction accuracy. |
| **First Appears** | Chapter 11 |

---

### 56. Transportability

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Advanced |
| **Rarity** | Rare |
| **Definition** | The problem of determining whether causal effects estimated in one population (source) are valid in another population (target) with a different covariate distribution. Requires understanding which features of the DGP differ between populations. |
| **Pokemon Analogy** | Does the causal effect of Exp. Share estimated in Kanto apply to trainers in Johto, where the Pokemon types, Gym Leaders, and regional culture differ? Transportability theory tells us when and how to adjust. |
| **First Appears** | Chapter 12 |

---

### 57. Treatment

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | The variable whose causal effect on the outcome we wish to estimate. Denoted $D$ or $T$. Can be binary (used Exp. Share or not), multi-valued (Bulbasaur, Charmander, Squirtle), or continuous (hours of training). |
| **Pokemon Analogy** | Whether the trainer used Exp. Share ($D = 1$) or not ($D = 0$). |
| **First Appears** | Chapter 1 |

---

### 58. TWFE (Two-Way Fixed Effects)

| | |
|:---|:---|
| **Type** | Estimator |
| **Tier** | Intermediate |
| **Rarity** | Common |
| **Definition** | A regression with unit and time fixed effects used to estimate treatment effects in panel data: $Y_{it} = \alpha_i + \lambda_t + \tau D_{it} + \varepsilon_{it}$. Under staggered treatment timing, the standard TWFE estimator can be biased due to "forbidden comparisons." |
| **Pokemon Analogy** | Regress trainer activity on city fixed effects (each city's baseline level), month fixed effects (seasonal trends), and a Team Rocket invasion indicator. The coefficient on invasion is the DiD estimate --- but beware if cities are invaded at different times. |
| **First Appears** | Chapter 9 |

---

### 59. 2SLS (Two-Stage Least Squares)

| | |
|:---|:---|
| **Type** | Estimator |
| **Tier** | Intermediate |
| **Rarity** | Common |
| **Definition** | The standard IV estimator. Stage 1: regress treatment on instrument(s) and covariates to get predicted treatment $\hat{D}$. Stage 2: regress outcome on $\hat{D}$ and covariates. The coefficient on $\hat{D}$ is the IV estimate of the causal effect. |
| **Pokemon Analogy** | Stage 1: predict Safari Zone visits from lottery outcome. Stage 2: regress rare Pokemon count on *predicted* visits. The lottery provides exogenous variation that isolates the causal effect of visiting the Safari Zone. |
| **First Appears** | Chapter 7 |

---

### 60. Unit

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | The entity for which we define treatment, outcome, and potential outcomes. Could be a person, firm, city, time period, or any object of study. Indexed by $i$. |
| **Pokemon Analogy** | A single trainer (row in `kanto_trainers.csv`), a single Pokemon (in the Protein RCT), or a single city-month (in the panel data). |
| **First Appears** | Chapter 1 |

---

### 61. Weak Instrument

| | |
|:---|:---|
| **Type** | Threat |
| **Tier** | Intermediate |
| **Rarity** | Common |
| **Definition** | An instrument that has a very small correlation with the treatment (low first-stage $F$-statistic, typically $F < 10$). Weak instruments lead to biased IV estimates (toward the OLS estimate), wide confidence intervals, and unreliable inference. |
| **Pokemon Analogy** | If winning the Safari Zone lottery barely increases the chance of actually visiting (most winners ignore the prize), the lottery is a weak instrument. The IV estimate will be noisy and biased. |
| **First Appears** | Chapter 7 |

---

### 62. Causal Effect

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | The difference between what *would* happen under treatment and what *would* happen under control: $\tau = Y(1) - Y(0)$. Can refer to individual ($\tau_i$), average ($\text{ATE}$), or subgroup effects ($\text{CATE}$, $\text{ATT}$). |
| **Pokemon Analogy** | The true number of extra badges Exp. Share causes a trainer to earn --- not the observed difference, which may be confounded. |
| **First Appears** | Chapter 1 |

---

### 63. External Validity

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Intermediate |
| **Rarity** | Common |
| **Definition** | The extent to which a causal finding from one study (sample, setting, time) applies to other populations or contexts. Related to transportability and generalizability. |
| **Pokemon Analogy** | The Pewter Protein RCT was conducted in Pewter City with Rock-type Pokemon. Does the finding generalize to Cerulean City's Water-types? To Johto trainers entirely? |
| **First Appears** | Chapter 12 |

---

### 64. Internal Validity

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | The extent to which a study accurately estimates the causal effect for the specific population and setting studied. Threats include confounding, selection bias, measurement error, and attrition. |
| **Pokemon Analogy** | Even if the Protein RCT result does not generalize to Johto, is the result correct *within Pewter City*? That is the question of internal validity. |
| **First Appears** | Chapter 4 |

---

### 65. Fundamental Problem of Causal Inference

| | |
|:---|:---|
| **Type** | Concept |
| **Tier** | Foundational |
| **Rarity** | Common |
| **Definition** | For any individual unit, we can observe at most one potential outcome. We observe $Y_i(1)$ if treated or $Y_i(0)$ if not, but never both. Therefore, the individual treatment effect $\tau_i = Y_i(1) - Y_i(0)$ is never directly observable. |
| **Pokemon Analogy** | You chose Charmander. You will never know what would have happened with Squirtle. No amount of data about *other* trainers changes the fact that *your* counterfactual is forever missing. |
| **First Appears** | Chapter 2 |

---

> *Professor Oak closes the Pokedex. "There are 65 entries here," he says, "but the world of causal inference is always expanding --- new estimators, new assumptions, new threats. Your Pokedex will never be truly complete. But with these 65, you have enough to navigate every route in Kanto."*

---

*Return to: [Table of Contents](../toc.md)*
