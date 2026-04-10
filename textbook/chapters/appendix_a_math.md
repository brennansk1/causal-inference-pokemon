# Appendix A: Mathematical Notation & Probability Review --- Professor Oak's Math Lab

---

*You arrive at Professor Oak's lab early in the morning, hoping to pick up a new Pokedex upgrade, but instead find the Professor surrounded by chalkboards covered in equations. "Ah, perfect timing!" he says, adjusting his glasses. "Before we send you off to study causal inference, we need to make sure your mathematical toolkit is in order. Think of this as leveling up your stats before a Gym battle --- you wouldn't challenge Sabrina without a solid foundation, would you?"*

---

## A.1 Sets and Logic

A **set** is a collection of distinct objects. In the Kanto region, we work with sets constantly.

**Notation.** We write sets with curly braces: $A = \{\text{Bulbasaur}, \text{Charmander}, \text{Squirtle}\}$ is the set of Kanto starters. The symbol $\in$ means "is an element of," so $\text{Pikachu} \notin A$ while $\text{Charmander} \in A$.

**Key operations:**

| Operation | Symbol | Definition | Pokemon Example |
|:---|:---:|:---|:---|
| Union | $A \cup B$ | All elements in $A$ or $B$ (or both) | Fire types $\cup$ Flying types = all Pokemon that are Fire, Flying, or both |
| Intersection | $A \cap B$ | All elements in both $A$ and $B$ | Fire types $\cap$ Flying types = $\{\text{Charizard}, \text{Moltres}\}$ |
| Complement | $A^c$ | All elements not in $A$ | (Water types)$^c$ = all non-Water types |
| Difference | $A \setminus B$ | Elements in $A$ but not in $B$ | Poison types $\setminus$ Grass types = pure Poison types |
| Empty set | $\emptyset$ | The set with no elements | Ice types $\cap$ Fire types $= \emptyset$ (no dual Ice/Fire in Gen I) |
| Subset | $A \subseteq B$ | Every element of $A$ is also in $B$ | $\{\text{Pikachu}\} \subseteq$ Electric types |

**De Morgan's Laws** are useful for manipulating complements of unions and intersections:

$$
(A \cup B)^c = A^c \cap B^c \qquad \text{and} \qquad (A \cap B)^c = A^c \cup B^c
$$

*Pokemon reading:* A Pokemon that is *not* (Fire or Water) must be *both* non-Fire *and* non-Water. A Pokemon that is *not* (Fire and Water simultaneously) is either non-Fire *or* non-Water (or both).

**Logical connectives.** We use $\implies$ for "implies" and $\iff$ for "if and only if." For example: $\text{badges} = 8 \implies \text{elite\_four\_attempted} = 1$ (you must have all eight badges to challenge the Elite Four), but $\text{elite\_four\_attempted} = 1 \not\Rightarrow \text{champion\_defeated} = 1$ (attempting does not guarantee victory).

---

## A.2 Probability Basics

### Sample Spaces and Events

A **sample space** $\Omega$ is the set of all possible outcomes of a random experiment. An **event** is any subset of $\Omega$.

*Example.* You throw a Poke Ball at a wild Pidgey. The sample space is $\Omega = \{\text{catch}, \text{escape}\}$. The event "you catch it" is $A = \{\text{catch}\}$.

For a more complex example, consider a wild Pokemon encounter on Route 1. The sample space might be $\Omega = \{\text{Pidgey}, \text{Rattata}, \text{Pikachu}\}$ with encounter probabilities $P(\text{Pidgey}) = 0.55$, $P(\text{Rattata}) = 0.40$, and $P(\text{Pikachu}) = 0.05$.

### Axioms of Probability (Kolmogorov)

For any probability measure $P$ on a sample space $\Omega$:

1. **Non-negativity:** $P(A) \geq 0$ for all events $A$.
2. **Normalization:** $P(\Omega) = 1$ (something must happen).
3. **Countable additivity:** For mutually exclusive events $A_1, A_2, \ldots$,

$$
P\!\left(\bigcup_{i=1}^{\infty} A_i\right) = \sum_{i=1}^{\infty} P(A_i)
$$

