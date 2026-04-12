---
title: "Chapter 7: Saffron City -- Difference-in-Differences and Synthetic Controls"
chapter_number: 7
source_file: "textbook/chapters/ch07_saffron_city.md"
estimated_runtime_minutes: 80
key_concepts:
  - Panel Data and Repeated Observations
  - Difference-in-Differences (DiD)
  - The Parallel Trends Assumption
  - Two-by-Two DiD Worked Example
  - The DiD Regression Formulation
  - Two-Way Fixed Effects (TWFE)
  - Event Study Plots and Pre-Trends Testing
  - Staggered Treatment Adoption
  - The Forbidden Comparison (Already-Treated as Controls)
  - Negative Weighting in TWFE
  - Goodman-Bacon Decomposition
  - Callaway and Sant'Anna Estimator
  - Sun and Abraham Interaction-Weighted Estimator
  - Synthetic Control Method
  - Donor Pools and Weighted Counterfactuals
  - Placebo Tests for Synthetic Control Inference
characters:
  - NARRATOR (trainer, first-person, curious and conversational)
  - OAK (professor, patient teacher, plain-English definitions)
  - BLUE (rival, confident, makes causal reasoning errors)
  - SABRINA (Saffron Gym Leader, measured, sees patterns across time)
---

# Chapter 7: Saffron City -- Difference-in-Differences and Synthetic Controls

## Part 1: The Crossroads of Kanto

[SCENE: The guarded gates of Saffron City. Traffic noise, industrial hum, and the distant clatter of construction. The air is heavy.]

NARRATOR: The road east from Celadon leads through a series of guarded checkpoints and into the heart of Kanto's commercial capital. Saffron City. I have seven badges now -- Boulder, Cascade, Thunder, Rainbow, Soul, Volcano, Marsh is next -- and this city feels different from every place I have been before. It is bigger. Louder. The buildings rise higher than anything in Cerulean or Vermilion. Silph Co. headquarters dominates the skyline, a glass-and-steel tower that catches the afternoon light.

But something is wrong. There are Team Rocket grunts on the corners. Shop windows are boarded up. Trainers walk quickly, eyes down. Team Rocket has occupied the city. They have seized Silph Co. headquarters, and the economic life of thousands of residents has been thrown into chaos.

And in the middle of all of this, Silph's engineers have just completed their most ambitious project: a powerful new Technical Machine called Shadow Surge. It teaches any compatible Pokemon a devastating Dark-type move. The TM was released first here in Saffron, partly as a morale boost, partly because the distribution infrastructure was already in place. Over the following months, it will roll out to other cities -- Cerulean, Vermilion, and finally Lavender Town.

[pause]

I find Professor Oak near the Pokemon Center, studying a stack of printouts. He looks up and gestures for me to sit down.

OAK: You have arrived at the crossroads of Kanto -- and, as it happens, the crossroads of causal inference. Look around you. Two things are happening at once in Saffron City. First, a new TM is rolling out across the region, reaching different cities at different times. Second, Team Rocket has invaded this city and only this city. Both events raise causal questions. Does Shadow Surge actually improve battle win rates? And what is the economic cost of Team Rocket's occupation?

NARRATOR: I nod. Both questions seem straightforward on the surface, but I have been on this journey long enough to know that nothing about causal inference is as simple as it looks.

OAK: Neither question can be answered by a randomized experiment. Shadow Surge was not randomly assigned to cities. Team Rocket did not flip a coin to decide where to invade. We are in the world of observational data. But we have something powerful: repeated observations of the same cities over time. We have panel data. And panel data, when used correctly, gives us tools that cross-sectional data cannot.

NARRATOR: Panel data. That term has come up before, but Oak wants to make sure I understand it clearly.

OAK: Panel data means we observe the same units -- in our case, cities -- at multiple points in time. We can track Saffron, Cerulean, Vermilion, and the rest month after month, watching how their outcomes evolve. This is different from a cross-sectional dataset, where you observe many units at a single point in time. And it is different from a time series, where you observe a single unit across many time points. Panel data gives you both dimensions: variation across units and variation across time. And that combination turns out to be extraordinarily useful for causal inference.

[pause]

---

[TEACHING SECTION]

NARRATOR: So here is the setup for our first question. It is Month Six of the Kanto League season. Silph Co. releases Shadow Surge in Saffron City but not yet in Cerulean City. We observe trainer battle win rates in both cities for two periods: before the release, covering Months One through Five, and after the release, covering Months Seven through Twelve. The question is simple: does Shadow Surge improve battle win rates?

We have four numbers to work with. Before Shadow Surge was released, Saffron trainers had an average win rate of zero point four five. Cerulean trainers had an average win rate of zero point four zero. After the release, Saffron's average win rate rose to zero point five eight. Cerulean's rose to zero point four four.

Now, the most natural thing in the world would be to compare Saffron's post-treatment win rate to Cerulean's post-treatment win rate and call the difference the effect of the TM. That difference is zero point five eight minus zero point four four, which is zero point one four. A fourteen percentage point advantage. Case closed, right?

BLUE: Obviously. Saffron is fourteen points ahead after Shadow Surge drops. That is the effect. I do not need fancy double-differencing to see that.

OAK: Blue, you are making a mistake we have seen before. You are comparing two groups after treatment and calling the entire gap a treatment effect. But Saffron was already ahead of Cerulean before Shadow Surge was ever released. Saffron trainers had a win rate of zero point four five; Cerulean trainers were at zero point four zero. That is a five percentage point gap that existed before the TM. Maybe Saffron trainers have better access to training facilities. Maybe Silph employees moonlight as competitive battlers. Whatever the reason, that pre-existing gap has nothing to do with Shadow Surge. If you just compare post-treatment averages, you are attributing that pre-existing advantage to the TM.

NARRATOR: But there is a second problem, too. Both cities saw their win rates rise over time. Saffron went from zero point four five to zero point five eight -- that is a thirteen percentage point increase. But is all of that increase caused by Shadow Surge? Not necessarily. The Kanto League season naturally features rising win rates as trainers accumulate experience and evolve their Pokemon. Cerulean also went up, from zero point four zero to zero point four four -- a four percentage point increase -- and Cerulean did not receive Shadow Surge at all. If I just look at Saffron's before-and-after change, I am conflating the TM's effect with this common upward trend.

So a simple before-and-after comparison within Saffron is biased because it includes the time trend. And a simple post-treatment comparison across cities is biased because it includes the pre-existing gap. What I need is a method that eliminates both sources of bias at once.

[pause]

OAK: And that method is difference-in-differences.

