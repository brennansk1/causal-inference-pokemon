---
title: "Chapter 8: Indigo Plateau & Beyond -- Advanced Topics & Frontiers"
chapter_number: 8
source_file: "textbook/chapters/ch08_indigo_plateau.md"
estimated_runtime_minutes: 100
key_concepts:
  - mediation analysis (NDE, NIE)
  - sequential ignorability
  - sensitivity analysis
  - Rosenbaum bounds
  - E-value
  - Oster bounds
  - Manski bounds
  - heterogeneous treatment effects (CATE)
  - causal forests
  - GATES and CLAN
  - policy learning
  - interference and SUTVA violations
  - spillover effects
  - exposure mapping
  - two-stage randomization
  - regression kink design
  - partial identification
  - causal discovery (PC algorithm)
  - double/debiased machine learning (DML)
  - TMLE
  - transportability
  - dynamic treatment regimes
  - marginal structural models
characters:
  - narrator
  - oak
  - blue
  - lorelei
  - agatha
  - bruno
  - lance
---

# Chapter 8: Indigo Plateau & Beyond -- Advanced Topics & Frontiers

## Part 1: The Elite Four Gauntlet Begins

[SCENE: A mountain path. Wind. Cold air. The sound of footsteps on stone.]

NARRATOR: The road from Viridian City narrows into a winding mountain path. Rock walls rise on either side, and the air grows colder with every step. Behind you lies the entire Kanto region -- eight Gym Badges earned, each one representing a different tool in your causal inference arsenal. Potential outcomes. Randomized experiments. DAGs and d-separation. Matching and propensity scores. Regression and doubly robust estimation. Instrumental variables and regression discontinuity. Difference-in-differences and synthetic control.

Ahead lies the Indigo Plateau.

You push through the gates and step into a vast, echoing hall. A League official checks your Badge case and nods.

NARRATOR: "Eight badges," she says. "You are cleared to challenge the Elite Four." She pauses. "But I should warn you -- each member guards a frontier of causal inference that most trainers never reach. Lorelei will test your understanding of mechanisms. Bruno will ask whether everyone responds the same way. Agatha will haunt you with the specter of unobserved confounding. And Lance will shatter your most basic assumption about how units interact."

She steps aside. "Beyond them waits the Champion. He thinks he knows everything about causation. Prove him wrong."

You take a deep breath. You adjust your bag. You walk through the first door.

---

### Lorelei's Ice Chamber: Mediation Analysis

[SCENE: A frozen chamber. Ice crystals hang from the ceiling. A woman sits on a throne of stalagmites.]

NARRATOR: The chamber is cold. Ice crystals hang from the ceiling, refracting light into prismatic arcs. Lorelei sits on a throne of frozen stalagmites, a Dewgong resting at her side. She adjusts her glasses and studies you.

LORELEI: Most trainers are satisfied knowing that a treatment works. I want to know how. Through what pathways does a cause produce its effect? Can you freeze out the direct path and isolate the indirect one?

NARRATOR: She gestures to the battlefield. Show me you understand mechanisms.

[TEACHING SECTION]

NARRATOR: In Chapters One through Seven, we focused on estimating the total effect of a treatment on an outcome. But in many settings, we want to understand the mechanism -- the causal pathway through which the effect operates. Mediation analysis decomposes the total effect into two pieces: a direct effect and an indirect effect that operates through a mediator.

Consider a concrete example from the Elite Four challenge. Suppose we want to understand whether using healing items during battles affects the probability of defeating all four members. One plausible mechanism is that items maintain Pokemon health between battles, which in turn affects the probability of winning later rounds. The question is: does item use affect outcomes only through health maintenance, or does it also have a direct effect -- perhaps through strategic confidence?

[OAK EXPLAINS: Natural Direct and Indirect Effects]

OAK: The modern framework for mediation defines two quantities using what we call nested counterfactuals. The Natural Direct Effect, or NDE, asks: what happens if we change the treatment from off to on, but we hold the mediator at the value it would naturally take under control? This captures the portion of the treatment effect that does not operate through the mediator.

The Natural Indirect Effect, or NIE, asks the opposite: what happens if we hold treatment fixed at on, but we let the mediator shift from its control value to its treatment value? This captures the portion of the effect that operates specifically through the change in the mediator.

