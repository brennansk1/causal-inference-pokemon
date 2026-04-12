---
title: "Chapter 5: Celadon City -- Regression, Weighting, and Doubly Robust Methods"
chapter_number: 5
source_file: "textbook/chapters/ch05_celadon_city.md"
estimated_runtime_minutes: 80
key_concepts:
  - OLS for Causal Inference
  - Conditional Mean Independence
  - Frisch-Waugh-Lovell Theorem
  - Omitted Variable Bias Formula
  - Signing the Bias
  - Oster's Delta (Coefficient Stability)
  - Bad Controls and Post-Treatment Bias
  - Kitchen-Sink Regression Mistake
  - DAG-Based Variable Selection
  - Inverse Probability Weighting (IPW)
  - Horvitz-Thompson Estimator
  - Hajek (Normalized) Estimator
  - Extreme Weights Problem
  - Augmented IPW / Doubly Robust Estimation
  - Double Robustness Property
  - Semiparametric Efficiency
characters:
  - NARRATOR (trainer, first-person, curious and conversational)
  - OAK (professor, patient teacher, plain-English definitions)
  - BLUE (rival, confident, makes causal reasoning errors)
  - ERIKA (Celadon Gym Leader, serene, exacting, demands rigorous identification)
---

# Chapter 5: Celadon City -- Regression, Weighting, and Doubly Robust Methods

## Part 1: The Department Store and the Workhorse of Social Science

[SCENE: Celadon City. Bustling streets. The hum of a neon sign. A bell chimes as a department store door opens and closes. Somewhere in the distance, the faint jingle of slot machines.]

NARRATOR: Celadon City is the commercial heart of Kanto. The Department Store towers six stories above the skyline, its glass front reflecting the afternoon sun. Inside, the shelves are loaded with everything a trainer could want. TMs for new battle moves. Stat-boosting vitamins like Calcium and Iron. Evolution stones. And the legendary Rare Candy. Trainers pour through the revolving doors from across the region, wallets open, absolutely convinced that spending more on premium items will transform them into Pokemon League champions.

I have four badges now. Boulder, Cascade, Thunder, and Marsh. This is my fifth challenge. And unlike the previous gyms, which tested physical endurance or strategic speed, Celadon is going to test something different. Gym Leader Erika does not care how hard you can hit or how fast you can dodge. She wants proof. Statistical proof. She will not award the Rainbow Badge to anyone who cannot rigorously separate cause from coincidence.

[pause]

I find Professor Oak near the perfume counter on the second floor. He is holding a shopping bag in one hand and a notebook in the other.

OAK: Ah, perfect timing. I have been collecting data on trainers who shop here. The big question everyone is debating is whether spending at the Celadon Department Store actually causes better battle outcomes, or whether the trainers who spend lavishly just happen to be wealthier and more experienced to begin with.

NARRATOR: Oak opens his notebook and shows me a table. Six trainers. For each one, he has recorded how many gym badges they have earned, whether they spent heavily at the Department Store, how wealthy they are, and how much prior experience they had before arriving in Celadon.

BLUE: [walking over, coffee in hand] I already crunched these numbers. The three trainers who spent big at the Department Store earned an average of seven badges. The three who did not earned an average of four. That is a three-badge difference. Department Store spending works. Case closed.

OAK: Is it, Blue? Or are you confusing the effect of spending with the effect of being the kind of trainer who can afford to spend?

NARRATOR: Blue shrugs and walks away. But Oak is not done with me. He sits me down at a table near the window and says the word that will define this entire chapter.

OAK: Regression.

[pause]

---

[TEACHING SECTION]

NARRATOR: Most people first encounter regression in a statistics course focused on prediction -- finding the best-fitting line through a cloud of data points. But regression can also serve as a tool for causal inference, provided we are willing to make specific assumptions about how the data were generated. And this distinction matters enormously. In prediction, we care about getting the forecast right -- we want our predicted Y-hat to be close to the actual outcome. In causal inference, we care about getting the treatment coefficient right -- we want our estimated tau-hat to reflect the true causal impact of the treatment. Same technique. Completely different goal. A model can be excellent at prediction and terrible at identifying causal effects, or vice versa. The criteria are not the same.

Here is the setup. We observe a group of trainers. For each one, we record an outcome -- say, gym badges earned. We record a treatment indicator -- whether they spent heavily at the Department Store or not. And we record a set of pre-treatment covariates -- things like wealth, prior experience, hometown, starter Pokemon type. The causal regression model says that the outcome equals some baseline, plus the treatment effect times the treatment indicator, plus the effect of all those covariates, plus random noise.

The coefficient on the treatment indicator is the number we care about. That is the parameter we hope captures the causal effect of spending at the Department Store. But when does it actually do that?

[OAK EXPLAINS: Conditional Mean Independence]

OAK: The answer hinges on something called conditional mean independence. Remember from Chapter One that every trainer has two potential outcomes. One is the number of badges they would earn if they spent heavily at the store. The other is the number they would earn if they did not. Conditional mean independence says this: once we condition on the covariates -- once we compare trainers with the same wealth and the same experience -- knowing whether a trainer actually spent at the Department Store gives us no additional information about their potential outcomes.

In other words, within groups of trainers who look the same on all the pre-treatment characteristics we measure, the decision to spend or not spend is essentially as good as random. Not literally random, of course. But random enough that the remaining variation in spending is unrelated to what the trainers would have earned otherwise.

NARRATOR: This is a weaker requirement than the full conditional independence assumption we used in Chapter Four for matching. There, we needed treatment to be independent of the entire distribution of potential outcomes -- the whole shape of the distribution, not just the average. Here, we only need independence of the conditional means. In practical terms, conditional mean independence says that the average potential outcome under control is the same for treated and untreated trainers, once you hold the covariates fixed. And likewise for the average potential outcome under treatment. There could still be differences in the spread or shape of the distributions, and that is fine. We only need the means to line up.

In DAG language, conditional mean independence holds when the covariates X block all backdoor paths between treatment and outcome -- at least with respect to the conditional expectation function. If you have drawn your DAG correctly and the covariates satisfy the backdoor criterion, you are in business.

[pause]

Now, even with conditional mean independence in hand, OLS only recovers the average treatment effect under additional conditions. Let me walk through them one at a time.

