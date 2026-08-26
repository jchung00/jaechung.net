---
title: Will AI Solve Markets?
date: 2026-08-24
summary: Can AI-driven trading clearly outperform previous iterations of systematic trading — and who will do it?
---
I have been grappling with this question for quite a while. It's become more of a hot topic recently. Every week, I hear of a new "neotrading lab" that is looking to solve markets using AI, some funded by YC.

Will AI solve markets?

If so, who?

Let's first define the question with a quick thought experiment.

If markets are completely, 100% solved, then markets should be perfectly efficient.

Price should become a pure reflection of all information. In any timeframe (t), expected price at t+1 should be a function of current price plus the risk-free rate and some risk premium.

Simply put, returns come from the cost of capital + cost of bearing risk. Classic profit centers in systematic trading such as market making, arbitrage, statistical arbitrage, etc should vanish.

I don't think this day will come anytime soon, if ever.

The market is a hot, rolling swarm of millions of participants. This causes a lot of entropy. The true distribution of reality is constantly evolving, and is non-stationary. With massive amounts of high quality data and information, you could get closer and closer to modeling the true distribution of how the market *should* price things. But that doesn't mean the markets will always behave that way.

A lot of the time, short term prices are a function of human emotion and speculative flows.

I think the real question here is:

**Will AI-driven trading clearly outperform previous iterations of systematic trading?**

Can AI outperform Jim Simons, "the man who solved the market"? RenTech averaged ~66% annual returns for over three decades at scale. That's a pretty high bar.

---

## What is AI capable of?

Intuitively, if AI can find alpha in markets, it seems like the most obvious way to monetize tokens. If returns per token > cost per token, you could have a money printing machine!

But how can we get AI to generate alpha? You could prompt Claude Code to build you an arbitrage bot and spend a lot of tokens doing so. But it won't generate you much in returns, if any.

To actually get close to solving this problem, it's important to understand the trading world and make a focused attempt at finding an edge.

In [*Starting a quantitative trading firm with 0 experience*](/writings/starting-a-quant-trading-firm/) I talked about the main edges that top firms have:

<figure><img src="/images/systematic-trading-edges.png" alt="1. Speed/latency (trading infrastructure), 2. Proprietary data/flow, 3. Research/alpha generation"></figure>

Let's start by touching on **speed/latency**.

A lot of the alpha in high frequency trading comes from the infrastructure, a lot of which is physical. In fact, having a low latency infrastructure is a prerequisite to even participate in this game. Trading opportunities will simply be invisible to you (happens too quickly or gone already) without it.

The state-of-the-art in traditional HFT is already hyperoptimized through many years of extreme competition. The level of innovation here has been shocking. A tick-to-trade is on the order of nanoseconds through FPGA/ASIC hot pathing. Pre-armed decisions on trading strategies trigger almost instantaneously. Jump has built crazy levels of custom hardware and microwave towers to gain an edge. Most top firms are colocated directly with the exchanges.

In pure arbitrage strategies, a fancy model at inference time with greater intelligence would only lead to more FLOPs and slow the trade down.

Sure, AI could help you build a strong low latency trading system, but it's unclear to me how AI would help gain a meaningful edge over incumbents in the pure HFT world.

One could argue that AI based models could become better short horizon price predictors than the typical linear / tree models when trading alpha-based predictive models. What if you could compress a big transformer-based model trained on massive amounts of orderflow data into a much smaller one that can run on a microsecond-level envelope? Could the larger model's predictive model survive the compression? What if we innovated specific inference hardware (Etched-style) that makes transformer inference a couple OOMs faster?

These are definitely cool projects, and I'm a huge tech optimist and AGI believer. But I'm somewhat skeptical that this could really generate significantly higher returns in the HFT world. Why?

1. It could be that existing small models (linear / small trees) already extract most of the extractable signal already for this specific timeframe
    1. A simple analogy would be that you don't need Fable to solve a simple linear equation like 2x+5=7 for you. It's overkill.
2. Even if there is some additional predictive power coming from bigger, transformer-like models, would the improvements really be significant enough to clearly outperform?
    1. It is more likely that bigger models would end up overfitting.
3. Bigger models at inference come with a big latency tradeoff that faces massive barriers.

Today, latency-sensitive HFT strategies that require more software / computation for "smarter" decision making (trading off of alphas, not as much for pure arb) can't really fit anything close to modern transformer-based models. A simple forward pass requires weights streamed from memory. Even just reading 1B parameters *once* would take hundreds of mics to milliseconds.

