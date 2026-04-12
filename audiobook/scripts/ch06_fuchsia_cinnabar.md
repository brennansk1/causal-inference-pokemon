---
title: "Chapter 6: Fuchsia City and Cinnabar Island -- Instrumental Variables and Regression Discontinuity"
chapter_number: 6
source_file: "textbook/chapters/ch06_fuchsia_cinnabar.md"
estimated_runtime_minutes: 85
key_concepts:
  - Unobserved Confounding
  - Instrumental Variables (IV)
  - The Three IV Assumptions (Relevance, Independence, Exclusion Restriction)
  - The Wald Estimator
  - Two-Stage Least Squares (2SLS)
  - Weak Instruments
  - Local Average Treatment Effect (LATE)
  - Compliance Types (Compliers, Always-Takers, Never-Takers, Defiers)
  - Monotonicity
  - Sharp Regression Discontinuity Design (RDD)
  - Fuzzy RDD
  - Local Linear Regression
  - Bandwidth Selection
  - McCrary Density Test
  - Placebo / Covariate Balance Tests
  - Fuzzy RDD as IV at the Cutoff
datasets:
  - safari_zone_lottery.csv
  - happiness_evolution.csv
characters:
  - NARRATOR (trainer, five badges, curious and increasingly confident)
  - OAK (professor, patient teacher, plain-English definitions)
  - BLUE (rival, overconfident, makes causal reasoning errors)
  - KOGA (Fuchsia Gym Leader, quiet, strategic, speaks in clipped sentences)
  - BLAINE (Cinnabar Gym Leader, intense, quiz-master energy, loves testing knowledge)
---

# Chapter 6: Fuchsia City and Cinnabar Island -- Instrumental Variables and Regression Discontinuity

## Part 1: The Safari Zone Lottery and the Instrumental Variables Idea

[SCENE: A coastal road. Sea breeze. The sound of waves fading as footsteps move inland through tall grass. A wooden sign creaks in the wind.]

NARRATOR: Five badges. Five cities. I have come a long way since Pallet Town. I have run randomized experiments in Pewter City. I have drawn DAGs and blocked backdoor paths in Cerulean. I have matched on observables in Vermilion. And in Celadon City, I built doubly robust estimators that combine the best of regression and propensity scores.

But every method I have learned so far -- every single one -- rests on the same deep assumption. You have to be able to measure and adjust for all the confounders. Every variable that affects both treatment and outcome has to be in your dataset. If it is not, the backdoor path stays open, and your estimate carries bias.

Today I arrive in Fuchsia City. And the lesson waiting here is about what happens when that assumption fails.

[pause]

The first thing I notice is the sign at the edge of town. It reads: "Fuchsia City -- Home of the Safari Zone." And below it, a smaller placard: "Weekly lottery for free Safari Zone passes. All registered trainers automatically entered."

A lottery. That detail is going to matter more than I realize.

[pause]

I head toward the Fuchsia Gym, but a crowd near the Safari Zone entrance catches my attention. Trainers are arguing. The debate sounds familiar -- like the starter argument back in Pallet Town, but with different stakes.

One trainer is insisting that Safari Zone training is the secret to competitive success. She waves her Pokedex, showing a win rate chart. "Trainers who attend the Safari Zone win sixty-eight percent of their battles. Trainers who do not attend win only forty-five percent. That is a twenty-three-point gap. The data speaks for itself."

Another trainer pushes back. "Correlation. Those trainers are already better. Patient people go to the Safari Zone because they enjoy the slow catching game. And patient people win more battles because they plan their strategy carefully. You are confusing the training with the trainer."

I watch the argument unfold. Neither side budges.

[SCENE: Inside the Fuchsia Gym. Dim lighting. The faint smell of incense. Koga sits cross-legged on a raised platform, eyes closed.]

NARRATOR: I step into the Gym. It is darker than I expected. The air is still, and the floor seems to absorb sound. Koga, the Fuchsia City Gym Leader, opens one eye.

KOGA: You heard the argument outside.

NARRATOR: I nod.

KOGA: Both sides are half right. The Safari Zone does help. But the gap they measured is inflated. Patient trainers choose to attend. Patient trainers also win more battles. The trait you cannot see is doing double duty.

NARRATOR: That phrase -- "the trait you cannot see." It hits differently after five chapters of learning to control for everything I can observe. Koga is talking about something beyond the reach of matching, beyond the reach of propensity scores, beyond the reach of doubly robust methods. He is talking about unobserved confounding.

KOGA: You need a tool that works when the confounder hides. The lottery outside. That is your tool.

[pause]

---

[TEACHING SECTION]

NARRATOR: Let me set up the problem formally. Suppose we want to estimate the causal effect of attending Safari Zone training on battle performance. The treatment is attendance -- did the trainer go to the Safari Zone or not? The outcome is win rate over the next twenty battles.

The naive comparison shows a twenty-three-percentage-point gap. Attendees win more. But here is the issue.

Think about a causal diagram. There are three variables. Safari Zone attendance is the treatment. Battle performance is the outcome. And patience -- a trait we cannot measure -- is the unobserved confounder. Patience affects attendance, because patient trainers enjoy the slow-paced catching game and are more likely to go. And patience affects battle performance, because patient trainers plan more carefully and win more often.

So there is a backdoor path from attendance to performance, running through patience. And because patience is not in our dataset, we cannot block that path. No regression, no matching, no propensity score can fix this. The methods from Chapters Three through Five are powerless here. They are what researchers call "selection on observables" strategies. They work beautifully when all confounders are measured. But patience is not measured. The most important confounders often are not.

[pause]

Now, here is where the lottery comes in.

[OAK EXPLAINS: The Instrumental Variable]

OAK: Every week, the Fuchsia City Warden draws names from the trainer registry for free Safari Zone passes. The lottery is random. It does not depend on patience, skill, or any other characteristic of the trainer. All registered trainers are automatically entered.

Now think about what this lottery does to the causal diagram. Add the lottery as a new variable. It has an arrow pointing to attendance -- lottery winners are more likely to go, because the five-hundred-Pokedollar admission fee is waived. But here is the crucial part. The lottery has no arrow pointing directly to battle performance. Winning a lottery ticket does not make you a better battler. The only way the lottery could improve your win rate is by getting you into the Safari Zone.