First, linearity. The true relationship between the covariates and the outcome has to be at least approximately linear. If the real relationship is wildly nonlinear -- if the effect of wealth on badges follows some complicated curve that a straight line cannot capture -- then the linear model is misspecified, and the treatment coefficient picks up some of that misspecification.

Second, constant treatment effects. The causal effect has to be roughly the same for everyone. If the Department Store helps some trainers a lot and others not at all, OLS does not recover a clean average treatment effect. Instead, it recovers a variance-weighted average of conditional treatment effects, which generally differs from the simple average across the population.

Third, correct specification. The control variables have to include all confounders -- every variable that jointly affects both spending and badges. Leave one out, and you get omitted variable bias. Include the wrong one -- specifically, a variable that is caused by the treatment -- and you get post-treatment bias. We will get to both of those traps later in this chapter. For now, the point is that regression is a conditional beast. Its causal interpretation depends entirely on whether you have conditioned on the right set of variables.

There is one more important special case worth mentioning. When the covariates are discrete -- say, a set of categories like wealth level (low, medium, high) and experience tier (novice, intermediate, expert) -- you can fully saturate the model by including a dummy variable for every cell in the cross-tabulation. In that case, the regression coefficient on treatment is a weighted average of within-cell treatment-control differences. The linearity assumption is automatically satisfied because you are fitting a separate mean in every cell. The catch is that the weighting is precision-weighted -- cells with more observations and less noise get more weight -- which is not the same as the population-weighted average that gives you the ATE. This distinction matters when treatment effects differ across cells and the distribution of covariates is not the same for treated and untreated groups.

[pause]

[OAK EXPLAINS: The Frisch-Waugh-Lovell Theorem]

OAK: Now let me tell you the single most useful piece of intuition for understanding what regression actually does when it "controls for" something. It is called the Frisch-Waugh-Lovell theorem, and once you understand it, you will never think about regression the same way again.

Here is the idea. Take the full regression -- outcome on treatment and covariates. The coefficient on the treatment variable from that full regression is numerically identical to the coefficient you would get from a much simpler procedure. Step one: regress the treatment indicator on all the covariates and save the residuals. Those residuals represent the part of treatment that the covariates cannot predict -- the leftover variation in spending that has nothing to do with wealth or experience. Step two: regress the outcome on all the covariates and save those residuals, too. Those residuals represent the part of the outcome that the covariates cannot explain. Step three: regress the outcome residuals on the treatment residuals. That simple bivariate regression -- one variable on the other, no controls, just residuals on residuals -- gives you the exact same coefficient as the full multiple regression.

NARRATOR: Let me say that again because it is worth pausing on. When you run a regression of badges on Department Store spending, controlling for wealth and experience, what you are really doing -- mechanically, mathematically, identically -- is this. First, you strip out everything that wealth and experience can tell you about who spends at the Department Store. What is left is the "as good as random" variation in spending -- the part that is not explained by being rich or experienced. Second, you strip out everything that wealth and experience can tell you about badge counts. What is left is the unexplained part of the outcome. Third, you ask: does the unexplained variation in spending predict the unexplained variation in badges?

That is what "controlling for" means. It means partialling out. Removing the predictable component. Isolating the residual signal.

In our Celadon City context, the Frisch-Waugh-Lovell theorem says: among trainers with similar wealth and similar experience, does the leftover variation in spending -- the part we cannot attribute to those characteristics -- predict leftover variation in battle outcomes?

[pause]

[WORKED EXAMPLE]

NARRATOR: Now let me walk you through Oak's data. He observed six trainers. I will give you the full picture.

Ash earned five badges, did not spend at the Department Store, had a wealth level of two, and an experience level of three. Misty earned seven badges, spent heavily, wealth of four, experience of five. Brock earned six badges, spent heavily, wealth of three, experience of four. Gary earned eight badges, spent heavily, wealth of five, experience of six. Jessie earned three badges, did not spend, wealth of one, experience of two. And James earned four badges, did not spend, wealth of two, experience of one.

First, the naive comparison. The three trainers who spent at the store -- Misty, Brock, and Gary -- earned seven, six, and eight badges, for an average of seven. The three who did not -- Ash, Jessie, and James -- earned five, three, and four, for an average of four. The naive difference is three badges. That is the number Blue was waving around.

Second, the short regression. If you regress badges on the spending indicator with no controls -- just a simple comparison of means -- you get a coefficient of three point zero. That is identical to the naive difference. No surprise there. Without controls, regression just computes the difference in group averages.

Third, the long regression. Now add wealth and experience as controls. When you run this regression -- and I encourage you to verify it in the companion notebook -- the coefficient on spending drops to approximately zero point eight.

[pause]

Let me say those two numbers side by side. Without controls: three point zero. With controls: zero point eight. The estimate dropped by more than two thirds.

What happened? Most of what looked like a Department Store "effect" was actually driven by confounding. Wealthier, more experienced trainers both spend more at the store and earn more badges. The naive comparison was picking up both the causal effect of spending and the confounding effect of being the kind of trainer who spends. Once we control for wealth and experience, most of that confounding is stripped away. What remains -- the zero point eight -- is the residual association between spending and badges, holding wealth and experience constant. If our model is correctly specified, that is the causal effect.

OAK: That dramatic decline -- from three point zero to zero point eight -- has a name. It is omitted variable bias. The short regression, which omitted wealth and experience, was biased upward. The long regression reduces that bias by including the confounders.

NARRATOR: And here is the Frisch-Waugh-Lovell interpretation of what just happened. When we ran the long regression, we effectively asked: among the six trainers, after removing the part of their spending decision that is predicted by their wealth and experience, and after removing the part of their badge count that is predicted by their wealth and experience, does the leftover variation in spending predict the leftover variation in badges? The answer is yes, but only by about zero point eight badges -- a far cry from the raw three-badge gap that Blue was excited about.

This is the power of "partialling out." It strips away the confounding and isolates the signal. Whether that remaining signal truly represents a causal effect depends, of course, on whether wealth and experience were the only confounders. If there are others we did not measure -- grit, talent, family connections -- then even zero point eight might be biased. We are going to formalize all of this in Part Two.

[pause]

[pause]

One more thing before we leave regression behind. I mentioned that regression and matching are closely related. Both condition on covariates to compare like with like. But they differ in important ways.