*Pokemon check:* The probabilities of encountering Pidgey, Rattata, or Pikachu on Route 1 must sum to 1 (assuming no other encounters). Each probability is non-negative. Since the encounters are mutually exclusive (you encounter exactly one species at a time), $P(\text{Pidgey or Rattata}) = P(\text{Pidgey}) + P(\text{Rattata}) = 0.95$.

### Useful Probability Rules

- **Complement rule:** $P(A^c) = 1 - P(A)$. The probability of *not* catching a Pokemon is $1$ minus the catch probability.
- **Addition rule:** $P(A \cup B) = P(A) + P(B) - P(A \cap B)$.
- **Multiplication rule:** $P(A \cap B) = P(A) \cdot P(B \mid A)$.

---

## A.3 Conditional Probability and Bayes' Rule

### Conditional Probability

The **conditional probability** of event $A$ given event $B$ is:

$$
P(A \mid B) = \frac{P(A \cap B)}{P(B)}, \quad P(B) > 0
$$

*Example.* What is the probability of catching a wild Abra, given that you used an Ultra Ball?

Let $C = \{\text{catch}\}$ and $U = \{\text{Ultra Ball used}\}$. If we know that $P(C \cap U) = 0.35$ (35% of all encounter attempts involve using an Ultra Ball and result in a catch) and $P(U) = 0.40$ (40% of attempts use an Ultra Ball), then:

$$
P(C \mid U) = \frac{0.35}{0.40} = 0.875
$$

### Bayes' Rule

**Bayes' theorem** inverts conditional probabilities:

$$
P(A \mid B) = \frac{P(B \mid A) \cdot P(A)}{P(B)}
$$

This is critical because the direction of conditioning matters enormously. $P(\text{Catch} \mid \text{Ultra Ball})$ is *not* the same as $P(\text{Ultra Ball} \mid \text{Catch})$.

*Kanto example.* A Kanto Ranger reports that 80% of trainers who defeated the Champion had used Exp. Share ($P(\text{Exp. Share} \mid \text{Champion}) = 0.80$). Does Exp. Share cause Championship victories? Not necessarily. We need to consider:

- $P(\text{Champion}) = 0.05$ (only 5% of trainers defeat the Champion)
- $P(\text{Exp. Share}) = 0.45$ (45% of all trainers use Exp. Share)

By Bayes' rule:

$$
P(\text{Champion} \mid \text{Exp. Share}) = \frac{0.80 \times 0.05}{0.45} \approx 0.089
$$

So even though 80% of Champions used Exp. Share, only about 8.9% of Exp. Share users become Champion. The base rates matter.

### Law of Total Probability

For a partition $\{B_1, B_2, \ldots, B_k\}$ of $\Omega$:

$$
P(A) = \sum_{i=1}^{k} P(A \mid B_i) \, P(B_i)
$$

*Example.* The overall catch rate of a wild Pokemon depends on which ball you use:

$$
P(\text{Catch}) = P(\text{Catch} \mid \text{Poke Ball}) P(\text{Poke Ball}) + P(\text{Catch} \mid \text{Great Ball}) P(\text{Great Ball}) + P(\text{Catch} \mid \text{Ultra Ball}) P(\text{Ultra Ball})
$$

---

## A.4 Random Variables

A **random variable** $X$ is a function that maps outcomes in a sample space to real numbers: $X: \Omega \to \mathbb{R}$.

### Discrete Random Variables

A discrete random variable takes on a countable number of values. Its distribution is described by a **probability mass function (PMF)**:

$$
p_X(x) = P(X = x), \quad \sum_x p_X(x) = 1
$$

*Example.* Let $X$ be the number of badges a trainer earns. $X \in \{0, 1, 2, 3, 4, 5, 6, 7, 8\}$. The PMF assigns a probability to each badge count.

### Continuous Random Variables

A continuous random variable can take any value in an interval (or union of intervals). Its distribution is described by a **probability density function (PDF)** $f_X(x)$:

$$
P(a \leq X \leq b) = \int_a^b f_X(x) \, dx, \quad \int_{-\infty}^{\infty} f_X(x) \, dx = 1
$$

*Example.* A Pokemon's IV (Individual Value) total ranges from 0 to 186. Across the population, $X = \text{team\_avg\_iv\_total}$ is approximately continuous, with a density function concentrated around 45--90.

