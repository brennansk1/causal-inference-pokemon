---
title: "Chapter 2: Pewter City -- Randomized Experiments"
chapter_number: 2
source_file: "textbook/chapters/ch02_pewter_city.md"
estimated_runtime_minutes: 70
key_concepts:
  - Randomized Controlled Trials (RCTs)
  - Independence of Potential Outcomes and Treatment
  - Balance Tables
  - Self-Selection Bias
  - Power Analysis
  - Stratified (Block) Randomization
  - Blinding (Single, Double, Triple)
  - SUTVA (Stable Unit Treatment Value Assumption)
  - Neyman Variance Estimation
  - Confidence Intervals and Hypothesis Testing
  - Regression Adjustment (Lin 2013)
  - Internal vs External Validity
  - Noncompliance and Intent-to-Treat
  - Instrumental Variables / LATE Preview
  - Attrition
  - Hawthorne Effect
  - Fisher Randomization Inference
  - Fisher vs Neyman Frameworks
  - Ethics of Experimentation
characters:
  - NARRATOR (trainer, first-person, curious and conversational)
  - OAK (professor, patient teacher, plain-English definitions)
  - BLUE (rival, confident, makes causal reasoning errors)
  - NURSE JOY (data-driven, skeptical but open-minded)
  - BROCK (gym leader, methodical, follows a fixed battle script)
---

# Chapter 2: Pewter City -- Randomized Experiments

## Part 1: The Coin Flip That Changes Everything

[SCENE: Rocky terrain outside Pewter City. Gravel crunching underfoot. The distant sound of a Pokemon battle echoing from the gym.]

NARRATOR: Viridian City is behind me. Route Two was short but steep, and as the path levels out, I see Pewter City laid out ahead -- a modest settlement carved into the rocky landscape, built around the famous Pewter City Gym. That is where Brock trains, the Rock-type specialist. Every new trainer who passes through Kanto has to face him eventually. His Geodude and his Onix have crushed more dreams than any other first gym leader in the region.

But before I challenge Brock, there is a scientific dispute to settle. One that will teach me why a simple coin flip is the most powerful tool in all of causal inference.

[pause]

I push through the doors of the Pewter City Pokemon Center. Inside, the place is buzzing. Trainers are everywhere -- some celebrating victories, others slumped in chairs with fainted Pokemon in their laps. And at the front desk, Nurse Joy is in the middle of what looks like a very heated argument.

NURSE JOY: I have had it. For three weeks now, every trainer who walks through that door has an opinion about Pewter Protein. "It definitely works." "It is a total scam." Everyone has an anecdote. Nobody has evidence.

NARRATOR: A trainer near the counter flexes his Machop's arm.

TRAINER: My Charmander hit twenty percent harder after one dose. You cannot argue with results.

NARRATOR: Another trainer, nursing a wounded Pidgey, shakes his head.

TRAINER TWO: I took it and Brock's Onix still destroyed me. Waste of money.

NARRATOR: Nurse Joy pulls up her logbook. She has been recording outcomes for every trainer who has come through her doors -- whether they took Pewter Protein, what Pokemon they used, whether they beat Brock, and how much damage they dealt. She has data. Plenty of it.

NURSE JOY: Here is the problem. Trainers who choose to buy Pewter Protein tend to be wealthier, more experienced, and more likely to already have a Water-type or Grass-type Pokemon -- the types that are super effective against Brock's Rock-types. So when they win, I cannot tell if they won because of the Protein, or because they were going to win anyway.

NARRATOR: The data is confounded. The very thing we learned about in Pallet Town -- that confounders create misleading associations -- is playing out right here in the Pokemon Center lobby. The trainers who self-select into buying Protein are systematically different from the trainers who do not buy it. Any simple comparison of their outcomes mixes together the real effect of the supplement with all of those pre-existing differences.

[pause]

That is when the door opens and Professor Oak walks in, lab coat slightly rumpled from the road.

OAK: Nurse Joy. I got your message. You said you needed a research consultation.

NURSE JOY: Professor, I have three weeks of data and I still cannot answer the most basic question: does Pewter Protein actually work?

OAK: You do not need more data, Nurse Joy. You need better data. You need a randomized controlled trial.

---

[TEACHING SECTION]

NARRATOR: Professor Oak reaches into his pocket and pulls out a coin. It is a Poke-coin -- Magikarp on one side, Gyarados on the other. He sets it on the counter.

OAK: Here is what we are going to do. For the next two hundred trainers who register for a Brock challenge, you flip this coin. Magikarp: the trainer gets the real Pewter Protein. Gyarados: they get an identical-looking Placebo Berry -- same size, same color, same taste, but no active ingredient. You do not tell them which one they received.

NURSE JOY: That is it? A coin flip decides who gets what?

OAK: That is the most powerful tool in all of causal inference.

[pause]

[OAK EXPLAINS: Why Randomization Works]

NARRATOR: Let me unpack what Professor Oak is proposing, because it sounds almost too simple to be meaningful. In Chapter One, we learned that every trainer has two potential outcomes. There is the outcome they would experience if they received Pewter Protein -- the treatment -- and the outcome they would experience if they received the Placebo Berry -- the control. The individual causal effect is the difference between those two potential outcomes. And the Average Treatment Effect, or ATE, is the average of that difference across the entire population.

The Fundamental Problem of Causal Inference tells us we can never observe both potential outcomes for the same trainer. We only see the one that corresponds to what they actually received. So when we compare the average outcomes of the treatment group to the control group, we need to ask: does that comparison actually give us the ATE?

From Chapter One, we know the naive comparison gives us two things added together. First, there is the actual treatment effect on the treated. Second, there is the selection bias -- the difference in baseline outcomes between the groups. In an observational setting, that selection bias is generally not zero. But under random assignment, something remarkable happens.

OAK: When we assign treatment with a coin flip, we create a situation where the treatment assignment is statistically independent of the potential outcomes. That is the key condition. It means that the kind of person who ends up in the treatment group is, on average, identical to the kind of person who ends up in the control group. Not because we matched them, not because we adjusted for differences, but because the coin does not know anything about them.