And the lottery has no arrow connecting it to patience. It is random. Patient trainers and impatient trainers win the lottery at the same rate.

This is the instrumental variables idea. Find a variable -- the instrument -- that shifts the treatment but has no other pathway to the outcome.

NARRATOR: Let me say that again because it is the core insight of this entire section. The lottery nudges people toward attending the Safari Zone. But the lottery itself has no direct effect on how well they battle. The only channel from lottery to performance runs through attendance. That is what makes the lottery an instrument.

[pause]

[TEACHING SECTION]

NARRATOR: For the lottery to serve as a valid instrument, three conditions have to hold. These are the three IV assumptions, and they are worth memorizing.

[OAK EXPLAINS: The Three IV Assumptions]

OAK: Assumption one is relevance. The instrument must actually affect the treatment. The lottery must change attendance behavior. If nobody who wins the lottery bothers going to the Safari Zone, the instrument is useless. This assumption is testable. You can check whether lottery winners attend at higher rates than lottery losers.

Assumption two is independence, also called exogeneity. The instrument must be as-if randomly assigned -- independent of all potential outcomes and all confounders, observed and unobserved. Because our lottery is literally random, this is highly plausible. Winners and losers are comparable in expectation on everything, including patience.

Assumption three is the exclusion restriction. This is the most subtle and the most consequential. It says the instrument affects the outcome only through the treatment. The lottery affects your win rate only by changing whether you attend the Safari Zone. There is no other channel. The lottery does not make you feel lucky and fight more boldly. The lottery does not save you money that you then spend on better healing items. The only door the lottery key opens is the Safari Zone door.

NARRATOR: Notice something important about these three assumptions. Relevance is testable -- you can check it in the data. Independence is guaranteed by the randomization of the lottery. But the exclusion restriction? You cannot test it. No statistical procedure in the world can determine whether the lottery has some tiny direct effect on performance that bypasses the Safari Zone.

[pause]

OAK: The exclusion restriction is what makes instrumental variables powerful and what makes them fragile. It is a substantive assumption that must be defended on theoretical and institutional grounds. The choice of instrument is as much an art as a science.

[pause]

NARRATOR: Now, assuming the lottery is a valid instrument, how do we actually compute the causal effect? The answer is beautiful in its simplicity.

[TEACHING SECTION]

NARRATOR: We break the problem into two observable relationships.

The first is called the reduced form. It is the effect of the instrument on the outcome. How much better do lottery winners perform compared to losers? In our data, lottery winners have an average win rate of fifty-eight percent. Lottery losers average fifty percent. The difference is eight percentage points. This is called the intent-to-treat effect -- the effect of being assigned to the instrument, regardless of whether you actually changed your behavior.

The second is called the first stage. It is the effect of the instrument on the treatment. How much more likely are lottery winners to actually attend the Safari Zone? Winners attend at a rate of seventy-two percent. Losers attend at thirty percent. The difference is forty-two percentage points. This tells us the compliance rate -- how many people's behavior is actually changed by the lottery.

[OAK EXPLAINS: The Wald Estimator]

OAK: The instrumental variables estimate is the ratio of these two quantities. You take the reduced form -- the eight-percentage-point intent-to-treat effect -- and divide it by the first stage -- the forty-two-percentage-point compliance rate. Eight divided by forty-two gives you approximately nineteen percentage points.

NARRATOR: Let me make sure the intuition is perfectly clear. The reduced form of eight percentage points tells us that lottery winners have better outcomes. But the effect is "watered down." Why? Because not everyone who wins the lottery changes their behavior. Some winners would have attended anyway -- they are always-takers. Some winners ignore the free pass and stay home -- they are never-takers. Only about forty-two percent of people actually changed their behavior because of the lottery.

So the eight-point improvement is a diluted version of the true causal effect. It is diluted by the fact that only forty-two percent of people were actually affected by the instrument. When we divide by the first stage, we concentrate the effect back onto the people whose behavior actually changed. We undo the dilution. And we get nineteen percentage points.

[pause]

Compare this to the naive comparison of twenty-three percentage points. The IV estimate is nineteen. The difference -- about four points -- is the upward bias from patience confounding. Patient trainers were inflating the naive estimate by selecting into the Safari Zone.