### Cumulative Distribution Function (CDF)

The **CDF** is defined for both discrete and continuous random variables:

$$
F_X(x) = P(X \leq x)
$$

Properties: $F_X$ is non-decreasing, $\lim_{x \to -\infty} F_X(x) = 0$, and $\lim_{x \to \infty} F_X(x) = 1$.

*Pokemon reading:* $F_{\text{badges}}(5) = P(\text{badges} \leq 5)$ is the fraction of trainers with five or fewer badges.

---

## A.5 Expectation and Variance

### Expectation

The **expected value** (or mean) of a random variable is its long-run average:

$$
E[X] = \begin{cases} \displaystyle\sum_x x \, p_X(x) & \text{(discrete)} \\[6pt] \displaystyle\int_{-\infty}^{\infty} x \, f_X(x) \, dx & \text{(continuous)} \end{cases}
$$

**Linearity of expectation** (holds regardless of dependence):

$$
E[aX + bY + c] = a \, E[X] + b \, E[Y] + c
$$

*Pokemon example.* In the Pokemon damage formula, damage is (roughly) proportional to base power $\times$ type effectiveness multiplier $\times$ STAB bonus. If we treat these as independent random components:

$$
E[\text{Damage}] = E[\text{Base}] \times E[\text{Type Multiplier}] \times E[\text{STAB}]
$$

Note: this simplification uses the fact that the expectation of a product of *independent* random variables equals the product of their expectations. In general, $E[XY] = E[X]E[Y] + \text{Cov}(X, Y)$.

### Variance and Standard Deviation

The **variance** measures the spread of a distribution:

$$
\text{Var}(X) = E\!\left[(X - E[X])^2\right] = E[X^2] - (E[X])^2
$$

The **standard deviation** is $\sigma_X = \sqrt{\text{Var}(X)}$.

**Variance of a linear combination:**

$$
\text{Var}(aX + b) = a^2 \, \text{Var}(X)
$$

For independent $X$ and $Y$:

$$
\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) \quad \text{(independence required)}
$$

*Pokemon example.* If a trainer's strategy score has $E[\text{strategy}] = 45$ and $\text{Var}(\text{strategy}) = 150$, then the standard deviation is $\sigma \approx 12.2$, meaning most trainers fall within about 12 points of the average strategy score.

---

## A.6 Covariance and Correlation

### Covariance

The **covariance** between two random variables measures their linear co-movement:

$$
\text{Cov}(X, Y) = E\!\left[(X - E[X])(Y - E[Y])\right] = E[XY] - E[X]E[Y]
$$

Properties:

- $\text{Cov}(X, X) = \text{Var}(X)$
- $\text{Cov}(X, Y) = \text{Cov}(Y, X)$
- $\text{Cov}(aX + b, \, cY + d) = ac \, \text{Cov}(X, Y)$
- $\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2\,\text{Cov}(X, Y)$

### Pearson Correlation Coefficient

The **correlation** normalizes covariance to $[-1, 1]$:

$$
\rho_{XY} = \frac{\text{Cov}(X, Y)}{\sigma_X \, \sigma_Y}
$$

*Pokemon example.* Consider the Attack and Speed base stats across all 151 Kanto Pokemon. If Pokemon with high Attack tend to have high Speed, $\rho > 0$. If tanks (high Attack) tend to be slow, $\rho < 0$. If there is no linear pattern, $\rho \approx 0$.

**Important caution.** Correlation measures *linear* association. Two variables can be strongly related but have $\rho = 0$ if the relationship is nonlinear. And as this entire textbook emphasizes: correlation does not imply causation.

---

## A.7 Common Distributions

### Bernoulli Distribution

$X \sim \text{Bernoulli}(p)$: a single binary trial.

$$
P(X = 1) = p, \quad P(X = 0) = 1 - p
$$
$$
E[X] = p, \quad \text{Var}(X) = p(1-p)
$$

*Pokemon example.* A critical hit occurs with probability $p = 1/16$ in Generation I. Let $X = 1$ if a critical hit lands, $X = 0$ otherwise. Then $X \sim \text{Bernoulli}(1/16)$.

### Binomial Distribution

