---
title: "Chapter 3: Cerulean City -- Observational Studies and Graphical Models"
chapter_number: 3
source_file: "textbook/chapters/ch03_cerulean_city.md"
estimated_runtime_minutes: 90
key_concepts:
  - Observational Studies
  - Confounding and Omitted Variable Bias
  - Selection Bias and Survivorship Bias
  - Berkson's Paradox (Collider Bias)
  - Simpson's Paradox
  - Directed Acyclic Graphs (DAGs)
  - Forks, Chains, and Colliders
  - d-Separation
  - The Backdoor Criterion
  - The Frontdoor Criterion
  - Structural Causal Models and the do-Operator
  - do-Calculus (Three Rules)
characters:
  - NARRATOR (trainer, first-person, curious and conversational)
  - OAK (professor, patient teacher, plain-English definitions)
  - BLUE (rival, confident, makes causal reasoning errors)
  - MISTY (Cerulean Gym Leader, sharp and data-driven)
  - BILL (eccentric researcher, enthusiastic about graphs and structure)
---

# Chapter 3: Cerulean City -- Observational Studies and Graphical Models

## Part 1: The Trouble with Observational Data

[SCENE: Cerulean City. The sound of flowing water. Footsteps on a stone bridge.]

NARRATOR: I step into Cerulean City with a fresh Boulder Badge pinned to my trainer card and the confidence of someone who has just run a proper randomized experiment. Back in Pewter City, I learned that randomization is the gold standard. It balances confounders, observed and unobserved, and it lets you estimate causal effects with clean authority. I left Pewter City feeling like I had the tools to answer any question.

But as I walk past the bike shop and toward the gleaming blue dome of the Cerulean Gym, a question begins to nag at me. What happens when you cannot randomize?

Cerulean City is built around water. There is the Cerulean Cave to the north, a treacherous cavern full of powerful wild Pokemon. There is the Cape to the east, where Bill the researcher lives in his lighthouse cottage. And in the heart of the city, there is the Gym, where Misty trains her Water-type team. Water, like observational data, flows where it will. You cannot command it into neat experimental channels. You have to learn to read its currents.

[pause]

I push open the gym doors. The inside is built around a massive pool. Misty is standing at the far end, arms crossed, staring at a laptop balanced on a diving board.

MISTY: Good. You are the trainer Oak sent. I have a problem, and I need someone who understands data.

NARRATOR: She waves me over and tilts the screen so I can see. It is a spreadsheet -- rows and rows of trainer records.

MISTY: Cerulean Cave, north of the city. You have heard of it. Trainers who survive its depths seem to emerge stronger. They win more gym badges, they perform better in league tournaments, and they command higher-level Pokemon. But I suspect the relationship is not so simple. I have five years of battle logs from two thousand trainers who passed through this city, and I want to know one thing. Does training in Cerulean Cave actually make trainers better? Or do better trainers simply choose to enter the Cave?

NARRATOR: I look at her data. It seems straightforward enough. There is a column for whether each trainer entered the Cave, and a column for how many gym badges they eventually earned. A simple comparison of means should answer her question, right?

MISTY: I already ran the naive comparison. Trainers who entered the Cave earned an average of five point eight badges. Trainers who did not averaged three point two. That is a difference of two point six badges. Should I conclude that Cave training causes a two point six badge improvement?

NARRATOR: Something in her tone tells me the answer is no.

[pause]

---

[TEACHING SECTION]

NARRATOR: Before we get into why that comparison is wrong, let me explain why Misty is stuck with observational data in the first place. Because there is a natural question here: if randomized experiments are the gold standard, why not just run one?

Three forces conspire against experimentation.

First, ethics. Misty cannot randomly force trainers into Cerulean Cave. The Cave is genuinely dangerous. Pokemon at levels far beyond what most trainers can handle roam its depths. Sending an unprepared trainer in there would be reckless and irresponsible. In the real world, we face the same constraint. We cannot randomly assign people to smoke, or to experience poverty, or to receive inferior medical care. Many of the most important causal questions involve treatments that would be unethical to assign.

Second, cost and feasibility. Running a randomized trial requires resources. Misty would need to intercept trainers arriving in Cerulean City, randomly assign half of them to train in the Cave while somehow enforcing that assignment, and then track their subsequent journey across the entire Kanto region. The logistics would be enormous, and trainers are free agents -- they do not take orders from gym leaders about where to go.

Third, timeliness. Misty has data right now. She has five years of battle logs sitting in the Cerulean Gym's Pokedex database. A new experiment would take a year or more to design, implement, and analyze. By then, the league season will be over and the information will be stale.

So observational data it is. It is abundant, it is cheap, and it already exists. But it comes with a trap.

[pause]

NARRATOR: Let me tell you about the trap. Misty's dataset has two thousand trainers. For each one, she observes whether they trained in the Cave, how many badges they earned, their years of experience, their starter Pokemon type, their family wealth, and a measured battle strategy score. There is also one more variable that she suspects matters enormously but cannot measure: natural talent. An innate ability for battling that some trainers just seem to have.

The naive comparison says Cave trainers earned two point six more badges. But here is the problem. Trainers who chose to enter the Cave are not a random sample. They tend to be more experienced -- they have survived enough of their journey to be confident about tackling a dangerous cavern. They tend to be wealthier -- they can afford healing items and escape ropes for the treacherous depths. And they tend to be more naturally talented, though Misty cannot measure that directly.

The comparison is contaminated. And the name for this contamination is confounding.

[OAK EXPLAINS: Confounding]

OAK: A confounder is a variable that influences both the treatment and the outcome, creating a spurious association that masquerades as a causal effect. Think of it as a hidden puppet master pulling strings on both sides. The confounder affects who gets treated and it affects the outcome, so when you compare treated and untreated groups, you are really comparing groups that differ in two ways: the treatment itself, and the confounder. You cannot separate the two effects just by looking at the raw numbers.

NARRATOR: Let me make this concrete with a character you already know.