The LLM-class inference we think of is probably 4-5 OOMs outside the latency budget for these ultra low timeframe strategies. For example, local inference of a ~100B parameter model would be 50-100ms, which is already 4 OOMs higher than the latency budget for some low-latency trades (10 micros). These are memory-bandwidth constraints that typical engineering won't be able to solve immediately.

There has been some [work](https://newsroom.amd.com/news/amd-acquires-taalas-ai-inference/) baking LLMs into ASICs already. For event-driven trades in HFT, LLMs could definitely be better at parsing announcements / earnings details and produce higher accuracy. But there will likely still be a tradeoff in the end of accuracy vs speed, and if a general classifier can still produce 90% of the accuracy but gets a better fill, the net returns may end up being similar.

### Proprietary data/flow

Another meaningful edge in systematic trading comes from proprietary data/flow. Market makers pay brokers for sending retail flow to them instead of the exchange (PFOF). A lot of the top firms have secured long term exclusive contracts, allowing them to trade on this high quality data and flow, some of which are immediately monetizable.

Retail flow is valuable because it's mostly uninformed. Market makers can fill it and pocket nice spreads.

It seems pretty clear that AI probably won't drastically change the game of proprietary data/flow anytime soon. The moat here is the exclusivity/access to the contracts.

---

## Quant research / alpha generation

AI probably has a better chance to disrupt quant research in the nearer future, especially in longer timeframes (mid-frequency / stat arb).

In systematic trading, researchers build models that generate alphas (predictions). These alphas can then be monetized.

Here's a simple example: you could create a fair value stream using the predictions (predicting the "fair value" of what the market should be at), and trade the current book against the predicted fair value. You would buy when the price is below your fair value, or sell when the price is above. If your predictions are mostly accurate (your alphas are good), you would generate returns.

Quant research shops typically have teams of human researchers following some form of this research loop:

1. Come up with an idea/hypothesis where there could be signal
2. Get the data / prune it
3. Feature engineering (take raw data and transform them into features)
4. Backtest model on historical data
5. Repeat until model is stronger
6. Simulate model on live data
7. Maybe deploy if strong enough

AI researchers may find this process strikingly familiar.

If you believe in AGI and that AI researchers will crack recursive self improvement, the quant research loop should seem automatable as well.

Instead of being limited to a smaller number of human researchers who need to eat and sleep, you could spawn thousands of AI agents that could be deployed across each step of the research process and review each other's works. Human researchers could focus on evaluation and discipline.

Note that in the above example, AI inference is not required in a production trading environment. We could use the power of AI to accelerate research and find stronger alphas, but the alphas can be traded with an existing monetization strategy and trading system. This reduces latency / computations needed during the actual trade execution.

This is likely what the optimal usage of AI in systematic trading looks like: a fully agent-integrated research infrastructure that constantly prints out new and improved alphas.

There's clear potential here, and could significantly improve upon previous iterations of systematic trading.

---

## How will they solve it?

If AI is indeed capable of solving quant research, who will do it, and how?

### The incumbents

Systematic trading is naturally hypercompetitive. There is no shortage of top-tier firms with some of the smartest people in the world trying to find an edge over each other.

Within just mid-frequency / stat-arb, which is where I identified as potentially the most "disruptable" by AI in the stack, you'll find some legendary names: RenTech, DE Shaw, Two Sigma, Citadel, Millennium, Jane Street, HRT and more. Most of these firms aren't just limited to higher timeframes. They have state-of-the-art trading systems that make some of them apex predators even in the HFT world.

These firms have some flavor if not all of the main edges already: speed/latency, proprietary data/flow, and the best quant researchers.

In the AI-powered quant research race, having large amounts of proprietary data will be difficult to overcome. When it comes to models, a critical limiting factor is whether your training set could capture a better empirical distribution of reality. Having access to more private (and higher quality) data that is already directly monetizable likely allows for the research loop to come up with stronger alphas.

An obvious key advantage is capital and scale. These firms have billions of dollars to acquire the best talent and fund ambitious research projects. They also have battle tested state-of-the-art infrastructure running ridiculous volumes in production. Their flow alone could be extremely valuable data for AI-powered research.

One "weakness" could be that incumbents are slow to adopt new technologies. Their infrastructure could be so robust that it has become rigid and difficult to change without breaking things.

This doesn't really seem to be the case though. Most of the people at these firms are highly technical, and extremely familiar with the core concepts of ML. Quant research and AI research have a lot of similarities already. Integrating AI into their existing research infrastructure and process doesn't seem too out of the ordinary. I believe they are already using AI across the stack to varying degrees.

Jane Street is clearly very pro-AI, and has been investing massive check sizes into some of the best companies. Their Anthropic stake alone added around $830M to a single quarter's trading revenue. It wouldn't be a surprise if they leveraged their relationship in order to get early access to the best, unreleased models. Maybe they would be willing to pay a premium on tokens to unlock stronger model capabilities and monetize them at a significant profit.

I think there's a high chance that AI-powered quant research will make a significant impact in the industry, and that in the future it will almost become a prerequisite to use it to some degree to generate competitive alphas in some automated way, similar to how a certain level of hardware and trading system became a prerequisite for traditional HFT.

The game could converge to maximizing dollar returns per token and increasing token efficiency, where tokens are just part of a trading strategy's cost function. Edge will come from how much proprietary, high quality data and scale a firm can have.

### "Neotrading labs"

I've been hearing "neotrading" a lot more recently, as more and more labs focused on trading keep popping up on my feed.

They are usually focused on a broad mission along the lines of "we will use AI to solve markets" or "we will use AI to hypercharge traders".

I think it would be helpful for these teams to focus on a specific area of the market to compete in. They should identify which type of trade they want to tackle (I'd recommend mid-frequency / stat-arb for the reasons above). They should also try to search for a pocket of the market where there is less competition (for now) and focus the whole team on that at first. Long-tail opportunities usually have less eyes on them.

For Manifold, this was getting in somewhat early on DEXs. Though it was a small pocket of the market back then, getting ahead of the curve gave us visibility on what to work on next, and we found ourselves in a positive feedback loop where we could iterate on real trades and data quickly.

Instead of running a massive research infrastructure buildout off the bat, they should identify the core components that are needed to complete, test, and trade the research loop.

Among many other things:

- Reliability should be the number one priority.
- Market data recorders should be clean and verifiable.
- The backtester and simulator should be transparent and easy to evaluate.

It's always better to start with a simple setup that you can trust. Complexity introduces obscurities that can really slow down progress. Making the research infrastructure easy for anyone to use also comes with more benefits. For example, agents could use/reconfigure it for more open ended research questions for free.

The first ones to complete a full agentic research loop, deploy an alpha in production, and generate even a small amount of real PnL will likely accelerate quickest from there.

As for the ideal team, I think that some combination of top AI researchers that worked at the frontier labs paired with some of the best quant researchers from the tier-1 stat-arb firms would be best for this mission. If the AI researchers on the team can convince their peers at the frontier labs to give them unreleased model access, or have special deals in place that reduce their token costs, this could evolve into a real edge.

It may be hard for neotrading labs to hire some of the best quant researchers. The good ones are extremely well paid, have several contractual barriers in place making it hard for them to leave, and are somewhat notorious for not being big risk takers in the first place. Ideally, the founding team is already a combination that has great respect and connections within their respective communities.

This may sound somewhat contradictory because I founded Manifold with no quant experience. Well, I don't recommend it. Manifold would probably have reached profitability sooner if I had prior experience. Solving markets with AI is arguably much harder and even more competitive than where I started. It will likely require some truly hardcore people. Jim Simons did it with some of the best scientists and mathematicians.

Even then, this journey will be far from easy for a startup. They will have to overcome a lot of the built-in advantages that the giants have. It's not impossible. But it definitely won't be a smooth sail where they turn on their agents and they start printing money.

---

## Reflection

It's amazing to see what humans are capable of.

I've seen first hand the crazy level of innovation and optimization in systematic trading. I've experienced the crazy growth of the AI boom in the last few years. The two spaces are now potentially starting to merge.

It's probably only a matter of time before AI-powered quant research makes massive upgrades to systematic trading.

It's also great to see more use cases for AI being monetized. Markets are a clear way to monetize tokens if done correctly. Hopefully this will bring more value back to the AI labs to power even more ambitious (and safe) research and scientific discoveries.

I know I'm being hypocritical, but I kind of wish that the smartest people would look into other exciting problems that could be much more valuable to the world.

The incentives of printing money off of markets inevitably pushes some of our best minds toward systematic trading. But systematic trading is a zero-sum game. The "we're making markets more efficient" argument is mostly cope. The fact that there's even a debate should be quite telling. Maybe the first 90% of innovations in market efficiency was socially valuable, but the marginal nanosecond upgrades to win the arbitrage faster does nothing for the world.

Solving coding was just the start. Solving Physical AI (robotics), our own biology (drug discovery, increasing our lifespans), etc are all exciting, interesting, and difficult problems that need more smart minds on it.

These are enormously positive sum endeavors, and can truly make our lives much better. Hopefully the AI labs will truly focus on pushing on these verticals despite immediately monetizable gains and push towards a better future. And hopefully the smartest people will be attracted towards building that future now.