Matching is nonparametric -- it makes no assumptions about the functional form of the relationship between covariates and outcomes. It just finds similar units and compares them directly. But matching gives equal weight to each matched pair, and it refuses to make comparisons when there are no close matches. If no untreated trainer looks like a particular treated trainer, matching throws up its hands and says "I cannot help you here." That honesty is a virtue.

Regression, on the other hand, imposes structure. It assumes the relationship is linear, or at least that you have specified the right functional form. In exchange for that assumption, it handles high-dimensional covariates gracefully -- you are not cursed by having many variables to match on. But regression also happily extrapolates. It draws a line through the data and extends it into regions where there may be no actual observations. If all the wealthy trainers are in the treatment group and all the poor trainers are in the control group, regression will still produce an estimate by projecting the line from one group into the territory of the other.

That willingness to extrapolate is both regression's greatest strength and its greatest vulnerability. When the overlap between treated and control groups is good -- when there are similar trainers on both sides -- regression and matching tend to agree. When overlap is poor, regression is essentially inventing data points that do not exist, and you should regard its estimates with real suspicion.

---

## Part 2: Bias Traps, Bad Controls, and the Weighting Alternative

[SCENE: The Celadon Game Corner. Flashing lights. The whir of slot machines. A suspicious man in a black uniform leans against a wall near the prize counter.]

NARRATOR: Behind the cheerful facade of the Celadon Game Corner, Team Rocket runs an elaborate scheme. They subsidize premium battle items -- Rare Candies, PP Ups, stat vitamins -- for trainers they want to recruit. But they do not hand out subsidies at random. They target trainers who are already strong. More badges. Higher-level Pokemon. Proven battle prowess. After all, Team Rocket wants useful recruits, not novices.

This creates a problem that should sound familiar by now. The trainers who receive subsidized items are systematically different from those who do not. Any naive comparison will confuse the effect of the items with the pre-existing superiority of the trainers who got them.

But before we tackle that weighting problem, we need to understand two critical pitfalls that can undermine even careful regression analyses. The first is omitted variable bias. The second is bad controls. Both are devastatingly common in real research, and both can silently destroy a causal estimate.

[pause]

---

[TEACHING SECTION: Omitted Variable Bias]

NARRATOR: Omitted variable bias is, arguably, the single most important concept in applied causal inference with observational data. It tells you exactly what happens when a relevant confounder is left out of a regression.

Here is the setup. Imagine two regressions. The short regression has just the treatment indicator -- spending at the Department Store -- and no controls. The long regression adds the omitted variable -- say, wealth. The OVB formula relates the two coefficients.

[OAK EXPLAINS: The OVB Formula]

OAK: The formula says this. The short-regression coefficient equals the long-regression coefficient plus a bias term. That bias term is the product of two things. The first is delta -- the coefficient from regressing the omitted variable on the treatment. It measures how much the omitted variable correlates with treatment. In our case, it measures how much wealthier the Department Store shoppers are compared to the non-shoppers. The second is gamma -- the coefficient on the omitted variable in the long regression. It measures how much the omitted variable affects the outcome, controlling for treatment. In our case, it measures how much an extra unit of wealth increases badges, holding spending constant.

The bias is the product: delta times gamma. If either one is zero -- if the omitted variable is unrelated to treatment or unrelated to the outcome -- there is no bias. Both links in the chain have to be present for bias to occur.

NARRATOR: This decomposition is incredibly useful because even when you cannot observe the omitted variable directly, you can often reason about the direction of the bias. This skill -- signing the bias -- is one of the most valuable tools in applied research.

The logic follows a simple two-by-two pattern. If delta and gamma are both positive, the bias is positive -- the naive estimate is inflated upward. If delta and gamma are both negative, the bias is also positive -- negative times negative equals positive. If one is positive and the other is negative, the bias is negative -- the naive estimate is deflated downward.

Here is how to apply it. Think about trainer "grit" -- an unobserved quality representing dedication and work ethic. Is grit correlated with Department Store spending? Almost certainly yes. Grittier trainers invest in every possible advantage, so they are more likely to spend at the store. That makes delta positive. Does grit affect badges, controlling for spending? Also yes. Grittier trainers train harder and win more regardless of what they buy. That makes gamma positive. So the bias is delta times gamma, which is positive times positive, which equals positive. The omitted variable bias pushes the naive estimate upward, making the Department Store look more effective than it really is.

Now consider a different omitted variable: risk aversion. Are risk-averse trainers more or less likely to spend at the Department Store? Probably less likely -- they are cautious with their money. That makes delta negative. Do risk-averse trainers earn more or fewer badges? Probably fewer -- they avoid challenging gyms and take fewer strategic risks. That makes gamma negative. Negative times negative equals positive. Even this very different confounder would bias the estimate in the same direction -- upward.

And that is exactly the pattern we saw. The naive estimate was three point zero. The controlled estimate was zero point eight. The bias was positive, inflating the apparent effect by over two points.

[pause]

Let me walk through the numbers to verify this. In our six-trainer dataset, the mean wealth among the three spenders -- Misty, Brock, and Gary -- is four plus three plus five, divided by three, which is four. The mean wealth among the non-spenders -- Ash, Jessie, and James -- is two plus one plus two, divided by three, which is about one point six seven. So delta, the wealth gap between spenders and non-spenders, is about two point three three. Suppose the coefficient on wealth in the long regression is about zero point nine. Then the bias is two point three three times zero point nine, which is about two point one. Add that to the long-regression estimate of about one point two, and you get approximately three point three -- close to the short-regression estimate of three point zero. The approximation is not exact because we are working with a tiny dataset and have simplified by looking at only one of the two omitted covariates, but the direction and magnitude are clear.

[pause]