$X \sim \text{Binomial}(n, p)$: number of successes in $n$ independent Bernoulli trials.

$$
P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}, \quad k = 0, 1, \ldots, n
$$
$$
E[X] = np, \quad \text{Var}(X) = np(1-p)
$$

*Pokemon example.* A trainer fights $n = 20$ wild battles. Each battle is won independently with probability $p = 0.7$. The number of wins $X \sim \text{Binomial}(20, 0.7)$, so $E[X] = 14$ and $\text{Var}(X) = 4.2$.

### Poisson Distribution

$X \sim \text{Poisson}(\lambda)$: number of events in a fixed interval.

$$
P(X = k) = \frac{e^{-\lambda} \lambda^k}{k!}, \quad k = 0, 1, 2, \ldots
$$
$$
E[X] = \lambda, \quad \text{Var}(X) = \lambda
$$

*Pokemon example.* The number of wild encounters per 100 steps on Route 1 follows approximately $\text{Poisson}(\lambda = 8)$. The mean and variance are both 8.

### Normal (Gaussian) Distribution

$X \sim N(\mu, \sigma^2)$: the bell curve.

$$
f_X(x) = \frac{1}{\sigma \sqrt{2\pi}} \exp\!\left(-\frac{(x - \mu)^2}{2\sigma^2}\right)
$$
$$
E[X] = \mu, \quad \text{Var}(X) = \sigma^2
$$

*Pokemon example.* Across the population of 2,000 Kanto trainers, strategy scores are approximately $N(45, 150)$. By the 68--95--99.7 rule, about 68% of trainers have strategy scores within one standard deviation ($\approx 12.2$ points) of the mean.

### Uniform Distribution

$X \sim \text{Uniform}(a, b)$: every value in $[a, b]$ is equally likely.

$$
f_X(x) = \frac{1}{b - a}, \quad a \leq x \leq b
$$
$$
E[X] = \frac{a + b}{2}, \quad \text{Var}(X) = \frac{(b-a)^2}{12}
$$

*Pokemon example.* Latent traits like patience, natural talent, and dedication are drawn from $\text{Uniform}(0, 100)$ in our DGP, so $E[\text{patience}] = 50$ and $\text{Var}(\text{patience}) \approx 833.3$.

---

## A.8 Law of Large Numbers

### Weak Law of Large Numbers (WLLN)

Let $X_1, X_2, \ldots, X_n$ be i.i.d. random variables with $E[X_i] = \mu$ and $\text{Var}(X_i) = \sigma^2 < \infty$. Then the sample mean $\bar{X}_n = \frac{1}{n}\sum_{i=1}^n X_i$ converges in probability to $\mu$:

$$
\bar{X}_n \xrightarrow{p} \mu \quad \text{as } n \to \infty
$$

More precisely, for any $\varepsilon > 0$:

$$
\lim_{n \to \infty} P\!\left(|\bar{X}_n - \mu| > \varepsilon\right) = 0
$$

*Pokemon example.* Suppose a trainer's true win rate is $\mu = 0.65$. After $n = 10$ battles, the observed win rate might be 0.80 or 0.50 --- high variance. After $n = 1000$ battles, the observed win rate will be very close to 0.65. The more battles you fight, the closer your observed average converges to your true ability. This is why we trust league-level statistics (large $n$) more than a single trainer's anecdote (small $n$).

---

## A.9 Central Limit Theorem

### Statement

Let $X_1, X_2, \ldots, X_n$ be i.i.d. with $E[X_i] = \mu$ and $\text{Var}(X_i) = \sigma^2 \in (0, \infty)$. Then the standardized sample mean converges in distribution to a standard Normal:

$$
\frac{\bar{X}_n - \mu}{\sigma / \sqrt{n}} \xrightarrow{d} N(0, 1) \quad \text{as } n \to \infty
$$

Equivalently:

$$
\bar{X}_n \overset{approx}{\sim} N\!\left(\mu, \, \frac{\sigma^2}{n}\right) \quad \text{for large } n
$$

*Pokemon example.* Suppose each battle yields a random reward $X_i$ with mean $\mu = 500$ Pokedollars and standard deviation $\sigma = 200$. If a trainer fights $n = 100$ battles, the average reward per battle will be approximately:

$$
\bar{X}_{100} \sim N\!\left(500, \, \frac{200^2}{100}\right) = N(500, \, 400)
$$

So the average reward has standard deviation $\sqrt{400} = 20$ Pokedollars. A 95% confidence interval would be approximately $500 \pm 1.96 \times 20 = [460.8, \, 539.2]$.

**Why the CLT matters for causal inference.** Nearly every estimator in this textbook (difference in means, IPW, AIPW, Wald, 2SLS, DiD) is an average or a function of averages. The CLT guarantees that, in large enough samples, these estimators are approximately Normal --- which is why we can construct confidence intervals and perform hypothesis tests using Normal critical values.

---

## A.10 Conditional Expectation and the Law of Iterated Expectations

### Conditional Expectation

The **conditional expectation** of $Y$ given $X = x$ is the expected value of $Y$ computed using the conditional distribution of $Y \mid X = x$:

$$
E[Y \mid X = x] = \begin{cases} \displaystyle\sum_y y \, P(Y = y \mid X = x) & \text{(discrete)} \\[6pt] \displaystyle\int_{-\infty}^{\infty} y \, f_{Y|X}(y \mid x) \, dy & \text{(continuous)} \end{cases}
$$

When we write $E[Y \mid X]$ (without specifying $X = x$), this is itself a *random variable* --- it is a function of $X$.

*Pokemon example.* $E[\text{badges} \mid \text{starter\_type} = \text{Water}]$ is the average badge count among Water-type starter trainers. This is a single number. But $E[\text{badges} \mid \text{starter\_type}]$ is a random variable that takes one of three values depending on whether the trainer chose Grass, Fire, or Water.

### Law of Iterated Expectations (LIE)

Also called the **law of total expectation** or **tower property**:

$$
E\!\left[E[Y \mid X]\right] = E[Y]
$$

In words: the average of the conditional averages (weighted by the distribution of $X$) equals the unconditional average.

More generally, for nested conditioning:

$$
E\!\left[E[Y \mid X, Z] \mid X\right] = E[Y \mid X]
$$

*Pokemon example.* Let $Y = \text{badges}$ and $X = \text{starter\_type}$. Then:

$$
E[\text{badges}] = P(\text{Grass}) \cdot E[\text{badges} \mid \text{Grass}] + P(\text{Fire}) \cdot E[\text{badges} \mid \text{Fire}] + P(\text{Water}) \cdot E[\text{badges} \mid \text{Water}]
$$

If we know the average badge count within each starter group and the proportion of trainers in each group, we can recover the overall average badge count. This decomposition is fundamental to causal inference: many identification strategies work by expressing a causal quantity as a weighted average of conditional expectations.

### Conditional Variance

The **law of total variance** decomposes overall variance into two components:

$$
\text{Var}(Y) = E\!\left[\text{Var}(Y \mid X)\right] + \text{Var}\!\left(E[Y \mid X]\right)
$$

- $E[\text{Var}(Y \mid X)]$: average within-group variance ("unexplained" variance)
- $\text{Var}(E[Y \mid X])$: between-group variance ("explained" by $X$)

*Pokemon example.* The total variance in badge counts comes from (1) variance *within* each starter-type group (not everyone who picks Squirtle earns the same badges) and (2) variance *between* starter-type groups (the group averages differ).

---

## A.11 Notation Reference Table

The following table collects all major notation used throughout this textbook.