[BLUE'S MISTAKE]

BLUE: Why bother with this lottery nonsense? Just compare people who went to the Safari Zone with people who did not. Attendees win twenty-three percent more. That is the answer. Simple.

OAK: Blue, that comparison conflates two things -- the causal effect of training and the pre-existing advantage of patient people. The IV estimate of nineteen percentage points strips away the selection bias by using only the variation in attendance that was induced by the lottery. That variation is, by construction, uncorrelated with patience.

BLUE: But the lottery misses so much data. You are throwing away information.

KOGA: You are not throwing away information. You are throwing away bias.

[pause]

---

## Part 2: LATE, Compliance Types, Two-Stage Least Squares, and Weak Instruments

[SCENE: A training area behind the Fuchsia Gym. Koga is demonstrating a technique with his Venomoth. Oak has arrived via bicycle.]

NARRATOR: The IV estimate of nineteen percentage points seems clean and powerful. But there is a question I have been avoiding. Nineteen percentage points for whom? For all trainers? For the ones who attended? For everyone in Fuchsia City?

The answer, it turns out, is none of those. The IV estimate applies to a very specific group of people. And understanding which group -- and why -- is one of the most important ideas in modern causal inference.

[TEACHING SECTION]

NARRATOR: When we have a binary instrument like the lottery -- win or lose -- and a binary treatment like attendance -- attend or not -- every trainer falls into one of four categories. These categories are defined by what a trainer would do under each possible lottery outcome. Think of it as two potential behaviors: what you would do if you won, and what you would do if you lost.

[OAK EXPLAINS: The Four Compliance Types]

OAK: The first type is the complier. A complier is a trainer who would attend the Safari Zone if they won the lottery but would not attend if they lost. The lottery changes their behavior. They are on the margin -- interested enough to go if it is free, but not willing to pay five hundred Pokedollars out of pocket. These are the people for whom the instrument makes a difference.

The second type is the always-taker. An always-taker attends the Safari Zone regardless of the lottery. They are wealthy or devoted. They buy their own ticket even if they lose the lottery. The lottery does not change their behavior at all.

The third type is the never-taker. A never-taker has no interest in the Safari Zone. Even a free pass does not entice them. Maybe they find it boring, or they are too busy training at the Gym. The lottery does not change their behavior either.

The fourth type is the defier. A defier would attend if they lost the lottery but refuse to attend if they won. They do the opposite of what the instrument encourages.

NARRATOR: Now, that fourth type -- the defier -- sounds bizarre. Who would refuse a free Safari Zone pass specifically because it was free? That behavior is hard to imagine. And in fact, we need an assumption that rules it out.

[OAK EXPLAINS: Monotonicity]

OAK: The monotonicity assumption says that the instrument weakly increases treatment for everyone. Winning the lottery never decreases anyone's probability of attending. No defiers exist. This is our fourth assumption, beyond the big three. In the Safari Zone context, it is very plausible. A free pass makes attendance weakly more attractive for every trainer. Nobody turns contrarian just because they won.

NARRATOR: Here is the punchline. Under the four assumptions -- relevance, independence, exclusion restriction, and monotonicity -- the IV estimate recovers the average treatment effect for compliers only. Not for always-takers. Not for never-takers. Not for the whole population. Just for the people whose behavior was changed by the instrument.

This result is called the Local Average Treatment Effect, or LATE. It was proven by Imbens and Angrist in nineteen ninety-four, and it is one of the most important results in modern econometrics.

[pause]

[THINK ABOUT THIS]

NARRATOR: Why does the IV estimate capture the effect only for compliers? Think about it this way. The Wald estimator uses only the variation in attendance that comes from the lottery. Always-takers attend regardless of the lottery -- the lottery creates no variation for them. Never-takers stay home regardless -- no variation for them either. The only people for whom the lottery creates variation in attendance are the compliers. So the IV estimate, by construction, reflects the experience of compliers alone.

This has a profound implication. The LATE of nineteen percentage points tells us what Safari Zone training does for marginal trainers -- the ones who are on the fence about attending. It does not tell us what training does for the devoted regulars or the completely uninterested. And those effects could be quite different.

[pause]

OAK: LATE is often dismissed as a second-best result. People want the average treatment effect for the whole population but have to settle for the effect on compliers. But think about it from a policy perspective. If the Fuchsia City Warden is considering making the Safari Zone free for everyone, who are the people whose behavior would change? The compliers. Always-takers already attend. Never-takers will not attend even if it is free. The compliers are precisely the policy-relevant population.

NARRATOR: That reframing helped me see LATE not as a limitation but as an answer to the right question.

[pause]

Now, there is one more thing about compliance types that is worth understanding. We can never directly identify any individual's type. We observe whether someone won the lottery and whether they attended, but that only narrows it down.

If someone won the lottery and attended, they are either a complier or an always-taker. We cannot tell which. If someone won the lottery and did not attend, they are definitely a never-taker. If someone lost the lottery and attended, they are definitely an always-taker. And if someone lost and did not attend, they are either a complier or a never-taker.

We can identify never-takers among winners and always-takers among losers individually. But we can never point to a single person and say with certainty, "this person is a complier."

[pause]

There is a useful relationship connecting the intent-to-treat effect and the LATE. The ITT equals the LATE times the proportion of compliers. In our example, zero point zero eight equals zero point one nine times zero point four two. The ITT is the diluted version of the LATE, diluted by the compliance rate. Dividing the ITT by the first stage undilutes it.

[pause]

---

[TEACHING SECTION]

NARRATOR: The Wald estimator is elegant, but it is limited. It handles only a single binary instrument and a single binary treatment, with no covariates. In practice, we often want to include control variables for efficiency, handle continuous instruments, or use multiple instruments at once. The generalization that handles all these cases is called Two-Stage Least Squares, or two-S-L-S.

[OAK EXPLAINS: Two-Stage Least Squares]

OAK: The idea is in the name. There are two stages.

In the first stage, you regress the treatment on the instrument and any covariates. In our example, you regress Safari Zone attendance on the lottery indicator, trainer level, and number of badges. Then you save the predicted values from this regression. These predicted values represent the part of attendance variation that is explained by the instrument -- the exogenous, as-if-random variation. All the endogenous variation -- the part of attendance driven by patience and other unobserved confounders -- is absorbed into the residual and discarded.

In the second stage, you regress the outcome on the predicted treatment values and the same covariates. You regress win rate on predicted attendance, trainer level, and badges. The coefficient on predicted attendance is your two-S-L-S estimate of the causal effect.

NARRATOR: Why does this work? Because the predicted attendance values contain only the variation that comes from the lottery. All the contaminated variation -- the part driven by patience, by motivation, by unmeasured ability -- has been stripped away. You are using only the clean, exogenous variation to estimate the causal effect.

Think of it as purifying the treatment variable. The original attendance variable is a mixture of good variation -- driven by the random lottery -- and bad variation -- driven by unobserved confounders. The first stage separates the two. The second stage uses only the good.

[pause]

In our Safari Zone data, the two-S-L-S estimate is nineteen point one percentage points -- virtually identical to the Wald estimate of nineteen point zero. That is expected when the model is well specified. But two-S-L-S gives us tighter standard errors because we include covariates that explain variation in the outcome.

[pause]

OAK: One critical warning. If you manually run the first-stage regression, save the predicted values, and then run a second ordinary least squares regression, the coefficient will be correct but the standard errors will be wrong. The naive second-stage standard errors do not account for the fact that the predicted treatment is itself an estimate with sampling uncertainty. Always use a dedicated two-S-L-S procedure that computes correct standard errors automatically.

[pause]

---

[TEACHING SECTION]

NARRATOR: The power of IV comes with a price. The estimates are only as good as the instrument. And there are two main ways an instrument can fail you.

[OAK EXPLAINS: Weak Instruments]

OAK: An instrument is weak if it has only a small effect on the treatment. The first-stage relationship between the instrument and the treatment is statistically significant but practically tiny. Weak instruments cause two severe problems.

First, bias. The two-S-L-S estimator is biased toward the ordinary least squares estimate in finite samples. With a weak instrument, your IV estimate can be nearly as biased as the naive comparison -- defeating the entire purpose.

Second, unreliable inference. Standard confidence intervals become too narrow. You reject null hypotheses too often. Your results look significant when they should not.

NARRATOR: There is a famous rule of thumb from Stock and Yogo, published in two thousand five. If the first-stage F-statistic exceeds ten, the instrument is considered sufficiently strong. In our Safari Zone lottery, the first-stage F-statistic is about one hundred twenty-eight -- well above ten. The lottery is a strong instrument.

But what if we were using a different instrument? Say, distance from a trainer's home to the Safari Zone. If trainers who live closer are only slightly more likely to attend, the first-stage F might be, say, four point two. With a weak instrument like that, the two-S-L-S estimate would be unreliable.

[pause]

To understand weak instruments intuitively, remember that the Wald estimator is a ratio. Reduced form divided by first stage. When the first stage is near zero -- a weak instrument -- you are dividing by a small and noisy number. Small errors in the denominator get amplified dramatically. In the extreme case where the instrument has zero effect on treatment, you would be dividing by zero. The estimator is undefined.

[pause]

[BLUE'S MISTAKE]

BLUE: I found a great instrument for Safari Zone attendance. Whether a trainer owns a Fishing Rod. Fishing Rod owners are way more likely to visit the Safari Zone. The first stage is super strong. So my IV is valid.

OAK: Blue, a strong first stage is necessary but not sufficient. Does owning a Fishing Rod satisfy the exclusion restriction? Trainers who own Fishing Rods are likely outdoorsy, patient, and experienced -- all traits that directly affect battle performance. The Fishing Rod is correlated with unobserved confounders. The independence assumption fails.

KOGA: A strong instrument that violates the exclusion restriction is worse than no instrument at all. It gives you confidence in a biased answer.

[pause]

NARRATOR: That is the fundamental tension of instrumental variables. Relevance is testable but not sufficient. The exclusion restriction is what actually makes the instrument valid, and it can never be tested with data. You have to argue for it on theoretical and institutional grounds. And no amount of statistical significance can substitute for a convincing argument.

[pause]

OAK: Let me give you one more example of how the exclusion restriction can fail. Suppose lottery winners feel lucky, and that psychological boost makes them fight more boldly and win more battles -- independent of whether they actually attend the Safari Zone. If this "luck effect" exists, the reduced form captures both the indirect effect through attendance and the direct effect through confidence. The IV estimate is biased upward.

NARRATOR: Could this happen with our Safari Zone lottery? Maybe. But the lottery is a standard weekly drawing -- nothing dramatic, nothing that would create a lasting psychological boost. Winners just get a slip of paper good for free entry. The exclusion restriction is plausible here, even if it is not provable.

[pause]

---

## Part 3: Cinnabar Island and the Regression Discontinuity Design

[SCENE: A ferry dock. Waves lap against the hull. The engine hums as the boat pulls away from Fuchsia City.]

NARRATOR: With the Soul Badge earned, I board the ferry to Cinnabar Island. The volcanic island rises from the sea ahead of me -- a cone of dark rock crowned with a research laboratory. Cinnabar is famous for two things: Blaine's Fire-type Gym, and the Pokemon research lab where scientists study evolution.

I lean on the railing as the island grows closer. In Fuchsia City, I learned to handle unobserved confounders by finding an instrument -- an external source of variation that shifts the treatment without directly affecting the outcome. Now I am about to learn a completely different strategy. One that does not require an instrument at all. One that exploits something much simpler: a threshold.

[pause]

[SCENE: The Cinnabar Island research lab. Bright fluorescent lights. Charts and graphs cover the walls. A man with wild white hair and sunglasses perched on top of his head stands in front of a chalkboard. This is Blaine.]

BLAINE: Pop quiz! What happens when a Pokemon's happiness score reaches two hundred and twenty?

NARRATOR: I know this one.

NARRATOR: It evolves.

BLAINE: Correct! And what is the causal effect of that evolution on battle performance?

NARRATOR: I hesitate. The naive answer is to compare evolved Pokemon to unevolved Pokemon. But after five chapters, I know that comparison is contaminated by selection bias. Pokemon with high happiness have dedicated trainers who invest in every aspect of their Pokemon's development. Comparing evolved to unevolved conflates the effect of evolution with the effect of having a good trainer.

BLAINE: Now you are thinking. But I did not ask you to compare all evolved Pokemon to all unevolved Pokemon. I asked about the effect of evolution. And I have a dataset that will let you estimate it cleanly -- if you know the trick.

[pause]

---

[TEACHING SECTION]

NARRATOR: Here is the setup. Every Pokemon has a happiness score -- a continuous measure from zero to two hundred fifty-five. It depends on time spent with the trainer, battles fought, items used, and other factors. The game mechanics dictate that when happiness reaches two hundred twenty, the Pokemon evolves. Below two hundred twenty, no evolution.

This is a sharp cutoff. At two hundred nineteen, the Pokemon does not evolve. At two hundred twenty, it does. The question is whether that evolution -- the crossing of the threshold -- causes improved battle performance.

[OAK EXPLAINS: The Regression Discontinuity Idea]

OAK: The identification strategy is simple and elegant. Compare Pokemon just above the cutoff to Pokemon just below it. A Pokemon with a happiness score of two hundred twenty-one evolved. A Pokemon with a happiness score of two hundred nineteen did not. But these two Pokemon are essentially identical in every other respect. Their trainers invested almost the same amount of effort. They have nearly the same experience. They differ by a mere two points on a zero-to-two-fifty-five scale. Yet one evolved and the other did not.

NARRATOR: Think about what this means. Near the cutoff, whether a Pokemon lands at two hundred nineteen or two hundred twenty-one is essentially random. It is the difference of one extra pat on the head, one fewer potion used, one more step walked. The variation is noise. And that noise acts like a natural coin flip -- some Pokemon land just above the threshold and evolve, others land just below and do not.

This is the local randomization interpretation. Near the cutoff, the regression discontinuity design mimics a randomized experiment. The Pokemon just above and just below the threshold are comparable on every dimension that matters -- trainer quality, training investment, battle experience -- except that one group evolved and the other did not.

[pause]

BLAINE: Here is the formal definition. The causal effect of evolution at the cutoff equals the limit of expected battle performance as happiness approaches two hundred twenty from above, minus the limit of expected battle performance as happiness approaches two hundred twenty from below. That jump -- the discontinuity in the outcome at the cutoff -- is the causal effect.

NARRATOR: Let me translate that into a picture you can hold in your mind. Imagine a scatter plot. The horizontal axis is happiness score, running from about one hundred fifty to two hundred fifty-five. The vertical axis is battle performance -- a standardized combat power index. Each dot is a Pokemon.

Now, as you scan from left to right, the dots trend gently upward. Happier Pokemon tend to perform better, because their trainers have invested more. The relationship is smooth and gradual. Nothing sudden.

Until you reach two hundred twenty. Right at that point, the dots jump. The line that was tracking smoothly at about fifty-two points of combat power suddenly leaps to about sixty-four. Then it continues trending gently upward on the other side.

That jump -- the vertical gap at the cutoff -- is the causal effect of evolution. It is about eleven and a half points on the combat power index.

[pause]

[THINK ABOUT THIS]

NARRATOR: Why can we interpret this jump as causal? Because of one key assumption: everything other than treatment varies smoothly at the cutoff. There is no reason to expect a sudden jump in trainer skill at exactly two hundred twenty. There is no reason for Pokemon genetics to change abruptly at that point. No other relevant factor snaps at the threshold. The only thing that jumps at two hundred twenty is evolution status. So the jump in outcomes must be caused by evolution.

This is called the continuity assumption. The conditional expectation of the outcome under both potential outcomes -- evolved and not evolved -- is continuous at the cutoff. In the absence of treatment, there would be no jump. The observed jump exists only because treatment switches on.

[pause]

---

[TEACHING SECTION]

NARRATOR: How do we actually estimate the size of that jump? The standard approach is called local linear regression.

[OAK EXPLAINS: Local Linear Regression]

OAK: The idea is to fit two separate linear regressions -- one on each side of the cutoff -- using only observations within a window around the threshold. The window is called the bandwidth.

On the left side, you take all Pokemon with happiness scores between, say, two hundred five and two hundred nineteen. You fit a straight line through their data, predicting combat power from happiness. Then you extrapolate that line to the cutoff -- to exactly two hundred twenty. That gives you the predicted combat power just below the threshold.

On the right side, you take all Pokemon with happiness scores between two hundred twenty and two hundred thirty-five. You fit another straight line. You extrapolate to the cutoff from above. That gives you the predicted combat power just above the threshold.

The RDD estimate is the difference between those two predicted values at the cutoff. The right-side intercept minus the left-side intercept.

NARRATOR: In our data, the left-side regression predicts a combat power of fifty-two point three at the cutoff. The right-side regression predicts sixty-three point eight. The difference is eleven point five, with a robust standard error of three point two. The ninety-five percent confidence interval runs from five point two to seventeen point eight.

Evolution causes an eleven-and-a-half-point increase in the standardized combat power index for Pokemon at the happiness threshold of two hundred twenty. That is a substantial and statistically significant effect.

[pause]

BLAINE: Pop quiz! Why local linear regression instead of a big global polynomial? Why not fit a single sixth-degree polynomial across the whole dataset?

NARRATOR: I remember this from the textbook chapter Blaine assigned. Global polynomials are dangerous because they let observations far from the cutoff influence the estimate at the cutoff. A Pokemon with a happiness score of one hundred fifty is seventy points away from the threshold -- it tells us almost nothing about what happens at two hundred twenty. But a high-order polynomial gives that distant observation leverage. It can pull the fitted curve around, creating wild oscillations near the boundary.

BLAINE: Correct! Gelman and Imbens wrote an entire paper in two thousand nineteen making this argument. Stick with local linear regression. The key mathematical property is that local linear regression has boundary bias of order h-squared, where h is the bandwidth, while simpler methods have bias of order h. That means local linear regression gives you a better approximation exactly where you need it -- at the cutoff.

[BLUE'S MISTAKE]

BLUE: I fit a sixth-degree polynomial on each side of the cutoff using all the data. My R-squared is zero point nine four. The effect is twenty-two point seven points. Much bigger than your estimate.

BLAINE: Your R-squared is meaningless here. Your polynomial is being pulled by a handful of influential observations with happiness scores near one hundred fifty and two hundred fifty-five. Runge phenomenon. Drop the data below one hundred eighty and your estimate changes dramatically. That sensitivity is exactly the problem.

[pause]

---

[TEACHING SECTION]

NARRATOR: The choice of bandwidth -- how wide the window around the cutoff should be -- is one of the most important decisions in any RDD analysis. And it involves a fundamental tradeoff.

[OAK EXPLAINS: Bandwidth Selection]

OAK: A small bandwidth uses fewer observations, all very close to the cutoff. The advantage is low bias -- the straight-line approximation is excellent over a narrow range. The disadvantage is high variance -- you have fewer data points, so the estimate is noisy.

A large bandwidth uses more observations, including ones farther from the cutoff. The advantage is lower variance -- more data means a more precise estimate. The disadvantage is higher bias -- the straight-line approximation may be poor over a wide range.

NARRATOR: In our data, the optimal bandwidth selected by the Cattaneo-Idrobo-Titiunik procedure is fifteen happiness points on each side of the cutoff. That gives us three hundred twelve Pokemon in the estimation window.

But good practice requires checking that the results are robust to other bandwidth choices. So we also compute the estimate at bandwidth eight, twelve, twenty, and thirty. The estimates range from nine point six to twelve point eight. All the confidence intervals overlap. The point estimate drifts downward slightly as the bandwidth widens, which makes sense -- the linear approximation gets worse at wider bandwidths, introducing a bit of bias. But the overall picture is stable.

[pause]

BLAINE: Pop quiz! What if a researcher runs the analysis with fifteen different bandwidths and reports only the one that gives the largest, most significant estimate?

NARRATOR: That is cherry-picking. A form of p-hacking. The bandwidth should be chosen by a principled, data-driven procedure before looking at the treatment effect, or the full range of estimates should be reported transparently.

BLAINE: Full marks. The optimal bandwidth selector provides a pre-committed choice. Always use it. And always show sensitivity.

[pause]

---

[TEACHING SECTION]

NARRATOR: Now, the RDD is only as credible as its assumptions. And there are three key diagnostic checks that every researcher must perform.

The first is the McCrary density test. This one checks for manipulation.

[OAK EXPLAINS: The McCrary Density Test]

OAK: The most important threat to an RDD is manipulation of the running variable. If trainers can precisely control their Pokemon's happiness to land just above two hundred twenty, then the Pokemon right above the cutoff are systematically different from those just below. Their trainers are more skilled, more strategic, more invested. The as-good-as-random argument collapses.

The McCrary density test checks whether the density of the running variable -- the distribution of happiness scores -- is continuous at the cutoff. Under no manipulation, you expect roughly equal numbers of Pokemon on both sides of two hundred twenty. If trainers are gaming the threshold, you would see bunching -- an excess of observations just above and a hollow just below.

NARRATOR: Imagine the histogram of happiness scores near the cutoff. If there is no manipulation, it should look smooth and continuous through two hundred twenty. No spike, no dip, no cliff. Just a gentle, unremarkable distribution.

In our data, that is exactly what we see. The histogram is roughly uniform between two hundred and two hundred forty. No visible bunching at two hundred twenty. The McCrary test statistic is negative zero point zero eight with a p-value of zero point six four. We fail to reject the null of no manipulation. Reassuring.

BLAINE: Why is manipulation unlikely here? Because happiness scores in the Pokemon world are a complex function of many inputs -- walking steps, using items, winning battles, leveling up -- and trainers do not see the exact number displayed. Precise manipulation is hard when you cannot see the precise score.

OAK: Contrast that with settings where the running variable is self-reported, like income for benefit eligibility, or precisely known, like a test score for program admission. In those settings, manipulation is a serious concern, and the McCrary test is essential.

[pause]

NARRATOR: The second diagnostic is the covariate balance test. The key assumption of RDD is that everything other than treatment is continuous at the cutoff. We can partially test this by checking whether pre-treatment covariates show discontinuities.

For each covariate -- Pokemon level, base attack, base defense, base speed -- we run the RDD with that covariate as the outcome. If the design is valid, none of these should show a significant jump at two hundred twenty. A Pokemon's level should not suddenly change at the threshold. Its base stats should not suddenly change either.

In our data, none of the covariates show a significant discontinuity. The estimated jumps are tiny -- negative zero point three for level, zero point eight for base attack, negative zero point five for base defense, zero point two for base speed -- and none are close to statistically significant. This is consistent with the identifying assumption.

[pause]

BLAINE: Pop quiz! What would it mean if base attack showed a significant discontinuity at two hundred twenty?

NARRATOR: It would be a red flag. It would suggest that something other than evolution changes at the cutoff. Maybe trainers who push their Pokemon past two hundred twenty are systematically investing in attack stats, and the jump in combat power is partly driven by that investment rather than evolution alone. The RDD would lose credibility.

BLAINE: Exactly. Covariate balance is not sufficient for validity, but a failure is nearly sufficient for invalidity.

[pause]

---

## Part 4: Fuzzy RDD, the Connection to IV, and the Road to Saffron City

[SCENE: Blaine's Gym, after the battle. The Volcano Badge glints in the firelight. Oak is reviewing notes.]

NARRATOR: I have the Volcano Badge. But Blaine is not done teaching.

BLAINE: Everything so far has been the sharp design. The cutoff perfectly determines treatment. At two hundred twenty, evolution happens. Below it, it does not. But pop quiz: what if some trainers press the B button during the evolution animation and cancel it?

NARRATOR: I know about B-button pressers. Some trainers prefer the unevolved form's aesthetics, or its moveset, or its type. They let happiness rise above two hundred twenty but cancel the evolution when it triggers.

BLAINE: Now the cutoff is no longer sharp. Crossing two hundred twenty increases the probability of evolution, but it does not guarantee it. Among Pokemon just above the threshold, maybe eighty-two percent actually evolve. The other eighteen percent had their evolution canceled. This is a fuzzy regression discontinuity design.

[pause]

[TEACHING SECTION]

NARRATOR: In the fuzzy RDD, the treatment probability jumps at the cutoff but does not go from zero to one. Below two hundred twenty, no Pokemon can evolve -- the probability is zero. Above two hundred twenty, eighty-two percent evolve -- the probability jumps to zero point eight two. The jump in treatment probability is zero point eight two.

Now, this should sound familiar.

[OAK EXPLAINS: Fuzzy RDD as Instrumental Variables]

OAK: The fuzzy RDD is conceptually identical to instrumental variables. The instrument is whether the running variable exceeds the cutoff -- an indicator for whether the Pokemon's happiness is at or above two hundred twenty. This indicator serves as an instrument for actual evolution status.

Think about it. The three IV assumptions hold. First, relevance: crossing the cutoff increases the probability of evolution from zero to eighty-two percent. Second, independence: near the cutoff, being just above or below is as good as random. Third, exclusion restriction: crossing the cutoff affects battle performance only through its effect on evolution. The cutoff itself has no direct effect.

NARRATOR: And the estimator is the same Wald ratio we used in Fuchsia City. Take the jump in outcomes at the cutoff and divide by the jump in treatment at the cutoff. The jump in combat power is nine point eight. The jump in evolution probability is zero point eight two. Nine point eight divided by zero point eight two gives us eleven point nine five.

The fuzzy RDD estimate is about twelve points -- slightly larger than the sharp RDD estimate of eleven point five. Why? Because the sharp design diluted the effect by averaging over both evolved Pokemon and B-button non-compliers above the threshold. The fuzzy design corrects for that dilution.

[pause]

And just as IV in Fuchsia City recovered a LATE -- the effect for compliers -- the fuzzy RDD recovers the effect for compliers at the cutoff. These are the Pokemon that evolve when above two hundred twenty and would not evolve if below. The B-button pressers are the non-compliers. They cross the threshold but refuse the treatment.

[pause]

BLAINE: Pop quiz! Both fuzzy RDD and standard IV use the Wald estimator structure. What is the key difference?

NARRATOR: The source of identifying variation. In standard IV, the instrument is some external variable -- like a lottery -- that provides exogenous variation in treatment across the whole population. The validity of the instrument depends on institutional arguments about the exclusion restriction.

In fuzzy RDD, the instrument is the cutoff itself. The identifying variation comes from the local randomization near the threshold. You do not need a lottery or an external nudge. You just need a sharp cutoff and the inability of units to precisely manipulate the running variable.

BLAINE: And that is why fuzzy RDD is often considered more credible than a typical IV design. The local randomization near the cutoff is a stronger form of exogeneity than most instruments can claim. The exclusion restriction is more plausible because crossing a threshold typically has no direct effect on outcomes other than through the treatment it triggers.

[pause]

[BLUE'S MISTAKE]

BLUE: I can do this faster. Pokemon above two hundred twenty have an average combat power of sixty-one point five. Those below average forty-eight point two. The effect is thirteen point three points.

OAK: Blue, you are making two errors at once. First, you are comparing all Pokemon above and below the cutoff, not just those near it. Pokemon with happiness of two hundred fifty are very different from those with happiness of one hundred eighty. The RDD uses only observations near the cutoff to ensure comparability.

BLAINE: And second, you are ignoring the fuzzy nature of the design. Not all Pokemon above two hundred twenty actually evolved. Your naive comparison conflates the effect of evolution with the effect of happiness itself.

BLUE: Fine. But my number is bigger.

KOGA: A bigger number is not a better number.

[long pause]

---

[TEACHING SECTION]

NARRATOR: Before we leave Cinnabar Island, let me take stock of what we have learned across these two cities and draw some connections.

In Fuchsia City, we learned instrumental variables. The key idea is to find an external source of variation -- the lottery -- that shifts the treatment without directly affecting the outcome. The instrument lets us estimate causal effects even when critical confounders are unobserved. The price we pay is that IV recovers only the LATE -- the effect for compliers, the people whose behavior is changed by the instrument.

On Cinnabar Island, we learned regression discontinuity. The key idea is to exploit a sharp threshold in a continuous running variable. Near the cutoff, treatment assignment is as good as random. We estimate the causal effect by measuring the jump in outcomes at the threshold. The price we pay is that RDD recovers only a local effect -- the effect for units right at the cutoff. We learn nothing about units far from the boundary.

Both methods share a deep structure. Both give up the dream of estimating the average treatment effect for the entire population. IV gives us the effect for compliers. RDD gives us the effect at the cutoff. Both are local estimands -- local to a specific subpopulation defined by the source of identifying variation.

And fuzzy RDD is literally IV at the cutoff. The same Wald ratio, the same compliance framework, the same LATE interpretation. The only difference is where the exogenous variation comes from.

[pause]

OAK: Let me offer some practical guidance for when to use each method.

Use instrumental variables when you have an external source of variation that plausibly satisfies the three assumptions -- relevance, independence, and the exclusion restriction. The exclusion restriction is the binding constraint. Spend most of your effort defending it.

Use regression discontinuity when treatment is determined by whether a continuous variable crosses a threshold. The running variable should not be precisely manipulable. Check the McCrary density test. Check covariate balance. Report bandwidth sensitivity.

And in both cases, be transparent about the local nature of your estimate. State clearly who the compliers are, or what happens at the cutoff, and discuss whether the results generalize to broader populations.

[pause]

NARRATOR: There is one more extension worth mentioning. We talked about the sharp design, where the cutoff perfectly determines treatment, and the fuzzy design, where it shifts the probability. There are also brief mentions in the literature of regression discontinuity in time -- where the running variable is a date rather than a continuous score -- and shift-share instruments, where the instrument is constructed by combining aggregate-level changes with unit-level exposure shares. These are advanced topics, but they build directly on the foundations we have laid here.

[pause]

---

[SCENE: The Cinnabar Island dock at sunset. NARRATOR stands with six badges pinned to a jacket. The ferry to the mainland waits.]

NARRATOR: Two cities. Two badges. Two fundamentally new strategies for causal inference.

The Soul Badge, from Koga, for mastering instrumental variables. I learned the Wald estimator, two-stage least squares, the LATE theorem, and the art of defending the exclusion restriction. I learned that when you cannot measure the confounder, you can sometimes find an instrument that works around it.

The Volcano Badge, from Blaine, for mastering regression discontinuity. I learned sharp and fuzzy designs, local linear regression, the McCrary density test, bandwidth sensitivity analysis, and the deep connection between fuzzy RDD and instrumental variables. I learned that a threshold in a continuous variable can create a natural experiment as credible as any randomized trial -- if you handle it carefully.

[pause]

Both methods share a common lesson that sets them apart from everything in Chapters Three through Five. They do not require you to measure confounders. They require you to find -- or exploit -- a source of variation in treatment that is as-if random. The lottery. The threshold. These sources of variation let you bypass the unobserved confounder entirely.

The price you pay is narrower identification. You do not get the ATE. You get the LATE, or the effect at the cutoff. But in many cases, those local effects are exactly what matters for policy.

[pause]

I board the ferry. Cinnabar Island shrinks behind me. Six badges down, two to go. The next stop is Saffron City, where Team Rocket has invaded and a mysterious new TM is being rolled out city by city. The staggered rollout will create a different kind of natural experiment -- one that requires difference-in-differences, synthetic control, and tools I have not learned yet.

But that is the next chapter.

[long pause]

---

## Chapter Summary and Comprehension Check

[SCENE: Professor Oak's study. A fire crackles. Oak sits across from the narrator with a cup of tea.]

OAK: Six badges. Let us make sure you have earned them. I want to hear it in your own words.

[pause]

NARRATOR: Here is what I know.

[TEACHING SECTION]

NARRATOR: Part one. Instrumental variables solve the problem of unobserved confounding. When a critical confounder is unmeasured -- like patience in the Safari Zone setting -- no amount of regression, matching, or propensity score weighting can remove the bias. An instrumental variable provides an alternative route to causal identification by finding an external source of variation that shifts the treatment but has no other pathway to the outcome.

The three IV assumptions are relevance, independence, and the exclusion restriction. Relevance means the instrument actually affects the treatment -- the lottery increases attendance. Independence means the instrument is as-if randomly assigned -- unrelated to confounders. The exclusion restriction means the instrument affects the outcome only through the treatment -- the lottery does not directly improve battle performance. Relevance is testable. Independence is guaranteed by randomization. The exclusion restriction is untestable and must be defended on substantive grounds.

[pause]

Part two. The Wald estimator is the ratio of the reduced form to the first stage. The reduced form is the effect of the instrument on the outcome -- the intent-to-treat effect. The first stage is the effect of the instrument on the treatment -- the compliance rate. Dividing the ITT by the compliance rate recovers the causal effect for compliers.

Two-stage least squares generalizes this to handle covariates, continuous instruments, and multiple instruments. The first stage regresses treatment on the instrument to extract the exogenous variation. The second stage regresses the outcome on the predicted treatment to estimate the causal effect.

Weak instruments -- those with a first-stage F-statistic below ten -- cause bias toward the OLS estimate and unreliable confidence intervals. Anderson-Rubin confidence sets provide valid inference regardless of instrument strength.

The IV estimate recovers the LATE -- the Local Average Treatment Effect for compliers. Compliers are the people whose treatment status is changed by the instrument. Always-takers are treated regardless. Never-takers are untreated regardless. Defiers are ruled out by the monotonicity assumption. Different instruments identify different LATEs because they affect different complier populations.

[pause]

Part three. Sharp regression discontinuity exploits a deterministic treatment rule based on a continuous running variable crossing a cutoff. At two hundred twenty happiness points, Pokemon evolve. The key assumption is continuity -- all factors other than treatment vary smoothly at the cutoff. Near the threshold, treatment assignment is as good as random.

Local linear regression is the standard estimation approach. Fit separate linear regressions on each side of the cutoff within a bandwidth, and take the difference in intercepts. Avoid global polynomials, which are sensitive to faraway data and prone to wild extrapolation.

The bandwidth trades off bias and variance. Small bandwidths yield low bias but high variance. Large bandwidths yield lower variance but more bias. Optimal bandwidth selectors like the Cattaneo-Idrobo-Titiunik procedure balance this tradeoff automatically. Always report results at the optimal bandwidth and show sensitivity to alternatives.

[pause]

Part four. Fuzzy RDD arises when crossing the cutoff increases the probability of treatment without determining it completely. The estimator is the ratio of the jump in outcomes to the jump in treatment at the cutoff -- exactly the Wald ratio from IV. Fuzzy RDD is IV at the discontinuity, with the cutoff indicator as the instrument.

Diagnostics are essential. The McCrary density test checks for manipulation of the running variable. Bunching at the cutoff is a red flag. Covariate balance tests check that pre-treatment characteristics are continuous through the cutoff. Bandwidth sensitivity analysis confirms that results do not depend on a particular window choice.

[pause]

OAK: And the connection between the two methods?

NARRATOR: Both IV and RDD bypass unobserved confounders by exploiting a source of as-if-random variation in treatment. Both recover local estimands -- LATE for IV, the effect at the cutoff for RDD. Fuzzy RDD is literally IV applied at the cutoff, making the connection explicit. The main difference is where the exogenous variation comes from. IV relies on an external instrument whose validity must be argued. RDD relies on a threshold in a running variable, with local randomization providing a more transparent source of credibility.

OAK: Well said. You have earned your badges.

[pause]

---

[TEACHING SECTION]

NARRATOR: Before we close, let me run through the questions you should be able to answer without notes.

For instrumental variables. Can you state the three IV assumptions in one sentence each, and say which are testable? Can you write the Wald estimator as a ratio and explain in plain English what each piece measures? Can you explain why OLS fails with unobserved confounders and how IV gets around the problem without ever measuring the confounder? Can you define the four compliance types and explain why LATE applies only to compliers? Can you state what monotonicity assumes and why it is necessary? Can you describe what a weak instrument is and what goes wrong when the first-stage F-statistic is below ten? Can you give a plausible way the exclusion restriction might fail for the Safari Zone lottery?

For regression discontinuity. Can you state the RDD estimand -- the limit of expected outcomes from above minus the limit from below -- and explain what it means causally? Can you state the core identifying assumption and explain why a discontinuity in a covariate at the cutoff is a bad sign? Can you explain why local linear regression is preferred over global polynomial fits? Can you describe what the bandwidth trades off and what happens as it approaches zero or infinity? Can you explain what the McCrary density test checks and what a failed test tells you? Can you compare sharp and fuzzy RDD and explain the connection to IV? Can you discuss what the RDD estimate identifies and how to think about external validity away from the cutoff?

[pause]

If you can answer all of those, you are ready for Saffron City. If some of them are shaky, go back through the relevant sections. The concepts from this chapter -- especially LATE, the exclusion restriction, and the continuity assumption -- will come back again and again in applied research.

[long pause]

---

[SCENE: The mainland dock. Night. Stars over the ocean. The lights of Saffron City glow in the distance.]

NARRATOR: Six badges. The journey is two-thirds complete. Behind me, Fuchsia City and Cinnabar Island. Ahead of me, Saffron City, where Team Rocket has invaded and a staggered policy rollout is waiting to be analyzed with difference-in-differences. Then Viridian City, and the Indigo Plateau beyond.

But right now, I stand at the dock and think about the two ideas that define this chapter. The lottery and the threshold. The instrument and the discontinuity. Two completely different strategies that solve the same fundamental problem: what do you do when the confounder hides?

You find a way around it. You find exogenous variation. You find a natural experiment embedded in the world. And you use it carefully, transparently, and honestly.

I step off the dock and head toward the city lights. Saffron awaits.

[long pause]

End of Chapter Six.