NARRATOR: Think about what the coin does not know. It does not know whether a trainer has a Water-type Pokemon, which would be devastating against Brock's Rock-types. It does not know the trainer's experience level, their number of gym badges, or their secret training regimen in Mt. Moon. It does not even know things that we could never measure -- like the trainer's natural battle instinct, their Pokemon's hidden Individual Values, or whether they had a good night's sleep. The coin is perfectly ignorant. And that perfect ignorance is what makes it so powerful.

When treatment assignment is independent of potential outcomes, the selection bias term vanishes. It becomes zero. And the simple difference in group averages gives us exactly the Average Treatment Effect. No regression needed. No fancy adjustment. Just a coin flip and a subtraction.

[pause]

OAK: Let me say that again, because this is the single most important idea in this chapter. Under random assignment, the difference in group means is an unbiased estimator of the causal effect. This is why the randomized controlled trial is called the gold standard. It is the only method in this entire textbook that balances both observed and unobserved confounders.

NARRATOR: In other words, every observational method we will encounter in the chapters to come -- matching, regression, difference-in-differences, instrumental variables, regression discontinuity -- every single one of them can only address confounders that we can observe or that have specific structural properties. Randomization handles all of them. Observed and unobserved. Known and unknown. That is its unique power.

[OAK EXPLAINS: Why "In Expectation" Matters]

OAK: Now, I need to add an important caveat. Randomization does not guarantee that the treatment and control groups are perfectly balanced in any single experiment. If you flip two hundred coins, you might get a hundred and five heads and ninety-five tails. By chance, the treatment group might end up with slightly more Water-type trainers. But the expected distribution is balanced. And with a large enough sample, deviations from perfect balance become small and quantifiable. We will make this precise later when we discuss variance estimation.

NARRATOR: So randomization guarantees balance on average, across all possible randomizations. Any single randomization might be slightly off, but we can measure how far off it is and account for that in our analysis. That is the beauty of the approach.

---

