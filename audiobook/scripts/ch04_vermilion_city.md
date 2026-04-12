---
title: "Chapter 4: Vermilion City -- Matching and Subclassification"
chapter_number: 4
source_file: "textbook/chapters/ch04_vermilion_city.md"
estimated_runtime_minutes: 75
key_concepts:
  - Matching Intuition (Counterfactual Twins)
  - Exact Matching
  - Coarsened Exact Matching (CEM)
  - Curse of Dimensionality
  - Mahalanobis Distance Matching
  - Propensity Score
  - Rosenbaum-Rubin Theorem
  - Propensity Score Matching
  - Subclassification / Stratification
  - Covariate Balance and Love Plots
  - Common Support / Overlap
  - Hidden Bias and Limitations
characters:
  - NARRATOR (trainer, first-person, curious and conversational)
  - OAK (professor, patient teacher, plain-English definitions)
  - BLUE (rival, confident, makes causal reasoning errors)
  - SURGE (Lt. Surge, Vermilion Gym Leader, loud, direct, military precision)
---

# Chapter 4: Vermilion City -- Matching and Subclassification

## Part 1: The S.S. Anne and the Problem of Unfair Comparisons

[SCENE: Vermilion Harbor. Seagulls calling. The deep horn of a cruise ship blowing. Trainers chattering as they file down a gangway. The clang of a metal dock.]

NARRATOR: The S.S. Anne is enormous. Its white hull fills the entire Vermilion Harbor, gleaming under the Kanto sun. I am standing on the dock with four hundred other trainers who have just spent a week on that ship. My legs still feel like they are swaying. Two Gym badges sit in my case -- Boulder and Cascade -- and I can already see the Vermilion Gym at the top of the hill, its lightning-bolt emblem catching the light.

But the real story of the day is not the Gym. It is the argument. Somewhere around the second day of the cruise, a training program appeared on the ship's schedule: Lt. Surge's Thunder Training. Three hours a day, six days, covering Electric-type battle strategy, defensive positioning, team composition, everything you would need to survive the Vermilion Gym. Some trainers signed up immediately. Others spent the week at the buffet, the pool, or the onboard Pokemon Center. Now, as we all file off the gangway, the debate has reached a fever pitch.

Does Thunder Training actually work?

[pause]

I find Professor Oak near the harbor terminal. He is scribbling in a notebook, already cataloging data.

OAK: Fascinating natural experiment. Four hundred trainers, same cruise, same destination. One hundred sixty of them completed the Thunder Training program. Two hundred forty did not. And they are all about to face the same Gym. This is exactly the kind of observational study we can learn from -- if we are careful.

NARRATOR: If we are careful. That is the part that matters. Because the naive answer is already circulating through the crowd.

BLUE: I already ran the numbers, Professor. Thunder Training graduates scored an average of seventy-two point four at the Vermilion Gym. Non-participants scored fifty-eight point one. That is a fourteen-point-three-point gap. Thunder Training is a game changer!

NARRATOR: Blue is waving a printout. Several trainers are nodding along. But Oak is shaking his head.

OAK: Blue, did you happen to look at who signed up for the training?

BLUE: What do you mean?

OAK: The trainers who chose Thunder Training already had an average of three point eight badges. The ones who skipped it had two point one. The participants had higher-level Pokemon, more battle experience, and better scores on strategic reasoning. They were already stronger trainers. You are comparing Dragonite trainers to Rattata trainers and crediting the difference to a one-week course.

[pause]

NARRATOR: And just like that, the fourteen-point gap starts to look a lot less impressive.

---

[TEACHING SECTION]

NARRATOR: Let me lay out the situation more carefully. We have four hundred trainers. For each one, we know whether they completed Thunder Training or not, and we know their performance score at the Vermilion Gym -- a number from zero to one hundred that combines damage dealt, Pokemon remaining, and time to victory or defeat. We also know a whole list of things about each trainer that were true before they ever set foot on the S.S. Anne: the number of badges they had already earned, the average level of their Pokemon team, their total career battles, a strategic reasoning score, their prior knowledge of Electric-type matchups, the number of species in their Pokedex, whether they carried a Ground-type Pokemon, the number of healing items in their bag, and how many hours they had spent training in the past month.

Now, remember the language of potential outcomes from Chapter One. The raw difference in group means -- fourteen point three points -- mixes together two things. The first is the actual causal effect of Thunder Training on the trainers who took it. The second is selection bias: the fact that Thunder Training participants would have performed better even without the training, simply because they are more experienced and more skilled.

Our goal is to separate these two things. We want to eliminate the selection bias so we can see the true causal effect. And in Chapter Three, we learned to draw DAGs to identify which variables are confounders -- which variables create those backdoor paths between treatment and outcome. But identifying confounders is only half the battle. We need a strategy for actually adjusting for them.