[TEACHING SECTION: Oster's Delta]

NARRATOR: Now, a natural question arises. We controlled for wealth and experience, and the estimate dropped from three to zero point eight. But what about the confounders we cannot observe? What about grit, natural talent, family connections, luck? Could those unobserved factors explain away the remaining zero point eight?

This is where Oster's method comes in. Emily Oster, in a paper published in two thousand nineteen, formalized a way to assess exactly this question. The idea is elegant. You look at how much the treatment coefficient changed when you added the controls you can observe. Then you extrapolate: how much would it change if you could also add all the controls you cannot observe?

[OAK EXPLAINS: Oster's Delta]

OAK: The key output is a number called delta. Think of it as a stress test. If delta equals three, then unobserved confounders would need to be three times as important as the observed controls to fully explain away your estimated effect. That is reassuring. If delta equals zero point five, then unobserved confounders that are only half as important as what you already controlled for could eliminate the effect entirely. That is concerning.

NARRATOR: Here is the calculation for our Department Store example. The short regression, with no controls, has an R-squared of zero point four zero and a coefficient of three point zero. The long regression, with wealth and experience, has an R-squared of zero point eight two and a coefficient of zero point eight. If we set the maximum possible R-squared -- the R-squared we would get if we could observe literally everything -- to one point zero, then delta works out to approximately zero point one five six.

That is well below one. It means that unobserved factors that are only about sixteen percent as important as wealth and experience could wipe out the remaining effect. The estimated Department Store effect is fragile. Erika would raise an eyebrow.

OAK: When you publish research, always report delta alongside your main estimates. Referees -- and Gym Leaders -- will respect the honesty. A high delta gives people confidence. A low delta tells them to be cautious. Either way, it is far better to disclose the fragility than to pretend it does not exist.

[pause]

---

[TEACHING SECTION: Bad Controls]

NARRATOR: If omitted variable bias is the most important concept in applied causal inference, bad control bias is the most common mistake. And it is a mistake that comes from the best of intentions.

Here is how it happens. A researcher wants to isolate the causal effect of some treatment. They reason: "I should control for as many variables as possible. The more controls, the better. That way I am holding everything constant." This sounds sensible. It is wrong.

The problem arises when one of those control variables is a consequence of the treatment -- a descendant on the causal diagram. Controlling for a descendant of treatment does not remove confounding. It blocks the very causal pathway you are trying to measure, or worse, it opens a spurious path that introduces new bias.

Let me make this concrete with the Exp Share example. The Exp Share is an item that distributes experience points across a trainer's entire team, not just the Pokemon that fought. We want to estimate its effect on gym badges earned. A natural confounder is the trainer's initial experience before they got the Exp Share. We should control for that. But a tempting and dangerous "control" is the trainer's average team level at the time badges are measured.

Why is average team level a bad control? Because using the Exp Share causes team levels to rise. Average team level is a consequence of the treatment. It sits on the causal pathway between Exp Share usage and badges earned. If you control for it, you are asking: "Holding team level constant, does the Exp Share help?" But the whole reason the Exp Share helps is that it raises team levels! You have surgically removed the mechanism through which the treatment operates. The coefficient on Exp Share, after controlling for team level, captures only whatever tiny direct effect remains -- the part of the Exp Share's benefit that does not flow through team levels. And that is approximately zero.

[BLUE'S MISTAKE: The Kitchen-Sink Regression]

BLUE: [sitting down at a Game Corner table, laptop open] All right, I just ran the definitive analysis. I regressed badges on Exp Share usage, controlling for team level, moves learned, and items used. The Exp Share coefficient is basically zero. See? Exp Shares do not help at all.

NARRATOR: Blue is beaming. He thinks he has run the most rigorous possible analysis by throwing every available variable into the regression. This is called the kitchen-sink approach, and it is one of the most common errors in applied research.

OAK: Blue, team level, moves learned, and items used are all consequences of using the Exp Share. By controlling for them, you have blocked every channel through which the treatment could possibly affect the outcome. Of course the coefficient is zero. You removed the effect yourself.

BLUE: But I controlled for everything!

OAK: That is exactly the problem. In causal inference, controlling for everything is not a virtue. It is a recipe for bias. More controls are not always better. Let the DAG guide your choices.

NARRATOR: Blue's mistake is so common it deserves emphasis. The intuition "more controls equals less bias" feels deeply natural. After all, if omitted variable bias comes from leaving variables out, surely including more variables should reduce bias, right? Wrong. Including variables that are descendants of treatment does not reduce confounding bias -- it introduces a different kind of bias. You are not holding things constant in a meaningful way. You are holding constant the mechanism through which the treatment operates, which is like asking whether a medicine works while holding the patient's recovery constant. Of course the answer is no -- you have defined the effect away.

The situation can actually be even worse than merely blocking causal channels. Sometimes controlling for a post-treatment variable does not just remove the effect -- it creates a brand new spurious association where none existed before. This happens when the control variable is a collider. Remember from Chapter Three that a collider is a variable caused by two or more other variables. If the treatment affects a variable, and some unobserved factor also affects that same variable and the outcome, then conditioning on the collider opens a backdoor path that generates fake bias.

Think of it this way. A trainer's "reputation score" might be affected by both whether they use an Exp Share and by some unobserved factor like natural charisma. Charisma also affects battle outcomes, because charismatic trainers get better tips and invitations to exclusive training events. Without conditioning on reputation, there is no problem -- the path through the collider is blocked. But once you control for reputation, you open a spurious channel from Exp Share through reputation back through charisma to badges. You have manufactured bias from thin air.

The correct rule is simple. Include a variable in your regression if and only if it is needed to block a backdoor path between treatment and outcome, and it is not a descendant of the treatment. If both conditions are met, it is a good control. If the second condition is violated -- if the variable is caused by the treatment -- it is a bad control, regardless of anything else.

Good controls are pre-treatment covariates that are common causes of both treatment and outcome. Wealth. Prior experience. Starter Pokemon type. Hometown. These are things that were determined before the treatment happened and that influence both who gets treated and what the outcome would be.

Bad controls are post-treatment variables that are consequences of the treatment. Average team level after using the Exp Share. Number of TMs purchased after deciding to invest in the Department Store. Pokemon friendship level after treatment.

There is also a category of neutral variables -- pre-treatment variables that predict the outcome but not the treatment, or vice versa. Including these does not bias the treatment coefficient. If they predict the outcome, they can actually help by reducing residual variance and tightening your confidence intervals. If they predict neither treatment nor outcome, they waste degrees of freedom without adding anything.

When in doubt, draw the DAG first. Apply the backdoor criterion from Chapter Three. Let the causal structure, not your intuition about "controlling for more," determine what goes into the regression.

[pause]

---

[TEACHING SECTION: Inverse Probability Weighting]

NARRATOR: Now let me return to the Game Corner problem. Team Rocket is handing out subsidized items to strong trainers. The treated group is systematically different from the control group. Regression is one way to handle this, but it relies on correctly specifying the functional form of the relationship between covariates and the outcome. What if we got that functional form wrong? What if the relationship is not linear?

There is an alternative approach that attacks the problem from the other direction. Instead of modeling the outcome, we model the treatment assignment mechanism. Instead of asking "what would the outcome look like if we could adjust for covariates," we ask "what would the world look like if treatment had been assigned randomly?" This approach is called inverse probability weighting, or IPW.

[OAK EXPLAINS: The Pseudo-Population]

OAK: Here is the key insight. In the observed data, treated and control groups look different because treatment was not assigned randomly. Team Rocket targeted strong trainers. IPW creates a pseudo-population -- a weighted version of the data -- where treatment is independent of covariates. In this pseudo-population, it is as if treatment were randomly assigned. Each trainer is weighted by the inverse of their probability of receiving the treatment they actually received. The resulting weighted sample represents the population we would have observed under random assignment.

NARRATOR: Let me unpack that. The propensity score, which we introduced in Chapter Four, is the probability that a given trainer receives treatment, given their observed characteristics. For the Game Corner, it represents Team Rocket's targeting function -- how likely they are to subsidize a trainer with a particular profile.

Now, consider a treated trainer with a propensity score of zero point eight. This trainer had an eighty percent chance of being treated. They are overrepresented among the treated -- there are lots of trainers like them in the treatment group. To make the treated group representative of the full population, we downweight this trainer. Their weight is one divided by zero point eight, which is one point two five.

Now consider a treated trainer with a propensity score of zero point two. This trainer had only a twenty percent chance of being treated but was treated anyway. They are underrepresented -- there are few trainers like them in the treatment group. We upweight them. Their weight is one divided by zero point two, which is five.

The same logic applies on the control side, but with one minus the propensity score. A control trainer with a propensity score of zero point eight had only a twenty percent chance of being a control unit. They are rare in the control group, so we upweight them by one divided by zero point two, which is five.

The foundational IPW estimator is called the Horvitz-Thompson estimator, originally developed for survey sampling back in nineteen fifty-two. The idea is simple but powerful. For the treated group, take each trainer's outcome, divide it by their propensity score, and average across the whole sample. For the control group, take each outcome, divide it by one minus the propensity score, and average across the whole sample. Then subtract the control weighted average from the treated weighted average. That is the IPW estimate of the average treatment effect.

The Horvitz-Thompson estimator has a beautiful theoretical property: it is exactly unbiased when the propensity scores are known. In a randomized experiment where you literally set the treatment probabilities, this estimator hits the truth on average with no systematic error.

[pause]

In practice, though, researchers almost always use the Hajek estimator instead -- a normalized version. The key difference is that instead of dividing by the total sample size, you divide each group's weighted outcomes by the sum of the weights within that group. Each term becomes a proper weighted average -- the weights sum to one within each group.

Why does this matter? Three reasons. First, the normalization stabilizes the estimator. The Horvitz-Thompson weights do not necessarily sum to the "right" total in finite samples, and the Hajek estimator self-corrects for this. Second, it reduces variance, sometimes dramatically. Third, it is more robust when the propensity score is estimated rather than known, which is always the case in observational studies. The cost is a tiny finite-sample bias that vanishes as the sample gets large. In virtually all applied settings, the Hajek estimator is preferred, and when people say "IPW estimator" without qualification, they usually mean the Hajek version.

[pause]

[TEACHING SECTION: The Extreme Weight Problem]

NARRATOR: IPW has an Achilles' heel, and it is worth understanding clearly. When a trainer's propensity score is very close to zero or very close to one, the corresponding weight explodes. A trainer with a propensity score of zero point zero one gets a weight of one hundred. A single trainer, carrying a weight of one hundred, can dominate the entire estimate. One unusual case can swing your conclusions dramatically.

In the Game Corner setting, imagine a trainer with zero badges and a level five Pokemon who somehow receives a Team Rocket subsidy -- maybe by accident, maybe because someone mixed up the paperwork. Their propensity score is near zero because Team Rocket almost never targets trainers like that. But because they happened to be treated, their IPW weight is enormous. The entire estimate hinges on this one outlier.

Extreme weights cause three problems. High variance, because the estimator is being driven by a handful of heavily weighted observations. Sensitivity to outliers, because one misclassified or unusual case can change everything. And instability, because small tweaks to the propensity score model -- adding or removing a covariate -- can dramatically shift which observations get extreme weights.

There are several remedies. You can trim the sample, dropping anyone whose propensity score falls below some threshold or above one minus that threshold. This changes what you are estimating -- you are no longer targeting the ATE for the whole population, but rather the ATE for the subpopulation with reasonable overlap. You can truncate or Winsorize the weights, capping them at some maximum value. This introduces a small bias but substantially reduces variance. You can use stabilized weights, which multiply the standard IPW weights by the marginal probability of treatment. Or you can use overlap weights, which give the most weight to observations in the region of best overlap and the least weight to extreme cases. Each approach involves a bias-variance tradeoff, and the right choice depends on the application.

[pause]

[WORKED EXAMPLE: The Game Corner]

NARRATOR: Let me walk through a concrete example. Oak observed eight trainers in Celadon City. Team Rocket subsidized items for four of them. The other four purchased at full price. For each trainer, Oak recorded their outcome -- badges earned -- and estimated a propensity score using logistic regression on prior badges and Pokemon level.

The naive comparison: the four subsidized trainers earned an average of six and a half badges. The four unsubsidized trainers earned an average of four and a half. The naive difference is positive two. It looks like the subsidized items helped by two full badges.

Now the Horvitz-Thompson estimate. When we divide each treated outcome by its propensity score and each control outcome by one minus its propensity score, something striking happens. The treated sum, weighted by inverse propensities, is about forty-three point eight. The control sum is about sixty-six point four. Divide each by the sample size of eight, and the HT estimate comes out to about negative two point eight three.

[pause]

That is a complete reversal. The naive comparison said positive two. The IPW estimate says negative two point eight three. After reweighting to account for Team Rocket's targeting, the subsidized items appear to hurt outcomes, or at least provide no benefit. The apparent advantage was entirely driven by selection: Team Rocket gave items to trainers who would have performed well regardless.

But notice the instability. One control trainer -- a strong trainer with a high propensity score who happened not to receive a subsidy -- gets an enormous weight. That single trainer is dominating the control-side calculation.

The Hajek estimate, which normalizes the weights, comes out to about negative zero point eight two. Much more moderate. The normalization tempers the influence of that extreme weight, yielding a more stable result. This is why the Hajek estimator is the standard choice in practice.

OAK: The lesson here is crucial. The naive comparison suggested a two-badge advantage for subsidized trainers. After IPW adjustment, the effect is negative or near zero. The apparent benefit was entirely driven by selection. Once we reweight to account for Team Rocket's targeting, the items themselves provide little or no benefit.

[pause]

---

## Part 3: Doubly Robust Estimation, the Rainbow Badge, and Beyond

[SCENE: The Celadon Gym. Sunlight filters through a glass ceiling onto a garden of potted plants and hanging vines. The air smells of flowers. Erika sits on a stone bench at the far end, arranging a bouquet. Her Vileplume dozes beside her.]

NARRATOR: The Celadon Gym is unlike any gym I have visited. It is more greenhouse than arena. Vines crawl up the walls. Wildflowers push through cracks in the stone floor. Sunlight pours through the glass roof and catches the moisture in the air, scattering tiny rainbows everywhere. At the far end of the garden, past the junior trainers who guard the path, sits Erika. She is arranging flowers with the kind of patience that suggests she has nowhere else to be.

She does not look up as I approach. But she speaks.

ERIKA: You have learned regression. You have learned weighting. Both are useful tools. But each one requires you to get a model exactly right. The outcome model. The treatment model. One wrong assumption, one misspecified relationship, and the entire estimate collapses. Tell me -- what happens when you are not sure which model is correct?

NARRATOR: I do not have an answer yet. But Oak, who has followed me into the gym, does.

OAK: That is exactly the right question, Erika. And it is what motivates the third tool in our arsenal.

[pause]

---

[TEACHING SECTION: The Best of Both Worlds]

NARRATOR: Here is where we stand. We have two approaches to estimating causal effects from observational data.

The first is outcome modeling -- regression. You model the relationship between covariates and the outcome, then compare predicted outcomes under treatment and control. This works if you get the outcome model right.

The second is treatment modeling -- inverse probability weighting. You model the probability of treatment given covariates, then reweight observations to create balance. This works if you get the propensity score model right.

Each approach is consistent -- it converges to the truth as the sample grows -- if its respective model is correctly specified. But in practice, you can never be certain that either model is correct. Are the true relationships linear? Did you include the right covariates? Is your propensity score model capturing the real assignment mechanism? These are hard questions, and the honest answer is usually "I am not sure."

What if we could combine both approaches and get an estimator that works if either model is correct? Not both. Either one.

That is exactly what the augmented inverse probability weighting estimator achieves. It is also called the doubly robust estimator. And it is the gold standard for modern applied causal inference.

[OAK EXPLAINS: AIPW]

OAK: Here is how it works, in plain language. You fit two models. An outcome model that predicts what each trainer's badges would be under treatment and under control. And a propensity score model that predicts each trainer's probability of receiving treatment. Then you combine them.

The estimator has three pieces. The first piece is the outcome model's prediction of the treatment effect. For each trainer, you take the predicted outcome under treatment minus the predicted outcome under control, and average across the sample. If the outcome model is correct, this by itself estimates the average treatment effect.

The second piece is a bias correction for the treated group. For each treated trainer, you look at the residual -- the gap between their actual outcome and what the outcome model predicted. You weight that residual by the inverse of the propensity score. If the outcome model is correct, these residuals have mean zero and this whole piece vanishes. But if the outcome model is wrong, this correction term kicks in and uses the propensity score weights to fix the error.

The third piece does the same thing for the control group. It corrects the outcome model's predictions for control units using their actual outcomes and inverse propensity weights.

The magic is in how these pieces interact. If the outcome model is right, the correction terms vanish and you are left with a consistent estimate. If the propensity model is right, the corrections are properly calibrated by the inverse weights, and you get a consistent estimate even though the outcome predictions are wrong. You need at least one of the two models to be correct. But you do not need both.

[pause]

ERIKA: [looking up from her flowers] Describe the double robustness property precisely.

NARRATOR: Here it is. The AIPW estimator is consistent for the average treatment effect if either the propensity score model is correctly specified, or the outcome model is correctly specified for both treated and control groups, but not necessarily both. The bias of the estimator is proportional to the product of the errors in both models. If either error is zero, the product is zero, and the bias vanishes.

[TEACHING SECTION: Four Scenarios]

NARRATOR: Let me walk through four scenarios to make this concrete. In each case, the true average treatment effect is one point zero. We have a sample of five hundred trainers.

Scenario one. Both models are correctly specified. The outcome model is linear in the covariates, which matches the true data-generating process. The propensity model is logistic in the covariates, which also matches. The AIPW estimate comes out to about one point zero two. Close to the truth. No surprise there.

Scenario two. The propensity score model is wrong, but the outcome model is correct. We deliberately misspecify the propensity score by ignoring the covariates entirely -- we just use the overall treatment rate as the propensity score for everyone. The pure IPW estimate, using this bad propensity model, comes out to about one point four two. Biased. But the AIPW estimate, which combines this bad propensity model with the correct outcome model, comes out to about one point zero one. Still close to the truth. The correct outcome model rescued the estimator.

Scenario three. The outcome model is wrong, but the propensity score model is correct. We deliberately misspecify the outcome model by ignoring the covariates -- we just use group means as our predictions. The pure regression estimate, using this bad outcome model, comes out to about one point three eight. Biased. But the AIPW estimate, combining this bad outcome model with the correct propensity model, comes out to about zero point nine eight. Still close to the truth. The correct propensity model rescued the estimator.

Scenario four. Both models are wrong. We misspecify both -- ignoring covariates in both the outcome model and the propensity model. The AIPW estimate comes out to about one point four two. Biased. With both models wrong, double robustness cannot save us. The safety net has two ropes, and both snapped.

[pause]

Let me put those four numbers side by side so the pattern is unmistakable. Both correct: one point zero two. Propensity wrong, outcome correct: one point zero one. Outcome wrong, propensity correct: zero point nine eight. Both wrong: one point four two. The first three are all within a whisker of the true effect of one point zero. Only the fourth -- both wrong -- is badly off. That is the double robustness property in action.

And notice something subtle about the fourth scenario. The bias in that case, about zero point four two, is not some wild new number. It is roughly the same as the bias you would get from either the pure regression or the pure IPW estimator alone when their respective models are misspecified. Double robustness does not make things worse when both models fail. It just cannot make them better. You are back to the same position you would be in with a single misspecified model.

ERIKA: [setting down a flower stem] So the estimator gives you two chances to get the analysis right. But it does not give you infinite chances.

OAK: Exactly. And there is an important subtlety that Blue keeps getting wrong.

[BLUE'S MISTAKE: Trusting Doubly Robust with Missing Confounders]

BLUE: [calling from the gym entrance] No problem! I will just use doubly robust estimation. That fixes everything!

OAK: Blue, what covariates are you using?

BLUE: Wealth. Same as before.

OAK: And what about trainer experience?

BLUE: I do not have that variable.

OAK: Then double robustness will not help you. The double robustness property protects against misspecification of functional form -- getting the shape of the relationship wrong. It does not protect against omitting key confounders from both models entirely. If experience is missing from both your outcome model and your propensity model, neither model is correctly specified, and the AIPW estimator inherits the bias of both.

NARRATOR: This is worth emphasizing. Double robustness gives you two chances to get the model form right. It does not create information about confounders you never measured. If the same critical variable is absent from both models, you are in scenario four -- both wrong -- and the safety net fails.

There is also a related framework called Targeted Maximum Likelihood Estimation, or TMLE, developed by Mark van der Laan and others. TMLE shares the double robustness property and the efficiency bound, but uses a different algorithmic procedure. It fits an initial outcome model, then "targets" or updates that model using a clever covariate derived from the propensity score. The main practical advantage of TMLE is that the final estimates respect the natural bounds of the outcome -- if you are predicting a probability, TMLE keeps its predictions between zero and one, whereas AIPW can occasionally produce nonsensical values outside those bounds. In modern applied work, AIPW and TMLE are the two leading doubly robust estimators, and either is a defensible choice.

[pause]

[TEACHING SECTION: Semiparametric Efficiency]

NARRATOR: Beyond double robustness, the AIPW estimator has another remarkable property. When both models are correctly specified, it achieves what statisticians call the semiparametric efficiency bound. What does that mean in plain language? It means that no other well-behaved estimator -- no other regular estimator in the statistical sense -- can have lower asymptotic variance. The AIPW estimator gives you the most precise possible estimate of the average treatment effect, given the data and the assumptions. You cannot do better. It is the theoretical ceiling.

This result, due to Jinyong Hahn in a nineteen ninety-eight paper, is one of the most elegant findings in modern econometrics. It says that the efficient influence function for the ATE has a specific form that combines exactly the three pieces of the AIPW estimator -- the outcome model predictions, the propensity-weighted residuals for the treated, and the propensity-weighted residuals for the controls. It is not a coincidence that the AIPW estimator looks the way it does. It was essentially reverse-engineered from the efficiency bound.

The efficiency bound also reveals something important about the structure of the problem. Estimation is hardest -- variance is highest -- when propensity scores are extreme, close to zero or close to one. The bound has terms that divide the outcome variance by the propensity score and by one minus the propensity score, so when either of those denominators is near zero, the variance explodes. This connects directly back to the overlap assumption and the extreme weight problem we discussed earlier. The efficiency bound quantifies exactly how much precision you lose when overlap is poor. It is a formal statement that some causal questions are inherently harder to answer than others, depending on how much treatment and control groups overlap in covariate space.

[pause]

[TEACHING SECTION: Practical Recommendations]

NARRATOR: For anyone doing applied work, here is the guidance that Oak and Erika would give.

First, start with regression as a baseline. It is simple, well-understood, and often sufficient when the outcome model is approximately linear and treatment effects are roughly constant.

Second, estimate the propensity score and check covariate balance in the weighted sample. If balance is poor, reconsider your model or the plausibility of the overlap assumption.

Third, use AIPW as your primary estimator for the final analysis. It provides double robustness and achieves the efficiency bound.

Fourth, report all three estimates -- regression, IPW, and AIPW. Agreement across estimators is reassuring. Disagreement is informative. If the three estimates tell very different stories, at least one of your models is misspecified, and you need to investigate further.

Fifth, conduct sensitivity analysis. Report Oster's delta. Assess how much unobserved confounding would be needed to explain away your results.

Sixth, examine the propensity score distribution for extreme values. If many observations have propensity scores below zero point zero five or above zero point nine five, consider trimming, truncation, or overlap weights. And remember: the extreme weight problem is not just a statistical nuisance. It is a signal. It tells you that there are regions of the covariate space where treated and control groups do not overlap -- where you are asking the data to make comparisons that the data cannot support.

Seventh, and this is the overarching lesson: always draw the DAG first. Before you run any regression, before you estimate any propensity score, before you combine any models, sit down and think about the causal structure. Which variables are confounders? Which are consequences of treatment? Which paths need to be blocked? The DAG disciplines your analysis. Without it, you are navigating without a map.

[pause]

ERIKA: [standing, brushing soil from her hands] You have demonstrated rigor. You have acknowledged uncertainty. And you have deployed the most defensible estimators available. Tell me -- what did you learn in Celadon City?

NARRATOR: I learned three tools. Regression adjusts for confounders by partialling them out of both the treatment and the outcome, isolating the residual variation that is as good as random. Inverse probability weighting adjusts for confounders by reweighting the sample so that it mimics what we would have observed under random assignment. And doubly robust estimation combines both approaches, giving us two chances to get the model right and achieving the best possible precision when both models are correct.

I also learned two traps. Omitted variable bias, which inflates or deflates the estimate when a confounder is left out, and which can be diagnosed with the OVB formula and stress-tested with Oster's delta. And bad controls, which arise when we condition on variables that are caused by the treatment, blocking the causal pathway or opening spurious associations.

ERIKA: [nodding] Acceptable.

[pause]

NARRATOR: She reaches into a small wooden box on the bench and produces a badge. It catches the light streaming through the glass ceiling and refracts it into a spectrum -- red, orange, yellow, green, blue, indigo, violet. The Rainbow Badge.

ERIKA: The Pokemon trainer with the most careful identification strategy in Celadon City.

NARRATOR: I pin the badge next to the four I already have. Five down. Three to go. Erika sits back down and returns to her flowers, as if nothing has happened. But as I turn to leave, she says one more thing.

ERIKA: A word of caution. Everything you have learned in this chapter relies on the assumption that you have measured and controlled for all relevant confounders. Regression, IPW, doubly robust -- none of them can help you if there is an unobserved factor driving both treatment and outcome that you never measured. In Fuchsia City, you will learn about a tool that does not require that assumption. It is called an instrumental variable. And it will change how you think about identification entirely.

[pause]

NARRATOR: I step out of the greenhouse gym and into the Celadon City evening. The neon signs of the Game Corner flicker across the street. The air has cooled, and I can smell the flowers from Erika's gym garden drifting through the open door behind me.

Five badges. The Rainbow Badge joins the Boulder, Cascade, Thunder, and Marsh badges in my case. Each one represents a different lesson. In Pallet Town, I learned that correlation is not causation. In Pewter City, that randomization is the gold standard. In Cerulean City, that DAGs give us a language for causal structure. In Vermilion City, that matching and propensity scores let us create fair comparisons. And now in Celadon City, I have learned the three workhorse estimators of applied causal inference -- regression, IPW, and doubly robust -- along with the traps of omitted variable bias and bad controls.

But Erika's parting words linger. Everything I have learned in Celadon relies on a demanding assumption: that I have measured and controlled for all relevant confounders. Conditional mean independence. Unconfoundedness. Selection on observables. Different names for the same deep requirement -- that there is nothing lurking in the shadows that drives both treatment and outcome and that I have failed to account for.

What if that assumption fails? What if there is an unobserved confounder that I cannot measure, no matter how hard I try?

Somewhere south, beyond the cycling road and the coastal routes, Fuchsia City waits. And with it, according to Erika, a fundamentally different approach to causal inference. Instrumental variables do not require you to measure every confounder. They find a source of variation in treatment that is as good as random -- an instrument -- and use only that variation to identify the causal effect. It is a completely different logic, and it will change how I think about identification entirely.

But that is the next chapter.

---

## Chapter Summary

NARRATOR: Let me pull the key ideas from Celadon City together before we move on.

[pause]

First, regression for causal inference. Ordinary least squares is the workhorse of applied social science. Under conditional mean independence -- the assumption that treatment is as good as random within covariate groups -- along with linearity and constant treatment effects, OLS recovers the average treatment effect. The Frisch-Waugh-Lovell theorem reveals what regression really does: it partials out the confounders, correlating the residual variation in treatment with the residual variation in outcomes. Regression is powerful but vulnerable to functional form misspecification and extrapolation beyond the data.

Second, omitted variable bias. The OVB formula says the short-regression coefficient equals the long-regression coefficient plus the product of two terms: how much the omitted variable correlates with treatment, and how much it affects the outcome. This decomposition lets you sign the bias even when you cannot observe the omitted variable. Oster's delta extends this logic by asking how important unobservables would need to be, relative to observables, to explain away the effect entirely.

Third, bad controls. The most common mistake in applied work is controlling for variables that are caused by the treatment. This blocks causal pathways, introduces collider bias, or both. The correct approach is DAG-based variable selection using the backdoor criterion: control for confounders, never for descendants of treatment. More controls are not always better.

Fourth, inverse probability weighting. IPW models the treatment assignment mechanism rather than the outcome. By reweighting observations so that each trainer's weight is the inverse of their probability of receiving the treatment they got, IPW creates a pseudo-population where treatment is as good as random. The Hajek estimator, which normalizes the weights, is preferred in practice. But extreme propensity scores remain a persistent challenge, causing high variance and instability.

Fifth, doubly robust estimation. The AIPW estimator combines outcome modeling and propensity weighting. It is consistent if either model is correctly specified, giving you two chances to get the analysis right. When both models are correct, it achieves the semiparametric efficiency bound -- the lowest possible variance among well-behaved estimators. It is the gold standard for modern applied causal inference.

[pause]

---

## Comprehension Check

NARRATOR: Before you leave Celadon City, test yourself on these questions.

First: What is the Frisch-Waugh-Lovell theorem, and why does it matter for understanding what regression does when it "controls for" covariates?

[long pause]

The Frisch-Waugh-Lovell theorem says that the treatment coefficient from a multiple regression is identical to the coefficient from a bivariate regression of the outcome residuals on the treatment residuals, where both sets of residuals come from first regressing each variable on the covariates. It matters because it reveals that "controlling for" covariates means stripping out the predictable part of both treatment and outcome, then asking whether the leftover variation in treatment predicts the leftover variation in outcomes. It shows that regression isolates the as-good-as-random variation in treatment status.

Second: What is the omitted variable bias formula, and how can you use it to sign the direction of bias even when you cannot observe the omitted variable?

[long pause]

The OVB formula says that the short-regression coefficient equals the long-regression coefficient plus the product of two terms: delta, which measures how much the omitted variable correlates with treatment, and gamma, which measures how much the omitted variable affects the outcome controlling for treatment. To sign the bias, think about whether delta and gamma are each positive or negative. If both are positive or both are negative, the bias is positive -- the naive estimate is inflated. If one is positive and the other negative, the bias is negative.

Third: Why is controlling for a post-treatment variable dangerous, and what is the kitchen-sink regression mistake?

[long pause]

A post-treatment variable is one that is caused by the treatment. Controlling for it blocks the causal pathway from treatment to outcome, absorbing the very effect you are trying to measure. It can also introduce collider bias, creating spurious associations. The kitchen-sink mistake is throwing every available variable into a regression on the theory that more controls are always better. In causal inference, this is wrong because some of those variables may be descendants of the treatment, and including them distorts the estimate.

Fourth: Explain the double robustness property of the AIPW estimator. What does it protect against, and what does it not protect against?

[long pause]

The AIPW estimator is consistent if either the outcome model or the propensity score model is correctly specified, but not necessarily both. Its bias is proportional to the product of the errors in both models, so if either error is zero, the bias vanishes. It protects against getting the functional form of one model wrong, as long as the other model compensates. It does not protect against omitting a key confounder from both models, because if the same variable is missing from both, neither model is correctly specified and the double robustness property fails.

Fifth: A trainer has a propensity score of zero point zero five and was treated. What is their IPW weight, and why might this be a problem?

[long pause]

Their IPW weight is one divided by zero point zero five, which equals twenty. This means that in the weighted pseudo-population, this one trainer counts as twenty trainers. The problem is that a single observation is exerting enormous influence over the estimate. If that trainer's outcome is at all unusual -- due to measurement error, an outlier experience, or simple randomness -- it will swing the entire estimate. This is the extreme weight problem, and it is why researchers use trimming, truncation, or overlap weights to stabilize IPW estimates.