[BLUE'S MISTAKE]

NARRATOR: I am standing outside the Cerulean Gym when Blue strolls up, Pidgeot preening on his shoulder.

BLUE: Cave training is the best thing I ever did. I trained in Cerulean Cave for two weeks, and look -- seven badges already. The data says Cave trainers earn two point six more badges. I rest my case.

NARRATOR: I ask him a simple question. Blue, you have been training Pokemon since you were five years old. Your grandfather is Professor Oak. You had a head start on every trainer in Kanto. How do you know it was the Cave and not your experience?

BLUE: Details.

NARRATOR: But they are not details. They are everything. Blue's mistake is the most fundamental error in causal reasoning. He has attributed all two point six extra badges to the Cave, but some -- maybe most -- of that difference comes from the fact that he was already an experienced, well-resourced trainer before he ever stepped foot inside.

[pause]

NARRATOR: Let me put precise numbers on Blue's error, because this is where it gets really instructive. Suppose the true data-generating process works like this. The true causal effect of cave training is zero point eight badges. That is what the Cave actually contributes. On top of that, each year of experience adds zero point five badges, regardless of whether you enter the Cave.

Now here is the key fact. In Misty's data, trainers who entered the Cave have, on average, three point six more years of experience than trainers who did not. The Cave-goers are a self-selected group of veterans.

[OAK EXPLAINS: Omitted Variable Bias]

OAK: When you leave out a relevant variable from your analysis, the bias follows a simple formula. The omitted variable bias equals the effect of the omitted variable on the outcome, multiplied by the relationship between the omitted variable and the treatment. In mathematical shorthand, it is the product of two quantities: how much the omitted variable affects badges, and how strongly the omitted variable correlates with cave training.

NARRATOR: So let us work through it. The effect of experience on badges is zero point five badges per year. The difference in experience between Cave and non-Cave trainers is three point six years. The omitted variable bias is zero point five times three point six, which equals one point eight.

That means the naive estimate of two point six is actually the true effect of zero point eight plus the bias of one point eight. Nearly seventy percent of the apparent Cave effect is actually just experience dressed up in a cave suit.

Blue's causal estimate is inflated by two hundred and twenty-five percent. He thinks the Cave gave him two point six extra badges. In reality, the Cave gave him zero point eight, and his years of training gave him the rest.

[pause]

NARRATOR: And here is what makes observational studies truly treacherous. Experience is not the only confounder. Wealth also confounds the relationship -- wealthier trainers can afford supplies for the Cave and better Pokeballs throughout their journey. Natural talent is another confounder -- more talented trainers select into Cave training and earn more badges. And natural talent, being unobserved, cannot be controlled for directly.

The total bias is the sum of every individual omitted variable bias. Even if you control for experience, the bias from wealth and natural talent remains. You can try to account for one confounder, then another, but if there is even one common cause that you cannot measure, your estimate is still wrong.

This is why observational studies are so dangerous. And this is why we need more sophisticated tools. But before we get to those tools, Misty has more bad news.

---

## Part 2: The Bias Family -- Selection, Survivorship, Simpson

[SCENE: Inside the Cerulean Gym office. Misty pours two glasses of water.]

NARRATOR: Misty sets a glass of water in front of me and opens a second set of concerns. Confounding, she explains, is not the only threat to observational studies. There is an entire family of related biases that arise not from omitted variables, but from how the sample itself is selected.

[OAK EXPLAINS: Selection Bias]

OAK: Selection bias occurs when the sample you are analyzing is not representative of the population you care about, and the reason for the non-representativeness is related to both the treatment and the outcome. You are not just looking at a random slice of the world. You are looking at a slice that was carved out by a process connected to the very things you are studying.

NARRATOR: Think about it this way. Misty's dataset contains trainers who reached Cerulean City -- the third city on the Kanto journey. But not every trainer who left Pallet Town made it this far. Some were defeated on Route One. Others gave up in Viridian Forest. Still others lost to Brock in Pewter City and went home.

The trainers who reached Cerulean City are survivors. They are, on average, stronger, more determined, and more talented than the full population of trainers who started their journey. If the factors that helped trainers survive long enough to reach Cerulean -- factors like talent and determination -- are also correlated with both Cave training and badge outcomes, then analyzing only the Cerulean sample distorts the relationship.

[pause]

NARRATOR: Now let me tell you about a specific and especially sneaky form of selection bias called survivorship bias. It is insidious precisely because the missing data is invisible. You do not see what you are missing.

MISTY: I found something troubling in the Protein supplement data from Pewter City. Let me show you.

NARRATOR: Remember from Chapter Two that Pewter City ran a randomized trial on Protein supplements. Suppose that among trainers who received Protein, some experienced adverse effects. Their Pokemon became over-aggressive and uncontrollable in battle, and those trainers quit their journey before reaching Cerulean City. If Misty analyzes the effect of Protein use in her Cerulean sample, she only sees the trainers for whom Protein worked well. The failures are gone. They dropped out. They are invisible.

MISTY: In my data, Protein users who reached Cerulean City average five point one badges. Non-users average four point three. That looks like a zero point eight badge advantage for Protein. But look at the full picture.

NARRATOR: Misty pulls up the complete records from Pewter City. Five hundred trainers received Protein. Only four hundred of them -- eighty percent -- made it to Cerulean. Five hundred trainers received a placebo. Four hundred and fifty of them -- ninety percent -- made it. The Protein caused a hundred trainers to drop out, and those dropouts are completely invisible in the Cerulean data.

When you look at everybody who started, including the dropouts, the average for Protein users is four point two badges and the average for non-users is four point zero badges. The true advantage is just zero point two badges, not zero point eight. The survivorship sample makes Protein look four times more effective than it actually is.

[pause]

NARRATOR: Now Misty turns to the most counterintuitive member of the bias family. This one can create associations -- even negative associations -- between variables that are completely independent in the population.

MISTY: Let me tell you about the Elite Four.

[OAK EXPLAINS: Berkson's Paradox]

OAK: Berkson's paradox, also called collider bias, occurs when you condition on a variable that is caused by two or more independent variables. Conditioning on that shared consequence induces a spurious association between its causes -- an association that does not exist in the broader population.

NARRATOR: Here is how it works. Consider two traits among Kanto trainers: natural talent, meaning innate battling ability, and training intensity, meaning hours spent practicing. In the general population, these two traits are independent. Talented trainers do not train any more or less than untalented ones.

Now consider the sample of Elite Four challengers -- the handful of trainers strong enough to take on Kanto's final gauntlet. To reach the Elite Four, a trainer needs to be either very talented, or very dedicated to training, or ideally both.

Here is the causal structure. Natural Talent causes Elite Four status. Training Intensity also causes Elite Four status. The two arrows converge at Elite Four Challenger. That is what makes it a collider -- two causes flowing into one shared effect.

Now watch what happens when you analyze data only among Elite Four challengers. If you learn that a particular challenger has low natural talent, what can you infer? They must have trained extremely hard. Otherwise, how did they get there? And if a challenger has extraordinary talent, they may not have needed to train as intensely. Within this elite group, talent and training become negatively correlated -- but that correlation is a complete artifact of selection.

MISTY: Let me give you the numbers. I pulled data on eight hundred trainers, split evenly across high and low talent and high and low training intensity. Among trainers with low talent and low training, only one percent reach the Elite Four -- just two out of two hundred. Among trainers with high talent but low training, fifteen percent make it -- thirty out of two hundred. High training but low talent, twelve point five percent -- twenty-five out of two hundred. And among trainers with both high talent and high training, twenty-two point five percent make it -- forty-five out of two hundred.

NARRATOR: In the full population, talent and training are independent. Knowing one tells you nothing about the other. But among the one hundred and two trainers who reached the Elite Four, the picture flips. Among challengers with low talent, ninety-two point six percent had high training. Among challengers with high talent, only sixty percent had high training. A strong negative association appears -- purely as an artifact of conditioning on the collider.

This is Berkson's paradox. It creates patterns that do not exist in reality. And it is especially dangerous because the induced association can feel intuitive after the fact. You think, "Of course less talented challengers trained harder -- they had to." But that reasoning is backwards. In the population, talent and training are unrelated. The negative association only appears because you restricted your view to a selected sample.

[pause]

---

NARRATOR: Now comes the paradox that really made my head spin. I am reviewing Misty's data in the gym office when I notice something strange. The overall data clearly shows that Cave training is associated with more badges. But when I break the data down by starter Pokemon type, the relationship reverses within every single group.

MISTY: Welcome to Simpson's paradox.

[OAK EXPLAINS: Simpson's Paradox]

OAK: Simpson's paradox occurs when a trend or association that appears in several subgroups of data reverses or disappears when the groups are combined. It is not merely a statistical curiosity. It strikes at the heart of causal reasoning. The question "which comparison is correct -- the aggregate or the subgroup?" cannot be answered by the data alone. It requires understanding the causal structure.

NARRATOR: Let me walk you through the numbers, because they are genuinely startling. Misty broke her data down by which starter Pokemon each trainer chose.

Among Fire-type starters -- trainers who began with Charmander. Four hundred of them trained in the Cave, and they averaged six point zero badges. Fifty did not train in the Cave, and they averaged six point five badges. Within Fire-type starters, Cave training is associated with zero point five fewer badges.

Among Water-type starters -- trainers who began with Squirtle. One hundred trained in the Cave and averaged three point zero badges. Three hundred and fifty did not, averaging three point five. Again, Cave training is associated with zero point five fewer badges.

Among Grass-type starters -- trainers who began with Bulbasaur. Three hundred trained in the Cave and averaged four point zero badges. Eight hundred did not, averaging four point five. Once more, zero point five fewer badges for Cave trainers.

Within every single starter type, Cave training is associated with worse outcomes. Negative zero point five across the board. You would think that when you combine these groups, the overall picture would also show a negative effect. But it does not.

MISTY: When I combine all trainers, the Cave group averages four point eight seven five badges and the non-Cave group averages four point two nine two. Overall, Cave training appears to be associated with positive zero point five eight three extra badges.

NARRATOR: Let me say that again, because it is genuinely paradoxical. In every subgroup, Cave training is associated with fewer badges. But in the aggregate, Cave training is associated with more badges. The sign flips from negative to positive when you combine the data.

[pause]

NARRATOR: How is this possible? The key is the unequal distribution of starter types across treatment groups. Fire-type starters tend to earn more badges overall -- perhaps because Charmander evolves into the powerful Charizard. And Fire-type trainers are massively overrepresented among Cave trainers. Fifty percent of Cave trainers have Fire starters, but only about four percent of non-Cave trainers do.

The mechanism works like this. Fire-type starters tend to belong to more aggressive, risk-taking trainers. Those trainers enter the Cave at higher rates, and they also earn more badges due to their starter's raw power. The starter type is a confounder. It simultaneously drives Cave selection and badge outcomes.

When you aggregate, you are not comparing like with like. You are comparing a Cave group that is mostly Fire-type trainers against a non-Cave group that is mostly Grass and Water types. The Fire-type advantage swamps the within-group Cave disadvantage, and the overall association flips.

MISTY: So which comparison should I trust? The subgroup results or the aggregate?

[OAK EXPLAINS: Resolving Simpson's Paradox]

OAK: You cannot resolve Simpson's paradox with statistics alone. The answer depends on the causal structure. If starter type is a confounder -- a common cause of both Cave training and badges -- then you should condition on it and trust the subgroup results. The within-group estimate of negative zero point five badges is closer to the causal effect. But if starter type is a mediator -- if Cave training somehow changes which Pokemon a trainer ends up using in battle -- then you should not condition on it, because that would block part of the causal effect you are trying to measure. The aggregate number would be preferred. The same data, the same numbers, two opposite conclusions -- all depending on what you believe about the arrows connecting the variables.

NARRATOR: This is the moment when the limitations of pure statistics become painfully clear. The numbers do not speak for themselves. Two analysts looking at the same dataset, with different beliefs about the causal structure, will reach different and potentially opposite conclusions. We need a language for making those causal beliefs explicit. We need a way to draw our assumptions on the table and reason about them systematically.

We need a map.

Misty points east, toward the Cape. "Go talk to Bill," she says. "He has been mapping the causal structure of the Kanto trainer journey for years. If anyone can help, it is him."

---

## Part 3: Bill's Lighthouse and the Language of Graphs

[SCENE: Route 25. Waves crashing. Seagulls. A knock on a wooden door.]

NARRATOR: I walk east along Route Twenty-Five toward the Sea Cottage, where Bill -- Kanto's most eccentric Pokemon researcher -- lives and works. The path is winding. Trainers challenge me along the way, but I am distracted. Misty's problems -- confounding, selection bias, Simpson's paradox -- all hinge on understanding something she called the causal structure. The invisible web of cause and effect that lies beneath the data.

I knock on Bill's door. There is a commotion inside, a flash of light, and the door opens to reveal a man who appears to be part Clefairy. Pink ears, round body, panicked expression.

BILL: Ah! Come in, come in! Small accident with the teleporter. Help me reverse this and I will show you something extraordinary.

NARRATOR: After a brief and slightly alarming process involving a machine that should probably not exist, Bill is back to normal -- a thin man with wild hair and thick glasses. He leads me to his study, and my jaw drops. One entire wall is covered with a massive diagram. Variables connected by arrows. A web of causal relationships spanning everything from trainer wealth to Pokemon happiness to battle outcomes.

BILL: Beautiful, is it not? This is a Directed Acyclic Graph. A DAG. It is the most important tool in causal inference.

[pause]

[OAK EXPLAINS: Directed Acyclic Graphs]

OAK: A Directed Acyclic Graph, or DAG, has three components. First, nodes. Each node is a circle representing a variable -- something you could measure or observe, like trainer experience, cave training, or badges earned. Second, directed edges. These are arrows connecting the nodes. An arrow from one variable to another means the first directly causes the second. And third, the acyclicity constraint. There are no loops. You cannot follow the arrows in their forward direction and end up back where you started. Causation flows forward -- there is no time travel.

NARRATOR: Let me repeat that, because each piece matters.

Nodes are variables. Arrows are direct causal effects. And no loops -- you can never follow the arrows forward and circle back to where you began.

A DAG is a map of your beliefs about how the world works. It is not derived from data. It is drawn from domain knowledge, from theory, and from careful reasoning. And here is a crucial point: the absence of an arrow is a stronger claim than its presence. If there is no arrow from wealth to badges in your DAG, you are asserting that wealth has no direct causal effect on badges. Every missing arrow is a testable, debatable assumption.

[pause]

NARRATOR: Bill walks me through constructing a DAG for Misty's problem, one variable at a time. I want you to picture this as he describes it. We are going to build a verbal arrow map -- a description of every causal relationship using words instead of pictures.

BILL: We start with the causal question itself. Cave Training causes Badges Earned. That is one arrow: Cave Training points to Badges Earned. This is the relationship we want to measure. Everything else we add is about understanding what might distort our view of that arrow.

NARRATOR: So our map begins with a single arrow: Cave Training to Badges Earned.

BILL: Now we add the first confounder. Experience causes Cave Training -- more experienced trainers are more confident about surviving the Cave, so they enter at higher rates. And Experience also causes Badges Earned -- experienced trainers do better in all gym battles regardless of the Cave. So Experience points to Cave Training, and Experience points to Badges Earned.

NARRATOR: Picture what we have now. Experience sits above and to the side. It sends one arrow down to Cave Training and another arrow down to Badges Earned. Experience is a common cause -- it influences both our treatment and our outcome. This is a fork. The arrows diverge from a single source. Experience causes Cave Training and Experience causes Badges Earned. That fork is what generates confounding.

BILL: Next, wealth. Wealth causes Cave Training -- wealthier trainers can afford supplies for the dangerous cave. Wealth also causes Starter Type -- wealthier families have connections that influence which starter Pokemon a trainer receives. And Starter Type causes Badges Earned, because type advantages matter in gym battles.

NARRATOR: Now the map is getting richer. Wealth sends an arrow to Cave Training and another arrow to Starter Type. Starter Type sends an arrow to Badges Earned. There is a confounding path that runs from Cave Training, backward through Wealth, forward through Starter Type, and into Badges Earned. It is an indirect backdoor route.

BILL: Now we add the mediator. Cave Training causes Strategy Score. The Cave teaches trainers to think on their feet -- to read their opponents, to plan three moves ahead. And Strategy Score causes Badges Earned. Better strategy leads to more victories.

NARRATOR: This is different from confounding. Strategy Score sits between Cave Training and Badges Earned. It is a link in the causal chain. Cave Training causes Strategy Score, and Strategy Score causes Badges Earned. This is a chain structure -- sequential causation, like evolution. Charmander evolves into Charmeleon, which evolves into Charizard. Each step causes the next. The effect of Cave Training flows through Strategy Score on its way to Badges Earned.

[pause]

BILL: And finally, the ghost in the machine. Natural Talent causes Cave Training -- more talented trainers select into the Cave. And Natural Talent causes Badges Earned -- talented trainers win more battles regardless. But here is the problem. Natural Talent is unobserved. We know it exists, but we cannot measure it. On my wall, I draw it with a dashed circle to show that it is hidden.

NARRATOR: The complete map now has six main variables: Wealth, Experience, Natural Talent, Cave Training, Strategy Score, Starter Type, and Badges Earned. Let me give you the full verbal arrow map.

Wealth causes Cave Training. Wealth causes Starter Type. Experience causes Cave Training. Experience causes Badges Earned. Natural Talent causes Cave Training. Natural Talent causes Badges Earned. Cave Training causes Badges Earned directly. Cave Training causes Strategy Score. Strategy Score causes Badges Earned. And Starter Type causes Badges Earned.

That is ten arrows, and together they tell the complete causal story of Misty's data. Every path, every backdoor, every potential source of bias is encoded in those arrows.

BILL: And it is acyclic. You cannot follow the arrows forward and end up back where you started. Badges Earned does not retroactively cause you to have trained in the Cave. Causation flows forward in time. There is no time travel in Kanto -- Celebi notwithstanding, and Celebi is a Johto Pokemon.

[pause]

---

NARRATOR: Bill settles into a chair and pulls out three small cards -- each one with a tiny diagram on it. These, he says, are the three fundamental building blocks of every DAG that has ever existed or ever will exist. Master these three, and you can read any graph.

BILL: Every DAG, no matter how enormous or tangled, is made up of just three types of path structures. I call them the three elemental structures. Each one describes what happens at a single intermediate node along a path.

[TEACHING SECTION: The Three Elemental Structures]

NARRATOR: Let me introduce them one at a time, each with a mnemonic to help it stick.

BILL: The first structure is the Fork. I call it the Eevee Structure. Think of Eevee -- a single Pokemon that can evolve into many different forms. Vaporeon, Jolteon, Flareon. One common source branching into multiple paths.

NARRATOR: In a fork, a single variable causes two others. The arrows split apart from a common origin. Variable Z causes Variable X, and Variable Z also causes Variable Y. The arrows go Z to X and Z to Y.

For Misty's problem, the fork looks like this. Experience causes Cave Training, and Experience causes Badges Earned. Experience is the Eevee -- one common cause splitting into two consequences.

Here is the critical rule for forks. Association flows through a fork by default. Because Z causes both X and Y, knowing something about X tells you something about Z, which tells you something about Y. The two endpoints are correlated even though neither one causes the other.

But -- and this is the key -- if you condition on Z, the common cause, the fork is blocked. Once you know Z, learning X gives you no additional information about Y through this path. Controlling for the common cause removes the spurious association.

Let me ground this with probabilities. Suppose half of trainers are experienced. Among experienced trainers, eighty percent enter the Cave and ninety percent earn many badges. Among inexperienced trainers, only twenty percent enter the Cave and thirty percent earn many badges.

If you just look at Cave trainers without accounting for experience, you will find that seventy-eight percent of them earn many badges. But the overall rate of earning many badges is only sixty percent. That gap -- seventy-eight versus sixty -- is the spurious association flowing through the fork. It makes the Cave look beneficial even if it has zero causal effect.

But once you condition on experience -- once you compare experienced Cave trainers to experienced non-Cave trainers, and inexperienced Cave trainers to inexperienced non-Cave trainers -- the spurious association vanishes. Within each experience level, the Cave gives no additional information about badges, because the fork is blocked.

[pause]

BILL: The second structure is the Chain. I call it the Evolution Structure. Think of a Pokemon evolution chain. Charmander becomes Charmeleon, which becomes Charizard. Each step causes the next in sequence.

NARRATOR: In a chain, causation flows in a straight line. Variable X causes Variable Z, and Variable Z causes Variable Y. The arrows go X to Z to Y.

For Misty's problem, the chain looks like this. Cave Training causes Strategy Score, and Strategy Score causes Badges Earned. The effect of the Cave flows through strategy on its way to badges.

Here is the rule for chains. Association flows through a chain by default, just like forks. Because X causes Z and Z causes Y, there is a genuine causal and statistical connection between X and Y.

But here is the danger. If you condition on Z -- the middle variable, the mediator -- you block the chain. You cut the causal pathway. And this is not a good thing if you are trying to measure the total effect of X on Y.

BILL: This is where Blue makes his second mistake in this chapter. He runs a regression predicting badges from both Cave Training and Strategy Score. He finds that the coefficient on Cave Training is small and insignificant, and he concludes the Cave does not help. But he has committed what we call the bad control error. By controlling for Strategy Score, he has blocked the very mechanism through which Cave Training works.

NARRATOR: Let me say that again because it is so important. The Cave helps trainers earn more badges by improving their strategy. Strategy is the pathway. If you statistically hold strategy constant, you are asking "does the Cave help, beyond its effect on strategy?" And the answer might be no -- but that does not mean the Cave does not help. It means the Cave helps precisely by improving strategy. Controlling for the mediator hides the total effect.

The rule: never control for a variable that sits on the causal path between treatment and outcome unless you specifically want to decompose the effect into direct and indirect components. That is a topic for Chapter Eight.

[pause]

BILL: The third and final structure is the Collider. I call it the Gym Badge Structure. Think of earning a particular Gym Badge. Multiple causes converge to produce that single outcome -- your team's strength, your battle strategy, maybe a bit of luck. Multiple arrows collide at one point.

NARRATOR: In a collider, two variables independently cause a third. Variable X causes Variable Z, and Variable Y also causes Variable Z. The arrows converge: X to Z and Y to Z.

For the Pokemon example we discussed earlier with Misty, think of the Elite Four. Natural Talent causes Elite Four Challenger status. Training Intensity also causes Elite Four Challenger status. Two arrows converge at Elite Four Challenger. That is a collider.

Here is what makes colliders fundamentally different from forks and chains. A collider blocks association by default. Even though both X and Y cause Z, there is no statistical association between X and Y through this path when you leave Z alone. Knowing that someone is talented tells you nothing about how hard they train -- the two traits are independent.

But -- and this is the critical twist -- if you condition on the collider Z, you open the path. You create an association between X and Y that did not exist before. Among Elite Four challengers, learning that someone has low talent tells you they must have trained extremely hard. Conditioning on the collider creates an "explaining away" effect.

And this extends to descendants of the collider too. If Elite Four Challenger status causes Media Coverage, then conditioning on Media Coverage also partially opens the collider path. You do not have to condition directly on the collider itself -- conditioning on anything it causes can introduce the bias.

[pause]

NARRATOR: Let me give you a summary table in words, because this is the engine of everything that follows.

For a fork -- the Eevee Structure -- the path is open by default, and conditioning on the middle node blocks it. Blocking a fork is good. It removes confounding.

For a chain -- the Evolution Structure -- the path is open by default, and conditioning on the middle node blocks it. But blocking a chain is usually bad. It removes part of the causal effect you are trying to measure.

For a collider -- the Gym Badge Structure -- the path is blocked by default, and conditioning on the middle node opens it. Opening a collider is bad. It introduces a spurious association that was not there before.

Forks and chains behave the same way: open by default, blocked when you condition. Colliders are the opposite: blocked by default, opened when you condition. This asymmetry is the key to everything.

[pause]

---

NARRATOR: Armed with the three building blocks, Bill leads me to the most powerful tool in the graphical causal inference toolkit.

BILL: This is d-separation. It is the algorithm that tells you whether your statistical analysis will give you a causal answer or garbage.

[OAK EXPLAINS: d-Separation]

OAK: D-separation is a graphical algorithm for determining whether two variables are statistically independent, given a set of variables you condition on. The "d" stands for "directional." Here is the rule. Two variables are d-separated by a conditioning set if and only if every path between them is blocked. A path is blocked if it contains at least one of the following: a non-collider -- a fork or chain node -- that you have conditioned on, or a collider that you have not conditioned on and whose descendants you have not conditioned on either. If even one path remains open, the variables are d-connected, meaning they may be statistically associated.

NARRATOR: Let me walk through this for Misty's problem. We want to know whether we can isolate the causal effect of Cave Training on Badges Earned. To do that, we need to block all the non-causal paths -- the backdoor paths -- while keeping the causal paths open.

BILL: Let me list every path from Cave Training to Badges Earned in our DAG.

Path One: Cave Training to Badges Earned directly. This is the causal path we want to measure. It has no intermediate nodes. It is always open.

Path Two: Cave Training to Strategy Score to Badges Earned. This is also a causal path, flowing through the mediator. Strategy is a chain node. This path is open unless we condition on Strategy Score -- which, as we discussed, we should not do.

Path Three: Cave Training, backward through Experience, forward to Badges Earned. This is a backdoor path. Experience is a fork node on this path. It is open by default, creating confounding. We can block it by conditioning on Experience.

Path Four: Cave Training, backward through Natural Talent, forward to Badges Earned. Another backdoor path. Natural Talent is a fork node. It is open by default. We could block it by conditioning on Natural Talent -- but Natural Talent is unobserved. We cannot condition on something we cannot measure.

Path Five: Cave Training, backward through Wealth, forward through Starter Type, forward to Badges Earned. Another backdoor path. Wealth is a fork node on this path. Open by default. We can block it by conditioning on Wealth or on Starter Type -- either one breaks the chain.

NARRATOR: Paths Three, Four, and Five are the backdoor paths. They are non-causal routes that generate confounding bias. We need to block all of them.

[pause]

[OAK EXPLAINS: The Backdoor Criterion]

OAK: The Backdoor Criterion gives you precise conditions for when you can estimate a causal effect by statistical adjustment. A set of variables satisfies the backdoor criterion relative to a treatment and an outcome if two conditions hold. First, no variable in the set is a descendant of the treatment. You must not condition on anything caused by the treatment -- that rules out Strategy Score. Second, the set blocks every backdoor path between the treatment and the outcome. Every non-causal path must have at least one blocked node.

NARRATOR: So what set of variables could we condition on to satisfy the backdoor criterion for Misty's problem?

BILL: Let us check. To block Path Three, we condition on Experience. Done. To block Path Five, we condition on Wealth or Starter Type. Let us say Wealth. Done. But Path Four runs through Natural Talent, and Natural Talent is unobserved. We cannot condition on it. And there is no other node on that path to block.

NARRATOR: This is the profound and sobering result. No valid adjustment set exists using only observed variables. Because Natural Talent is an unobserved confounder that sits on its own backdoor path, and there is no observed variable that can block that path, no amount of regression adjustment can recover the true causal effect of Cave Training on Badges Earned.

The DAG does not just tell us what to condition on. It also tells us when no conditioning strategy can work. Many researchers proceed with regression, hoping they have controlled for enough. The DAG forces you to confront the hard question: is there an unobserved confounder that no amount of regression can fix?

For Misty's problem, the answer is yes. The backdoor is locked by an unobserved confounder. We need a different strategy.

[pause]

NARRATOR: But before despair sets in, Bill has one more trick to show me. And it requires a different door entirely.

---

## Part 4: Through the Front Door and Beyond

[SCENE: Bill's study. Evening light through a lighthouse window.]

NARRATOR: Bill pauses at a section of his wall diagram and points to an unusual configuration.

BILL: Sometimes the backdoor is locked. No valid adjustment set exists because of an unobserved confounder. But occasionally -- just occasionally -- you can go through the front door instead.

[OAK EXPLAINS: The Frontdoor Criterion]

OAK: The frontdoor criterion is a remarkable result. It allows you to identify a causal effect even when there is an unobserved confounder between the treatment and the outcome, provided the effect operates entirely through an observed mediator that satisfies certain conditions.

NARRATOR: Let me set up the specific structure. We have Cave Training as the treatment, Strategy Score as the mediator, Badges Earned as the outcome, and Natural Talent as the unobserved confounder. Natural Talent causes Cave Training and Natural Talent causes Badges Earned -- that is the unblockable backdoor.

But notice something special about Strategy Score. The only thing that causes Strategy Score in our model is Cave Training. Natural Talent does not directly affect how much strategy you learn in the Cave -- the Cave improves everyone's strategy equally, regardless of innate ability. That means there are no unobserved confounders between Cave Training and Strategy Score.

Furthermore, every causal effect of Cave Training on Badges flows through Strategy Score. There is no other mechanism.

And here is the third condition. The backdoor path from Strategy Score to Badges -- the path that goes from Strategy Score backward to Cave Training backward to Natural Talent forward to Badges -- can be blocked by conditioning on Cave Training itself.

These three conditions together are the frontdoor criterion. They let us identify the total effect of Cave Training on Badges by going through the front door -- through the mediator -- instead of trying to block the locked backdoor.

[pause]

BILL: Let me show you how the math works, step by step, using Misty's data. I will use a simplified version where Strategy Score is binary -- high or low -- and Badges is binary -- six or more badges, versus fewer than six.

NARRATOR: Here are the numbers from Misty's data.

Among trainers who entered the Cave, seventy-five percent developed high strategy. Among those who did not enter the Cave, only thirty percent developed high strategy. That is the first piece: the effect of Cave Training on Strategy Score.

Now for the second piece, the relationship between Strategy Score and Badges, broken down by Cave Training status. Among Cave trainers with high strategy, eighty percent earned six or more badges. Among Cave trainers with low strategy, fifty percent did. Among non-Cave trainers with high strategy, seventy percent earned six or more badges. Among non-Cave trainers with low strategy, thirty percent did.

And one more fact: forty percent of trainers entered the Cave, sixty percent did not.

BILL: The frontdoor formula works in two steps. First, identify the effect of the treatment on the mediator. Since there are no unobserved confounders between Cave Training and Strategy Score, we can read this directly from the data. Cave Training raises the probability of high strategy from thirty percent to seventy-five percent.

Second, identify the effect of the mediator on the outcome. There are confounders between Strategy Score and Badges -- Natural Talent confounds them through the path that goes from Natural Talent to Cave Training to Strategy Score. But we can block that path by conditioning on Cave Training. Then we average over the distribution of Cave Training in the population.

NARRATOR: Let me walk through the calculation for what happens when we intervene to set Cave Training to yes.

For the high-strategy group: the probability of high strategy given Cave Training is seventy-five percent. The effect of high strategy on badges, averaged over the population, is eighty percent times forty percent -- that is the share who were Cave trainers -- plus seventy percent times sixty percent -- the share who were not. That gives zero point three two plus zero point four two, which equals zero point seven four.

For the low-strategy group: the probability of low strategy given Cave Training is twenty-five percent. The averaged effect is fifty percent times forty percent plus thirty percent times sixty percent. That gives zero point two zero plus zero point one eight, which equals zero point three eight.

Combining: the probability of earning six or more badges if everyone trained in the Cave is seventy-five percent times zero point seven four plus twenty-five percent times zero point three eight. That equals zero point five five five plus zero point zero nine five, which equals zero point six five zero. Sixty-five percent.

Now for the scenario where nobody trains in the Cave. High strategy probability is thirty percent, low strategy is seventy percent. Using the same averaged effects of zero point seven four and zero point three eight. Thirty percent times zero point seven four plus seventy percent times zero point three eight equals zero point two two two plus zero point two six six, which equals zero point four eight eight. About forty-nine percent.

The causal effect: sixty-five percent minus forty-nine percent equals sixteen point two percentage points. Cave Training increases the probability of earning six or more badges by about sixteen percentage points. And we identified this despite the unobserved confounder.

[pause]

BILL: The frontdoor criterion is rare in practice. It requires a complete mediator that captures every causal path from treatment to outcome, no unobserved confounders between treatment and mediator, and the ability to observe the mediator. Those conditions are stringent. But when they hold, you can extract causal information from observational data even when the primary relationship is hopelessly confounded.

[pause]

---

NARRATOR: Bill turns to the most abstract part of his wall. A set of mathematical equations, each corresponding to a node in the DAG.

BILL: The DAG is the picture. But behind the picture, there is a complete mathematical model called a Structural Causal Model. And from that model, Judea Pearl derived three rules that can, in principle, answer any identifiable causal question from observational data.

[OAK EXPLAINS: Structural Causal Models]

OAK: A Structural Causal Model, or SCM, has three components. First, a set of background variables -- things determined outside the model that we take as given. Second, a set of endogenous variables -- the variables we are modeling, like experience, cave training, strategy, and badges. Third, a set of structural equations -- one for each endogenous variable -- that specify how it is determined by its direct causes and some background noise. Each equation represents a mechanism. A stable process by which a variable is produced.

NARRATOR: For the Kanto Trainer example, each variable has its own equation. Experience is determined by background factors. Wealth is determined by background factors. Natural Talent is determined by background factors. Cave Training is determined by Experience, Wealth, Natural Talent, and some randomness. Starter Type is determined by Wealth and some randomness. Strategy Score is determined by Cave Training and some randomness. And Badges Earned is determined by Cave Training, Experience, Natural Talent, Strategy Score, Starter Type, and some randomness.

The key insight is that these equations represent mechanisms -- stable processes that continue to operate even when we intervene. When we perform an intervention -- say, forcing a trainer into the Cave regardless of their experience, wealth, or talent -- we replace one equation. The Cave Training equation gets deleted and replaced with a fixed value. But every other equation stays the same. Experience still affects badges the same way. Strategy still mediates the Cave's effect the same way. Only the mechanism that determined Cave entry has changed.

[pause]

[OAK EXPLAINS: The do-Operator]

OAK: This is the most profound distinction in Pearl's framework: the difference between observing and intervening. The expression "P of Y given do X equals x" -- the do-operator -- denotes what happens to Y after an intervention that forces X to a particular value, regardless of what would normally cause X. This is fundamentally different from the observational conditional "P of Y given X equals x," which tells you about Y among units that naturally happened to have X equal to x. Observing is passive. Intervening is active. The do-operator captures the difference.

NARRATOR: In graph terms, the intervention corresponds to surgery on the DAG. When you intervene on X, you delete all arrows pointing into X. You sever X from its causes. Then you set X to the value you chose. The remaining structure stays intact. This is called graph surgery, or the truncated factorization.

Think about it this way. In the observational world, Cave Training is determined by experience, wealth, and talent. Trainers who enter the Cave are a self-selected, non-random group. In the interventional world -- the do-world -- we force Cave Training to be on or off. It is no longer connected to its causes. The confounding arrows are cut.

This is exactly what a randomized experiment does in practice. Randomization severs the treatment from its causes. The do-operator is the mathematical formalization of that severing.

[pause]

NARRATOR: And now, the crown jewel of Pearl's framework. The three rules of do-calculus.

BILL: These three rules, proved by Pearl in nineteen ninety-five, are complete. That means any causal effect that can be identified from observational data can be derived by applying some combination of these three rules. And if the rules cannot identify an effect, then the effect is genuinely non-identifiable -- no clever statistical trick, no machine learning algorithm, no amount of data can recover it.

NARRATOR: I will describe them conceptually rather than symbolically, because the intuition matters more than the notation for an audio format.

Rule One: Adding or removing observations. You can add or remove a variable from your conditioning set if that variable is d-separated from the outcome in the graph where the treatment has been intervened on. In plain English: if a variable carries no information about the outcome once you have intervened on the treatment and conditioned on everything else, you can safely ignore it.

Rule Two: Exchanging interventions and observations. You can replace an intervention with an observation -- swap a "do" for a "see" -- if the outcome is d-separated from the variable in a specific modified graph. This is the rule that converts interventional quantities, which you cannot directly compute from data, into observational quantities, which you can. It is the workhorse rule for identification.

Rule Three: Removing interventions. You can remove a "do" operator entirely if, in the appropriately modified graph, the outcome is d-separated from the variable. This rule lets you simplify complex interventional expressions.

BILL: The three rules are complete. The backdoor formula is a special case. The frontdoor formula is a special case. Every identification result we have discussed can be derived by applying these rules in the right sequence.

NARRATOR: And here is what makes this both empowering and humbling.

It is empowering because given a correct DAG, we have a systematic, mechanical procedure for determining whether a causal question is answerable from observational data. If it is, the rules tell us the exact formula to use.

It is humbling because when the do-calculus says "non-identifiable," there is no escape. No amount of data, no sophisticated algorithm, no clever regression can identify the effect. The only options are to collect new data that changes the DAG, to make additional assumptions like parametric restrictions, or to use a different identification strategy entirely -- instrumental variables, difference-in-differences, regression discontinuity. Those are the subjects of future chapters.

[pause]

---

[BLUE'S MISTAKE]

NARRATOR: As I am leaving Bill's cottage, I run into Blue on Route Twenty-Five. He has a laptop open and a triumphant grin.

BLUE: I just ran a kitchen-sink regression with every variable I could find. Experience, wealth, starter type, strategy score, the number of Pokeballs in their bag, their favorite color, whether they prefer Moomoo Milk or Lemonade. I controlled for everything. The causal effect is identified.

NARRATOR: I look at Bill. Bill sighs.

BILL: Regression is just a tool for implementing the adjustment formula. It does not justify which variables to adjust for. Without a DAG, Blue has no way to know whether his variables satisfy the backdoor criterion. He might be controlling for a mediator, which would block part of the causal effect and bias his estimate downward. He might be conditioning on a collider, which would open a non-causal path and introduce entirely new bias. He might be including irrelevant variables that add noise without helping. "I controlled for everything" is not a causal argument. A DAG is.

NARRATOR: Blue waves his hand dismissively. "Details," he says. And he walks off toward Vermilion City.

[pause]

NARRATOR: I watch him go and think about everything I have learned today. I came to Cerulean City with a naive comparison of means -- five point eight versus three point two -- and the assumption that more data and more control variables would solve any problem. I am leaving with a fundamentally different understanding.

The world has a causal structure, invisible but real, and it governs what we can learn from observational data. DAGs make that structure explicit. The three elemental structures -- forks, chains, and colliders -- govern how information flows and how conditioning changes that flow. D-separation tells us which associations are causal and which are spurious. The backdoor criterion tells us when adjustment works and what to adjust for. The frontdoor criterion offers an alternative when backdoor adjustment fails. And the do-calculus draws the final boundary between what is identifiable and what is not.

Tomorrow, I head south toward Vermilion City, where Lieutenant Surge has a different kind of problem. His question is not about which variables to condition on, but about how to estimate the magnitude of a treatment effect when the conditions for identification are met. We will learn the mechanics of matching, subclassification, and inverse probability weighting -- the practical tools that turn the DAG's theoretical permission into actual numbers.

But that is Chapter Four. For now, the sun is setting over the Cape, the orange light is glinting off the water, and I have earned the Cascade Badge.

---

## Chapter Summary

NARRATOR: Let me recap the key concepts from Cerulean City.

First, observational studies. When experiments are unethical, infeasible, or impractical, we must learn from the data we have. Observational data is abundant and cheap, but it is vulnerable to biases that randomization would have eliminated.

Second, confounding. A confounder is a common cause of treatment and outcome that creates a spurious association. The omitted variable bias formula tells us the bias equals the effect of the omitted variable on the outcome times the relationship between the omitted variable and the treatment. Even when we cannot compute the exact bias, we can often determine its direction through signed analysis.

Third, selection bias, survivorship bias, and Berkson's paradox. These all arise from conditioning on variables caused by treatment or outcome. Survivorship bias hides failures by analyzing only those who survived some process. Berkson's paradox creates associations between independent variables by conditioning on their common effect -- a collider.

Fourth, Simpson's paradox. Aggregate and subgroup associations can point in opposite directions. Whether to aggregate or stratify depends on the causal structure, not the data. Two analysts with different DAGs will reach different conclusions from the same numbers.

Fifth, Directed Acyclic Graphs. DAGs encode causal assumptions explicitly. Each node is a variable, each arrow is a direct causal effect, and the absence of an arrow is a strong and testable claim. DAGs are drawn from domain knowledge, not from data.

Sixth, the three elemental structures. Forks -- the Eevee Structure -- represent common causes and generate confounding. Chains -- the Evolution Structure -- represent mediation and transmit causal effects. Colliders -- the Gym Badge Structure -- represent common effects and block association by default but open it when conditioned on. The asymmetry between colliders and the other two structures is the engine of everything.

Seventh, d-separation. The algorithm for reading conditional independence from a DAG. It tells you which paths are open, which are blocked, and whether conditioning on a particular set of variables will remove confounding or introduce new bias.

Eighth, the backdoor criterion. It identifies valid adjustment sets for estimating causal effects. When it is satisfied, the adjustment formula converts observational data into causal estimates. When it cannot be satisfied due to unobserved confounders, no regression can save you.

Ninth, the frontdoor criterion. A remarkable result that enables causal identification through a complete mediator, even in the presence of unobserved confounding of the primary relationship. Rare in practice, but conceptually powerful.

And tenth, Structural Causal Models and do-calculus. The complete mathematical foundation for causal inference from observational data. The do-operator formalizes the distinction between observing and intervening. The three rules of do-calculus are provably complete -- they can derive any identifiable causal effect, and when they fail, the effect is genuinely beyond reach.

Next stop: Vermilion City and the practical tools of estimation.

[pause]

---

## Comprehension Check

NARRATOR: Before we leave Cerulean City, check yourself on these questions.

First: What is a confounder, and why does a naive comparison of outcomes between Cave trainers and non-Cave trainers overestimate the causal effect of the Cave?

[long pause]

A confounder is a variable that causes both the treatment and the outcome, creating a spurious association. The naive comparison overestimates the Cave effect because trainers who choose to enter the Cave tend to be more experienced, wealthier, and more talented. These traits help them earn badges regardless of Cave training. The observed gap of two point six badges includes both the true Cave effect -- about zero point eight badges -- and the confounding bias from these pre-existing advantages.

Second: Explain the difference between selection bias and confounding. What is Berkson's paradox, and how does it relate to the collider structure in a DAG?

[long pause]

Confounding arises from a common cause of treatment and outcome -- a fork in the DAG. Selection bias arises from conditioning on a common effect of treatment and outcome, or their causes -- a collider in the DAG. Berkson's paradox is the phenomenon where conditioning on a collider creates a spurious association between its independent causes. In the Elite Four example, talent and training intensity are independent in the population, but among Elite Four challengers -- a collider caused by both -- they become negatively correlated because low talent in that selected group implies high training.

Third: Name the three elemental DAG structures and state, for each, whether conditioning on the middle node opens or blocks the path.

[long pause]

The fork, or common cause structure, is open by default and blocked when you condition on the middle node. The chain, or mediation structure, is also open by default and blocked when you condition on the middle node. The collider, or common effect structure, is blocked by default and opened when you condition on the middle node or any of its descendants. The collider behaves opposite to the other two.

Fourth: What is the backdoor criterion, and why can it not be satisfied with observed variables alone in Misty's full Kanto Trainer DAG?

[long pause]

The backdoor criterion requires finding a set of non-descendant variables that blocks every backdoor path from treatment to outcome. In the full Kanto Trainer DAG, one backdoor path runs through Natural Talent, which is unobserved. Since Natural Talent cannot be conditioned on and no other observed variable lies on that path, there is no way to block it. Therefore, no set of observed variables satisfies the backdoor criterion, and the causal effect cannot be identified by regression adjustment alone.

Fifth: Briefly describe the frontdoor criterion and explain how it identifies the causal effect of Cave Training on Badges despite the unobserved confounder Natural Talent.

[long pause]

The frontdoor criterion works when all causal effects of the treatment flow through an observed mediator, there are no unobserved confounders between the treatment and the mediator, and the treatment itself blocks the backdoor paths from the mediator to the outcome. In Misty's problem, Strategy Score is the mediator. Cave Training's effect on Strategy is unconfounded because Natural Talent does not directly affect strategy learning. And the backdoor path from Strategy to Badges through Natural Talent is blocked by conditioning on Cave Training. The formula combines these two identified steps -- the effect of Cave Training on Strategy and the effect of Strategy on Badges -- to recover the total causal effect. The result: Cave Training increases the probability of six or more badges by about sixteen percentage points, identified despite the unobserved confounder.
