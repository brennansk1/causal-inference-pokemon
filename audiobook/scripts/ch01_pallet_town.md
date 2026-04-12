---
title: "Chapter 1: Pallet Town -- What Is Causal Inference?"
chapter_number: 1
source_file: "textbook/chapters/ch01_pallet_town.md"
estimated_runtime_minutes: 60
key_concepts:
  - Correlation vs. Causation
  - Confounders
  - Pearl's Ladder of Causation
  - The Fundamental Problem of Causal Inference
  - Potential Outcomes Framework (Rubin Causal Model)
  - Average Treatment Effect (ATE)
  - Selection Bias Decomposition
  - Counterfactual Reasoning
  - Key Assumptions (Ignorability, Positivity, Consistency, SUTVA)
characters:
  - NARRATOR (trainer, first-person, curious and conversational)
  - OAK (professor, patient teacher, plain-English definitions)
  - BLUE (rival, confident, makes causal reasoning errors)
---

# Chapter 1: Pallet Town -- What Is Causal Inference?

## Part 1: Correlation, Causation, and the Starter Debate

[SCENE: Early morning in Pallet Town. Birdsong. A door creaks open.]

NARRATOR: I wake up in a small house at the edge of a quiet town. Sunlight is pushing through the curtains. Downstairs, my mom is watching the morning news -- something about a new discovery on Route One. Today is the day I have been waiting for. Professor Oak has invited me to his laboratory to receive my very first Pokemon.

I have been thinking about this for weeks, obviously. Which one should I pick? The Grass type? The Fire type? The Water type? I have read every forum post, every article, every breakdown of League statistics I can find. And I still do not know.

I step outside. The cool Pallet Town air hits my face. And almost immediately, I hear an argument drifting from the road ahead.

Two trainers are standing nose to nose near the town gate. One of them is insisting that Charmander is the key to becoming Champion. The other one swears that Squirtle guarantees more Gym Badges. A small crowd has gathered. Everyone has anecdotes. Everyone has statistics pulled from the latest issue of Pokemon Trainer Monthly. Nobody agrees. One person is waving a chart on their phone. Someone else is citing their cousin's friend who swept the League with a Blastoise. It is the oldest argument in Pallet Town, and it shows no sign of resolution.

[pause]

I make my way to the lab, where Professor Oak is calibrating a Pokedex. His grandson Blue is already there, arms crossed, leaning against the wall. Blue has that smug look he always has -- like he has already figured out the answer to every question you have not even thought to ask yet.

BLUE: Professor, the data is clear. Trainers who pick Squirtle average six point eight Gym Badges. Charmander trainers average only five point nine. Squirtle is obviously superior.

NARRATOR: Oak sets down the Pokedex. He looks at me, then back at Blue.

OAK: Is it, though? If I gave this young trainer Charmander instead of Squirtle, would their journey turn out differently? And how could we ever know?

NARRATOR: Blue rolls his eyes. Oak smiles.

OAK: That is the question that will occupy us for the rest of this book.

---

[TEACHING SECTION]

NARRATOR: So here is the situation. Every year, a new group of trainers walks into Professor Oak's lab and faces the same choice: Bulbasaur, Charmander, or Squirtle. And every year, the same debate rages through the streets of Pallet Town. One camp cites league records showing that Water-type starters are associated with higher badge counts. Another camp points to Championship rosters dominated by Fire-type starters. Both sides wave data at each other. Neither side agrees.

What is going on? The trainers are confusing two fundamentally different ideas -- correlation and causation. And this confusion is not unique to Pallet Town. It is, arguably, the most common error in all of human reasoning. It is the entire reason that a field called causal inference exists.

[pause]

Let me start with what correlation actually means. Informally, two things are correlated when knowing something about one tells you something about the other. If trainers who pick Squirtle tend to earn more badges, then starter choice and badge count are correlated.

[OAK EXPLAINS: Correlation]

OAK: Correlation is measured on a scale from negative one to positive one. Positive one means two variables move together perfectly -- when one goes up, the other always goes up by the same proportional amount. Negative one means they move in perfectly opposite directions. Zero means there is no straight-line relationship at all. The key thing to remember is that correlation describes a pattern in what you can see. It tells you what tends to happen together. It does not, by itself, tell you what would happen if you stepped in and changed something.

NARRATOR: In other words, correlation is about patterns in observed data. That is it. It does not tell you about cause and effect.

Now, Oak has some data from the Kanto Trainer Registry. The numbers go like this. Trainers who chose Bulbasaur earned an average of five point four badges with a win rate of fifty-two percent. Charmander trainers did a bit better -- five point nine badges and a fifty-six percent win rate. And Squirtle trainers came in highest at six point eight badges and a sixty-one percent win rate.