NARRATOR: Difference-in-differences. DiD for short. The idea is elegant. You take two differences and subtract one from the other.

The first difference captures the total change in Saffron over time. That is zero point five eight minus zero point four five, which equals zero point one three. This first difference includes both the treatment effect and the common time trend. It tells you everything that happened in Saffron -- the TM's effect plus the natural improvement all trainers experience over the season.

The second difference captures the change in Cerulean over time. That is zero point four four minus zero point four zero, which equals zero point zero four. This second difference captures only the common time trend, because Cerulean did not receive Shadow Surge. Whatever is driving Cerulean's improvement -- experience, evolution, seasonal effects -- is also driving part of Saffron's improvement.

Now subtract the second difference from the first. Zero point one three minus zero point zero four equals zero point zero nine. That is the difference-in-differences estimate. Nine percentage points. Shadow Surge increases trainer win rates by approximately nine percentage points.

[pause]

Let me say that again more slowly, because this is the core idea and I want it to be completely clear.

The first difference -- within Saffron, over time -- removes the pre-existing level of Saffron's win rate. You are looking at change, not level. The second difference -- the control group's change over time -- removes the common trend that affects both cities. What is left, after both differences, is the part of Saffron's change that cannot be explained by either the baseline or the trend. That residual is the treatment effect.

OAK: Think of it this way. You and Blue are both training your Pokemon. Every day, you both gain about the same amount of experience -- you are on parallel paths. Then you receive the Shadow Surge TM, and your win rate jumps. If I want to estimate how much Shadow Surge helped you, I can look at how much your improvement exceeded Blue's, beyond what the pre-existing gap would have predicted. Saffron improved by thirteen points. Cerulean improved by four. The difference -- nine points -- is the effect of Shadow Surge.

[pause]

NARRATOR: There is a beautiful way to visualize this. Imagine a graph with time on the horizontal axis and win rate on the vertical axis. Before treatment, you see two lines. Saffron's line runs above Cerulean's, reflecting the pre-existing gap of five percentage points. But both lines slope upward at the same rate -- they are parallel. Then, at Month Six, when Shadow Surge is released, Saffron's line jumps upward by nine percentage points and continues along a higher trajectory. Cerulean's line just keeps going along its original path.

The DiD estimate is the vertical distance between where Saffron actually ended up and where Saffron would have been if it had just followed the same trend as Cerulean. That hypothetical path -- the dashed line showing where Saffron would have been without the TM -- is the counterfactual. The counterfactual win rate for Saffron in the post-period is zero point four five plus the four-point trend, which gives zero point four nine. Saffron actually hit zero point five eight. The gap between zero point five eight and zero point four nine is zero point zero nine. That is the DiD estimate.

[pause]

---

[TEACHING SECTION]

NARRATOR: Now let me connect this to regression, because in practice, researchers almost never compute DiD by hand from a table of four numbers. They run a regression. And the regression form makes everything precise.

You set up two indicator variables. The first is a treatment group indicator that equals one if the observation comes from Saffron and zero if it comes from Cerulean. The second is a post-period indicator that equals one if the observation is from the post-treatment period and zero if it is from the pre-treatment period. Then you include an interaction term -- the product of these two indicators -- which equals one only for Saffron observations in the post-treatment period.

The regression looks like this, spoken out loud. The outcome, win rate, equals an intercept, plus a coefficient on the treatment group indicator, plus a coefficient on the post-period indicator, plus a coefficient on the interaction term, plus an error.

The intercept captures the mean outcome for the control group in the pre-period. That is Cerulean's pre-treatment average of zero point four zero.

The coefficient on the treatment group indicator captures the pre-treatment difference between Saffron and Cerulean. That is zero point zero five.

The coefficient on the post-period indicator captures the change over time in the control group. That is Cerulean's improvement of zero point zero four.

And the coefficient on the interaction term -- this is the one we care about -- captures the additional change in the treated group beyond what the control group experienced. That is zero point zero nine. The DiD treatment effect.

OAK: You can verify this. The model says Saffron's post-treatment win rate equals the intercept of zero point four zero, plus the Saffron effect of zero point zero five, plus the time trend of zero point zero four, plus the treatment effect of zero point zero nine. Add those up: zero point four zero plus zero point zero five plus zero point zero four plus zero point zero nine equals zero point five eight. That matches Saffron's observed post-treatment win rate exactly. The model accounts for every piece of the outcome: the baseline, the group difference, the time trend, and the causal effect of the TM.

[pause]

NARRATOR: And this is what makes DiD powerful. It eliminates two types of confounders simultaneously. First, time-invariant confounders -- the permanent characteristics that make Saffron different from Cerulean. Better training facilities, wealthier trainers, proximity to Silph Co. These factors make Saffron's win rate permanently higher, but they are constant over time. Differencing over time removes them. Second, common time trends -- seasonal effects, region-wide changes, the general progression of the League. These affect both cities equally. Differencing across groups removes them.

What DiD cannot eliminate is something that changes differently across groups at the same time as treatment. A shock that hits Saffron but not Cerulean right when Shadow Surge is released. If Team Rocket's invasion depresses Saffron's win rates at the exact same moment the TM is released, the DiD estimate would conflate the positive TM effect with the negative invasion effect. And this brings us to the single most important assumption in all of difference-in-differences.

[pause]

---

[TEACHING SECTION]

NARRATOR: The parallel trends assumption. This is the load-bearing wall of every DiD analysis, and I need to be very precise about what it says and what it does not say.

OAK: The parallel trends assumption states this: in the absence of treatment, the treated group and the control group would have followed the same trend over time. Not the same level -- Saffron can be permanently above Cerulean. The assumption is about trends, not levels. It says that the gap between the two groups would have stayed constant if treatment had never occurred.

NARRATOR: Let me unpack what this means. It does not require that Saffron and Cerulean have the same win rate. They clearly do not -- Saffron starts five points higher. It does not require that the two cities are similar on observable characteristics. They can differ on every measurable trait -- population, wealth, infrastructure. As long as those differences produce only level shifts and not differential trends, the assumption holds. And it does not require that nothing else changes besides treatment. Other events can happen -- a new route opening, a weather event, a League rule change -- as long as those events affect both cities equally.

What the assumption does require is that no time-varying confounder hits the treated group differently from the control group at the moment of treatment. If something happens only to Saffron at the same time as Shadow Surge, the estimate is biased.

[pause]

And here is the critical thing: the parallel trends assumption is fundamentally untestable. The left side of the assumption involves what Saffron's win rate would have been without Shadow Surge in the post-period. That is a counterfactual. We never observe it. Once Saffron receives the TM, we cannot know what would have happened without it. This is the fundamental problem of causal inference showing up again, now in the DiD setting.