[SCENE: Nurse Joy's desk at the Pokemon Center. She has her logbook open and is reviewing the enrollment data.]

NARRATOR: Nurse Joy runs the trial. Two hundred trainers walk through the doors over the next several weeks. Each one receives their coin-flip assignment. After enrollment is complete, she compiles what is called a balance table -- a comparison of pre-treatment characteristics across the two groups -- to check whether the randomization actually achieved approximate balance.

She calls me over to look at the numbers.

NURSE JOY: One hundred and two trainers ended up in the Protein group, and ninety-eight in the Placebo group. Here is what the two groups look like before treatment.

NARRATOR: The average trainer level in the Protein group is fourteen point eight. In the Placebo group, it is fourteen point three. A difference of just half a level -- statistically indistinguishable, with a p-value of zero point five two.

NURSE JOY: Twenty-eight point four percent of Protein trainers have a Water-type Pokemon. In the Placebo group, it is twenty-six point five percent. A gap of less than two percentage points.

NARRATOR: The same pattern holds across the board. Percentage with Grass-type Pokemon? Fifteen point seven versus seventeen point three -- tiny difference, not significant. Average number of Pokemon on the team? Three point eight versus three point nine. Prior gym badges? Zero point nine versus zero point eight. Percentage of first-time challengers? Sixty-one point eight versus sixty-four point three. Average Pokemon level? Thirteen point two versus twelve point nine.

None of the differences between the groups come anywhere close to statistical significance. The groups look comparable on every dimension Nurse Joy measured. The randomization worked.

OAK: And remember -- even if one or two of these characteristics had shown a statistically significant imbalance by chance, that would not invalidate the experiment. When you run multiple comparisons at a five percent significance level, you expect roughly one in twenty to come up significant purely by luck. What would be concerning is a systematic pattern of large imbalances across many variables, which would suggest a problem with the randomization procedure itself.

[pause]

[BLUE'S MISTAKE]

NARRATOR: Right as Nurse Joy is reviewing her balance table, the Pokemon Center doors burst open. Blue strides in, arms full of shopping bags.

BLUE: Hey losers. I already know Pewter Protein works. I have been using it for a week and my Squirtle is destroying everything. I do not need some nerdy experiment to tell me what is obvious.

OAK: Blue, you chose to buy Protein because you are wealthy, experienced, and you already have a Water-type starter -- the perfect counter to Brock's Rock-types. Trainers like you would have won anyway. Your personal experience tells us nothing about whether the Protein itself had any effect.

NARRATOR: And the data proves Oak right. Among trainers who voluntarily purchased Pewter Protein -- trainers like Blue who self-selected into using it -- the win rate against Brock is seventy-eight percent. Among trainers who did not buy it, the win rate is only forty-five percent. That is a thirty-three percentage point gap, and it is exactly the kind of number that makes people like Blue say "See? It works!"

But Nurse Joy's randomized trial tells a different story. In the trial, where assignment was determined by a coin flip rather than by personal choice, the win rate is fifty-two percent in the Protein group and forty-three percent in the Placebo group. A nine percentage point difference. The true effect of Pewter Protein exists, but it is much smaller than Blue's naive comparison suggests.

OAK: The gap between Blue's estimate of thirty-three percentage points and the experimental estimate of nine percentage points -- a difference of twenty-four percentage points -- is pure selection bias. That is how much Blue's number was inflated by the fact that stronger trainers chose to buy Protein. This is exactly the danger we warned about in Chapter One: drawing causal conclusions from observational data without proper adjustment.

NARRATOR: Blue shrugs and walks away. He does not care about selection bias. He is too busy being confident. But for the rest of us, this comparison between the naive observational estimate and the clean experimental estimate is one of the most vivid demonstrations of why randomized experiments matter. The truth was buried under twenty-four percentage points of confounding, and only the coin flip dug it out.

---

## Part 2: Designing and Analyzing the Experiment

[SCENE: Professor Oak's makeshift research office in the back of the Pokemon Center. Papers spread across the desk. A whiteboard with diagrams.]

NARRATOR: A randomized experiment does not design itself. The coin flip is the heart of the method, but an enormous amount of thought has to go into the architecture surrounding that flip. Professor Oak walks me through the key decisions he and Nurse Joy made when planning the trial.

[TEACHING SECTION]

[OAK EXPLAINS: Precise Treatment Definition]

OAK: The first rule of experimental design is that a vague treatment yields vague conclusions. "Pewter Protein" could mean many things -- different doses, different timings, different formulations. We had to nail down exactly what we were testing.

NARRATOR: Here is what they settled on. The treatment arm was exactly one tablet of Pewter Protein, ten milligrams, from Lot one fifty-one manufactured by Silph Co., administered orally with two hundred milliliters of water, exactly sixty minutes before the trainer's scheduled Brock battle. The control arm was exactly one Placebo Berry tablet, identical in size -- eight millimeters in diameter -- identical in color, weight, and taste, administered under the exact same conditions. Both were given by Nurse Joy, in a private room, following a standardized script.

OAK: This precision matters for three reasons. First, replicability -- another researcher in Cerulean City could run the same experiment with the same treatment. Second, it anchors the causal estimand: we are estimating the effect of this specific intervention, not "supplements in general." Third, it supports blinding -- trainers cannot distinguish treatment from control.

[pause]

NARRATOR: For the outcome, Nurse Joy had several options. She could measure whether the trainer beat Brock -- a simple yes-or-no binary outcome. She could measure total damage dealt to Brock's Pokemon -- a continuous measure with more granularity. She could count the number of turns it took to win, or how many of the trainer's Pokemon were still standing at the end. Each measure captures something different.

She chose total damage dealt as the primary outcome and beat Brock as a secondary outcome. The continuous measure provides more statistical power -- meaning she can detect smaller effects -- while the binary win-or-lose measure is what trainers actually care about.

OAK: Critically, we declared these choices before we analyzed the data. We pre-registered them. This prevents the temptation to run multiple analyses after the fact and cherry-pick the most favorable result -- a practice known as p-hacking or specification searching. If you test enough outcomes, something will be significant by chance. Pre-registration holds you accountable to the question you set out to answer.

[pause]

[OAK EXPLAINS: Power Analysis]

NARRATOR: Before enrolling a single trainer, Professor Oak insisted on a power analysis. This is the step where you figure out whether your planned sample size is large enough to actually detect a meaningful effect, if one exists.

OAK: Statistical power is the probability of correctly detecting a real treatment effect. If the power of your study is too low, you might run the entire experiment and come back with an inconclusive result -- not because the treatment does not work, but because you did not have enough data to see it. A power analysis forces you to think carefully about this before you start.

NARRATOR: The way it works is this. You need four ingredients. First, you pick a significance level -- the threshold for calling a result statistically significant. The conventional choice is five percent, or zero point zero five. Second, you pick a power level -- the probability of detecting the effect. The convention is eighty percent, meaning you want an eighty percent chance of catching a real effect. Third, you need an estimate of how variable the outcome is -- how spread out the damage numbers are from trainer to trainer. Oak estimated a standard deviation of thirty-five HP in both groups, based on pilot data from Viridian City. Fourth, you need the minimum detectable effect -- the smallest effect you would consider practically meaningful.

OAK: That last piece is the most important. A power analysis forces you to think about what effect size would actually matter. If Pewter Protein only adds two HP of damage -- less than a single Scratch attack -- no trainer would care, even if we could prove it was statistically significant. We powered this study to detect a fifteen HP difference, because that is roughly the damage from one extra Tackle attack, which could plausibly swing a close battle.

NARRATOR: When Oak plugged all of those numbers into the formula -- the significance level, the desired power, the standard deviation, and the minimum detectable effect -- the calculation said they needed approximately eighty-six trainers per group, or one hundred seventy-two total. Oak rounded up to two hundred to provide a buffer for dropout and to push the power up to about eighty-seven percent. The lesson here is that two hundred was not a number pulled from thin air. It was a number justified by the question: how many trainers do we need to have a good shot at detecting a meaningful effect?

OAK: Always think about practical significance, not just statistical significance. A tiny effect that is statistically significant is not necessarily worth caring about. And a large sample that detects a trivial effect has not told you anything useful.

---

[TEACHING SECTION]

[OAK EXPLAINS: Stratified Randomization]

NARRATOR: Pure coin-flip randomization is simple and valid, but Professor Oak wanted to make it more efficient. Nurse Joy had noticed that the single strongest predictor of how a trainer performs against Brock is whether they have a Water-type or Grass-type Pokemon. Those types are super effective against Rock, and they make a huge difference in battle outcomes. If, by pure chance, more of those trainers ended up in one group, the estimate would be noisier than necessary.

OAK: The solution is called stratified randomization, sometimes called block randomization. Instead of one big coin-flip for all two hundred trainers, we divide them into groups -- called strata or blocks -- based on important pre-treatment characteristics, and then we randomize separately within each group.

NARRATOR: For this trial, Nurse Joy created two blocks. Block A was trainers with a type advantage -- those who had at least one Water or Grass-type Pokemon. There were seventy-eight of them, and she assigned exactly thirty-nine to Protein and thirty-nine to Placebo. Block B was trainers without a type advantage -- one hundred twenty-two trainers, with sixty-one assigned to each group. The total came to two hundred trainers, one hundred in each arm, perfectly balanced on the single most important predictor of the outcome.

OAK: Within each block, treatment and control are exactly balanced on the blocking variable. This eliminates one source of sampling variability and improves precision. The efficiency gain is proportional to how strongly the blocking variable predicts the outcome. Since type advantage is a powerful predictor of damage dealt against Brock, this was a significant improvement over simple randomization.

NARRATOR: Importantly, stratified randomization does not compromise the fundamental independence condition. Within each stratum, treatment assignment is still random and independent of potential outcomes. The overall treatment effect is estimated as a weighted average of the within-stratum effects, where each stratum's weight reflects its share of the total sample.

[pause]

Professor Oak also explained why they did not use cluster randomization -- where you randomize entire groups, like all trainers at one Pokemon Center getting Protein and all trainers at another getting Placebo. That approach makes sense when individual randomization is logistically impossible, but it comes with a serious cost. Trainers within the same cluster tend to be similar to each other -- they trained in the same area, faced similar wild Pokemon, might even know each other. That similarity means adding more trainers within a cluster gives diminishing returns, and the effective sample size can drop dramatically. For this trial, since all trainers were visiting the same Pokemon Center in Pewter City, individual randomization was feasible and far more efficient.

[OAK EXPLAINS: Blinding]

OAK: Blinding prevents what we call expectation effects -- changes in behavior caused by knowing your treatment status rather than by the treatment itself. We implemented double-blinding. The trainers do not know which tablet they received -- the Protein and the Placebo look, taste, and smell identical. And Brock does not know either. He battles every challenger with the same team, Geodude and Onix, using the same strategy. He has no idea which trainers received Protein.

NARRATOR: There is also triple-blinding, where even the person analyzing the data does not know which group is which. In this trial, Nurse Joy recorded outcomes, but the treatment codes were not unblinded until after the primary analysis was locked in. An independent statistician -- one of Oak's research assistants -- handled the analysis using coded data.

The purpose of all this blinding is to prevent subtle biases. If a trainer knows they got the real Protein, they might battle more aggressively, and any improvement could be due to confidence rather than chemistry. If Brock somehow knew which trainers had the supplement, he might battle them differently. Blinding eliminates these contaminating channels.

---

[SCENE: The data is in. Nurse Joy and Professor Oak are gathered around the analysis printout.]

[TEACHING SECTION]

NARRATOR: The trial is complete. Every trainer has battled Brock. Every outcome has been recorded. Now it is time to look at the results, and I want to walk through this step by step, because the analysis of a randomized experiment is one of the most elegant procedures in all of statistics.

Nurse Joy has summary statistics for both groups. In the Protein group, one hundred trainers dealt an average of one hundred forty-two point seven HP of total damage to Brock's Pokemon, with a standard deviation of thirty-six point two HP. In the Placebo group, one hundred trainers dealt an average of one hundred twenty-eight point four HP, with a standard deviation of thirty-three point eight HP.

OAK: Step one is the point estimate. We simply subtract the control group average from the treatment group average. One hundred forty-two point seven minus one hundred twenty-eight point four gives us fourteen point three HP. That is our estimated treatment effect. Pewter Protein appears to increase total damage dealt by about fourteen point three hit points.

NARRATOR: But how confident should we be in that number? It is based on a sample, and samples are noisy. If Nurse Joy ran the same experiment again with a different set of two hundred trainers, she would get a somewhat different estimate. The standard error tells us how much our estimate would typically bounce around across these hypothetical repetitions.

OAK: Step two is the standard error. We compute it by taking the sample variance in the treatment group -- that is the standard deviation squared, thirty-six point two squared, which gives us one thousand three hundred ten point four four -- and dividing by the treatment group size of one hundred. Then we do the same for the control group: thirty-three point eight squared gives us one thousand one hundred forty-two point four four, divided by one hundred. We add those two numbers together -- thirteen point one zero plus eleven point four two gives us twenty-four point five three -- and take the square root. The standard error is four point nine five HP.

NARRATOR: So our estimate of fourteen point three HP has a standard error of four point nine five HP. The estimate is nearly three times its standard error, which is a good sign -- it means the signal is large relative to the noise.

OAK: Step three is the confidence interval. We take our point estimate and add and subtract one point nine six times the standard error. One point nine six times four point nine five is nine point seven. So the ninety-five percent confidence interval runs from fourteen point three minus nine point seven, which is four point six, up to fourteen point three plus nine point seven, which is twenty-four point zero.

NARRATOR: In plain English: we are ninety-five percent confident that the true effect of Pewter Protein on total damage dealt lies somewhere between four point six and twenty-four point zero HP. The entire interval is above zero, which means we can be quite confident that the effect is positive -- Protein really does something.

OAK: Step four is the formal hypothesis test. The test statistic is the point estimate divided by the standard error: fourteen point three divided by four point nine five gives us two point eight nine. For a two-sided test, the p-value corresponding to a test statistic of two point eight nine is zero point zero zero four. At the conventional significance level of five percent, we reject the null hypothesis of no treatment effect.

[pause]

NARRATOR: Let me put this all together in plain language. Pewter Protein increases the total damage a trainer deals to Brock's Pokemon by an estimated fourteen point three HP. The ninety-five percent confidence interval runs from four point six to twenty-four point zero HP. The result is statistically significant, with a p-value of zero point zero zero four. And it is practically meaningful -- fourteen point three HP is roughly equivalent to one additional Tackle attack, which could turn a close loss into a win.

For the secondary outcome -- whether the trainer actually beat Brock -- the win rate was fifty-two percent in the Protein group versus forty-three percent in the Placebo group. That is a nine percentage point difference. But the confidence interval for this binary outcome was wider, running from negative one point eight to positive nineteen point eight percentage points, and the p-value was zero point one zero -- not quite statistically significant at the five percent level. This is a lesson in why outcome choice matters for statistical power. A binary win-or-lose variable carries less information than a continuous damage variable. The continuous outcome detected the effect clearly; the binary outcome saw the same pattern but could not nail it down with enough precision.

---

[TEACHING SECTION]

[OAK EXPLAINS: Regression Adjustment]

NARRATOR: Can we do even better than the simple difference in means? The answer is yes, without sacrificing the unbiasedness guarantee that randomization provides.

OAK: A researcher named Winston Lin published a paper in two thousand thirteen that proposed a specific regression approach for analyzing randomized experiments. The idea is straightforward. You take your outcome and regress it on the treatment indicator, plus your pre-treatment covariates, plus the interaction between treatment and those covariates. The interaction term is critical -- it allows the relationship between covariates and the outcome to differ across treatment and control groups.

NARRATOR: What this regression does is soak up residual variation in the outcome -- variation that is not related to the treatment but that adds noise to the estimate. Since randomization balanced the covariates across groups in expectation, including them in the model cannot introduce bias. But it can reduce the standard error by explaining away some of the outcome variation.

OAK: For the Pewter Protein trial, Nurse Joy included the covariates from her balance table: trainer level, number of Pokemon, whether the trainer had a Water or Grass-type, and prior gym badges. The regression-adjusted estimate came out to fourteen point eight HP -- barely different from the unadjusted estimate of fourteen point three. That is reassuring, because a large change would have suggested the groups were not well balanced. But the standard error shrank from four point nine five to three point nine one -- a twenty-one percent reduction. The confidence interval narrowed to seven point one to twenty-two point five HP, and the p-value dropped to zero point zero zero zero two.

NARRATOR: The intuition is simple. The type of Pokemon a trainer has strongly predicts how much damage they deal. But since randomization balanced this variable across groups, including it in the model just removes noise from the estimate -- like putting on noise-canceling headphones so you can hear the signal more clearly.

[pause]

[BLUE'S MISTAKE]

NARRATOR: Blue reappears at the worst possible moment, having apparently been eavesdropping from the hallway.

BLUE: Hold on. If the experiment worked, why are you running a fancy regression? Sounds like you are just torturing the data until it tells you what you want to hear.

OAK: Actually, Blue, it is the opposite. In a randomized experiment, covariate adjustment cannot introduce bias -- the covariates are already balanced in expectation. All it does is reduce noise. Think of it like tuning a radio to get a clearer signal. The signal -- the treatment effect -- stays the same. The static gets quieter.

NARRATOR: Blue's instinct that regression adjustments can be dangerous is not entirely wrong -- in observational studies, poorly specified regressions can absolutely introduce bias. But in a well-run randomized experiment, the situation is different. Lin's method has the special property that it is at least as precise as the unadjusted difference in means, and it stays unbiased regardless of whether the regression model is correctly specified. It is strictly an improvement.

---

## Part 3: Threats, Limits, and Deeper Inference

[SCENE: Late evening at the Pokemon Center. Most trainers have left. Nurse Joy, Professor Oak, and Brock are reviewing the trial results over coffee.]

NARRATOR: The Pewter Protein trial produced a clear result. But a result is only as good as the assumptions behind it. In this final part, we confront the complications, the limitations, and the deeper philosophical questions that surround randomized experiments.

[TEACHING SECTION]

[OAK EXPLAINS: SUTVA -- The Assumption Behind Everything]

NARRATOR: Every result we have derived so far -- the unbiasedness of the difference in means, the validity of the confidence interval, the meaning of the p-value -- all of it rests on an assumption so fundamental that it often goes unstated. It is called SUTVA, the Stable Unit Treatment Value Assumption.

OAK: SUTVA has two parts. The first part says no interference. That means one trainer's treatment status does not affect another trainer's outcome. In this trial, each trainer battles Brock independently. Trainer A taking Protein should not change what happens to Trainer B. The second part says no hidden variations of treatment. That means Pewter Protein is the same Pewter Protein for every treated trainer. There is only one version of the treatment.

NARRATOR: In the Pewter Protein trial, no interference seems plausible at first glance. Each trainer walks in, battles Brock alone, walks out. But there are subtle ways it could break down.

What if trainers in the Pokemon Center lobby share their tablets? A control trainer might get half a Protein tablet from a friendly treated trainer. What if trainers waiting for their battle talk to each other, and a trainer who just won on Protein shares strategy tips with the next trainer in line? "Use Ember on Geodude first, then switch to your Water-type for Onix." Now the control trainer's behavior has been influenced by a treated trainer's experience.

And here is a subtler one. What if Brock himself adapts? If he notices that the early Protein trainers are hitting harder, he might start using more Potions or switching strategies. Now later trainers are facing a different version of Brock -- one whose behavior has been shaped by earlier trainers' treatment status. That is interference through the opponent.

OAK: To mitigate these threats, Nurse Joy scheduled trainers at staggered times, prevented them from interacting in the waiting area, and made sure Brock followed a fixed battle script with no deviations. Perfect compliance with SUTVA is impossible in the real world, but we can take reasonable precautions.

NARRATOR: The no-hidden-variations part requires that Pewter Protein means the same thing for every treated trainer. What if some tablets were stored in a hot stockroom and lost potency while others were properly refrigerated? What if some trainers accidentally received a slightly different dose from a faulty production batch? Then there is not one treatment but multiple versions, and the potential outcomes are no longer well-defined.

Professor Oak addressed this by ensuring all tablets came from the same manufacturing lot, stored under controlled conditions, administered by Nurse Joy personally following a standardized protocol.

[BLUE'S MISTAKE]

BLUE: You people are so paranoid. I shared my Protein with three friends, I told everyone in the Pokemon Center about my strategy for beating Brock, and I made sure everybody knew which trainers were in the treatment group. Experiments are for nerds -- I am just helping people out!

OAK: Blue, you have just single-handedly violated every aspect of SUTVA that Nurse Joy spent weeks trying to protect. You shared the treatment, creating interference. You spread strategic information, contaminating the control group. And you unblinded the study, introducing expectation effects. If you had done this inside the trial, you would have invalidated the results.

NARRATOR: Blue is the walking embodiment of every SUTVA violation in the textbook. If someone ever asks you what interference looks like in practice, just point to Blue.

---

[TEACHING SECTION]

[OAK EXPLAINS: Internal versus External Validity]

NARRATOR: An experiment can succeed brilliantly at answering the question it asks while failing to answer the question we actually care about. These two dimensions are called internal validity and external validity, and they are often in tension.

OAK: Internal validity asks: did the experiment correctly identify the causal effect in this specific study, with this specific population, under these specific conditions? Nurse Joy's trial has strong internal validity. The randomization was clean, the balance table checked out, the blinding was maintained, SUTVA was reasonably preserved. We can be confident that the fourteen point three HP estimate reflects the real effect of Pewter Protein in this trial.

NARRATOR: External validity asks a different question: does the result generalize beyond this specific experiment?

OAK: And that is where things get trickier. We showed that Pewter Protein works against Brock's Rock-type Pokemon in Pewter City. But would it work against Misty's Water-type Pokemon in Cerulean City? Protein might boost physical Attack stats, which is exactly what you need against Rock-types with high Defense. Against Water-types, the optimal strategy might rely on Special Attack instead.

NARRATOR: Would it work for a different population of trainers? Pewter City trainers are typically early in their journey -- low-level Pokemon, small teams, limited experience. Would Protein have the same effect on experienced trainers with Level Fifty Pokemon challenging the Elite Four? There might be ceiling effects, where experienced Pokemon already hit near maximum damage, or floor effects, where novice Pokemon cannot absorb the Protein's benefits.

Would it work in a different context? The Pewter Gym is an indoor arena with controlled conditions. Would Protein work the same in a wild Pokemon encounter, where terrain, weather, and surprise play a role?

And would a different dose or timing work? The trial tested exactly ten milligrams, sixty minutes before battle. Would five milligrams work? Would twenty milligrams work better, or cause side effects?

OAK: Internal and external validity often pull in opposite directions. The tighter you control an experiment -- standardized dose, controlled setting, homogeneous population, strict protocol -- the higher the internal validity but the narrower the generalizability. A looser, more "pragmatic" trial that enrolled all trainers across Kanto, let them take Protein whenever they wanted, and measured outcomes across all gym types would have higher external validity but would sacrifice internal validity to noncompliance, interference, and treatment variation.

NARRATOR: The standard scientific approach is to establish internal validity first -- prove the effect exists under controlled conditions -- and then investigate generalizability through replication across different contexts. Nurse Joy's Pewter City trial is the first step. Future trials in Cerulean City, Vermilion City, and beyond will map the boundaries of the effect. There is a formal theory of this called transportability, developed by Pearl and Bareinboim, which uses causal diagrams to identify exactly which conditions must hold for a result to generalize from one population to another. We will touch on that in Chapter Eight.

---

[TEACHING SECTION]

NARRATOR: Now let us talk about practical complications -- the messy realities that threaten even well-designed experiments.

[OAK EXPLAINS: Noncompliance and Intent-to-Treat]

OAK: In an ideal experiment, every trainer takes the assigned treatment. In reality, compliance is imperfect. Some trainers assigned to Protein refuse to take the tablet -- maybe they are skeptical, or they feel sick that day. And in our trial, Blue was handing out Protein in the lobby, so some control trainers managed to get their hands on the real thing.

NARRATOR: The temptation is to analyze based on what trainers actually took rather than what they were assigned. This is a grave error. It reintroduces the very selection bias that randomization was designed to eliminate. Trainers who comply with their assignment may differ systematically from those who do not. If we compare "Protein takers" to "non-takers" regardless of assignment, we are back in the observational world.

OAK: The standard solution is called Intent-to-Treat analysis, or ITT. You analyze every trainer according to their assigned treatment, regardless of whether they actually complied. If a trainer was assigned to Protein but threw the tablet away, they stay in the Protein group for the analysis. If a control trainer snuck some Protein from Blue, they stay in the Placebo group.

NARRATOR: The ITT preserves the integrity of randomization -- since assignment is random, the ITT comparison is unbiased for the effect of being assigned to treatment. However, it generally underestimates the effect of actually taking the treatment, because some assigned trainers did not follow through. Think of it as a "diluted" effect estimate.

In the Pewter Protein trial, suppose twelve of one hundred trainers assigned to Protein refused to take it, and five of one hundred control trainers obtained Protein from Blue. The ITT analysis still compares all one hundred assigned-Protein trainers against all one hundred assigned-Placebo trainers, even though compliance was imperfect.

[pause]

[OAK EXPLAINS: Preview of Instrumental Variables and LATE]

OAK: Can we recover the effect of actually taking Protein despite noncompliance? Yes -- using the randomized assignment as what is called an instrumental variable. This leads to a framework called the Local Average Treatment Effect, or LATE, developed by Imbens and Angrist in nineteen ninety-four. The basic idea is elegant. You take the ITT estimate -- the effect of being assigned to treatment -- and divide it by the compliance rate -- the fraction of people whose actual treatment status was changed by the assignment. The result tells you the causal effect of the treatment for the group of people who actually complied with their assignment. These people are called compliers.

NARRATOR: We will develop this machinery fully in Chapter Six, when we reach Fuchsia City and Cinnabar Island and tackle instrumental variables in depth. For now, the key takeaway is that noncompliance does not have to be fatal. The ITT gives you a clean, unbiased estimate of the effect of assignment. And if you need the effect of actual treatment, instrumental variables can get you there -- under certain assumptions.

[pause]

[OAK EXPLAINS: Attrition]

NARRATOR: When trainers drop out of the study before outcomes are recorded, the remaining sample may no longer be balanced -- even if the original randomization was perfect.

OAK: Suppose eight trainers in the Placebo group who lost badly to Brock leave without reporting their results, while only two trainers in the Protein group do the same. The remaining data overrepresent trainers who performed well, especially in the control group. That biases the estimated treatment effect downward.

NARRATOR: When attrition rates differ across groups, there is a technique called Lee bounds that provides a principled approach. You trim the group with lower attrition to match the attrition rate of the other group, then report best-case and worst-case effect estimates. If even the worst-case bound excludes zero, the result is robust to attrition. But the best defense is prevention -- Nurse Joy stationed an assistant at the gym exit to record outcomes for every trainer, win or lose.

[OAK EXPLAINS: The Hawthorne Effect]

OAK: The Hawthorne effect -- named after a famous series of experiments at a factory in the nineteen twenties -- refers to behavior changes caused by the awareness of being studied, rather than by the treatment itself. If trainers know they are in an experiment, they might try harder, battle more carefully, and use items more strategically.

NARRATOR: If this elevated effort is symmetric across groups -- both treatment and control trainers try equally hard -- it inflates both group averages but does not bias the treatment-control comparison. The estimated effect of Protein stays valid, but it applies to a population of trainers who are trying their hardest, which might differ from real-world casual battling.

If the Hawthorne effect is asymmetric -- say, Protein trainers try harder because they believe they have an advantage -- that becomes a confound. Double-blinding is the primary defense. If trainers cannot tell which tablet they received, they cannot adjust their effort based on treatment status.

---

[TEACHING SECTION]

[OAK EXPLAINS: Fisher's Randomization Inference]

NARRATOR: Everything we have discussed so far about confidence intervals and p-values relied on what is called Neyman's framework -- treating the observed data as one draw from a hypothetical population and deriving the sampling distribution over repeated experiments. There is an older approach, developed by R. A. Fisher, that takes a fundamentally different perspective.

OAK: Fisher proposed something called the sharp null hypothesis. Where Neyman's null hypothesis says the average treatment effect is zero -- allowing some individuals to benefit and others to be harmed as long as it averages out -- Fisher's null says the treatment has absolutely no effect on any individual. Zero effect for every single trainer. Not on average. For each and every one.

NARRATOR: This is a stronger claim, but it has a beautiful consequence. Under Fisher's sharp null, both potential outcomes are observed for every trainer. Why? Because if the treatment has zero effect on everyone, then it does not matter which tablet they got -- their outcome would have been the same either way. The outcome we observed is both their treated potential outcome and their untreated potential outcome.

OAK: And that means we can figure out exactly what the test statistic would have been under every possible random assignment. The outcomes are fixed -- only the labels change. So we can build the entire distribution of the test statistic under the null, and see where our observed result falls within it.

NARRATOR: Let me illustrate with a small example. Imagine a miniature version of the trial with just ten trainers -- five assigned to Protein and five to Placebo. The five Protein trainers dealt one hundred fifty-five, one hundred eighty, one hundred thirty, one hundred forty-five, and one hundred sixty HP of damage. The five Placebo trainers dealt one hundred twenty, one hundred thirty-five, one hundred ten, one hundred forty, and one hundred twenty-five.

The average in the Protein group is one hundred fifty-four. The average in the Placebo group is one hundred twenty-six. The observed difference is twenty-eight HP.

Now, under Fisher's sharp null, every trainer would have produced the same outcome regardless of assignment. There are two hundred fifty-two possible ways to assign five out of ten trainers to the treatment group. For each of those two hundred fifty-two assignments, we can compute what the difference in means would have been.

For instance, one alternative assignment might place Ash, Misty, Jessie, James, and Ritchie in the treatment group and the other five in control. With those labels, the treatment group average would be one hundred forty and the control group average would also be one hundred forty, giving a difference of zero.

We compute all two hundred fifty-two such statistics and build a histogram -- the permutation distribution. It turns out to be roughly bell-shaped, centered at zero. Our observed value of twenty-eight sits way out in the right tail.

OAK: The Fisher exact p-value is the fraction of permutations where the test statistic is at least as extreme as what we observed. In this small example, suppose eighteen of the two hundred fifty-two permutations produce a difference at least as large as twenty-eight in absolute value. Then the p-value is eighteen divided by two hundred fifty-two, which is zero point zero seven one.

NARRATOR: At the five percent significance level, we would not quite reject the sharp null in this tiny sample. But the result is suggestive, and the full two-hundred-trainer trial confirmed the effect decisively. The small-sample example is just to show how the method works.

For large experiments, enumerating every possible permutation is computationally impossible -- the number of ways to assign one hundred out of two hundred trainers is an astronomically large number. In practice, researchers approximate the permutation distribution by drawing a large number of random permutations -- say ten thousand or one hundred thousand -- and computing the test statistic for each.

[pause]

[OAK EXPLAINS: Fisher versus Neyman]

NARRATOR: The Fisher and Neyman frameworks lead to the same general conclusions in most cases, but they differ in philosophy and emphasis.

OAK: Fisher focuses on testing. His null hypothesis is sharp -- it specifies every individual's treatment effect as zero. His inference is based on the exact permutation distribution over all possible random assignments. It requires no distributional assumptions and gives exact p-values even in small samples. But it is primarily a testing framework -- it tells you whether to reject the null, not how big the effect is.

NARRATOR: Neyman focuses on estimation. His null hypothesis is weaker -- it only says the average effect is zero, allowing individual effects to vary. His inference is based on the sampling distribution over hypothetical repetitions of the experiment. It gives you a point estimate, a standard error, and a confidence interval. It requires large-sample approximations for the test statistic to follow a normal distribution, but it provides a richer set of inferential tools.

OAK: Fisher and Neyman famously disagreed about the foundations of statistical inference. Their debates in the nineteen thirties were legendary and sometimes acrimonious. Fisher emphasized testing and what he called fiducial probability. Neyman emphasized estimation and confidence intervals. Both contributed indispensable ideas to experimental statistics. Modern practice draws from both traditions.

NARRATOR: In applied work today, most researchers use Neyman's framework for their primary analysis -- reporting a point estimate, standard error, confidence interval, and p-value -- and sometimes report Fisher randomization inference as a robustness check. The potential outcomes framework that we have been using throughout this textbook, formalized by Donald Rubin in nineteen seventy-four and elaborated by Holland in nineteen eighty-six, synthesized both traditions into a unified approach.

---

[TEACHING SECTION]

[OAK EXPLAINS: Ethics of Experimentation]

NARRATOR: There is one more topic we need to address before we leave Pewter City. Is it ethical to withhold a potentially beneficial treatment from control trainers?

OAK: The Pewter Protein trial is justifiable because of what is called clinical equipoise. Before the trial, there was genuine uncertainty about whether Protein works. If we already knew it worked, randomizing some trainers to Placebo would be denying them a known benefit. But we did not know. That is the whole point of running the experiment.

NARRATOR: The trial had several additional safeguards. First, informed consent -- every trainer was told they would receive either Protein or Placebo, and that the goal was to determine whether Protein works. They agreed to participate under those terms. Second, no harm -- the Placebo Berry is inert. It does not make anyone worse off than they would be without the study. Losing to Brock is disappointing but not dangerous. Nurse Joy heals all Pokemon for free. Third, data monitoring -- if interim results had shown that Protein was causing serious Pokemon health issues, the trial would have been stopped immediately. And fourth, post-trial access -- after the trial concluded and Protein was shown to be effective, all control trainers were offered free Protein before their next gym challenge.

OAK: Ethics in experimentation is not a checkbox exercise. It requires genuine engagement with the question of whether the study respects the participants' autonomy and welfare. The history of science includes deeply unethical experiments that produced valid results, and the lesson of that history is that validity is not enough. An experiment must be both scientifically sound and ethically justified.

---

[SCENE: Morning. The sun is rising over Pewter City. The narrator is standing outside the gym, Pewter Protein results in hand, ready to face Brock.]

NARRATOR: I take one last look at the data. Fourteen point three HP. Statistically significant. Practically meaningful. The coin flip did what no amount of arguing in the Pokemon Center lobby could do -- it separated the real effect from the noise of self-selection and confounding.

BROCK: Ready for your battle, challenger?

NARRATOR: I nod. Brock leads me inside. His Geodude is already waiting on the arena floor.

As I reach for my Pokeball, I think about everything I have learned. A coin flip can be more powerful than the most sophisticated statistical technique, because it solves the problem at its source. It does not try to adjust for confounders after the fact. It prevents them from forming in the first place. Randomization is not just a method. It is a philosophy -- the idea that the fairest way to learn the truth is to let chance, not choice, determine who gets what.

Nurse Joy is watching from the stands. Professor Oak has already left for Cerulean City, where another scientific question awaits. And Blue? Blue is somewhere on the road ahead, still confident that his personal experience is all the evidence he needs.

I throw my Pokeball. The battle begins.

[pause]

---

## Chapter Summary

NARRATOR: Let me step back and pull together everything we covered in Pewter City. This was a dense chapter, and the ideas here form the foundation for everything that comes next.

[pause]

First: randomization creates independence between treatment assignment and potential outcomes. When a coin flip decides who gets the treatment, the treatment and control groups are balanced -- in expectation -- on every characteristic, observed and unobserved. This eliminates selection bias, and it is the one property that no observational method in this textbook can match.

Second: the difference-in-means estimator -- just subtracting the control group average from the treatment group average -- is unbiased for the Average Treatment Effect under random assignment. No modeling assumptions are required. No regression. Just a subtraction.

Third: experimental design matters enormously. A precise treatment definition, a well-chosen outcome measure, a power analysis to determine sample size, stratified randomization to improve precision, and blinding to prevent expectation effects -- all of these decisions shape the quality of the evidence.

Fourth: under randomization, the Average Treatment Effect, the Average Treatment Effect on the Treated, and the Average Treatment Effect on the Control all coincide. The distinction between estimands, which will become critical in observational settings, collapses in an experiment.

Fifth: Neyman's framework provides the standard tools for inference -- variance estimation, standard errors, confidence intervals, and hypothesis testing. The variance is estimated conservatively by summing the sample variances in each group divided by their respective sample sizes, and the standard error is the square root of that sum.

Sixth: regression adjustment, following Lin's two thousand thirteen approach, can improve precision by absorbing residual outcome variation without introducing bias, as long as the specification includes treatment-covariate interactions. It is strictly an improvement over the unadjusted estimate.

Seventh: SUTVA -- the Stable Unit Treatment Value Assumption -- requires no interference between units and no hidden variations of treatment. Without it, potential outcomes are not well-defined, and the entire inferential framework unravels.

Eighth: internal validity asks whether the experiment worked as designed. External validity asks whether the results generalize to other populations, settings, and conditions. The two are often in tension, and the standard approach is to establish internal validity first and then investigate generalizability through replication.

Ninth: Fisher's randomization inference provides exact p-values by computing the test statistic under all possible random assignments, using the sharp null hypothesis to treat all potential outcomes as observed. Fisher's approach complements Neyman's, with the two frameworks typically yielding similar conclusions.

Tenth: practical complications -- noncompliance, attrition, the Hawthorne effect -- are inevitable. The Intent-to-Treat analysis preserves the benefits of randomization. Instrumental variables, which we will develop in Chapter Six, can recover the effect on compliers when noncompliance is present.

[pause]

NARRATOR: Tomorrow we press on to Cerulean City and face Misty. In that next chapter, we leave the clean world of experiments behind and enter the murkier waters of observational data. When you cannot randomize -- when you have to work with the data the world gives you, not the data you designed -- the challenge of causal inference becomes harder and the methods become more creative. We will learn about matching, subclassification, and propensity scores -- tools for making observational data behave more like experimental data. It will not be as clean as a coin flip. But with the right assumptions and the right techniques, we can still learn something real.

Welcome to Chapter Three.

[pause]

---

## Comprehension Check

NARRATOR: Before we leave Pewter City, check yourself on these questions.

First: Why does random assignment eliminate selection bias? Explain in plain language what the coin flip achieves that no observational adjustment can.

[long pause]

Random assignment makes treatment status independent of potential outcomes. Because the coin knows nothing about the trainer -- their experience, their Pokemon, their hidden abilities -- the kind of person who ends up in the treatment group is, on average, identical to the kind of person who ends up in the control group. This balances both observed and unobserved confounders in expectation, eliminating the selection bias term entirely. No observational method can balance unobserved confounders, because you cannot adjust for what you cannot measure.

Second: In the Pewter Protein trial, the difference-in-means estimate was fourteen point three HP with a standard error of four point nine five. What does the standard error measure, and what does the resulting confidence interval of four point six to twenty-four point zero tell us?

[long pause]

The standard error measures how much the estimate would vary if we repeated the same experiment many times with different random assignments. It captures the precision of our estimate. The ninety-five percent confidence interval of four point six to twenty-four point zero means that if we repeated this experiment over and over, ninety-five percent of the intervals we constructed would contain the true treatment effect. Since this interval does not include zero, we can reject the null hypothesis of no effect at the five percent significance level.

Third: What is SUTVA, and give one example of how it could be violated in the Pewter Protein trial?

[long pause]

SUTVA, the Stable Unit Treatment Value Assumption, has two parts. First, no interference: one trainer's treatment status must not affect another trainer's outcome. Second, no hidden variations of treatment: the treatment must be the same for every treated unit. An example of a violation would be trainers sharing strategy tips in the Pokemon Center lobby. If a treated trainer who just beat Brock tells a control trainer which attacks to use, the control trainer's outcome has been influenced by someone else's treatment status, violating the no-interference condition.

Fourth: What is the difference between internal and external validity, and why are they often in tension?

[long pause]

Internal validity asks whether the experiment correctly identified the causal effect within the study -- in this specific population, under these specific conditions. External validity asks whether the result generalizes to other populations, settings, or conditions. They are in tension because the steps you take to improve internal validity -- standardizing the treatment, controlling the environment, using a homogeneous population -- narrow the conditions under which the result was established, making it harder to claim the findings apply elsewhere. Conversely, a broader, more realistic study improves generalizability but introduces more threats to internal validity.

Fifth: Explain the difference between Fisher's and Neyman's approaches to inference in randomized experiments. When would you prefer one over the other?

[long pause]

Fisher's approach uses the sharp null hypothesis, which says the treatment has zero effect on every individual. Under this null, all potential outcomes are observed, so you can build the exact permutation distribution of the test statistic over all possible random assignments and compute an exact p-value. Neyman's approach uses a weaker null that says only the average effect is zero, and derives the sampling distribution using repeated-sampling theory to produce point estimates, standard errors, and confidence intervals. You would prefer Fisher's approach when you have a small sample and want exact p-values without distributional assumptions. You would prefer Neyman's approach when you want a point estimate and confidence interval, not just a test, or when the sample is large enough for the normal approximation to be accurate. In practice, most researchers report both.

[pause]

NARRATOR: Pewter City is behind us. The Boulder Badge is in hand. Ahead lies Route Three and the long road to Cerulean City, where Misty and the challenge of observational data await.

---