[BLUE'S MISTAKE]

BLUE: See? I told you. Squirtle trainers earn almost a full badge more than Charmander trainers. Case closed. Pick the turtle.

OAK: Not so fast, Blue. You are looking at a pattern in the data -- that is correlation. But you are claiming something much stronger. You are claiming that choosing Squirtle causes a trainer to earn more badges.

NARRATOR: And there is the distinction. Causation is a claim about what would happen under an intervention. To say "choosing Squirtle causes you to earn more badges" is to claim that if we could take a specific trainer and force them to pick Squirtle rather than Charmander -- holding everything else about that trainer constant -- they would earn more badges. That is a much stronger claim than just noticing that Squirtle trainers happen to do better.

Correlation says: "Trainers who pick Squirtle happen to earn more badges." Causation says: "If you picked Squirtle, you would earn more badges." The first is a statement about patterns in data. The second is a statement about a mechanism in the world.

[pause]

So why might correlation fail to capture causation? The answer, in a single word, is confounders.

[OAK EXPLAINS: Confounders]

OAK: A confounder is a variable that influences both the treatment and the outcome at the same time. It creates a spurious association -- a statistical relationship that looks real but is actually being driven by this lurking third factor.

NARRATOR: Here is an example that makes this concrete. Suppose trainers from Cerulean City -- a wealthy, water-themed city -- disproportionately choose Squirtle. Makes sense, right? Water city, Water-type starter. But Cerulean trainers also tend to come from families with more resources. They have better training equipment. They have access to expensive held items like Leftovers and Choice Bands. They can afford private tutoring from retired Gym Leaders. These advantages help them earn more badges regardless of which starter they pick.

So in this scenario, wealth is a confounder. It affects starter choice -- Cerulean kids tend to pick Water types. And it affects badge count -- Cerulean kids have resources that help them win. The observed correlation between Squirtle and badges is partly, and maybe entirely, driven by this confounder.

BLUE: Come on. I looked at the league data. Squirtle trainers earn zero point nine more badges than Charmander trainers on average. The numbers do not lie.

OAK: The numbers do not lie, Blue, but they do not tell the whole story. You are ignoring a critical possibility: wealthy trainers from Cerulean City disproportionately pick Water types, and they also buy better items, hire better tutors, and enter more competitions. The association between Squirtle and badges may have nothing to do with Squirtle itself.

NARRATOR: Blue has made the classic mistake. He has confused correlation with causation. This mistake is so common it has its own Latin phrase: cum hoc ergo propter hoc -- "with this, therefore because of this."

And this is not a made-up problem. In real observational studies across medicine, economics, and the social sciences, confounders routinely create misleading associations. The history of science is full of confident causal claims that turned out to be confounded.

For decades, doctors observed that women who took hormone replacement therapy had lower rates of heart disease. It seemed like a clear win. But when randomized trials were finally conducted, the therapy actually slightly increased heart disease risk. The original association was confounded: women who chose the therapy tended to be wealthier and more health-conscious, and those traits were doing the heavy lifting -- not the hormones.

Class size and student achievement? Same pattern. Schools in affluent areas tend to have smaller classes and higher test scores, but that correlation reflects neighborhood wealth, not the causal effect of shrinking a classroom. Hospital quality and mortality rates? Hospitals that treat the sickest patients often have the worst survival statistics -- not because they are bad hospitals, but because their patient population starts out in worse shape.

Again and again, people looked at correlations, jumped to causal conclusions, and got burned.

[pause]

[TEACHING SECTION]

NARRATOR: Now I want to tell you about something that helped me organize all of these ideas in my head. It comes from a computer scientist and philosopher named Judea Pearl, and he calls it the Ladder of Causation. It is a hierarchy -- three rungs -- and each rung represents a fundamentally different type of question.

[OAK EXPLAINS: Pearl's Ladder of Causation]

OAK: Rung One is Association, which you can think of as "Seeing." Questions at this level ask about patterns in observed data. What do we see when we look at the numbers? For example: "What is the average badge count among trainers who chose Squirtle?" You can answer this question by looking at the Kanto Trainer Registry. No intervention required. You simply filter the data to Squirtle trainers and compute the average.

Rung Two is Intervention, which you can think of as "Doing." Questions at this level ask what would happen if we actively changed something in the world. For example: "If we assigned trainers to use Squirtle, regardless of their preferences, what would their average badge count be?" This question cannot be answered from observational data alone. It requires either an experiment where you randomly assign starters, or a set of assumptions strong enough to bridge the gap.

The critical difference is this. On Rung One, you are looking at trainers who happened to choose Squirtle, and those trainers might be different from everyone else in all sorts of ways. On Rung Two, you are imagining what would happen if you stepped in and assigned Squirtle to everyone, which would break the connection between starter choice and all those confounding factors.

And then there is Rung Three: Counterfactual, which you can think of as "Imagining." Questions at this level ask about what would have happened in a specific case under a different scenario. For example: "Ash chose Charmander and earned six badges. How many badges would he have earned if he had chosen Bulbasaur instead?" This is the most demanding type of question. It requires reasoning about a specific individual in a specific alternative scenario -- not just average effects across a whole population.

NARRATOR: Here is the critical insight. Each rung of the ladder strictly requires more information than the one below it. You cannot answer Rung Two questions with Rung One data alone. And you cannot answer Rung Three questions with Rung Two information alone. The ladder is a one-way escalator. You can always go down -- if you know the answer to a Rung Two question, you certainly know the answer to the corresponding Rung One question. But you cannot go up. Seeing cannot get you to Doing. Doing cannot get you to Imagining.

BLUE: Come on, Professor. Data is data. If I have enough of it, I can answer any question.

OAK: That is a common belief, Blue, and it is wrong. No amount of Rung One data can answer a Rung Two question. You would need either an experiment or a set of causal assumptions to bridge that gap. The data tells you what is. Only causal reasoning can tell you what would be.

NARRATOR: This explains why so many debates -- in science and in Pallet Town -- go around in circles. People try to answer Rung Two or Rung Three questions using Rung One data. They look at patterns in what they can see and try to draw conclusions about what would happen if they intervened, or what would have happened if things had been different. But the data alone cannot get them there. To climb the ladder, you need something more.

[pause]

And that brings us to what might be the central lesson of this entire book.

OAK: Data alone cannot establish causation. No matter how large your dataset, no matter how sophisticated your statistical model, you cannot move from association to intervention without making assumptions about the underlying causal structure of the world. This is not a failure of statistics. It is a fundamental feature of the problem.

NARRATOR: The good news is that we have powerful tools for making these assumptions explicit, checking whether they are plausible, and working out their implications. That is what the rest of this book is about. We are going to learn to draw causal diagrams, to figure out when causal effects can be estimated from observational data, and to design experiments and quasi-experiments that let us make credible causal claims.

But first, we need to understand the fundamental challenge that makes all of this necessary.

OAK: Let me give you one more example to drive this home. Suppose a Pokemon Center notices that trainers who use Hyper Potions have higher win rates than those who use regular Potions. Should the Center recommend Hyper Potions to all trainers? Not necessarily. Trainers who buy Hyper Potions may be wealthier, more experienced, or more dedicated. The observed correlation may reflect these underlying differences, not the effect of the potion itself. Recommending Hyper Potions based on this correlation alone could waste money without improving outcomes. To make a sound recommendation, the Center would need to estimate the causal effect -- which requires either a randomized experiment or a careful observational study with credible assumptions.

NARRATOR: That is the real-world stakes of getting this right. Correlation can mislead you into spending money, changing policy, or making decisions based on patterns that have nothing to do with actual cause and effect. Causation is what matters when you need to act. And the gap between the two -- the methods for bridging it, the assumptions required, the traps to avoid -- that is where causal inference lives. That is what this entire book is about.

[pause]

---

## Part 2: The Fundamental Problem and the Potential Outcomes Framework

[SCENE: Inside Professor Oak's lab. Three Poke Balls sit on a table.]

NARRATOR: I stand before three Poke Balls on Oak's table. They are arranged in a neat row. Bulbasaur on the right. Squirtle in the middle. Charmander on the left. My hand hovers. I think about everything I have read, everything I have heard, all those arguments in the street. And then I stop thinking and just reach. I pick up the one on the left.

The Poke Ball opens, and Charmander appears on the table. A small orange lizard with a flame dancing on the tip of its tail. It blinks up at me. I feel a rush of excitement -- this is my partner.

Blue pushes off the wall, walks over, and grabs Squirtle without hesitation.

BLUE: Good luck with that.

NARRATOR: He walks out the door without looking back. Typical Blue. Professor Oak watches me bond with Charmander for a quiet moment -- the little fire lizard is already nuzzling my hand. And then Oak says something that will stay with me for the entire journey.

OAK: You have made your choice. And now there is something you will never, ever know: what would have happened if you had chosen Bulbasaur.

[pause]

NARRATOR: At first, this sounds like a throwaway comment. Something a quirky old professor would say to be dramatic. But Oak is deadly serious. And the more I think about it, the more I realize he is right. This is not a limitation of technology or data. It is not something that could be solved with a better Pokedex or a larger survey. It is a logical impossibility. I cannot both choose Charmander and not choose Charmander at the same time. The moment I pick up that Poke Ball, the other two paths through reality cease to be observable.

[pause]

[TEACHING SECTION]

NARRATOR: This idea has a name. It is called the Fundamental Problem of Causal Inference, and it was articulated most clearly by a statistician named Paul Holland in nineteen eighty-six. Here is the core statement.

OAK: The Fundamental Problem of Causal Inference is this: it is impossible to observe both potential outcomes for the same unit. At most one potential outcome is ever observed. The other is forever missing.

NARRATOR: Let me make this concrete. Suppose we want to know the causal effect of choosing Charmander versus Bulbasaur on the number of Gym Badges a trainer earns. For a specific trainer -- let us call him Ash -- there are two potential realities.

In Reality A, Ash chooses Charmander and earns some number of badges. In Reality B, Ash chooses Bulbasaur and earns some number of badges. The individual causal effect for Ash is simply the difference between these two numbers -- the badges he would earn with Charmander minus the badges he would earn with Bulbasaur.

The problem? We can only ever see one of these realities. If Ash picks Charmander, we observe what happens with Charmander, but what would have happened with Bulbasaur is forever unknown. If he picks Bulbasaur, the reverse is true. We can never observe both.

[pause]

One powerful way to think about this is through the lens of missing data. Imagine you could lay out a table tracking five trainers who each chose between Charmander and Bulbasaur. You have two columns for potential outcomes: badges with Charmander, and badges with Bulbasaur.

Ash chose Charmander and earned six badges. So you write six in the Charmander column. But the Bulbasaur column? Question mark. You have no idea. Misty chose Bulbasaur and earned seven badges. So you write seven in the Bulbasaur column, but the Charmander column is a question mark. Brock chose Charmander and got eight badges. Gary chose Bulbasaur and got five. Erika chose Charmander and got four. Every single row has exactly one observed number and one question mark. There are no exceptions.

And this is not an accident of bad data collection. It is not something that more funding or better technology could fix. It is a structural feature of reality itself. Each trainer walked one path. The other path is counterfactual -- it exists in the realm of "what might have been," but not in the realm of observable fact. Because each individual causal effect requires both potential outcomes, and we can observe at most one, we can never compute the causal effect for any specific person. Every single individual effect is unknowable.

[THINK ABOUT THIS]

NARRATOR: Now, you might be thinking: could Ash just choose Charmander, complete his journey, then go back in time and choose Bulbasaur? Setting aside the physics for a moment, even this thought experiment fails. The Ash who returns to choose Bulbasaur is not the same Ash. He now has memories and experience from his Charmander journey. The person has changed.

What about trying both options on separate occasions? Well, the second journey happens at a different time, in different conditions, with an older and more experienced trainer. The causal effect of starter choice at one point in time cannot be identified by observing the same person at a completely different point in time.

This is why the fundamental problem is truly fundamental. It is not a gap in our data. It is a feature of the logical structure of causation itself.

NARRATOR: I am starting to wonder if Oak is going to tell me the whole thing is hopeless. But he is not done.

OAK: But before you lose hope, here is the crucial insight. While individual causal effects are unknowable, average causal effects across populations can sometimes be identified -- under the right assumptions. We cannot know what would have happened to Ash specifically if he had chosen differently. But if we set things up correctly, we can learn about the average effect of starter choice across many trainers. The shift from individual effects to average effects, combined with assumptions about how treatment is assigned, is the foundation of modern causal inference.

NARRATOR: And that is the way forward. When Professor Oak randomly assigns starters to trainers in a controlled experiment -- literally flipping a coin to decide who gets what -- something remarkable happens. The average of the missing potential outcomes in the treatment group equals, in expectation, the average of the observed outcomes in the control group. The groups are balanced not just on the things you can see, but on the things you cannot see, too.

Randomization does not solve the fundamental problem for any one individual. Ash will still never know what would have happened with Bulbasaur. But it solves the problem on average, across many trainers -- and that turns out to be enough for science. It is enough to guide decisions. It is enough to separate the signal from the noise.

[pause]

---

[TEACHING SECTION]

NARRATOR: All right. We have established the fundamental problem. Individual causal effects are unknowable. But average effects are sometimes within reach. Now we are ready to get precise about all of this -- to build the formal machinery that makes rigorous causal reasoning possible.

The framework we are going to use is called the Rubin Causal Model, also known as the potential outcomes framework. It was developed by a statistician named Donald Rubin in the nineteen seventies and extended by many others since then. It is, in many ways, the standard language of modern causal inference.

Here is the setup. Imagine a population of trainers. Each trainer may or may not receive a treatment. For a concrete example, let us say the treatment is using an Exp. Share -- an item that distributes experience points across a trainer's entire Pokemon team.

For each trainer, we define a treatment indicator. It equals one if the trainer uses Exp. Share, and zero if they do not.

Then, for each trainer, we define two potential outcomes. The first is the number of badges they would earn if they used Exp. Share. The second is the number of badges they would earn if they did not use Exp. Share. Both of these potential outcomes are defined for every trainer, regardless of whether they actually receive the treatment. They represent the outcomes that would happen under each condition.

[OAK EXPLAINS: Potential Outcomes]

OAK: Think of each trainer as having two possible futures: one where they use Exp. Share and one where they do not. Both futures are real in the sense that they are well-defined. But only one of them will ever actually happen -- only one will ever be observed. The pair of potential outcomes is the foundation on which everything else is built.

NARRATOR: The individual treatment effect for any specific trainer is simply the difference between their two potential outcomes. How many more badges would they earn with Exp. Share compared to without it? If a trainer would earn seven badges with Exp. Share and five without, their individual treatment effect is two badges. Simple subtraction.

But as we just discussed, this individual effect is never directly observable, because we can only see one of the two potential outcomes for any given trainer. We are right back at the fundamental problem.

[pause]

So we turn to population-level summaries. The most common one is called the Average Treatment Effect, or ATE.

[OAK EXPLAINS: Average Treatment Effect]

OAK: The Average Treatment Effect answers this question: if we could somehow observe both potential outcomes for every trainer in the population and take the difference, what would the average of those differences be? It is the expected effect of treatment, averaged across everyone.

NARRATOR: There are two close cousins of the ATE. The first is the Average Treatment Effect on the Treated, or ATT. This one restricts attention to the trainers who actually received treatment. Among the trainers who used Exp. Share, what was the average causal effect?

The second is the Average Treatment Effect on the Control, or ATC. This one focuses on the untreated group. Among trainers who did not use Exp. Share, how much would they have benefited, on average, if they had?

OAK: These three quantities -- ATE, ATT, and ATC -- are not the same in general. They coincide only when the treatment effect is identical for everyone, or when treatment assignment is completely independent of potential outcomes. Otherwise, each one tells you something different. The ATE is the average effect across the whole population. The ATT tells you about the people who actually got treated. The ATC tells you about the people who did not. The ATE is a weighted average of the ATT and the ATC, where the weights are the proportions of the population in each group.

[pause]

NARRATOR: Now, in practice, what we actually observe is exactly one potential outcome per trainer. The observed outcome follows what is called the switching equation. It is simple logic: if a trainer used Exp. Share, we observe their outcome under Exp. Share. If they did not use it, we observe their outcome without it. The treatment status acts like a switch that selects which potential outcome we get to see.

The most natural thing to do when trying to estimate a causal effect is to just compare the average outcomes between the two groups. You take the average badges among trainers who used Exp. Share, subtract the average badges among those who did not, and call that the effect. This is the naive estimator.

But here is where things get tricky.

[OAK EXPLAINS: The Selection Bias Decomposition]

OAK: The naive comparison of group averages does not, in general, give you the causal effect. It gives you the causal effect plus something called selection bias. Here is what is going on. The naive estimate equals the ATT -- the real causal effect among the treated -- plus a bias term. That bias term measures the difference in baseline outcomes between the treatment and control groups. In other words, it measures how different these groups would have been even in the absence of treatment.

Selection bias is zero only when the treatment and control groups have the same average potential outcome under the control condition -- meaning they would have done equally well, on average, even without treatment. This holds by design in a randomized experiment. But it is often violated in observational data.

[BLUE'S MISTAKE]

BLUE: I ran the numbers. Exp. Share users average seven point two badges. Non-users average five point eight. That is a one point four badge effect. Pretty impressive, right?

OAK: Blue, you are ignoring the fact that trainers who seek out and use Exp. Share are probably more dedicated, more strategic, and more experienced. They would earn more badges even without the item. Part of that one point four badge gap -- maybe all of it -- is selection bias, not a causal effect of the item.

NARRATOR: That is the crux of it. When people self-select into treatment -- when they choose for themselves whether to use Exp. Share, whether to take a medication, whether to enroll in a program -- the treated group and the control group almost always differ in ways that have nothing to do with the treatment itself. The go-getters sign up. The cautious ones opt out. The wealthy can afford it. The informed seek it out. All of those differences contaminate the naive comparison, making it look like the treatment is more effective, or less effective, than it really is.

[pause]

Let me walk through a concrete example to make all of this tangible. Professor Oak runs a study with six trainers. Now, imagine he has access to a parallel-universe machine -- purely for educational purposes -- so he can see both potential outcomes for every trainer. He would never have this in real life, but it helps us understand the math.

Here is what he finds. Ash used Exp. Share and would earn seven badges with it, five without -- so his individual effect is two. Misty did not use Exp. Share; she would earn eight with it and seven without -- her effect is one. Brock used it; six with, four without -- effect of two. Erika did not use it; five with, three without -- effect of two. Surge used it; eight with, six without -- effect of two. Sabrina did not; seven with, six without -- effect of one.

The ATE -- the average effect across all six trainers -- is the average of two, one, two, two, two, and one, which comes out to about one point six seven.

The ATT -- just among the treated trainers Ash, Brock, and Surge -- is the average of two, two, and two, which is exactly two.

The ATC -- among the control group of Misty, Erika, and Sabrina -- is the average of one, two, and one, which is about one point three three.

And you can verify: the ATE equals one half times the ATT plus one half times the ATC, which is one half times two plus one half times one point three three, giving us one point six seven. It checks out.

[pause]

Now, in practice, we do not have Oak's parallel-universe machine. We only observe seven badges for Ash (because he used Exp. Share), seven badges for Misty (because she did not), six for Brock, three for Erika, eight for Surge, and six for Sabrina. The naive estimator is the average among the treated -- seven plus six plus eight divided by three, which is seven -- minus the average among the control -- seven plus three plus six divided by three, which is about five point three three. The naive estimate is one point six seven.

That happens to match the ATE in this case. But do not be fooled -- that is a numerical coincidence. When we decompose the naive estimator, we find the ATT is two, and the selection bias is negative zero point three three. The treated trainers actually had lower baseline potential outcomes than the controls -- perhaps because less naturally talented trainers were the ones who sought out Exp. Share. The naive estimator underestimates the ATT but overshoots it because of the negative bias pulling it down.

[THINK ABOUT THIS]

NARRATOR: Here is another example that reveals a subtle but important point. Imagine a study of whether using a Rare Candy before the first Gym battle improves the chance of winning. There are four trainers. Red used a Rare Candy and won -- but he would have won anyway. Leaf used a Rare Candy and won -- she would have lost without it. Silver did not use a Rare Candy and won -- he would have won either way. Kris did not use one and lost -- she would have lost either way.

The true ATE is zero point two five -- only one out of four trainers actually benefits.

But the naive estimator? The two treated trainers both won, so their average is one. Of the two control trainers, one won and one lost, so their average is zero point five. The naive estimate is zero point five -- which is double the true ATE.

Here is the twist: the selection bias in baseline outcomes is actually zero. Both groups have the same average outcome under the control condition. So where is the discrepancy coming from? The naive estimator correctly recovers the ATT, not the ATE. And the ATT and ATE differ because the treatment effect is different for different people, and the people who benefited most happened to end up in the treatment group.

OAK: This is worth pausing on. Even with zero selection bias in baseline outcomes, the naive estimator recovers the ATT, not the ATE. And the two can differ whenever treatment effects vary from person to person and are correlated with who actually gets treated.

NARRATOR: Think about what that means in practice. You might have a situation where the naive comparison looks perfectly clean -- the two groups had the same baseline potential -- and you would still be getting a misleading picture of the overall effect. Not because anyone is lying or because the data is bad, but because the people who chose to get treated are the ones who benefit most. The naive estimator is telling you about them specifically, not about everyone.

This is why simply "running the numbers" is never enough. You have to think about what those numbers actually represent and which population they apply to.

[pause]

NARRATOR: One last thing before we move on. The assignment mechanism -- the process that determines which units receive treatment -- is the key to the entire enterprise of causal inference. Different assignment mechanisms require different strategies for identifying causal effects.

When treatment is randomly assigned, like flipping a coin, we get a randomized experiment -- that is Chapter Two. When treatment depends on potential outcomes only through observed characteristics like trainer experience or hometown, we can use techniques like matching and regression -- Chapters Three through Five. When an external variable pushes trainers toward treatment without directly affecting the outcome, we can use instrumental variables -- Chapter Six. When treatment is determined by whether some measure crosses a threshold, we get regression discontinuity -- Chapter Seven. And when the timing of treatment varies across groups and time periods, we can use difference-in-differences -- Chapter Eight.

Each chapter in this book introduces a different identification strategy for a different type of assignment mechanism. But they all rest on the same foundation -- the potential outcomes framework, the selection bias decomposition, the key assumptions -- everything we have built here in Pallet Town. This chapter is the bedrock. Everything that follows is built on top of it.

---

## Part 3: Counterfactuals and the Causal Toolkit

[SCENE: Route One. Tall grass. The sound of rustling.]

NARRATOR: Charmander and I take our first steps onto Route One. The tall grass swishes against my ankles. The air smells like pine and wild berries. And almost immediately, the grass rustles violently and a wild Pidgey bursts out. Charmander steps forward, the flame on its tail flaring up, and launches an Ember attack. The Pidgey goes down.

Pretty smooth. But as we keep walking, I catch myself wondering. What if I had picked Bulbasaur? Would I be struggling right now against these Normal-type Pidgeys? Or would Vine Whip have made this fight even easier? What if I had picked Squirtle -- would I already be ahead of Blue?

This kind of thinking -- reasoning about events that did not happen but could have -- is called counterfactual reasoning. And it is so natural, so automatic, that we barely notice ourselves doing it. Every trainer who loses a battle thinks, "If only I had used a different move." Every researcher who observes an outcome wonders, "What would have happened under different conditions?" Every person who has ever made a choice thinks, at some point, about the path not taken.

[OAK EXPLAINS: Counterfactuals and Possible Worlds]

OAK: The philosopher David Lewis developed a formal way to think about counterfactual statements. He used the concept of possible worlds. When you say, "If Ash had chosen Bulbasaur, he would have earned seven badges," you are making a claim about the closest possible world to our own in which Ash chose Bulbasaur. The closest world is not one where the laws of physics are different or where Kanto has sixteen Gyms. It is the world that is identical to ours in every respect except that Ash's hand moved to a different Poke Ball.

This philosophical framework maps directly onto the potential outcomes framework. The counterfactual outcome -- how many badges Ash would have earned with Bulbasaur -- is precisely the outcome in that closest possible world. The potential outcomes framework and Lewis's possible worlds are, in essence, two different languages for the same idea.

NARRATOR: So every potential outcome is, at its core, a counterfactual. It describes what would happen to a specific person under a specific condition. The observed outcome is the potential outcome that was actually realized. The unobserved potential outcome is the counterfactual -- the outcome that would have been observed if treatment had been different.

And when we define the individual causal effect as the difference between two potential outcomes, we are defining it as the gap between an actual outcome and a counterfactual outcome.

[pause]

[TEACHING SECTION]

NARRATOR: It is useful to distinguish two types of causal questions. The first type is called "effects of causes," or forward-looking questions. These start with a cause and ask about its effect. For example: "What is the effect of Exp. Share on badge count?" The potential outcomes framework is tailor-made for this. We define the treatment, specify potential outcomes, and estimate something like the ATE.

The second type is called "causes of effects," or backward-looking questions. These start with an observed effect and ask which cause is responsible. For example: "Why did Ash earn only six badges? Was it because he chose Charmander?" These questions are fundamentally harder because they require reasoning about specific counterfactual scenarios for specific individuals -- Rung Three of Pearl's Ladder.

OAK: Statistics is generally better suited to "effects of causes" than "causes of effects." When we estimate the ATE, we are answering: what is the effect of this cause? But when a trainer wonders why they lost a particular battle, they are asking about the causes of a specific effect -- a question that requires individual-level counterfactual reasoning, which is fundamentally unobservable.

NARRATOR: That does not mean backward-looking questions are unimportant. They are central to legal reasoning -- was the factory's pollution the cause of this person's illness? They matter for policy evaluation -- did this education reform actually cause the improvement we observed? And they are everywhere in everyday life -- did choosing Charmander cost me that Gym Badge against Misty? These questions matter enormously. But they are harder to answer rigorously, and doing so requires additional tools that we will return to in later chapters.

[BLUE'S MISTAKE]

BLUE: I just lost to the Elite Four. And I can tell you exactly what went wrong. I would have won if I had used my Alakazam instead of Pidgeot in the final battle. No question.

OAK: Blue, that is a specific counterfactual claim about a single moment in a single battle. It feels obviously true to you, but it is impossible to verify. Perhaps using Alakazam would have prompted your opponent to switch strategies, leading to a different loss. Counterfactual claims about individuals are inherently speculative, no matter how confident they feel. This is the fundamental problem in action.

NARRATOR: Oak is right. We all do this. We replay events in our minds -- that battle, that decision, that one moment where things went wrong -- and we feel absolutely certain that one different choice would have changed everything. But certainty is not the same as knowledge. The feeling of knowing is not the same as actually knowing. Counterfactual claims about specific individuals in specific situations are, strictly speaking, beyond what we can ever prove. And recognizing that takes a kind of intellectual humility that does not come naturally. It certainly does not come naturally to Blue.

[pause]

---

[TEACHING SECTION]

NARRATOR: All right. We have covered the big ideas. Now I want to run through the key terms that will follow us through the rest of this journey -- a kind of causal Pokedex, if you will. Every student of causal inference needs a reference for these concepts, and this is ours.

[OAK EXPLAINS: Key Terminology]

OAK: Let me walk through the essential terms. First, treatment. This is the variable whose causal effect we want to study. It is the thing we are asking about. Using an Exp. Share versus not using one. Choosing Charmander versus Squirtle. Training on Route One versus Route Two.

Second, outcome. This is the variable we measure to assess the effect of treatment. Number of Gym Badges earned, win rate in battles, time to complete the Pokemon League.

Third, unit. This is the entity for which we define potential outcomes. Usually it is an individual trainer, but it could be a Pokemon, a battle, or a Gym, depending on the research question.

Fourth, the assignment mechanism. This is the process that determines which units receive treatment. It is the key to the entire enterprise. Is it random, like Oak flipping a coin? Or is it driven by the trainers' own choices and characteristics? The nature of the assignment mechanism determines which tools we need to identify causal effects.

NARRATOR: Those are the building blocks. Now let me cover a few more concepts that show up everywhere in this field.

OAK: A confounder is a variable that causally affects both the treatment and the outcome. Trainer experience is a perfect example. Experienced trainers are more likely to use advanced items and more likely to earn badges regardless. If we do not account for experience, the observed association between the item and badges will overstate the true causal effect.

A mediator is different. It sits on the causal pathway between treatment and outcome. Suppose Exp. Share causes Pokemon to level up faster, which in turn causes more Gym wins. Pokemon level is a mediator. If you control for it, you block the very causal channel you are trying to measure, and you might find no effect even when the effect is real.

And then there is a collider -- a variable that is caused by two or more other variables simultaneously. This one is tricky because conditioning on a collider can create a spurious association between its causes. Suppose both having a strong starter and having natural talent make a trainer more likely to get into the Pokemon Hall of Fame. If you restrict your analysis to Hall of Fame trainers, you may find a negative association between starter strength and talent -- because among Hall of Famers, those with weaker starters must have compensated with greater talent. That association is entirely spurious. It only appears because you conditioned on the collider.

NARRATOR: Confounders, mediators, and colliders. Three different roles a variable can play, and each one has different implications for how we should handle it in our analysis. Getting this wrong can lead to badly biased estimates or, worse, to causal conclusions that are exactly backwards.

Let me say that one more time because it matters. A confounder is a common cause of both the treatment and the outcome -- you need to adjust for it. A mediator is on the pathway from treatment to outcome -- if you adjust for it, you block the very effect you are trying to measure. And a collider is caused by both treatment and outcome -- if you condition on it, you create a spurious association that was not there before. Same statistical operation -- conditioning on a variable -- but with completely different consequences depending on the variable's role in the causal structure. This is why causal diagrams, which we will learn about in later chapters, are so important. They tell you which variables to adjust for and which ones to leave alone.

[pause]

OAK: Now, the key assumptions. These are the conditions we need to hold for our causal estimates to be valid.

First, ignorability -- sometimes called unconfoundedness or conditional independence. This means that treatment assignment is independent of potential outcomes, at least after you condition on observed characteristics. In plain English, it means that within groups of trainers who look the same on measurable traits, whether someone gets treated has nothing to do with what their outcomes would be. If this holds, you can remove confounding by controlling for those traits.

Second, positivity, also called overlap. For every combination of characteristics in the population, there must be a positive probability of receiving each treatment. You need both treated and untreated trainers in every subgroup. If every trainer from Cerulean City uses Exp. Share and no trainer from Lavender Town does, you cannot compare treated and untreated trainers within those subgroups. You need some variation everywhere.

Third, consistency. The treatment must be well-defined. If a trainer uses Exp. Share, their observed outcome must equal their potential outcome under Exp. Share. This sounds obvious, but it requires that "using Exp. Share" means the same thing for everyone. If some trainers equip it to their lead Pokemon and others equip it to their weakest, those are different versions of treatment, and the analysis breaks down.

[pause]

And fourth, SUTVA -- the Stable Unit Treatment Value Assumption. This has two parts. The first is no interference: one trainer's treatment should not affect another trainer's outcome. Whether your rival uses Exp. Share should not change how many badges you earn. The second part is no hidden variations of treatment, which overlaps with consistency.

NARRATOR: SUTVA sounds technical, but the interference piece is really intuitive once you think about it. Imagine trainers competing for limited Gym slots. If one trainer's team gets stronger because of Exp. Share, it might actually make it harder for other trainers to beat the Gym. That would be interference -- one person's treatment affecting another person's outcome. When that happens, the whole framework has to be generalized.

OAK: SUTVA is easy to state but easy to violate. In many real-world settings, units interact. One person's vaccination protects their neighbors. One firm's pricing strategy affects competitors' sales. When SUTVA fails, we need to redefine the unit or the treatment. We will come back to this in Chapter Ten.

NARRATOR: So there you have it. Four key assumptions: ignorability, positivity, consistency, and SUTVA. They are the load-bearing walls of causal inference. Without them, the whole structure cannot support credible causal claims. With them, we can build something solid.

[pause]

I look down at Charmander. The little fire lizard is asleep in my arms as we walk through the last stretch of Route One. The sun is starting to set, and Viridian City's lights are flickering on in the distance. I have been thinking about everything Oak said, and I realize something. Every choice I make on this journey -- which Pokemon to catch, which items to use, which routes to take -- is, in a way, a causal question. And I will never get to see the paths I did not walk. But if I set things up carefully, if I think clearly about what I am comparing and why, I can still learn something real about what works and what does not.

That is the promise of causal inference. Not perfect knowledge about individual counterfactuals, but rigorous knowledge about average effects, built on explicit assumptions and careful reasoning.

---

## Chapter Summary

NARRATOR: Let me step back and pull all of this together. We covered a lot of ground in Pallet Town, and I want to make sure the big ideas are clear before we move on.

[pause]

First, and most fundamentally: correlation is not causation. Observed associations between variables can be driven by confounders -- common causes that affect both the treatment and the outcome. Moving from correlation to causation requires either experimental design or strong, explicit assumptions about the causal structure.

Second, the Fundamental Problem of Causal Inference. We can observe at most one potential outcome for each individual. The other potential outcome -- the counterfactual -- is forever missing. Individual causal effects are, therefore, unobservable.

Third, the Potential Outcomes Framework gives us a rigorous language for causal questions. Each person has two potential outcomes, one under treatment and one under control. The key quantities we want to estimate are the Average Treatment Effect, the Average Treatment Effect on the Treated, and the Average Treatment Effect on the Control.

Fourth, the selection bias decomposition. The naive comparison of group means does not give us the causal effect. It gives us the causal effect plus selection bias. That bias measures how different the treated and control groups would have been even without the treatment.

Fifth, Pearl's Ladder of Causation distinguishes three levels of causal reasoning: association, or seeing; intervention, or doing; and counterfactual, or imagining. Each level requires strictly more information than the one below it.

Sixth, counterfactual reasoning -- thinking about what would have happened under different conditions -- is the conceptual foundation of causal inference. The potential outcomes framework provides a rigorous language for counterfactual claims.

Seventh, the key assumptions for causal identification. Ignorability means no unmeasured confounders. Positivity means overlap between treatment groups. Consistency means a well-defined treatment. And SUTVA means no interference between units. Without these assumptions, causal effects generally cannot be identified from data.

And eighth, the assignment mechanism -- the process by which units are assigned to treatment -- is the central object of study. Different assignment mechanisms require different identification strategies, and those strategies are the subject of every chapter that follows.

[pause]

NARRATOR: Charmander grows stronger as we cross Route One. Viridian City passes in a blur of errands and close encounters with wild Rattata. Ahead lies Pewter City and its famous Rock-type Gym.

At the Pewter City Pokemon Center, I overhear Nurse Joy in a heated discussion with a group of trainers. She says she is tired of arguing about whether Protein actually makes Pokemon stronger, or whether trainers who buy Protein just happen to be more dedicated. She has an idea for how to settle it once and for all.

She looks at me. "We are going to run an experiment."

Tomorrow we head to Pewter City, where Nurse Joy has a radical idea for settling the Protein debate -- a radical idea called randomization. We will learn why random assignment is the gold standard for causal inference, how it eliminates selection bias by construction, and what happens when the real world refuses to cooperate.

Welcome to Chapter Two: Pewter City -- Randomized Experiments.

[pause]

---

## Comprehension Check

NARRATOR: Before we leave Pallet Town, check yourself on these questions.

First: What is the difference between correlation and causation, and why does observing one not justify claiming the other?

[long pause]

Correlation tells you what patterns exist in observed data -- what tends to happen together. Causation tells you what would happen if you intervened and changed something. Observing a correlation does not justify a causal claim because confounders -- variables that affect both the treatment and the outcome -- can create spurious associations that look like causal relationships but are not.

Second: State the Fundamental Problem of Causal Inference in one sentence, and explain why it is a logical impossibility rather than a practical limitation.

[long pause]

It is impossible to observe both potential outcomes for the same unit at the same time. This is not a practical limitation because counterfactual outcomes do not exist as observable quantities. They are, by definition, events that did not occur. No amount of better technology or larger data can overcome a logical impossibility.

Third: What is the selection bias decomposition, and what does it tell us about the naive comparison of group means?

[long pause]

The naive comparison of means equals the Average Treatment Effect on the Treated plus a selection bias term. The selection bias measures the difference in baseline outcomes between the treatment and control groups -- how different they would have been even without the treatment. When selection bias is not zero, the naive comparison over- or under-estimates the true causal effect.

Fourth: Name the three rungs of Pearl's Ladder of Causation and give a Pokemon example of each.

[long pause]

Rung One is Association, or Seeing: "What fraction of Squirtle trainers earned eight badges?" Rung Two is Intervention, or Doing: "If we assigned every trainer to use Squirtle, what would the average badge count be?" Rung Three is Counterfactual, or Imagining: "Ash chose Charmander and earned six badges -- how many would he have earned with Bulbasaur?" Each rung requires more information than the one below it.

Fifth: Name the four key assumptions for causal identification and briefly explain each one.

[long pause]

Ignorability means treatment assignment is independent of potential outcomes, conditional on observed characteristics -- in plain English, there are no unmeasured confounders lurking behind the scenes. If this holds, adjusting for the right observable traits removes the bias. Positivity means that for every type of unit in the population, there is a positive probability of being in either the treated or the control group -- you need overlap, you need comparison cases everywhere. Consistency means the treatment is well-defined and means the same thing for everyone -- no ambiguity about what "treated" means. And SUTVA, the Stable Unit Treatment Value Assumption, means one unit's treatment does not affect another unit's outcome, and there are no hidden variations of treatment.