This chapter introduces the oldest and most intuitive family of such strategies. It is called matching.

[OAK EXPLAINS: The Matching Idea]

OAK: The logic of matching is beautifully simple. If you want to know whether Thunder Training helps, compare a trained trainer to an untrained trainer who is otherwise identical. Same number of badges. Same team level. Same battle experience. Same strategic ability. If the trained trainer still performs better, you can attribute the difference to the training itself. The challenge is that "otherwise identical" is far harder to achieve than it sounds.

NARRATOR: In other words, matching is about finding each treated person's counterfactual twin -- someone who looks just like them on every measurable dimension, except that the twin did not receive the treatment. You pair them up, look at the difference in outcomes, and average those differences across all your pairs.

The formal target is the Average Treatment Effect on the Treated, or ATT. For each of the one hundred sixty trainers who completed Thunder Training, you find a matched partner from the two hundred forty who did not. You take the difference in their Gym scores. You average all one hundred sixty differences. That average is your estimate of what Thunder Training did for the people who actually took it.

The logic mirrors the ideal experiment we cannot run. In a randomized controlled trial, randomization ensures that treated and control groups are comparable on everything -- observed and unobserved. Matching tries to construct a comparison group that resembles the treated group on all the things we can measure. If we succeed, and if there are no unobserved confounders -- the conditional ignorability assumption from Chapter Three -- then the matched comparison is as good as a randomized experiment.

[pause]