OAK: But we are not entirely in the dark. While we cannot test parallel trends directly, we can examine pre-treatment trends. If Saffron and Cerulean were moving in parallel before the TM was released, that is at least consistent with the assumption that they would have continued to do so afterward. It is not proof -- trends could diverge after treatment for reasons unrelated to the TM -- but it is the best diagnostic we have.

NARRATOR: And this diagnostic brings us to one of the most important tools in applied DiD research: the event study plot.

[pause]

Imagine a timeline. On the horizontal axis, you have periods relative to treatment. Negative numbers are pre-treatment periods. Zero is the moment of treatment. Positive numbers are post-treatment periods. The period just before treatment -- period negative one -- is the reference point, set to zero by convention.

At each point on this timeline, you estimate a coefficient that measures the difference between the treated and control groups, relative to that reference period. Now picture the results as dots on this timeline, each with a vertical line through it representing a confidence interval.

Here is what you want to see. In the pre-treatment periods -- the dots at negative five, negative four, negative three, negative two -- you want those dots to hover near zero. Close to the horizontal axis. With confidence intervals that overlap zero. This pattern tells you that before treatment, the treated and control groups were not diverging. Their trends were parallel. The pre-treatment dots near zero are not proof of parallel trends, but they are reassuring evidence.

Then, at period zero, when treatment hits, you want to see the dots jump. A sharp upward shift. And in the post-treatment periods -- one, two, three, four -- the dots should stay elevated, showing a persistent treatment effect.

In our Shadow Surge example, the event study looks clean. The pre-treatment coefficients at periods negative five through negative two are tiny -- negative zero point zero one, positive zero point zero two, negative zero point zero one, positive zero point zero one. All statistically insignificant. All hovering near zero. The treated and control groups were on parallel paths before the TM arrived. Then at period zero, the coefficient jumps to zero point zero seven. At period one, it is zero point zero eight. Period two, zero point zero nine. It grows slightly and then stabilizes around zero point one zero to zero point one one. This is consistent with trainers learning to use the TM effectively over time.

BLUE: Wait. I thought you said parallel trends was untestable. Now you are testing it with this event study thing?

OAK: Good question, Blue, and a common confusion. The event study does not test the parallel trends assumption itself. What it tests is whether treated and control groups had parallel trends in the pre-treatment period. That is a necessary but not sufficient condition. If pre-trends are not parallel, the assumption is almost certainly violated. But even if pre-trends look perfect, the assumption could still fail in the post-treatment period. Something could change at the exact moment of treatment. Pre-trends are a diagnostic, not a proof.

BLUE: So you are telling me that the whole thing rests on an assumption you cannot actually verify.

OAK: Welcome to observational causal inference.

[pause]

NARRATOR: Blue actually raises an important point here. Parallel trends can fail in several ways. The most obvious is differential pre-existing trends. If Saffron's win rate was already rising faster than Cerulean's before Shadow Surge -- maybe because Silph Co. was investing heavily in trainer development -- then DiD would attribute the continued divergence to the TM, even if the TM had no effect at all.

Another way is compositional changes. If skilled trainers migrate to Saffron to access Shadow Surge, the mix of trainers in Saffron changes at the moment of treatment. The post-treatment group is literally different people than the pre-treatment group.

And then there are simultaneous shocks. If Team Rocket's invasion hits Saffron's economy at the same time as Shadow Surge is released, the estimated effect conflates the TM benefit with the invasion cost.

When parallel trends is implausible, researchers have options. They can condition on covariates -- control for observable characteristics that might drive differential trends. They can use triple differences, which adds a third layer of differencing using a within-group comparison unaffected by treatment. Or they can conduct sensitivity analysis, bounding the treatment effect under specified violations of the assumption.

But for now, let us take the assumption at face value and move to the next stage: what happens when treatment does not arrive everywhere at once.

[pause]

---

## Part 2: The TWFE Trap and the Modern Revolution

[SCENE: Inside the Saffron City Gym. The air is still. Psychic energy hums. Sabrina sits cross-legged on a raised platform, eyes closed.]

NARRATOR: The Saffron Gym is unlike any I have visited. The lights are low. The floor is polished to a mirror sheen. And Sabrina, the Gym Leader, sits perfectly still at the center of it all. She is a Psychic-type specialist -- her Pokemon include Abra, Kadabra, and the formidable Alakazam. But what strikes me most is her demeanor. She is measured. Patient. She does not speak quickly or carelessly. Every word she says carries the weight of someone who has thought about it for a long time before letting it out.

SABRINA: You have been learning about difference-in-differences. Two groups. Two time periods. A clean double difference. It is elegant in its simplicity. But the real world is rarely so clean. In the real world, treatment does not arrive at one moment for one group. It rolls out. It staggers. Different units receive it at different times. And when that happens, the simple tools can deceive you.

NARRATOR: She opens her eyes and looks directly at me.

SABRINA: I see patterns across time. I see the flow of cause and effect as it ripples through periods and across groups. And I see the trap that waits for the researcher who extends the simple two-by-two framework without thinking carefully about what that extension actually does.

[pause]

---

[TEACHING SECTION]

NARRATOR: Here is the situation. Shadow Surge did not reach every city at once. Silph Co.'s production was limited. Distribution was staggered. Saffron got it first, in Period Six. Cerulean got it in Period Ten. Vermilion in Period Fourteen. Lavender Town in Period Eighteen. And four cities -- Pewter, Celadon, Fuchsia, and Cinnabar -- never received it at all.

We observe all eight cities for twenty-four periods. The outcome is average trainer win rate. Now, the natural instinct is to generalize the DiD regression. Instead of a simple treatment group indicator and a post-period indicator, you use what is called two-way fixed effects. TWFE.

In TWFE, you include a fixed effect for each city -- that is, a separate intercept for every city that absorbs all of its permanent characteristics. And you include a fixed effect for each time period -- a separate intercept for every month that absorbs all common temporal shocks. Then you add a single treatment indicator that turns on once a city has received Shadow Surge.

OAK: The city fixed effects do the same job as the treatment group indicator in the two-by-two case. They absorb permanent differences between cities. The time fixed effects do the same job as the post-period indicator. They absorb common time trends. In the simple two-city, two-period setting, TWFE is numerically identical to the DiD regression with an interaction term. It gives you the exact same number.

NARRATOR: So far, so good. TWFE seems like the natural generalization. For decades, this was the standard approach in economics, political science, and the social sciences. Thousands of published papers used exactly this specification. You include unit and time fixed effects, add a treatment indicator, and estimate the average effect. Simple. Clean. Trusted.