And here is the beautiful part: the total effect decomposes exactly into NDE plus NIE. Every bit of the treatment effect flows either through the mediator or around it.

NARRATOR: But there is a catch. To identify these effects, we need an assumption called sequential ignorability. Treatment must be as-if randomly assigned given covariates -- that is the standard ignorability we have seen before. But we also need the mediator to be as-if randomly assigned, conditional on treatment and covariates. This second assumption is far more demanding, because the mediator is typically not randomly assigned.

[BLUE'S MISTAKE]

BLUE: I ran three regressions -- outcome on treatment, mediator on treatment, and outcome on both. The indirect effect through Pokemon health is zero point one five, and the direct effect is zero point zero eight. Therefore sixty-five percent of the total effect operates through health.

OAK: But Blue, your mediator -- average team HP entering each battle -- is also affected by the opponent's strategy, which independently affects the outcome. There is a confounder of the mediator-to-outcome relationship that you have not accounted for. In the presence of such confounders, this classic decomposition does not recover causal mediation effects. You need the formal potential outcomes framework and you need to be honest about the sequential ignorability assumption.

NARRATOR: In the Elite Four data, the mediation analysis finds that roughly sixty percent of the total effect of item use operates through the health maintenance pathway, while forty percent operates through other channels. But the sensitivity analysis reveals that a moderately sized confounder could nullify the indirect effect. The finding is suggestive, not ironclad.

Lorelei's Dewgong falls. She nods approvingly. "You understand that knowing a treatment works is not enough. Understanding how it works -- and being honest about the assumptions required -- is the mark of a serious researcher."

She steps aside. The door to the next chamber opens.

---

### Agatha's Ghost Chamber: Sensitivity Analysis

[SCENE: Darkness. Purple mist. A cackling laugh. An old woman materializes from fog.]

NARRATOR: The room is dark. Purple mist coils along the floor. Somewhere in the shadows, something cackles. Then Agatha materializes from the fog, leaning on her cane, a Gengar grinning at her shoulder.

AGATHA: Every study you have ever read rests on the assumption that you have measured everything that matters. But what about the things you cannot see? The ghosts in your model? The unobserved confounders that lurk behind every observational estimate?

NARRATOR: Her Gengar's eyes glow red.

AGATHA: Can your estimates survive my ghosts?

[TEACHING SECTION]

NARRATOR: Throughout this book, we have relied on assumptions like conditional ignorability, the exclusion restriction, and the parallel trends assumption. Each is, at its core, a claim about what we do not need to worry about. But these assumptions are untestable. Sensitivity analysis asks: how robust are our conclusions to violations of these assumptions?

Rather than treating identification assumptions as binary -- satisfied or not -- sensitivity analysis parameterizes the degree of violation and examines how the estimated effect changes.

[OAK EXPLAINS: Rosenbaum Bounds]

OAK: Rosenbaum developed a framework for matched observational studies. The key parameter is gamma, which measures how much an unobserved confounder could alter the odds of treatment assignment. When gamma equals one, there is no hidden bias -- it is as if we had a randomized experiment. As gamma increases, we allow more hidden bias. For each value of gamma, we compute the worst-case p-value. The sensitivity value is the smallest gamma at which the result becomes statistically insignificant.

A sensitivity value of gamma equals two means that an unobserved confounder would need to double the odds of treatment for one unit relative to its match in order to explain away the observed effect. Whether gamma equals two is large depends on context.

NARRATOR: There is also the E-value, introduced by VanderWeele and Ding. The E-value is a model-free measure: the minimum strength of association that an unobserved confounder would need to have with both the treatment and the outcome to fully explain away an observed effect.

For example, if we observe a risk ratio of two point five for the effect of Experience Share on defeating the Elite Four, the E-value works out to about four point four four. That means an unobserved confounder would need a risk ratio of nearly four and a half with both Experience Share use and Elite Four victory to explain away what we see. That is a very strong confounder.

OAK: And then there is Oster's approach, which asks a different question: how much does the treatment effect estimate change as you add observed controls? If adding controls barely moves the coefficient, then unobserved confounders -- which are presumably similar to observed ones -- would also barely move it. The key parameter delta represents the ratio of selection on unobservables to selection on observables.

NARRATOR: Finally, there is Manski's approach to partial identification. Rather than asking how large the bias must be, Manski asks: what can we learn with minimal assumptions? His worst-case bounds place no restrictions on the relationship between treatment and potential outcomes among the untreated. The bounds are wide -- often too wide to be informative -- but they are assumption-free. They represent the price of honesty.

[pause]

OAK: As Manski wrote: better to have wide bounds that are honest than narrow confidence intervals based on incredible assumptions.

NARRATOR: In our worked example, we estimate that Experience Share increases the probability of defeating the Elite Four by a factor of one point eight. The E-value is three point zero -- a moderately strong confounder would be needed. The Rosenbaum bounds hold significance up to gamma equals one point six. The Oster bound at delta equals one is still meaningfully different from zero. Taken together, the Exp Share effect is moderately robust but not impervious to confounding -- a common and honest conclusion.

Agatha's Gengar fades into the shadows. The old woman studies you. "You did not flinch when I showed you the ghosts. Good. A researcher who pretends there are no unobserved confounders is more dangerous than one who knows they exist."

She taps her cane on the floor. The mist parts, revealing the third door.

## Part 2: Bruno and Lance

### Bruno's Fighting Ring: Heterogeneous Treatment Effects

[SCENE: A shaking chamber. Two Machamp sparring. A muscular man sits cross-legged.]

NARRATOR: The chamber shakes. Two Machamp are sparring in the center of a raised platform. Bruno sits cross-legged at the edge, shirtless, his arms folded across his chest. He opens one eye as you enter.

BRUNO: You have spent this entire journey estimating average effects. But not everyone is average. Different fighters respond differently to the same training. The question is not just does the treatment work -- it is for whom does it work, and how much?

[TEACHING SECTION]

NARRATOR: The Average Treatment Effect is a useful summary, but it masks potentially enormous variation. A drug that helps half the population and harms the other half has an ATE of zero -- the same as a drug that does nothing for anyone. Policy-makers, clinicians, and trainers all want to know: who benefits, who is harmed, and who is unaffected?

The Conditional Average Treatment Effect, or CATE, captures this heterogeneity. It is the average treatment effect for the subpopulation with specific characteristics. If we could estimate CATE as a function of those characteristics, we would have a complete picture of treatment effect variation.

[OAK EXPLAINS: Causal Forests]

OAK: Wager and Athey introduced causal forests -- a machine learning method specifically designed to estimate the CATE. The key innovation is adapting random forests to the causal inference setting. A standard random forest predicts the expected outcome given covariates. A causal forest instead estimates the expected treatment effect given covariates, by partitioning the covariate space into regions where treatment effects are most heterogeneous.

A critical innovation is honesty -- the sample is split so that one subsample determines the tree structure and a separate subsample estimates the treatment effects within each leaf. This prevents overfitting and allows valid confidence intervals for the CATE -- a remarkable result for a machine learning method.

NARRATOR: Once we have CATE estimates, we can summarize them. The GATES approach -- Sorted Group Average Treatment Effects -- sorts everyone by their predicted CATE, divides them into groups like quintiles, and estimates the actual average effect within each group. If the predictions are informative, we should see a monotonically increasing pattern: the group predicted to benefit most should show the largest estimated effect.

OAK: And the CLAN -- Classification Analysis -- complements GATES by asking: what are the characteristics of the most-affected and least-affected groups? This reveals who benefits most, not just that heterogeneity exists. For policy purposes, CLAN is often the most actionable output.

NARRATOR: In the Kanto trainer data, the GATES analysis reveals striking heterogeneity in the Experience Share effect. The bottom quintile -- trainers predicted to benefit least -- shows an estimated effect of essentially zero. The top quintile shows an estimated effect of two point seven additional badges. The CLAN analysis reveals that the top quintile consists predominantly of trainers with diverse teams of four or more types and moderate experience. The Experience Share allows their underleveled team members to catch up, dramatically improving type coverage. Trainers who already have a concentrated, high-level team see almost no benefit.

The optimal treatment rule recommends Experience Share for trainers with team diversity above the median and experience below the seventy-fifth percentile. Under this rule, expected badge count increases by one point eight, versus zero point nine under treat-all.

NARRATOR: Bruno nods. "Not every fighter needs the same training regimen. The master understands that individual differences are not noise to be averaged away -- they are signal to be understood."

He bows and steps aside. The third door creaks open. A chill runs down your spine.

---

### Lance's Dragon Chamber: Interference and Spillovers

[SCENE: A vast arena open to the sky. Dark clouds. A caped figure with three Dragonite.]

NARRATOR: The final Elite Four chamber is vast -- an arena open to the sky, where dark clouds swirl overhead. Lance stands at the far end, his cape billowing, flanked by three Dragonite. As you enter, two of them turn to face you -- and each other.

LANCE: Your entire journey has relied on a single, foundational assumption: that one trainer's treatment does not affect another trainer's outcome. But dragons do not fight in isolation. My Dragonite share the battlefield. When one uses Earthquake, the other feels it too. What happens when SUTVA fails?

[TEACHING SECTION]

NARRATOR: Recall from Chapter One the Stable Unit Treatment Value Assumption -- SUTVA. It says each unit's potential outcome depends only on its own treatment assignment, not on anyone else's. SUTVA is often reasonable -- whether Ash uses Experience Share should not affect Misty's badge count. But in many settings, it fails spectacularly.

In double battles, using Earthquake damages your partner Pokemon. In vaccination, my vaccination protects not only me but also those around me. In job training programs, training some workers may worsen outcomes for untrained workers competing for the same jobs.

When SUTVA fails, the standard potential outcomes framework breaks down. Each person's outcome depends on the entire vector of everyone's treatment assignments. With a thousand people and binary treatment, that is two to the power of one thousand possible treatment vectors -- far too many to estimate.

[OAK EXPLAINS: Effects Under Interference]

OAK: To make progress, we define new causal quantities. The direct effect asks: what happens when we change your own treatment, holding everyone else's treatment fixed? The spillover effect, or indirect effect, asks: what happens when we change others' treatments, holding yours fixed?

To tame the complexity, we use exposure mappings -- functions that summarize the relevant aspects of others' treatments into something manageable. For example, instead of tracking every neighbor's exact treatment, we might just track the proportion of your neighbors who were treated. Under this simplification, the potential outcomes become workable again.

NARRATOR: There is a clever experimental design called two-stage randomization. In stage one, you randomly assign clusters to different treatment intensities -- say, thirty percent treated versus seventy percent treated. In stage two, within each cluster, you randomly assign individuals to treatment or control at the designated intensity. This design lets you estimate both direct and spillover effects.

NARRATOR: In the double battle worked example, the direct effect of using multi-target moves is plus thirty-three point four damage. But the spillover effect is negative twelve point four -- your partner takes splash damage. The total effect is only plus sixteen point two, because the spillover partially offsets the direct benefit. A coordinator who accounts for interference would use multi-target moves more selectively than a naive analysis would suggest.

Lance recalls his Dragonite. "SUTVA is a convenient fiction. In a world where units interact -- and they always do -- you must account for the connections between them."

He steps aside, and the final door swings wide.

## Part 3: The Frontier Corridor

[SCENE: A quiet corridor between the Elite Four chambers and the Champion's arena. Bookshelves line the walls.]

NARRATOR: Between the Elite Four and the Champion's chamber, there is a quiet corridor lined with bookshelves. Before you face the Champion, there are a few more tools to gather.

---

### Regression Kink Design

NARRATOR: In Chapter Six, we learned about the Regression Discontinuity Design, which exploits a jump in the probability of treatment at a threshold. But what if treatment does not jump -- instead, the intensity of treatment changes slope? A Regression Kink Design exploits a kink -- a change in slope -- in the relationship between a running variable and treatment intensity at a threshold.

Consider the Kanto League training program, which provides subsidized training hours based on a performance score. Below the threshold of fifty, trainers receive a flat ten hours per week. Above fifty, hours increase linearly -- ten plus half a point for every score point above fifty. There is no jump in training hours at the threshold, only a change in slope. By estimating the change in slope of outcomes at the threshold and dividing by the change in slope of treatment, we can estimate the effect of marginal training hours.

---

### Bounds and Partial Identification

NARRATOR: Manski posed a profound question: if we are unwilling to make any assumptions about the relationship between treatment and potential outcomes, what can we still learn? The answer is partial identification -- we cannot pin down the exact treatment effect, but we can bound it. The worst-case bounds replace what we cannot observe with the extreme possible values. The bounds are wide, but they are assumption-free.

Adding the assumption of monotone treatment response -- that treatment can only help, never hurt -- can substantially tighten the bounds. And Lee bounds address sample selection, where outcomes are only observed for a selected subset potentially affected by treatment.

[pause]

OAK: Wide bounds may seem uninformative, but they can still rule out interesting hypotheses. If the entire identified set is positive, we can conclude the treatment is beneficial even without point identification.

---

### Causal Discovery

NARRATOR: Throughout this textbook, we have assumed the causal graph based on domain knowledge. But what if we could learn the causal structure directly from data? This is the goal of causal discovery.

The PC algorithm starts with a complete undirected graph connecting every pair of variables, then systematically removes edges by testing whether pairs of variables are conditionally independent. After removing edges, it orients the remaining ones using the patterns we learned in Chapter Three -- specifically by identifying colliders, which have a distinctive signature in the data.

But there is a fundamental limitation: multiple DAGs can produce the same set of conditional independences. These observationally indistinguishable DAGs form what is called a Markov equivalence class. Without additional assumptions or experimental data, we cannot uniquely determine the causal direction from observational data alone.

OAK: Causal discovery is a powerful complement to domain knowledge, but it is not a replacement. The methods tell us which graphs are consistent with the data -- they cannot uniquely determine the true graph. Always combine algorithmic output with substantive knowledge.

---

### Double Debiased Machine Learning

NARRATOR: Machine learning methods -- random forests, neural networks, gradient boosting -- are extraordinary at prediction. But naive application to causal inference fails for a subtle reason: regularization bias. When you use a penalized method to estimate a treatment effect, the penalty that improves prediction accuracy also shrinks the treatment coefficient toward zero.

[BLUE'S MISTAKE]

BLUE: I trained a gradient-boosted model to predict badge count from all features including an Exp Share indicator. The coefficient is the causal effect.

OAK: No, Blue. The regularization shrinks all coefficients, and the model optimizes for prediction, not causal estimation. The coefficient is biased and the standard errors are meaningless. You need a framework that separates the machine learning estimation of nuisance parameters from the estimation of the causal parameter of interest.

NARRATOR: That framework is Double Debiased Machine Learning, or DML, developed by Chernozhukov and colleagues. The key ideas are twofold. First, construct a moment condition for the causal parameter that is insensitive to small errors in nuisance parameter estimation -- this is called Neyman orthogonality, and it is the debiasing step. Second, use cross-fitting: split the sample into folds, estimate nuisance parameters on one portion, and compute the causal estimate on the other. This avoids overfitting.

The result is remarkable: the causal estimate converges at root-n rate with valid confidence intervals, even when the nuisance parameters are estimated with machine learning methods that converge much more slowly. First-order errors in nuisance estimation do not contaminate the causal estimate.

There is also Targeted Maximum Likelihood Estimation, or TMLE, which achieves the semiparametric efficiency bound -- no regular estimator can have smaller asymptotic variance. It is also doubly robust.

---

### Transportability

NARRATOR: A map on the library wall catches your eye. It shows not just Kanto but the region to the west: Johto. A label reads: "Just because it works in Kanto does not mean it works in Johto."

Suppose we have estimated that Experience Share increases badge count by one point five badges in a rigorous Kanto study. A League official in Johto asks: can we apply this finding? The answer depends on why Johto might differ. Different gyms, different Pokemon distributions, different trainer demographics.

Pearl and Bareinboim formalized this using selection diagrams -- DAGs with special nodes indicating where the two populations differ. If the populations differ only in covariates but not in the causal mechanisms, the effect is transportable after reweighting for the covariate differences.

Using the CATE estimates from our causal forest and reweighting to the Johto covariate distribution, we obtain a transported effect of one point nine badges -- larger than the Kanto estimate, driven by Johto's higher team diversity.

OAK: Transportability requires that we know what differs between populations and that these differences are captured in measured covariates. If Johto gyms have fundamentally different battle mechanics that interact with Experience Share in unmeasured ways, no amount of reweighting will help.

---

### Dynamic Treatment Regimes

NARRATOR: All methods in Chapters One through Seven consider a single treatment at a single point in time. But many treatments are dynamic -- administered sequentially over time, with each decision depending on evolving status.

In the Elite Four challenge, a trainer faces four sequential battles. Before each battle, the trainer decides whether to use healing items. Crucially, the health of the team entering each battle is both a confounder -- sicker teams benefit more from items -- and affected by prior treatment -- using items last round improves health this round.

This creates a vicious cycle. Standard regression adjustment for health introduces collider bias, while failing to adjust leaves confounding bias. Neither approach works.

[BLUE'S MISTAKE]

BLUE: I controlled for team health at every stage in a regression and found no effect of item use. Items do not work.

OAK: But by conditioning on health at each stage, you have blocked the very pathway through which prior item use operates. This is the time-varying version of the bad controls problem from Chapter Three.

NARRATOR: Marginal Structural Models, developed by Robins, Hernan, and Brumback, solve this using inverse probability of treatment weighting applied to the entire treatment history. The weights create a pseudo-population where time-varying confounders no longer predict treatment -- analogous to what randomization achieves in a single-period setting.

In the Elite Four data, using marginal structural models, the probability of a full sweep is twenty-two percent under never using items, sixty-one percent under always using items, and sixty-eight percent under the optimal dynamic regime estimated via Q-learning. The optimal regime prescribes: use items before a battle if average team HP is below fifty-five percent or if the upcoming opponent has a type advantage.

## Part 4: The Champion Battle

[SCENE: Blaze of light. Grand arena. Cameras flashing. A crowd roaring. A familiar smirking figure.]

NARRATOR: You step through the final door and into a blaze of light. The Champion's chamber is a grand arena, cameras flashing, a crowd roaring. And there, standing at the far end with his arms crossed and that infuriating smirk, is Blue.

BLUE: So you made it. But can you beat me? I have studied the data. I know everything about causation.

NARRATOR: Professor Oak's voice crackles through the arena speakers.

OAK: Six rounds. In each round, Blue will make a causal claim. Identify the fallacy. Score four out of six to earn the Championship.

NARRATOR: The stadium lights focus. The battle begins.

---

### Round One: The Starter Selection

BLUE: I analyzed five thousand League records. Trainers who chose Squirtle average six point eight badges. Charmander trainers average five point nine badges. Squirtle is objectively the best starter.

[THINK ABOUT THIS]

NARRATOR: Take a moment. What is the fallacy here?

[long pause]

NARRATOR: The fallacy is confounding -- the original sin of causal inference. The mistake Blue has been making since Chapter One. Trainers do not randomly choose starters. Squirtle is disproportionately chosen by trainers from wealthier families with better training resources. The association is confounded by socioeconomic background.

The correct approach: use matching, propensity score weighting, or doubly robust estimation to adjust for confounders. The adjusted effect of Squirtle versus Charmander may be much smaller -- or zero.

Blue's first Pokemon goes down. Five rounds remain.

---

### Round Two: The Elite Four Paradox

BLUE: Among trainers who made it to the Elite Four, those who trained the hardest actually have lower win rates. Hard work does not pay off at the highest level.

[THINK ABOUT THIS]

[long pause]

NARRATOR: The fallacy is collider bias, also known as selection bias. Making it to the Elite Four is a collider -- it is caused by both hard work and natural talent. Conditioning on this collider induces a spurious negative association. Among those who made it, the hard workers tend to be less talented -- they compensated with effort -- and the effortless ones tend to be more talented. The negative association within this selected group is an artifact, not evidence that hard work is harmful.

The correct approach: analyze the full population, not the selected subsample. Or explicitly model the selection process.

Blue's Pidgeot goes down.

---

### Round Three: The Cave Training Anecdote

BLUE: I trained in Cerulean Cave for a month and then won the Championship. Cave training works -- I am living proof.

[THINK ABOUT THIS]

[long pause]

NARRATOR: The fallacy is selection bias combined with anecdotal evidence. Blue is a single observation -- a sample size of one. Moreover, he is the grandson of Professor Oak, has access to exceptional resources, and possesses an extraordinary team. His success may have nothing to do with cave training.

The correct approach: a controlled study with a proper comparison group. At minimum, a matched comparison with similar trainers who did not train in the cave.

Blue's Alakazam faints.

---

### Round Four: The Potion Paradox

BLUE: My data shows that trainers who use more Potions during battles have more losses. Potions cause losing.

[THINK ABOUT THIS]

[long pause]

NARRATOR: The fallacy is reverse causality. The causal arrow runs the wrong way. Trainers use Potions because they are losing -- their Pokemon are taking damage -- not the other way around. Potion use is a consequence of battle difficulty, not a cause of losses.

The correct approach: an instrument, such as random variation in Potion prices across PokeMarts, could break the reverse causality. Or a randomized experiment where trainers are assigned Potion strategies before battles begin.

Blue's Arcanine falls.

---

### Round Five: Simpson's Gym Paradox

BLUE: I checked the data: Water types beat Rock types at a higher overall rate than Fire types do. But weirdly, Fire types do better than Water types against Rock types in every single gym. The overall data must be wrong -- Water types are clearly better.

[THINK ABOUT THIS]

[long pause]

NARRATOR: The fallacy is Simpson's Paradox, which we first encountered in Chapter Three. The overall association reverses when conditioning on gym. Water-type trainers disproportionately challenge gyms where Rock types are rarer, while Fire-type trainers disproportionately challenge Rock-heavy gyms like Pewter City. Within any given gym, Fire types perform better, but the aggregated data reverse the relationship because of the non-random distribution of gym selection. Gym Choice is a common cause -- a confounder -- of both Type Matchup and Win Rate.

Blue's Exeggutor is defeated.

---

### Round Six: The Badge Control

BLUE: I ran a regression of Elite Four performance on Exp Share use, controlling for number of badges, team level, win rate, and total battles fought. After controlling for everything, Exp Share has no significant effect. It is useless.

[THINK ABOUT THIS]

[long pause]

NARRATOR: The fallacy is bad controls -- post-treatment bias. Badges, team level, win rate, and total battles are all caused by Exp Share use. They are post-treatment variables. Controlling for them blocks the causal pathways through which Exp Share operates. Of course the coefficient shrinks to zero: Blue has adjusted away the very mechanism of the treatment.

The correct approach: only control for pre-treatment covariates. If you want to understand the mechanism, use mediation analysis from Section Eight Point One -- do not simply control for the mediator.

Blue's final Pokemon -- his starter, that Squirtle from Chapter One, now a Blastoise -- falls.

## Part 5: Champion

[SCENE: The arena erupts. Confetti. Flashing lights.]

NARRATOR: The arena erupts. Professor Oak's voice booms through the speakers.

OAK: Six for six. Flawless.

NARRATOR: Blue stands frozen for a moment. Then, slowly, he uncrosses his arms.

BLUE: I was making the same mistakes the whole time, was I not? Confounding. Colliders. Reverse causality. Bad controls. I was so focused on the data that I forgot to think about the structure.

OAK: The data never speaks for itself, Blue. It always needs a causal framework to interpret it.

NARRATOR: Oak turns to you. He opens a case. Inside: a golden badge, larger than the others, engraved with a stylized directed acyclic graph.

OAK: You are the Causal Inference Champion of the Kanto Region.

[pause]

NARRATOR: You look at the badge. Eight gym badges, each representing a tool you earned along the way. Potential outcomes in Pallet Town. Randomized experiments in Pewter City. DAGs in Cerulean City. Matching in Vermilion City. Regression and doubly robust estimation in Celadon City. Instrumental variables and regression discontinuity in Fuchsia City and Cinnabar Island. Difference-in-differences and synthetic control in Saffron City. And here at the Indigo Plateau: mediation, sensitivity analysis, heterogeneous effects, interference, machine learning, transportability, and the Champion's gauntlet of causal fallacies.

[pause]

NARRATOR: The journey through Kanto taught you more than methods. It taught you a way of thinking. That correlation is not causation. That data alone cannot answer causal questions -- you need assumptions, and those assumptions must be stated, tested, and defended. That the right method depends on the right DAG. That honesty about what you do not know is more valuable than false precision about what you think you do.

---

### Post-Credits Scene

[SCENE: A video call. Professor Oak's face on a screen.]

NARRATOR: The screen fades to black. Then, slowly, a familiar jingle plays -- the sound of a video call connecting. Professor Oak's face appears, his lab visible behind him.

OAK: Ah, Champion. I am glad I caught you. I have been reviewing some data from the Johto region -- the region to the west. They have their own Gyms, their own Pokemon, their own training programs. The thing is, their trainers are quite different from ours. Different demographics, different team compositions, different battle styles.

NARRATOR: He adjusts his glasses.

OAK: The Johto League wants to implement some of the programs we have studied here in Kanto. But they are worried: will our Kanto results transport to Johto? I have been working on selection diagrams, reweighting methods, formal transportability conditions. And I have heard rumors of even stranger challenges in Johto -- treatments that change over time, interference patterns we have never seen, confounders that are themselves proxied by other variables.

NARRATOR: He smiles.

OAK: I think there is a whole new journey waiting for you, Champion. The methods you have learned are not just tools for Kanto -- they are a framework for thinking about causation wherever you go. Professor Elm in New Bark Town has been expecting you. He has some interesting data.

NARRATOR: Oak winks. The screen goes dark. Somewhere, a Hoothoot calls into the night.

Your journey continues.

## Chapter Summary

NARRATOR: Let us take one final look back at what we learned at the Indigo Plateau.

First, mediation analysis with Lorelei. The total effect of a treatment decomposes into the Natural Direct Effect and the Natural Indirect Effect. Identification requires sequential ignorability -- a strong assumption that demands sensitivity analysis.

Second, sensitivity analysis with Agatha. No observational study is immune to unobserved confounding. Rosenbaum bounds, E-values, Oster bounds, and Manski bounds provide complementary frameworks for assessing robustness.

Third, heterogeneous treatment effects with Bruno. The ATE masks individual variation. Causal forests, GATES, and CLAN reveal who benefits most. Policy learning leverages heterogeneity to design optimal treatment rules.

Fourth, interference with Lance. When SUTVA fails, standard estimands are undefined. Exposure mappings, partial interference, and two-stage randomization allow identification of direct and spillover effects.

Fifth, the frontier corridor. Regression kink designs exploit slope changes. Partial identification provides honest bounds. Causal discovery learns DAG structure from data. Double debiased machine learning uses ML for nuisance parameters while maintaining valid inference. Transportability formalizes when effects generalize across populations. Dynamic treatment regimes handle sequential treatments with time-varying confounding.

And sixth, the Champion Battle. Six common causal fallacies -- confounding, collider bias, anecdotal evidence, reverse causality, Simpson's paradox, and bad controls -- reviewed and defeated.

## Comprehension Check

NARRATOR: For the final time, check yourself on these questions.

First: What is the difference between the Natural Direct Effect and the Natural Indirect Effect? Why is sequential ignorability stronger than standard ignorability?

[long pause]

The NDE captures the treatment effect holding the mediator at its control value. The NIE captures the effect operating through the mediator. Sequential ignorability adds the requirement that the mediator is as-if random conditional on treatment and covariates -- ruling out unobserved mediator-outcome confounders.

Second: What does an E-value of three mean?

[long pause]

An unobserved confounder would need a risk ratio of at least three with both the treatment and the outcome to explain away the observed effect.

Third: Why do causal forests split the sample into a structure-finding half and an estimation half?

[long pause]

This is the honesty property. It prevents the tree from overfitting to the outcomes used for estimation, which allows valid confidence intervals for the CATE.

Fourth: If your partner in a double battle uses Earthquake and your Pokemon takes damage, is that a SUTVA violation?

[long pause]

Yes. Your outcome depends on your partner's treatment assignment, not just your own. This is interference.

Fifth: In Blue's final round, why does controlling for badges, team level, and win rate eliminate the Exp Share effect?

[long pause]

Because those are post-treatment variables -- they are caused by Exp Share. Controlling for them blocks the causal pathways through which the treatment operates, making the coefficient artificially shrink to zero.