[BLUE'S MISTAKE]

BLUE: Wait. I already compared the groups. The difference was fourteen point three. What is wrong with that?

OAK: Everything, I am afraid. You made the most fundamental error in observational causal inference: treating an associational comparison as a causal one. Without adjusting for confounders, the raw mean difference is a biased estimate of the causal effect. You are comparing apples to oranges and concluding that apples taste better because they are apples.

NARRATOR: To be fair to Blue, he collected the right data. His mistake is in the analysis, not the measurement. Matching gives us a principled way to use that data correctly.

[THINK ABOUT THIS]

NARRATOR: For matching to yield a valid causal estimate, we need two key assumptions. The first is conditional ignorability, which says that once we account for all the observed covariates, treatment assignment is effectively random. There are no unobserved confounders. The second is overlap, sometimes called common support. This says that for every combination of covariate values observed among treated trainers, there is at least some probability of finding a control trainer with similar values. If both assumptions hold, matching eliminates selection bias completely.

The question is how to match. The next several sections explore increasingly sophisticated answers.

---

## Part 2: Finding the Right Twin

[SCENE: The Vermilion Pokemon Center. Tables pushed together. Oak has spread out printed spreadsheets. Blue is peering over his shoulder. In the background, the sound of a healing machine chiming.]

NARRATOR: Let us start with the most straightforward version of matching and work our way up.

---

[TEACHING SECTION]

NARRATOR: The most obvious approach is exact matching. For each treated trainer, find a control trainer with exactly the same values on every covariate. If a Thunder Training graduate has four badges, a team level of thirty-two, one hundred fifty career battles, and a strategy score of sixty-eight, we search the control group for someone with those exact same numbers who skipped the training.

If we find an exact match, there is zero covariate imbalance within that pair. The comparison is clean. In theory, this is the gold standard.

In practice, it is nearly impossible.

[OAK EXPLAINS: The Curse of Dimensionality]

OAK: Here is the problem. We have ten covariates, and many of them take dozens or hundreds of possible values. Even if we discretize each one into just a handful of bins, the total number of possible covariate combinations explodes. With our S.S. Anne data, even a conservative discretization produces roughly twenty-seven billion possible cells. With only four hundred trainers, the vast majority of those cells are empty. Finding a control trainer who matches a treated trainer on all ten covariates simultaneously is virtually impossible. This is what we call the curse of dimensionality -- as the number of covariates grows, the covariate space expands exponentially, and the data become hopelessly sparse.

NARRATOR: In other words, exact matching works beautifully when you have two or three discrete covariates. When you have ten covariates with continuous values, almost every treated trainer is one of a kind. There is nobody in the control group who matches them exactly on everything.

[pause]

NARRATOR: So researchers came up with a clever compromise. It is called Coarsened Exact Matching, or CEM, proposed by Iacus, King, and Porro in two thousand twelve. The idea is to take each covariate, group its values into a small number of broader bins, and then do exact matching on those bins instead of the original values.

For example, instead of matching on the exact number of badges -- zero through seven -- you could group badges into three categories: low, which covers zero through two; mid, covering three through five; and high, covering six and seven. You do the same for team level and for whether the trainer has a Ground-type Pokemon. Now instead of billions of cells, you have three times three times two equals eighteen strata. That is manageable.

You place every trainer into one of those eighteen strata based on their coarsened covariate values. Any stratum that contains at least one treated and one control trainer is a valid comparison group. Any stratum that contains only treated trainers or only control trainers gets pruned -- those trainers cannot be matched.

In our example, consider four of those strata. Stratum A contains trainers with low badges, low team level, and no Ground-type. It has three treated trainers and twenty-eight controls. That is a matched stratum. Stratum B has mid badges, mid team level, and a Ground-type present. Twenty-two treated, fifteen controls. Also matched. Stratum C has high badges, high team level, and a Ground-type. Eighteen treated, just two controls. Matched, but thin on the control side. Stratum D has high badges, high team level, and no Ground-type. Eight treated, zero controls. Pruned entirely. Those eight treated trainers are dropped from the analysis because no one in the control group has a similar profile.

Within each surviving stratum, you compare the average Gym score of treated trainers to the average Gym score of control trainers. That gives you a within-stratum treatment effect. Then you take a weighted average across strata, where the weight for each stratum reflects the share of matched treated trainers it contains.

[OAK EXPLAINS: Why CEM Bounds Imbalance]

OAK: CEM has a remarkable theoretical property. The maximum imbalance between treated and control groups is bounded by the coarsening the researcher chooses. If you coarsen team level into bins of width ten, you know that any matched treated-control pair differs by at most ten levels on that variable. This bound holds regardless of the data. You set it before you ever look at outcomes. Compare this to other matching methods where the degree of imbalance is discovered only after matching and depends on the data in unpredictable ways. CEM lets you choose your acceptable imbalance first and then find matches that satisfy it. That is a powerful guarantee.

NARRATOR: The tradeoff, of course, is between precision and sample size. Wider bins give you more matches but less precise comparisons. Narrower bins give you better comparisons but fewer matches. The researcher has to navigate that tradeoff thoughtfully. But CEM's great advantage is transparency -- you can see exactly what tradeoff you are making.

[pause]

---

NARRATOR: Now, CEM is elegant, but it still struggles as the number of covariates grows. Even with coarsened bins, the number of strata multiplies quickly. So the next approach is to define a distance metric that measures how similar two trainers are, and then match each treated trainer to the nearest control trainer in the covariate space.

[TEACHING SECTION]

NARRATOR: The most common distance metric for matching is the Mahalanobis distance. The idea is to measure how far apart two trainers are across all their covariates simultaneously, while accounting for the fact that different covariates are measured on very different scales.

Think about it. Battle experience ranges from five to five hundred. Badges range from zero to seven. If you just compute the raw distance, battle experience dominates everything because its numbers are so much bigger. A difference of fifty battles would swamp a difference of three badges, even though three badges might matter a great deal more.

[OAK EXPLAINS: Mahalanobis Distance]

OAK: The Mahalanobis distance solves this scaling problem. It takes the differences between two trainers on each covariate and rescales them using the inverse of the covariance matrix. In plain English, it adjusts for two things at once. First, it standardizes each covariate so that a one-unit difference on badges is comparable to a one-unit difference on battle experience. Second, it accounts for correlations between covariates. If badges and team level tend to move together, the Mahalanobis distance does not double-count that shared information. The result is a single number that tells you how similar two trainers really are, taking all their covariates into account on a fair footing.

NARRATOR: Let me walk through a small example. Take a treated trainer named Alice. She has four badges and a team level of thirty-two. Now consider three potential control matches. Bob has four badges and a team level of thirty. Carol has three badges and a team level of thirty-five. Dan has five badges and a team level of twenty-eight.

When you compute the Mahalanobis distance from Alice to each control, Bob comes out closest with a distance of about zero point two seven. Carol is farther away at about zero point eight three, and Dan is farthest at about zero point nine three. Bob is the nearest neighbor, which makes intuitive sense -- he matches Alice on badges exactly and is very close on team level.

[pause]

NARRATOR: Once you have a distance metric, nearest-neighbor matching is straightforward. One-to-one matching pairs each treated unit with its single closest control. K-to-one matching pairs each treated unit with its K nearest controls and averages their outcomes.

You also have to decide whether to match with or without replacement. Without replacement means each control trainer can be paired with at most one treated trainer. Once Bob is matched to Alice, he is off the market for everyone else. This avoids using the same control observation multiple times, but it can force bad matches later on when the pool of available controls shrinks. The order you match in matters, which introduces some arbitrariness.

With replacement means a single control trainer can serve as the match for multiple treated trainers. If Bob happens to be the closest control for three different treated trainers, he appears in three different pairs. This generally produces better individual matches because the best control is always available, but it reduces your effective sample size because some control observations carry heavy weight.

NARRATOR: One more refinement. A caliper sets a maximum acceptable distance. If no control trainer falls within the caliper radius of a treated trainer, that treated trainer goes unmatched and is dropped from the analysis. A tight caliper means excellent match quality but a smaller sample. A loose caliper means you keep more observations but accept some poor matches. A common rule of thumb is to set the caliper at zero point two standard deviations of the logit of the propensity score -- but we have not talked about propensity scores yet. That is next.

---

## Part 3: The Propensity Score and Beyond

[SCENE: The deck outside the Vermilion Pokemon Center. Late afternoon sun. Oak is drawing a diagram on a whiteboard he has commandeered from the Center's break room. Lt. Surge walks up, in full military gear, arms crossed.]

SURGE: You eggheads still out here arguing about statistics? In the army, we matched soldiers to training programs by gut instinct. Worked fine.

OAK: And how did you evaluate whether the training actually worked?

SURGE: The ones who survived were better soldiers!

OAK: That is... survivorship bias, but we will save that for another day. Let me show you something remarkable about reducing a complicated problem to a single number.

[pause]

---

[TEACHING SECTION]

NARRATOR: Here is the problem we have been building toward. Matching on many covariates simultaneously is difficult. With ten covariates, we are searching for neighbors in a ten-dimensional space, and the curse of dimensionality makes close neighbors increasingly rare. What if we could reduce the entire problem to matching on a single number that captures everything relevant about those ten covariates?

This is exactly what the propensity score achieves.

[OAK EXPLAINS: The Propensity Score]

OAK: The propensity score is the probability that a particular trainer received the treatment, given everything we observe about them. For our study, it is the probability that a trainer completed Thunder Training, given their badges, team level, battle experience, strategic reasoning, Electric-type knowledge, Ground-type status, items, training hours, and Pokedex count. It compresses all those variables into one number between zero and one.

NARRATOR: Think of it this way. If a trainer has a propensity score of zero point seven, that means a trainer with their exact profile had a seventy percent chance of signing up for Thunder Training. A score of zero point two means only a twenty percent chance. The score summarizes how likely someone was to be treated based on their observable characteristics.

The power of the propensity score comes from a remarkable theorem proved by Rosenbaum and Rubin in nineteen eighty-three.

[OAK EXPLAINS: The Rosenbaum-Rubin Theorem]

OAK: The theorem says this. If adjusting for the full set of covariates is sufficient to eliminate confounding -- that is, if conditional ignorability holds given all your observed variables -- then adjusting for the propensity score alone is also sufficient. You can collapse ten covariates into one number and lose nothing relevant to confounding. The practical payoff is enormous. Instead of trying to find a control trainer who matches on ten dimensions simultaneously, you only need to find one whose propensity score is close to yours.

NARRATOR: Let me say that again, because it is remarkable. Instead of finding a counterfactual twin who matches you on badges and team level and battle experience and strategy score and every other variable, you find a twin who simply had the same probability of being treated. If that probability is the same, the theorem guarantees that the distribution of covariates is balanced between the two groups. Within any group of trainers who share the same propensity score, treatment assignment is effectively random with respect to the covariates.

[pause]

NARRATOR: In practice, we do not know the true propensity score. We have to estimate it from the data. The most common approach is logistic regression, where you predict treatment status from all the covariates.

For the S.S. Anne data, the logistic regression reveals some intuitive patterns. Each additional badge increases the odds of participating in Thunder Training by about forty-one percent. Having a Ground-type Pokemon nearly doubles the odds, which makes sense -- trainers who already have a type advantage against Electric might be especially interested in learning to exploit it. Battle experience, strategy score, and Electric-type knowledge all positively predict participation. Items carried, interestingly, has almost no predictive power.

For a specific trainer -- say Alice with four badges, team level thirty-two, one hundred fifty battles, strategy score sixty-eight, Electric-type knowledge of seven, a Ground-type on her team, eight items, forty-five training hours, and sixty-two Pokedex entries -- the estimated propensity score comes out to about zero point nine eight. Alice is almost certainly a Thunder Training participant, which is consistent with her strong profile.

[THINK ABOUT THIS]

NARRATOR: Before using propensity scores for matching, we need to check something called overlap or common support. The propensity score distributions for treated and control groups must overlap substantially. In our data, the treated trainers have propensity scores ranging from zero point zero eight to zero point nine eight, with a median of zero point five eight. The control trainers range from zero point zero two to zero point eight nine, with a median of zero point two five.

The distributions overlap in the range from about zero point zero eight to zero point eight nine. But treated trainers with propensity scores above zero point eight nine have no comparable controls. They are in a region of non-overlap. These trainers are so likely to have signed up for Thunder Training that there is essentially nobody like them in the control group. Matching in that region is unreliable.

[pause]

[BLUE'S MISTAKE]

BLUE: So I just run a logistic regression, compute the score, and match on it? That handles all confounding?

OAK: Only confounding from observed variables. If there is a confounder you did not include in your model -- like natural talent or patience -- the propensity score will not help.

BLUE: But my model has a pretty good fit!

OAK: The fit of your propensity score model is irrelevant to whether you have captured all confounders. A model that perfectly predicts treatment based on five variables still misses the sixth if you did not include it. Propensity scores balance what you put in. They have no magical power over what you leave out.

NARRATOR: This is a critical point worth repeating. The propensity score balances observed covariates. It reduces a multidimensional matching problem to a one-dimensional one. It enables consistent estimation of causal effects under the assumption that all confounders are observed. But it does not balance unobserved covariates. It does not guarantee that the propensity score model is correctly specified. And it does not eliminate all sources of bias. The propensity score is only as good as the conditional ignorability assumption. If that assumption fails, no propensity score method can save us.

---

[TEACHING SECTION]

NARRATOR: Now let us actually do propensity score matching. The procedure is simple: for each treated trainer, find the control trainer whose estimated propensity score is closest. Then compare their outcomes.

Let me trace through a small example. Imagine five treated trainers and eight controls. The first treated trainer, call them T-one, has an estimated propensity score of zero point seven two and a Gym score of seventy-eight. Their nearest control is C-six, with a propensity score of zero point seven five. The gap is only zero point zero three -- an excellent match. C-six scored seventy-two at the Gym. The within-pair difference is plus six.

The second treated trainer, T-two, has a score of zero point four five and a Gym score of sixty-five. The closest control is C-five at zero point four seven, a gap of just zero point zero two. C-five scored sixty-two. The difference is plus three.

T-three has a propensity score of zero point six one and a Gym score of seventy-one. The nearest control is C-seven at zero point six zero, almost identical. C-seven scored sixty-four. The difference is plus seven.

T-four has a score of zero point eight three and a Gym score of eighty-two. The closest available control is C-two at zero point six nine. The gap here is zero point one four -- noticeably larger than the others. C-two scored seventy. The difference is plus twelve.

Finally, T-five has a score of zero point three eight and a Gym score of sixty. The closest control is C-one at zero point four zero, a gap of zero point zero two. C-one scored fifty-eight. The difference is plus two.

Average the five within-pair differences: six plus three plus seven plus twelve plus two equals thirty, divided by five. The estimated ATT is six point zero.

[pause]

NARRATOR: Notice that T-four's match was the weakest. The gap of zero point one four is considerably larger than the others. If we had imposed a caliper of zero point one zero, meaning no match is allowed with a propensity score distance greater than zero point one, T-four would have gone unmatched. The ATT would have been estimated from only four pairs: six plus three plus seven plus two divided by four equals four point five. The caliper changes both the estimate and the population it applies to.

[OAK EXPLAINS: Greedy vs. Optimal Matching]

OAK: There is another subtlety. The matching I just described is called greedy or nearest-neighbor matching. You go through the treated trainers one by one and grab the closest available control. This is fast, but it can produce suboptimal pairings. The first treated trainer might take a control that would have been a much better match for a later treated trainer. Optimal matching solves this by minimizing the total distance across all matched pairs simultaneously. It finds the globally best set of pairings rather than making locally good choices one at a time. For most datasets of moderate size, optimal matching is computationally feasible and is preferred when the stakes are high.

[pause]

NARRATOR: Now, Abadie and Imbens proved a cautionary result in two thousand sixteen. Propensity score matching can actually increase the distance between matched units on the original covariates, even when the propensity scores are close. Two trainers might both have a propensity score of zero point five zero, but they arrived at that score through completely different routes. One might have many badges but low strategy. The other might have few badges but high strategy. Their propensity scores match, but their covariate profiles are quite different.

This result has led some researchers, most notably King and Nielsen in two thousand nineteen, to argue that propensity score matching should be used with caution, and that direct covariate matching -- Mahalanobis distance or CEM -- may be preferable when the number of covariates is manageable.

The practical recommendation is clear: after propensity score matching, always check covariate balance. Do not assume the match is good just because the propensity scores are close.

---

[TEACHING SECTION]

NARRATOR: There is an elegant alternative to pairing each treated trainer with a single control. Instead of finding one-to-one matches, you can divide the entire sample into groups -- strata -- based on the propensity score, and compare treated and control outcomes within each stratum. This is called subclassification or stratification.

[OAK EXPLAINS: Subclassification]

OAK: The idea is straightforward. Sort all four hundred trainers by their estimated propensity score. Divide them into, say, five groups based on the quintiles of the score distribution. Within each group, the treated and control trainers have roughly similar propensity scores, which means their covariates should be roughly balanced. Compare the average outcomes within each group and then combine those comparisons into an overall estimate.

NARRATOR: For our S.S. Anne data, here is what the five strata look like.

The first stratum covers propensity scores from about zero point zero two to zero point two zero. It contains eight treated trainers and seventy-two controls. These are the trainers least likely to have signed up for Thunder Training. Within this stratum, the treated trainers averaged fifty-two point three at the Gym, and the controls averaged forty-seven point one. The within-stratum difference is five point two.

The second stratum runs from zero point two zero to zero point three five. Twenty-two treated, sixty-eight controls. The difference is six point two.

The third stratum covers zero point three five to zero point five five. Thirty-eight treated, fifty-two controls. The difference is six point three.

The fourth stratum covers zero point five five to zero point seven five. Forty-eight treated, thirty-six controls. The difference is six point four.

The fifth stratum covers zero point seven five to zero point nine eight. Forty-four treated, but only twelve controls. The difference here is seven point two.

[pause]

NARRATOR: To get the overall ATT, you take a weighted average of these within-stratum effects. The weight for each stratum is the share of treated trainers it contains. Stratum one has eight out of one hundred sixty treated trainers, so its weight is zero point zero five. Stratum two has twenty-two out of one hundred sixty, weight zero point one three eight. Stratum three, zero point two three eight. Stratum four, zero point three zero zero. Stratum five, zero point two seven five.

Multiply each weight by its stratum effect and add them up: zero point zero five times five point two, plus zero point one three eight times six point two, plus zero point two three eight times six point three, plus zero point three zero zero times six point four, plus zero point two seven five times seven point two. The total comes to six point five two.

This estimate of six point five two points is dramatically smaller than the naive difference of fourteen point three. It confirms that much of the raw gap was selection bias, not a treatment effect. And it lines up nicely with the propensity score matching estimate of six point zero from the paired analysis, which is reassuring. Two different methods, similar answers.

[OAK EXPLAINS: Cochran's Rule of Five]

OAK: A classical result from Cochran in nineteen sixty-eight provides useful guidance. Subclassification into just five strata based on a single confounding covariate removes approximately ninety percent of the bias from that covariate. With the propensity score summarizing multiple covariates, five to ten strata are typically sufficient for substantial bias reduction.

NARRATOR: Subclassification has several practical advantages over one-to-one matching. First, no units are discarded. Every treated and control trainer appears in exactly one stratum, as long as overlap holds. Second, it is computationally simple -- just sorting and stratifying, no optimization required. Third, it is transparent. You can inspect each stratum individually. If one stratum shows a wildly different treatment effect, that might signal something interesting -- effect heterogeneity, or a problem with the model. Fourth, standard errors are straightforward to compute.

The main disadvantage is residual confounding. Within each stratum, the propensity score is not perfectly constant, so some covariate imbalance may remain. Using more strata helps but reduces the sample size per stratum.

---

[SCENE: Inside the Vermilion Pokemon Center. Oak pulls out a final set of printouts.]

[TEACHING SECTION]

NARRATOR: We have now seen several ways to match: exact matching, coarsened exact matching, Mahalanobis distance matching, propensity score matching, and subclassification. But how do we know if any of them actually worked? How do we know our matching created balanced groups?

This is where covariate balance assessment comes in, and it is arguably the most important step in any matching analysis.

[OAK EXPLAINS: Standardized Mean Difference]

OAK: The primary diagnostic is the Standardized Mean Difference, or SMD. For each covariate, you take the difference in means between the treated and control groups, and divide by a pooled standard deviation. This puts the imbalance on a common scale, so you can compare imbalance across covariates that are measured in different units. The threshold is straightforward: an SMD below zero point one is considered good balance. Between zero point one and zero point two five is moderate -- it might be acceptable but warrants attention. Above zero point two five is substantial imbalance, meaning the matching has failed to adequately balance that covariate.

NARRATOR: We should also check variance ratios. Beyond asking whether the means are similar, we want to know whether the spreads are similar. The variance ratio divides the variance in the treated group by the variance in the control group. A ratio near one means balanced variances. Anything between zero point five and two is generally acceptable.

[pause]

NARRATOR: For the S.S. Anne data, the balance results are striking. Before matching, every single covariate showed substantial imbalance. The SMD for badges was zero point eight five. For team level, zero point nine one. Battle experience, zero point seven eight. Strategy score, zero point eight two. Electric-type knowledge, zero point seven two. Ground-type status, zero point five eight. Even items carried, which had the smallest imbalance, was at zero point two one. These are enormous gaps.

After one-to-one propensity score matching, the picture transformed. Badges dropped to zero point zero four. Team level to zero point zero six. Battle experience to zero point zero eight. Strategy score to zero point zero five. Electric-type knowledge to zero point zero three. Ground-type status to zero point zero seven. Items carried to zero point zero two. Hours training to zero point zero nine. Pokedex count to zero point zero six. Every single SMD fell below zero point one zero. Every variance ratio landed comfortably between zero point five and two. The matching worked.

NARRATOR: There is a visual tool that makes this even clearer. It is called a Love plot, named after the researcher Thomas Love. Imagine two columns of dots arranged vertically, one for each covariate. On the horizontal axis is the standardized mean difference. A vertical reference line marks zero -- perfect balance. Two more vertical lines mark plus and minus zero point one, the threshold for acceptable balance.

For each covariate, there are two dots. One represents the SMD before matching, and the other represents the SMD after matching. Before matching, the dots are scattered far to the right of center -- some as far as zero point nine one. After matching, every single dot snaps close to zero, clustering tightly within the reference lines. The Love plot gives you an immediate visual verdict: matching succeeded.

[pause]

[OAK EXPLAINS: What To Do When Balance Is Poor]

OAK: If matching fails to achieve adequate balance on one or more covariates, do not despair. There are several concrete steps. First, re-specify the propensity score model -- try adding interaction terms or polynomial terms for covariates that remain imbalanced. Second, try a different matching method entirely. If propensity score matching gives poor balance, Mahalanobis distance matching or CEM might do better. Third, tighten the caliper to force closer matches, accepting that you will lose some treated units. Fourth, increase the matching ratio from one-to-one to k-to-one, averaging over multiple controls. Fifth, if matching proves consistently difficult, consider alternative estimators like inverse probability weighting or doubly robust estimation, which we will encounter in Chapter Five.

NARRATOR: And here is a principle that Professor Oak emphasizes above all else.

OAK: A common misunderstanding is that the propensity score model should be evaluated by how well it predicts treatment assignment. In fact, the goal is not prediction but balance. A model with a modest fit but excellent covariate balance is preferable to one with a high fit but residual imbalance. The propensity score is a tool for balance, not a prediction model. Its quality is judged entirely by whether it achieves balance.

---

[SCENE: The steps of the Vermilion Gym. Sunset. Surge is leaning against the door frame.]

[TEACHING SECTION]

NARRATOR: Before we go into that Gym, we need to be honest about what matching can and cannot do. Because matching is intuitive, transparent, and powerful -- but like every method in causal inference, it rests on assumptions that may be violated.

SURGE: In the army, we had a saying. No plan survives first contact with the enemy.

NARRATOR: The same is true for statistical methods. No method survives first contact with unobserved confounders.

[pause]

NARRATOR: The critical assumption behind all matching methods is conditional ignorability -- the assumption that, given the covariates we observed, treatment assignment is as good as random. But what if there are variables we did not observe?

Consider two things we could not measure about the S.S. Anne passengers. The first is patience. Patient trainers are more likely to complete a grueling week-long training program and more likely to persevere through a difficult Gym battle. The second is natural talent. Naturally talented trainers are drawn to intensive training and they perform better in any battle, regardless of training.

Both patience and natural talent create backdoor paths from Thunder Training to Gym performance. And because we did not observe them, they do not appear in our propensity score model. Matching on observed covariates does not block these paths. Our estimated ATT of roughly six to six and a half points is likely biased upward. Some of that estimate reflects the advantage that patient, naturally talented trainers have even without the training.

If the true causal effect is, say, four points, then roughly two to two and a half points of our estimate is residual confounding bias. No amount of re-specifying the propensity score model or trying different matching algorithms can fix this. The problem is in the data, not the method.

[OAK EXPLAINS: Matching Is a Design]

OAK: I want to emphasize something many researchers overlook. Matching is not just a statistical technique. It is a research design. When you match, you are constructing a comparison group that approximates what a randomized experiment would have produced. This is a design step, just as choosing your sample or your treatment is a design step.

The practical implication is that matching should be done before looking at outcomes. Assess covariate balance. Iterate on the propensity score model. Try different matching specifications. Do all of this without peeking at the outcome variable. Only after you are satisfied with the matched sample should you estimate the treatment effect. This separation of design and analysis protects against the temptation to choose the matching specification that gives the answer you want.

NARRATOR: There are other limitations too. Positivity violations occur when some trainers are essentially guaranteed to be treated or guaranteed to be untreated given their characteristics. If trainers with zero badges and very low team levels were never offered Thunder Training, no matching can create valid comparisons for treated trainers in that region.

And there is model dependence. Different matching specifications -- one-to-one versus five-to-one, with versus without replacement, different calipers -- can yield different results. This is not unique to matching; regression has the same issue. But it means we should report results across multiple reasonable specifications. If conclusions are robust, we can be more confident. If they vary substantially, the evidence is weaker.

[pause]

NARRATOR: These limitations are not reasons to abandon matching. They are reasons to understand what matching can and cannot do, and to look ahead to more powerful tools.

In Chapter Five, we will visit the Celadon City Department Store and learn about regression and inverse probability weighting. We will discover doubly robust estimators that work even when one of our two models is wrong. In Chapter Six, we will encounter instrumental variables, which can identify causal effects even when there are unobserved confounders -- precisely the scenario where matching fails.

For now, matching has taught us something fundamental. To estimate a causal effect, you need to find fair comparisons. You need to match like with like. And you need to be honest about whether you succeeded.

---

## Chapter Summary

NARRATOR: Let me gather everything we learned in Vermilion City.

First, matching intuition. The core idea is to compare each treated trainer to an untreated trainer who is as similar as possible on observed covariates. This approximates what a randomized experiment would give you.

Second, exact matching and CEM. Exact matching demands identical covariate values, which is infeasible in high dimensions because of the curse of dimensionality. Coarsened Exact Matching relaxes this by grouping covariates into bins and matching on those bins. It offers a transparent tradeoff between match quality and sample size, and it bounds the maximum imbalance by design.

Third, distance-based matching. The Mahalanobis distance accounts for differences in scale and correlations between covariates. Nearest-neighbor matching -- with or without replacement, with or without calipers -- finds the closest control trainers in covariate space.

Fourth, the propensity score. This is the probability of treatment given observed covariates. The Rosenbaum-Rubin theorem tells us that conditioning on this single number is sufficient to eliminate confounding from observed variables. We typically estimate it with logistic regression.

Fifth, propensity score matching. Match treated and control trainers on their estimated propensity scores. It is computationally simple, but it can increase covariate imbalance if the propensity score model is wrong. Always check balance afterward.

Sixth, subclassification. Divide the propensity score into strata, estimate treatment effects within each stratum, and combine them. This uses all observations and avoids discarding data. Five strata remove roughly ninety percent of bias from a single confounder.

Seventh, covariate balance assessment. Standardized mean differences, variance ratios, and Love plots are essential diagnostics. The goal of matching is balance, not prediction. If the SMD is below zero point one for every covariate, you have a good match.

Eighth, limitations. Matching adjusts only for observed confounders. Unobserved confounders, positivity violations, and model dependence remain threats. These motivate the methods we will learn in the chapters ahead.

[pause]

NARRATOR: Let me put this chapter in the arc of our journey. In Pallet Town, we learned the language of potential outcomes. In Pewter City, we saw that randomization solves the causal inference problem by design. In Cerulean City, we learned to identify confounders using DAGs. Here in Vermilion City, we took our first step toward adjusting for those confounders in observational data -- finding each trainer's counterfactual twin. The naive fourteen-point gap shrank to about six points once we compared like with like. But the twin we found may not be as identical as we hoped. Hidden variables lurk beneath the surface. Our next challenges will equip us with more powerful tools to confront them.

Thunder Badge earned. On to Celadon City.

---

## Comprehension Check

NARRATOR: Before we leave Vermilion City, check yourself on these questions.

First: Why is the raw difference of fourteen point three points between Thunder Training graduates and non-participants not a valid estimate of the causal effect?

[long pause]

Because the trainers who chose Thunder Training were already stronger -- more badges, higher-level Pokemon, more battle experience. The raw difference confounds the causal effect with pre-existing selection bias. Matching corrects for this by comparing treated trainers to control trainers with similar observed characteristics.

Second: What is the propensity score, and why does the Rosenbaum-Rubin theorem matter?

[long pause]

The propensity score is the probability that a trainer received treatment given their observed covariates. The Rosenbaum-Rubin theorem says that if adjusting for the full set of covariates eliminates confounding, then adjusting for the propensity score alone is also sufficient. This lets us collapse a multidimensional matching problem into a one-dimensional one without losing the ability to control for confounders.

Third: What is the most important diagnostic after matching, and what threshold indicates success?

[long pause]

The most important diagnostic is covariate balance, measured by the Standardized Mean Difference for each covariate. An SMD below zero point one for every covariate indicates good balance. If any covariate has an SMD above zero point one, the researcher should re-specify the propensity score model, try a different matching method, tighten the caliper, or consider alternative estimation strategies.

Fourth: Name one thing matching cannot protect against, even when the code runs perfectly.

[long pause]

Unobserved confounders. Matching adjusts only for variables you include in the analysis. If there is a confounding variable you did not measure -- like patience or natural talent in our S.S. Anne example -- matching on observed covariates will not block the backdoor path through that unmeasured variable. The resulting estimate will be biased, and no amount of matching refinement can fix it. This is the fundamental limitation of all selection-on-observables methods.

---

*Next stop: Celadon City, where the Department Store has everything a trainer could want -- and where we will learn about regression, inverse probability weighting, and doubly robust estimation.*