And then, starting in the late two thousand tens, a series of landmark papers revealed a disturbing fact.

[pause]

When treatment is adopted at different times by different units, and treatment effects are heterogeneous -- meaning they vary across groups or grow over time -- the TWFE estimator can be severely biased. It can even give the wrong sign. It can report a negative effect when the true effect is positive for every group at every time period.

BLUE: Come on. That cannot be right. Fixed effects on both dimensions, standard errors clustered, R-squared through the roof. How can that possibly go wrong?

SABRINA: Because the regression is making comparisons you did not ask it to make. And some of those comparisons are deeply flawed.

[pause]

NARRATOR: Let me explain what is actually happening inside the TWFE regression. When the model estimates its single treatment coefficient, it is not computing one clean DiD. It is implicitly computing a weighted average of every possible two-by-two DiD that can be constructed from the data. Some of those two-by-two comparisons are perfectly valid. Others are dangerous.

There are three types of comparisons the model makes. The first type compares newly-treated cities to never-treated cities. Saffron, treated in Period Six, is compared to Pewter, which is never treated. This is a clean comparison. Pewter is genuinely untreated and serves as a valid control.

The second type compares newly-treated cities to not-yet-treated cities. Saffron, treated in Period Six, is compared to Cerulean, which is not treated until Period Ten. During the window between Periods Six and Nine, Cerulean is genuinely untreated. This comparison is also valid.

The third type is the problem. When Cerulean becomes treated in Period Ten, the model may use Saffron -- which has been treated since Period Six -- as a control unit. But Saffron is not an untreated control. It is an already-treated city whose treatment effect may still be evolving. If Shadow Surge's effect grows as trainers master the TM, then Saffron's rising win rate makes Cerulean's treatment look less effective by comparison. In extreme cases, Saffron's continued improvement can make newly-treated Cerulean look like it is getting worse, even though the TM is actually helping.

OAK: This third type of comparison -- using already-treated units as controls -- is what we call the forbidden comparison. It is forbidden because the control group is contaminated by treatment. An already-treated unit whose effect is still growing is not a valid stand-in for "what would have happened without treatment."

[pause]

NARRATOR: The mechanics of why this happens are subtle but important. Andrew Goodman-Bacon, in a landmark paper published in two thousand twenty-one, showed that the TWFE coefficient can be written as a weighted average of all possible two-by-two DiD estimates. The weights depend on group sizes and the variance of the treatment indicator for each comparison. The weights sum to one, but they are not guaranteed to be positive when already-treated units serve as controls. And when treatment effects are heterogeneous -- when they differ across groups or change over time -- those forbidden comparisons can pull the overall estimate in the wrong direction.

Let me walk through the numbers from our Shadow Surge example. Suppose the true effect of Shadow Surge grows over time as trainers learn to use it. For Saffron, the effect starts at five percentage points and grows to fifteen after twelve treated periods. For Cerulean, it starts at five and grows to ten over eight treated periods. Vermilion goes from five to eight over four periods. Lavender, treated for only two periods, has an effect of about five points.

The true average treatment effect across all treated city-period combinations is approximately eight percentage points. That is the number we want.

But when we run TWFE, the model computes its weighted average of all those two-by-two comparisons. The clean comparisons -- treated versus never-treated -- give an average DiD of about eight point five percentage points, and they receive forty-five percent of the weight. The comparisons between earlier and later-treated cities, using the later group as control, give about seven point three percentage points and receive thirty percent of the weight. But the forbidden comparisons -- later-treated versus already-treated, using the already-treated as control -- give only about two point one percentage points and receive twenty-five percent of the weight.

Multiply each by its weight and add them up: eight point five times zero point four five, plus seven point three times zero point three, plus two point one times zero point two five. That gives approximately zero point zero three eight plus zero point zero two two plus zero point zero zero five, which equals zero point zero six five. Six point five percentage points.

The TWFE estimate is six point five. The true average effect is about eight. TWFE is biased downward by roughly twenty percent. And in more extreme scenarios -- where early-treated units have large, growing effects and later-treated units have smaller effects -- the bias can be far worse. TWFE can report an estimate near zero, or even negative, when every group's true effect is positive.

BLUE: I ran the TWFE regression on the staggered Shadow Surge data and got five point two percentage points. Standard errors are tiny, R-squared is huge, fixed effects on both dimensions. This is airtight.

SABRINA: Your regression is secretly comparing newly-treated cities to cities whose treatment effects are still maturing. That makes the new treatment look less effective than it actually is. Your five point two is contaminated.

[pause]

---

[TEACHING SECTION]

NARRATOR: So the Goodman-Bacon decomposition is a diagnostic tool. It breaks the TWFE estimate apart into its component two-by-two comparisons and shows you the weight on each type. If the weight on forbidden comparisons -- the already-treated-as-control type -- is small, TWFE may be approximately unbiased. If that weight is large, you have a problem. The decomposition does not fix the bias. It reveals it.

The fix comes from a new generation of estimators that emerged in the late two thousand tens and early two thousand twenties. These are sometimes called heterogeneity-robust estimators, and they share a common principle: only make valid comparisons. Never use already-treated units as controls.

[pause]

The first and perhaps most widely used is the Callaway and Sant'Anna estimator, published in two thousand twenty-one. The idea is beautifully clean. Instead of estimating a single overall treatment effect, you estimate the effect separately for each treatment cohort at each time period. A cohort is a group of units that received treatment at the same time. Saffron is the Period Six cohort. Cerulean is the Period Ten cohort. And so on.

For each cohort at each time period after that cohort's treatment began, you estimate what Callaway and Sant'Anna call the group-time average treatment effect on the treated. This is the treatment effect for that specific cohort at that specific time. And crucially, the comparison group used to estimate each of these effects is either the set of never-treated units or the set of not-yet-treated units. Both choices avoid the forbidden comparison.

Each group-time estimate is essentially a simple two-by-two DiD. You take the cohort's outcome at the current period, subtract its outcome in the period just before treatment, and then subtract the same change for the comparison group. Clean. Simple. No contamination from already-treated units.

Once you have this full grid of group-time effects, you can aggregate them in different ways. You can average across all cohorts and time periods to get an overall treatment effect. You can average within each cohort to get cohort-specific effects. You can average across cohorts at each event time -- meaning each number of periods since treatment -- to create what looks like an event study. Each of these aggregations tells you something different.

