---
title: "Appendix: Mathematical Foundations"
chapter_number: 9
source_file: "textbook/chapters/appendix_a_math.md"
estimated_runtime_minutes: 40
key_concepts:
  - probability basics
  - random variables
  - expectation and variance
  - conditional probability
  - Bayes theorem
  - law of large numbers
  - central limit theorem
  - hypothesis testing
  - confidence intervals
  - p-values
characters:
  - narrator
  - oak
---

# Appendix: Mathematical Foundations

NARRATOR: This appendix is optional. If you are comfortable with probability, random variables, hypothesis testing, and confidence intervals, you can skip ahead to Chapter One. If you would like a refresher -- or if this is your first encounter with these ideas -- Professor Oak will walk you through the mathematical prerequisites for everything that follows.

## Part 1: Probability and Random Variables

[TEACHING SECTION]

OAK: Let us start with the language of uncertainty. A probability is a number between zero and one that measures how likely an event is to occur. Zero means impossible. One means certain. Everything else falls in between.

NARRATOR: When we flip a fair coin, the probability of heads is zero point five. When a trainer enters a gym battle, the probability of winning depends on many factors -- team composition, type advantages, experience level. We use probability to formalize this uncertainty.

OAK: A random variable is a quantity whose value is determined by a random process. If we let X represent the number of badges a randomly selected trainer has earned, then X is a random variable. It might take the value zero, or three, or eight, depending on which trainer we happen to select. The key insight is that while any individual outcome is uncertain, the pattern of outcomes across many repetitions is predictable.

NARRATOR: Two fundamental properties of a random variable are its expectation and its variance. The expectation -- the expected value, or mean -- is the long-run average. If we could sample trainers forever and average their badge counts, that average would converge to the expected value.

OAK: The variance measures spread -- how far individual values tend to fall from the mean. A small variance means values cluster tightly around the mean. A large variance means they are dispersed widely. The standard deviation is simply the square root of the variance, and it has the advantage of being in the same units as the original variable.

NARRATOR: Conditional probability is where things get interesting for causal inference. The conditional probability of event A given event B is the probability of A among cases where B has occurred. For example, the probability of winning a gym battle given that you have a type advantage is typically much higher than the unconditional probability of winning.

OAK: Bayes' theorem connects conditional probabilities in a powerful way. It tells us how to update our beliefs when we observe new evidence. If we know the probability of having a type advantage given that we won, and we know the overall probability of winning and the overall probability of having a type advantage, Bayes' theorem tells us the probability of winning given that we have a type advantage. It is the mathematical foundation for reasoning from evidence to causes.

## Part 2: Key Theorems and Statistical Inference

[TEACHING SECTION]

NARRATOR: Two theorems underpin almost everything in this textbook.

OAK: The Law of Large Numbers says that as the sample size grows, the sample average converges to the population mean. This is why large studies are more informative than small ones: with enough data, the noise averages out and the signal remains.

The Central Limit Theorem goes further. It says that regardless of the shape of the underlying distribution, the sampling distribution of the sample mean becomes approximately normal -- bell-shaped -- as the sample size grows. This is why the normal distribution appears everywhere in statistics: it describes the behavior of averages, not individual observations.

NARRATOR: These two theorems give us the machinery for statistical inference.

OAK: A hypothesis test formalizes the question: is the pattern we see in the data real, or could it have arisen by chance? We start with a null hypothesis -- typically, that there is no effect. We compute a test statistic that measures how far the data are from what we would expect under the null. We then compute a p-value: the probability of observing a test statistic at least as extreme as ours, if the null hypothesis were true. A small p-value -- conventionally below zero point zero five -- leads us to reject the null.

NARRATOR: But a p-value is not the probability that the null hypothesis is true. It is the probability of the data given the null. This is a subtle but critical distinction that trips up even experienced researchers.

OAK: A confidence interval provides a range of plausible values for the parameter. A ninety-five percent confidence interval means: if we repeated the study many times, ninety-five percent of the intervals we construct would contain the true parameter value. It does not mean there is a ninety-five percent probability that the true value lies in this particular interval.

NARRATOR: One more important concept: standard errors. The standard error of an estimator measures how much the estimate would vary across repeated samples. Small standard errors mean our estimate is precise. Large standard errors mean it is noisy. Standard errors are the bridge between point estimates and confidence intervals -- the interval is typically the estimate plus or minus about two standard errors.

OAK: With these tools in hand, you have the mathematical foundation for the entire textbook. Everything else builds on probability, expectation, variance, the law of large numbers, the central limit theorem, hypothesis testing, and confidence intervals. When you encounter these concepts in the chapters ahead, you will know exactly what they mean.

NARRATOR: That concludes the mathematical foundations. When you are ready, return to Chapter One to begin your journey through Kanto.
