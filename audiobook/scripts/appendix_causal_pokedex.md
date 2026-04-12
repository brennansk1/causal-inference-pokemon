---
title: "Appendix: The Causal Pokedex"
chapter_number: 10
source_file: "textbook/chapters/appendix_d_glossary.md"
estimated_runtime_minutes: 20
key_concepts: []
characters:
  - narrator
  - oak
---

# Appendix: The Causal Pokedex

NARRATOR: This is the Causal Pokedex -- a quick-reference guide to the key terms and concepts from the textbook. Each entry gives you the term, a plain-English definition, and which chapter it first appeared in. You can listen straight through as a review, or come back to individual entries when you need a refresher.

[pause]

OAK: Let us begin.

[TEACHING SECTION]

OAK: Average Treatment Effect, or ATE. The expected difference in outcomes between treatment and control, averaged across the entire population. First introduced in Chapter One.

OAK: Average Treatment Effect on the Treated, or ATT. The expected treatment effect among those who actually received treatment. Also Chapter One.

OAK: Backdoor criterion. A graphical rule that tells you which variables to condition on to identify a causal effect from observational data. You need to block all backdoor paths from treatment to outcome without opening any new spurious paths. Chapter Three.

OAK: Causal forest. A machine learning method that estimates heterogeneous treatment effects by partitioning the covariate space into regions with different treatment effects. Chapter Eight.

OAK: CATE, or Conditional Average Treatment Effect. The average treatment effect for a subgroup defined by specific covariate values. Chapter Eight.

OAK: Collider. A variable caused by two or more other variables. Conditioning on a collider opens a spurious association between its causes. Chapter Three.

OAK: Confounder. A variable that causes both the treatment and the outcome, creating a spurious association between them. Chapter One.

OAK: Counterfactual. The outcome that would have occurred under an alternative treatment assignment. Fundamentally unobservable for any individual. Chapter One.

OAK: DAG, or Directed Acyclic Graph. A diagram representing causal assumptions, with nodes for variables and arrows for direct causal effects. No loops allowed. Chapter Three.

OAK: d-separation. A graphical criterion for determining whether two variables are conditionally independent given a set of conditioning variables, based on the structure of the DAG. Chapter Three.

OAK: Difference-in-Differences, or DiD. A method that compares changes over time between a treatment group and a control group, under the assumption that both groups would have followed parallel trends in the absence of treatment. Chapter Seven.

OAK: Double Debiased Machine Learning, or DML. A framework for using machine learning to estimate nuisance parameters while maintaining valid inference for the causal parameter of interest. Uses Neyman orthogonality and cross-fitting. Chapter Eight.

OAK: Doubly robust estimation. An estimator that combines an outcome model and a propensity score model, and is consistent if either model is correctly specified. Chapter Five.

OAK: E-value. The minimum strength of association an unobserved confounder would need with both treatment and outcome to explain away an observed effect. Chapter Eight.

OAK: Exclusion restriction. The assumption that an instrument affects the outcome only through its effect on the treatment. Chapter Six.

OAK: Fundamental problem of causal inference. We can never observe both potential outcomes for the same unit at the same time. Chapter One.

OAK: Ignorability. The assumption that treatment assignment is independent of potential outcomes, conditional on observed covariates. Also called selection on observables or conditional independence. Chapter One.

OAK: Instrumental variable, or IV. A variable that affects the treatment but has no direct effect on the outcome, used to estimate causal effects when there is unmeasured confounding. Chapter Six.

OAK: Inverse probability weighting, or IPW. A method that weights each observation by the inverse of its probability of receiving its actual treatment, creating a pseudo-population where treatment is independent of covariates. Chapter Five.

OAK: LATE, or Local Average Treatment Effect. The average treatment effect among compliers -- units whose treatment status is affected by the instrument. Chapter Six.

OAK: Love plot. A visual diagnostic showing covariate balance before and after matching, with standardized mean differences plotted for each covariate. Chapter Four.

OAK: Matching. A method that pairs treated and control units with similar covariate values to reduce confounding bias. Chapter Four.

OAK: Mediator. A variable on the causal path from treatment to outcome. The treatment affects the mediator, which in turn affects the outcome. Chapter Eight.

OAK: Natural Direct Effect, or NDE. The effect of changing treatment while holding the mediator at its natural control value. Chapter Eight.

OAK: Natural Indirect Effect, or NIE. The effect of shifting the mediator from its control value to its treatment value, while holding treatment fixed. Chapter Eight.

OAK: Parallel trends assumption. The assumption that treatment and control groups would have followed the same trajectory over time in the absence of treatment. Required for difference-in-differences. Chapter Seven.

OAK: Potential outcomes. The outcomes a unit would experience under each possible treatment assignment. The pair of potential outcomes defines the individual causal effect. Chapter One.

OAK: Propensity score. The probability of receiving treatment given observed covariates. A summary statistic sufficient for removing confounding from observed covariates. Chapter Four.

OAK: Regression Discontinuity Design, or RDD. A method that estimates causal effects by exploiting a threshold in a running variable that determines treatment assignment. Chapter Six.

OAK: Rosenbaum bounds. A sensitivity analysis framework that asks: how much hidden bias would be needed to explain away an observed treatment effect in a matched study? Chapter Eight.

OAK: Selection bias. The bias that arises when the treated and untreated groups differ systematically in ways that affect the outcome, beyond the treatment itself. Chapter One.

OAK: Simpson's Paradox. A phenomenon where an association that holds in every subgroup reverses when the subgroups are combined. Typically caused by a confounding variable. Chapter Three.

OAK: SUTVA, the Stable Unit Treatment Value Assumption. The assumption that each unit's outcome depends only on its own treatment, not on others' treatments, and that there are no hidden variations of treatment. Chapter One.

OAK: Synthetic control. A method that constructs a weighted combination of untreated units to serve as a counterfactual for a single treated unit, used in comparative case studies. Chapter Seven.

OAK: Transportability. The conditions under which a causal effect estimated in one population can be applied to a different population. Chapter Eight.

[pause]

NARRATOR: That is the Causal Pokedex. Thirty-three entries covering the core vocabulary of causal inference. If you can define each of these terms and explain when and why each matters, you have a solid command of the field.

OAK: And remember -- the Pokedex is never truly complete. There are always more concepts to discover.