In our Shadow Surge example, the Callaway-Sant'Anna estimates, using never-treated cities as the comparison, show exactly the pattern we would expect. Saffron's effect starts at five percentage points in Period Six and grows steadily to fifteen by Period Twenty-Four. Cerulean starts at five in Period Ten and reaches ten. Vermilion starts at five in Period Fourteen and reaches eight. Lavender, treated only in Period Eighteen, shows five to six points. The simple average across all group-time cells is about eight point one percentage points -- essentially the true average effect.

OAK: Think of it this way. You are trying to measure how much a Rare Candy boosts a Pokemon's strength. You give Rare Candies to different Pokemon at different times. If you use a Pokemon that already received a Rare Candy as a control for a newly treated Pokemon, and the early Pokemon is still gaining strength from its candy, you will underestimate the effect for the new Pokemon. The modern methods say: only compare to Pokemon that have not yet received any Rare Candy. That way, your control group is truly untreated.

[pause]

NARRATOR: The second major estimator comes from Liyang Sun and Sarah Abraham, also published in two thousand twenty-one. Their approach stays within the regression framework that researchers are familiar with, which makes it easier to adopt in practice. The key insight is that the standard event study regression -- the one that estimates a coefficient at each period relative to treatment -- goes wrong because it forces all cohorts to have the same effect at each event time. If Saffron's effect at event time three is different from Cerulean's effect at event time three, the standard regression smashes them together in a way that creates contamination.

Sun and Abraham's fix is to interact the event-time indicators with cohort indicators. This lets each cohort have its own effect at each event time. You then aggregate across cohorts using appropriate weights to get a clean event study plot that is robust to treatment effect heterogeneity. The resulting plot -- what they call the interaction-weighted estimator -- shows the true dynamic pattern of effects without the distortions that plague the naive TWFE event study.

This matters for a practical reason. In many applied papers, the event study plot is the centerpiece of the empirical analysis. If that plot is based on a naive TWFE specification and treatment effects are heterogeneous, the plot can show spurious pre-trends -- making it look like parallel trends is violated when it is not -- or it can mask true dynamics, making a growing effect look flat. Using the Sun-Abraham estimator produces a clean plot that reflects the actual pattern of treatment effects.

[pause]

NARRATOR: Let me line up the estimates from our Shadow Surge example. The naive TWFE estimate is six point five percentage points. The Callaway-Sant'Anna estimate is eight point one. The Sun-Abraham estimate is eight point zero. The true average treatment effect is eight point one. The modern estimators all recover the truth, up to minor sampling variation. TWFE is biased downward by about twenty percent because of contamination from the already-treated comparisons.

And remember, this is a relatively mild case. In settings with more dramatic heterogeneity -- where early-treated units have very large effects and later-treated units have small effects, or where effects grow steeply over time -- the TWFE bias can be devastating.

SABRINA: The lesson is this. In a staggered setting, always run the Goodman-Bacon decomposition to check for problematic comparisons. And always use a heterogeneity-robust estimator -- Callaway-Sant'Anna, Sun-Abraham, or one of the other modern alternatives -- for your primary analysis. The naive TWFE regression is a relic of a time when we did not understand what it was actually doing.

[pause]

NARRATOR: There are other modern estimators worth knowing about, even if I will not go into as much detail. Clement de Chaisemartin and Xavier D'Haultfouille showed that even in a simple two-period, two-group setting, the TWFE estimator can be decomposed into a weighted sum of individual-level treatment effects where some weights may be negative. Their estimator focuses on the instantaneous treatment effect at the moment of switching, comparing units whose treatment status changes to units whose status stays the same. This avoids contamination from dynamic effects entirely.

And Kirill Borusyak, Xavier Jaravel, and Jann Spiess proposed what they call the imputation estimator. The logic is transparent and elegant. First, fit the TWFE model using only untreated observations -- units that have not yet been treated, or are never treated. This gives you estimated fixed effects for each unit and each time period. Then, for each treated observation, use those fixed effects to predict what the outcome would have been absent treatment. The treatment effect is simply the gap between the observed outcome and this imputed counterfactual. Aggregate as desired. The imputation estimator is efficient and transparent, and it gives essentially the same answers as Callaway-Sant'Anna.

OAK: All of these methods share the same core principle: build the counterfactual using only genuinely untreated observations. Never use an already-treated unit as a control. The methods differ in their implementation details and their statistical properties, but the philosophy is the same.

[pause]

---

[TEACHING SECTION]

NARRATOR: Before we leave Part Two, I want to revisit the event study plot one more time, because it plays such a central role in applied work and because understanding it is essential.

Remember the picture. A horizontal timeline of periods relative to treatment. Dots at each period, each representing an estimated coefficient. Vertical lines through the dots representing confidence intervals. The period just before treatment is the reference point, set to zero.

Now imagine looking at this picture from a robust estimator -- Callaway-Sant'Anna or Sun-Abraham. In the pre-treatment region, the dots cluster near the horizontal zero line. They bounce around a little -- negative zero point zero one here, positive zero point zero two there -- but they are all small and their confidence intervals all overlap zero. This is the visual signature of parallel trends. The treated and control groups were not diverging before treatment.

Then, at event time zero, the dot jumps up. In our example, it lands at about seven percentage points. At event time one, it is eight points. Two, nine points. Three, ten. The dots trace out the dynamic treatment effect -- how the impact of Shadow Surge evolves over time as trainers learn to use it.

If instead you saw a steady upward drift in the pre-treatment dots -- the dots at negative five, negative four, negative three getting progressively further from zero -- that would be alarming. It would suggest that the treated and control groups were already diverging before treatment, which undermines the parallel trends assumption. And if you saw a sharp jump at event time negative one or negative two, that might suggest anticipation effects -- trainers changing behavior before the TM was officially released, perhaps because Silph announced it in advance.

The event study plot is not a formal test. It is a visual diagnostic. But it is arguably the single most important figure in any DiD analysis. If the pre-treatment dots are not near zero, the analysis is in trouble.

[pause]

---

## Part 3: Building a Doppelganger