| Symbol | Meaning | First Used |
|:---|:---|:---:|
| $Y$ | Outcome variable (e.g., badges earned) | Ch. 1 |
| $X$ or $D$ or $T$ | Treatment or exposure variable | Ch. 1 |
| $\mathbf{X}$ | Vector of covariates / controls | Ch. 2 |
| $Y_i(1), Y_i(0)$ | Potential outcomes for unit $i$ under treatment / control | Ch. 2 |
| $Y_i^{obs}$ | Observed outcome for unit $i$; equals $Y_i(D_i)$ | Ch. 2 |
| $\tau$ | Generic causal effect | Ch. 2 |
| $\tau_i = Y_i(1) - Y_i(0)$ | Individual treatment effect (ITE) | Ch. 2 |
| $\text{ATE} = E[Y(1) - Y(0)]$ | Average treatment effect | Ch. 2 |
| $\text{ATT} = E[Y(1) - Y(0) \mid D=1]$ | Average treatment effect on the treated | Ch. 2 |
| $\text{ATC} = E[Y(1) - Y(0) \mid D=0]$ | Average treatment effect on the control | Ch. 2 |
| $\text{CATE}(\mathbf{x}) = E[Y(1) - Y(0) \mid \mathbf{X} = \mathbf{x}]$ | Conditional average treatment effect | Ch. 10 |
| $\text{LATE}$ | Local average treatment effect (compliers) | Ch. 7 |
| $P(Y \mid X)$ | Conditional probability / distribution | Ch. 1 |
| $P(Y \mid do(X))$ | Interventional distribution (Pearl's do-operator) | Ch. 1 |
| $E[Y \mid X]$ | Conditional expectation | Ch. 1 |
| $E[Y \mid do(X = x)]$ | Causal (interventional) expectation | Ch. 3 |
| $\perp\!\!\!\perp$ | Statistical independence | Ch. 2 |
| $Y(d) \perp\!\!\!\perp D \mid \mathbf{X}$ | Conditional independence / ignorability | Ch. 2 |
| $e(\mathbf{x}) = P(D=1 \mid \mathbf{X} = \mathbf{x})$ | Propensity score | Ch. 5 |
| $G$ | Directed acyclic graph (DAG) | Ch. 3 |
| $\text{pa}(X)$ | Parents of node $X$ in a DAG | Ch. 3 |
| $X \perp_d Y \mid Z$ | $d$-separation in a DAG | Ch. 3 |
| $Z$ | Instrument (instrumental variables context) | Ch. 7 |
| $D_i$ | Treatment indicator (binary: 0 or 1) | Ch. 2 |
| $c$ | Cutoff value in regression discontinuity | Ch. 8 |
| $R_i$ | Running variable in RDD | Ch. 8 |
| $\Delta Y$ or $Y_{post} - Y_{pre}$ | First difference (DiD context) | Ch. 9 |
| $\hat{\tau}$ | Estimated causal effect | Ch. 4 |
| $\text{SE}(\hat{\tau})$ | Standard error of the estimator | Ch. 4 |
| $\alpha$ | Significance level (typically 0.05) | Ch. 4 |
| $\beta$ | Regression coefficient or power ($1 - P(\text{Type II error})$) | Ch. 4 |
| $\mathbb{1}\{\cdot\}$ | Indicator function: 1 if condition is true, 0 otherwise | Ch. 2 |
| $n$ | Sample size | Ch. 4 |
| $N$ | Population size | Ch. 4 |
| $\hat{\mu}$ | Estimated mean | Ch. 4 |
| $\text{Var}(X)$ | Variance of random variable $X$ | App. A |
| $\text{Cov}(X, Y)$ | Covariance of $X$ and $Y$ | App. A |
| $\rho_{XY}$ | Pearson correlation between $X$ and $Y$ | App. A |
| $\sigma^2$ | Variance (population parameter) | App. A |
| $s^2$ | Sample variance | Ch. 4 |
| $\Phi(\cdot)$ | Standard Normal CDF | App. A |
| $\phi(\cdot)$ | Standard Normal PDF | App. A |
| $\xrightarrow{p}$ | Convergence in probability | App. A |
| $\xrightarrow{d}$ | Convergence in distribution | App. A |
| $O_p(\cdot)$ | Stochastic order (big-O in probability) | Ch. 11 |
| $\hat{\theta}_{DR}$ | Doubly robust estimator | Ch. 6 |
| $w_i$ | IPW weight for unit $i$ | Ch. 6 |
| $\mathcal{L}$ | Loss function or likelihood | Ch. 10 |

---

> **Professor Oak's Parting Advice**
>
> "Mathematics is to causal inference what a Pokedex is to a trainer --- it does not battle for you, but without it, you are navigating blind. Every theorem we use in this textbook rests on the foundations laid out in this appendix. When you encounter an unfamiliar symbol or formula in the chapters ahead, come back here. This lab is always open."

---

*Next: Appendix B --- Python Environment & Data Guide*