[SCENE: A quiet room behind Sabrina's gym. Maps of Kanto cover the walls. Economic indicators are pinned above each city.]

NARRATOR: We have spent the first two parts of this chapter on difference-in-differences and its modern extensions. Now we turn to a fundamentally different problem. Team Rocket invaded Saffron City in Period Eight. They seized Silph Co. headquarters and disrupted the economic life of the entire city. We want to estimate the economic cost of this invasion.

But there is a challenge that DiD cannot easily address. The invasion affected only one city. There is no natural control group. No other Kanto city was invaded. And no single uninvaded city is a convincing stand-in for Saffron. Celadon is a commercial hub, but its industrial composition differs. Vermilion is a port city with different economic drivers. Cerulean relies on tourism. Each city is similar to Saffron in some ways but different in others.

SABRINA: When no single comparison exists, you must construct one. You must build a doppelganger.

[pause]

NARRATOR: The synthetic control method, developed by Alberto Abadie and his co-authors starting in two thousand three, does exactly this. Instead of picking one control city, it constructs a weighted combination of multiple untreated cities that together approximate what Saffron would have looked like in the absence of Team Rocket's invasion. This weighted combination is called Synthetic Saffron.

OAK: The metaphor I like is this. No single Pokemon can perfectly replicate the strengths of your Charizard. But perhaps a team of Arcanine, Gyarados, Vaporeon, and Golem comes very close in terms of stats and type coverage. Arcanine gets forty-two percent of the weight. Gyarados gets thirty-one percent. Vaporeon gets eighteen percent. Golem gets nine. If your Charizard suddenly loses a battle it should have won, and this team of substitutes performs normally, you know something happened specifically to Charizard -- it was not just bad luck affecting all Fire-types.

NARRATOR: That is the intuition. Let me walk through how it works.

[pause]

---

[TEACHING SECTION]

NARRATOR: We have seven potential donor cities -- every Kanto city except Saffron. The method works by finding a set of non-negative weights, one for each donor city, that sum to one. These weights are chosen so that the weighted average of the donor cities' pre-treatment characteristics matches Saffron's pre-treatment characteristics as closely as possible.

The pre-treatment characteristics typically include two kinds of things. First, the entire pre-treatment outcome trajectory -- the economic activity index for each donor city in each pre-treatment period. Matching on the full pre-treatment path is the most important requirement, because a synthetic control that tracked Saffron closely before the invasion provides a credible counterfactual for what would have happened after. Second, predictor variables -- observable characteristics like population, number of registered trainers, distance to the nearest port, and industrial composition. These help the method select donors that are structurally similar to Saffron.

The non-negativity constraint -- all weights must be zero or positive -- and the summing-to-one constraint serve an important purpose. They ensure that the synthetic control is an interpolation, not an extrapolation. You are combining existing cities in plausible proportions, not creating an impossible Frankenstein city with negative amounts of Cerulean and three hundred percent of Lavender.

[pause]

In our example, the optimization finds the following weights. Celadon gets forty-two percent -- it is the other major commercial center in Kanto, so it is no surprise that it carries the most weight. Vermilion gets thirty-one percent -- a port city with substantial economic activity. Cerulean gets eighteen percent -- a mid-sized city with tourism. Pewter gets nine percent. And Fuchsia, Cinnabar, and Lavender all get zero weight. They are too dissimilar to be useful.

Synthetic Saffron, then, is roughly forty-two percent Celadon, thirty-one percent Vermilion, eighteen percent Cerulean, and nine percent Pewter. Not a real city, but a data-driven composite that mirrors the real Saffron in the ways that matter.

Let me check the pre-treatment fit. Saffron's average economic activity in the pre-treatment period -- Periods One through Seven -- is eighty-seven point three. Synthetic Saffron's is eighty-six point eight. Close. Saffron's population is one hundred forty-five thousand. Synthetic Saffron's is one hundred forty-one thousand. Close. Saffron has two thousand three hundred forty registered trainers. Synthetic Saffron has two thousand two hundred ninety. Close. The match is excellent across the board.

And more importantly, the pre-treatment outcome trajectory of Synthetic Saffron closely tracks actual Saffron period by period. In Period One, Saffron is at eighty-five point two and Synthetic Saffron is at eighty-four point nine -- a gap of only zero point three. In Period Two, eighty-six point one versus eighty-five point eight. Period Three, eighty-six point eight versus eighty-six point five. All the way through Period Seven, eighty-eight point nine versus eighty-eight point six. The pre-treatment gaps are tiny -- always around zero point three or less. The doppelganger is a near-perfect match.

[pause]

And then comes the invasion.

In Period Eight, Saffron's economic activity drops to eighty-four point one. Synthetic Saffron -- which represents what Saffron would have looked like without the invasion -- continues upward to eighty-nine point one. The gap is negative five points. In Period Nine, Saffron falls further to eighty point five while Synthetic Saffron rises to eighty-nine point five. The gap widens to negative nine points. By Period Ten, Saffron is at seventy-eight point two and Synthetic Saffron is at eighty-nine point nine. Negative eleven point seven. Period Eleven: seventy-six point eight versus ninety point two. Negative thirteen point four. Period Twelve: seventy-seven point five versus ninety point six. Negative thirteen point one.

The estimated effect of Team Rocket's invasion is devastating. By Period Twelve, Saffron's economy is more than thirteen index points below where it would have been -- a decline of roughly fourteen and a half percent. The invasion did not just stop growth. It reversed it, sending the economy plummeting while the rest of Kanto continued to prosper.

SABRINA: The power of the synthetic control is that no single city told us this. Celadon alone would have given one counterfactual. Vermilion alone, another. Neither would have been convincing. But the weighted combination -- forty-two percent Celadon, thirty-one percent Vermilion, eighteen percent Cerulean, nine percent Pewter -- produces a composite that tracked Saffron almost perfectly for seven periods, then diverged sharply at the exact moment of invasion. That divergence is the causal effect.

[pause]

---

[TEACHING SECTION]

NARRATOR: There is a natural question at this point. How do we know this result is statistically meaningful? With only one treated city, we cannot compute standard errors in the usual way. There is no sampling distribution to appeal to. We have a single treated unit and a single estimated effect. How do we know it is not just noise?

The answer comes from placebo tests. The idea is simple and clever. You take the synthetic control method and apply it to every donor city in turn, pretending each one was the treated unit. You apply the same procedure to Celadon, pretending Celadon was invaded and using the remaining cities as donors. You do the same for Vermilion. For Cerulean. For Pewter. For every city in the donor pool.

For each of these placebo cities, you compute the post-treatment gap -- the difference between the city's actual outcome and its synthetic control's prediction. If the method is well-calibrated, these placebo gaps should be small, because the placebo cities were not actually treated. Any gap you see is just the noise inherent in the method -- the residual imperfection of the synthetic match.

Then you compare Saffron's gap to the distribution of placebo gaps. If Saffron's gap is much larger than any of the placebos, the effect is statistically significant. It is not just noise. Something real happened to Saffron.

A common refinement uses the ratio of post-treatment prediction error to pre-treatment prediction error for each city. A large ratio means the city had a small pre-treatment gap, meaning the synthetic match was good, but a large post-treatment gap, meaning something happened after the treatment date. A large ratio for Saffron, relative to the placebos, is strong evidence of a genuine treatment effect.

In our example, Saffron's ratio is thirty-eight point seven. The largest placebo ratio -- for Celadon -- is only four point two. Saffron's ratio dwarfs every placebo. The effect is unmistakable.

[pause]

OAK: There is one caveat. With only eight total cities, the smallest possible p-value from a pure permutation test is one divided by eight, which is zero point one two five. That is not significant at the conventional five percent level. This is not because the effect is small or uncertain -- it is because we simply do not have enough donor units to generate a fine-grained permutation distribution. With twenty or more donor units, a p-value of one divided by twenty, or zero point zero five, becomes achievable. This is a practical limitation of synthetic control in small donor pools.

NARRATOR: So synthetic control gives us a powerful way to estimate causal effects when there is only one treated unit, but it does have real limitations. You need a reasonable donor pool. The pre-treatment fit needs to be good. And inference is limited by the number of donors available for placebo tests.

[pause]

---

[TEACHING SECTION]

NARRATOR: Blue, of course, has tried his hand at synthetic control. And, of course, he has made a mistake.

BLUE: I built a synthetic control for Vermilion City to estimate the effect of the new port expansion. My synthetic Vermilion uses ninety-five percent Cinnabar Island and five percent Lavender Town. The pre-treatment fit is terrible -- the synthetic version is twenty points below real Vermilion in every period. But look at this. After the port expansion, the gap between Vermilion and the synthetic version grows by another eight points. That eight points is the effect of the expansion. Right?

OAK: Blue, your synthetic control does not resemble Vermilion at all. If your doppelganger cannot track the treated unit before treatment, there is no reason to trust it after treatment. A twenty-point gap in every pre-treatment period means your weighted combination of Cinnabar and Lavender is simply not a plausible stand-in for Vermilion. The post-treatment gap could reflect the treatment effect, or it could reflect the dozens of ways in which your synthetic control was always a poor match. You have no way to tell the difference.

SABRINA: A synthetic control is only as credible as its pre-treatment fit. If the doppelganger does not track the treated unit before the intervention, the method fails. Good pre-treatment fit is not a sufficient condition for a valid estimate, but it is a necessary one.

[pause]

NARRATOR: This brings us to practical recommendations for anyone using these methods. I want to walk through them carefully, because after everything we have covered, the question "which method should I use?" deserves a clear answer.

First, always start with the raw data. Before running any regression or constructing any synthetic control, plot the outcome time series for each unit. Look at the trends. Look for obvious violations of parallel trends. Look for outliers, structural breaks, or compositional changes. The plot will tell you more than any regression table.

Second, if you have multiple treated and control units observed over time, difference-in-differences is your starting point. But if treatment adoption is staggered -- if different units receive treatment at different times -- do not rely on naive two-way fixed effects. Run the Goodman-Bacon decomposition as a diagnostic. Check the weight on already-treated-as-control comparisons. And use a heterogeneity-robust estimator -- Callaway-Sant'Anna, Sun-Abraham, or the imputation estimator -- for your primary analysis.

Third, always report the event study plot from a robust estimator. Not from a naive TWFE regression. The robust event study gives you the correct picture of pre-treatment trends and post-treatment dynamics.

Fourth, if you have a single treated unit and no obvious control, synthetic control is the way forward. But make sure your pre-treatment fit is excellent. If the synthetic control does not track the treated unit before treatment, the post-treatment estimates are not credible. Run placebo tests to assess statistical significance, and be honest about the limitations imposed by a small donor pool.

Fifth, be explicit about your identifying assumptions. For DiD, that means stating the parallel trends assumption clearly and providing evidence for or against it. For synthetic control, that means showing the pre-treatment fit and discussing why the donor pool is appropriate.

OAK: And above all, remember that these methods are complements, not substitutes. DiD works best when you have multiple treated and control units with plausible parallel trends. Synthetic control works best when you have a single treated unit and a good donor pool. In some cases, you might use both -- DiD for the multi-unit analysis and synthetic control as a robustness check for a key case.

[pause]

---

[TEACHING SECTION]

NARRATOR: Before we leave Saffron City, let me mention some frontier extensions that push these methods even further.

The first is augmented synthetic control, developed by Eli Ben-Michael, Avi Feller, and Jesse Rothstein. Standard synthetic control can struggle when no weighted combination of donor units closely matches the treated unit's pre-treatment path. The augmented version adds a bias correction based on an outcome model. If the standard synthetic control achieves a perfect match, the correction is zero and you get the same answer. If the match is imperfect, the outcome model fills the gap. It is doubly robust in spirit -- consistent if either the synthetic control provides a good match or the outcome model is correctly specified.

The second is synthetic difference-in-differences, proposed by Dmitry Arkhangelsky, Susan Athey, David Hirshberg, Guido Imbens, and Stefan Wager. This estimator elegantly combines the strengths of DiD and synthetic control. Standard DiD uses equal weights on all control units but requires parallel trends. Standard synthetic control uses optimized unit weights but does not adjust for time trends. Synthetic DiD uses both -- optimized unit weights like synthetic control, and optimized time weights that upweight pre-treatment periods most similar to the post-treatment period. In simulations, it tends to have lower variance than synthetic control and lower bias than DiD.

And the third is matrix completion, which treats the causal inference problem as a missing data problem. Arrange the panel data as a matrix with units as rows and time periods as columns. The treated observations are missing in the sense that we observe the outcome under treatment but want the outcome under no treatment. Under the assumption that the matrix of untreated potential outcomes has low rank -- meaning outcomes are driven by a small number of underlying factors -- techniques from the matrix completion literature can fill in the missing entries. This approach nests both DiD and synthetic control as special cases.

These are active areas of research. The toolkit continues to grow. But the core principles remain the same: build credible counterfactuals, use only valid comparisons, and be transparent about your assumptions.

[pause]

SABRINA: You have learned to see across time. You have learned to build a counterfactual from thin air. And you have learned that even the most trusted tools can deceive you when the world is more complex than the model assumes. The Marsh Badge is yours.

---

## Chapter Summary

[SCENE: Outside the Saffron Gym. Evening light. The city is quieter now.]

NARRATOR: Let me pull everything together. We covered an enormous amount of ground in Saffron City, and I want the key ideas to be crystal clear.

[pause]

First, difference-in-differences. The core idea is simple: take the change over time in the treated group and subtract the change over time in the control group. The first difference removes time-invariant characteristics of the treated group. The second difference removes common time trends. What remains is the treatment effect. In the two-by-two case with two groups and two periods, this reduces to a single number: treated change minus control change. In our Shadow Surge example, that was thirteen percentage points minus four percentage points, giving nine percentage points.

Second, the parallel trends assumption. This is the identifying assumption for all DiD analyses. It states that in the absence of treatment, the treated and control groups would have followed the same trend over time. The assumption is about trends, not levels -- the groups can start at different points, as long as they would have changed at the same rate. Parallel trends is fundamentally untestable, but event study plots provide a crucial diagnostic by checking whether pre-treatment trends were parallel.

Third, two-way fixed effects regression. In the simple two-by-two setting, TWFE is identical to DiD. But in staggered settings -- where different units receive treatment at different times -- TWFE can be severely biased. The bias arises because TWFE implicitly uses already-treated units as controls, generating what we called forbidden comparisons. When treatment effects are heterogeneous, these comparisons can pull the estimate in the wrong direction.

Fourth, the modern DiD revolution. The Goodman-Bacon decomposition reveals the source of TWFE bias by breaking the estimate into its component two-by-two comparisons. Modern estimators -- Callaway and Sant'Anna, Sun and Abraham, de Chaisemartin and D'Haultfouille, Borusyak, Jaravel, and Spiess -- avoid the forbidden comparison entirely. They estimate treatment effects using only genuinely untreated observations as controls, producing clean, interpretable estimates even with heterogeneous effects and staggered adoption.

Fifth, the event study plot. This is a graph of estimated treatment effects at each period relative to treatment. Pre-treatment coefficients should hover near zero if parallel trends holds. Post-treatment coefficients trace out the dynamic effect. Always produce this plot from a robust estimator, not from naive TWFE, which can show spurious patterns.

Sixth, the synthetic control method. When only one unit is treated and no single control unit is a convincing match, synthetic control constructs a weighted combination of untreated donor units that approximates the treated unit's pre-treatment characteristics. The weights are non-negative and sum to one, ensuring the counterfactual is an interpolation, not an extrapolation. The treatment effect is the gap between the treated unit's actual outcome and the synthetic control's prediction in each post-treatment period.

Seventh, inference for synthetic control. With only one treated unit, standard confidence intervals are not available. Instead, researchers use placebo tests -- applying the same method to each donor unit in turn and comparing the treated unit's gap to the distribution of placebo gaps. The resolution of the permutation distribution is limited by the number of donors.

And eighth, practical guidance. Always plot the raw data first. Use the Goodman-Bacon decomposition as a diagnostic. Use heterogeneity-robust estimators for staggered DiD. Ensure excellent pre-treatment fit for synthetic control. Report robust event study plots. Be explicit about identifying assumptions.

[pause]

NARRATOR: I step out of the Saffron Gym with six badges on my jacket and Sabrina's words echoing in my mind. I have learned to see across time, to difference out confounders, to build counterfactuals from weighted combinations of the observed world. And I have learned that even the most elegant tools can deceive when the world is more complex than the model assumes. The TWFE trap is a lesson I will not forget.

Ahead lies the final stretch. Victory Road leads to the Indigo Plateau, where the Elite Four await. Each champion guards a frontier of causal inference: mediation analysis reveals the mechanisms through which causes operate. Heterogeneous treatment effects uncover for whom treatments work best. Sensitivity analysis probes the robustness of our conclusions to hidden bias. And interference -- the bane of SUTVA -- forces us to confront a world where one unit's treatment affects another's outcome.

The path is steep. But the summit offers a commanding view of the entire causal landscape.

[pause]

---

## Comprehension Check

NARRATOR: Before we leave Saffron City, check yourself on these questions.

First: Why does the DiD estimator require two differences rather than one? What specific type of bias does each difference eliminate?

[long pause]

The first difference -- within the treated group, over time -- eliminates the permanent level of the treated group's outcome. It removes time-invariant characteristics like geography, wealth, or infrastructure that make the treated group permanently different from the control. The second difference -- subtracting the control group's change over time -- eliminates common temporal trends that affect both groups equally, such as seasonal effects or region-wide economic changes. Together, the two differences isolate the treatment effect by removing both sources of bias. A single before-and-after comparison within the treated group would include the common time trend. A single post-treatment comparison across groups would include the pre-existing gap.

Second: State the parallel trends assumption in plain English. Is it testable? What is the best available diagnostic?

[long pause]

The parallel trends assumption says that in the absence of treatment, the treated and control groups would have followed the same trend over time. Not the same level -- just the same trend. It is fundamentally untestable because it involves a counterfactual: what the treated group would have done without treatment, which we can never observe. The best available diagnostic is the event study plot, which checks whether the two groups were on parallel paths before treatment. If pre-treatment coefficients are near zero, that is consistent with parallel trends. But even perfect pre-trends do not guarantee the assumption holds in the post-treatment period.

Third: Explain the forbidden comparison problem in staggered DiD. Why does using already-treated units as controls cause bias?

[long pause]

When treatment arrives at different times, the standard TWFE regression implicitly uses already-treated units as controls for newly-treated units. If treatment effects grow over time -- if early-treated units are still experiencing increasing effects -- their rising outcomes make newly-treated units look worse by comparison. The already-treated unit's outcome includes both its baseline trend and its evolving treatment effect. Using it as a control attributes the evolving treatment effect to the baseline, which contaminates the comparison. This can cause the TWFE estimate to be too small, too large, or even the wrong sign.

Fourth: What is the synthetic control method, and how does it differ from DiD?

[long pause]

The synthetic control method constructs a weighted combination of untreated donor units that closely matches the treated unit's pre-treatment characteristics and outcome trajectory. The weights are non-negative and sum to one, ensuring the counterfactual is an interpolation. The treatment effect is the gap between the treated unit's actual post-treatment outcome and the synthetic control's prediction. DiD compares groups that already exist in the data, using parallel trends to justify the comparison. Synthetic control builds a comparison from scratch, using pre-treatment fit to justify the counterfactual. DiD works best with multiple treated and control units. Synthetic control works best with a single treated unit and a good donor pool.

Fifth: How do you conduct inference for synthetic control when there is only one treated unit?

[long pause]

You use placebo tests. Apply the same synthetic control procedure to each donor unit in turn, pretending each one was treated. For each placebo, compute the post-treatment gap between the unit's actual outcome and its synthetic control's prediction. Compare the real treated unit's gap to the distribution of placebo gaps. If the treated unit's gap is much larger than any placebo's, the effect is statistically significant. The resolution of this test is limited by the number of donor units -- with only eight units, the smallest possible p-value is one over eight, or zero point one two five.
