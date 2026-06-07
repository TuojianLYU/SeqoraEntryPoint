---
name: serenity-market-strategy
description: Analyze markets, sectors, and individual tickers using a Serenity-inspired investment research framework focused on unknown bottlenecks, AI/semiconductor supply chains, hidden beneficiaries, catalyst timing, financial materiality, positioning, derivative/ETF pass-throughs, and downside invalidation. Use when the user asks for stock market direction, ticker recommendations, trade idea analysis, AI/semi supply-chain opportunities, or why a specific asset may be mispriced.
---

# Serenity Market Strategy

## Overview

Use this skill to analyze market direction and individual securities through a Serenity-inspired investment framework. The goal is analytical capability, not stylistic imitation.

Treat Serenity's public posts as examples of research instincts: finding overlooked bottlenecks, mapping demand into listed beneficiaries, checking whether the impact is financially material, and identifying where market pricing may be stale or structurally wrong.

Do not impersonate Serenity, promise returns, or present analysis as financial advice.

## Core Workflow

1. Define the question:
   - broad market direction
   - sector or theme analysis
   - single-ticker thesis
   - basket comparison
   - event/catalyst setup
2. Gather current facts before making a market call:
   - price action, valuation, estimates, market cap, revenue mix, balance sheet
   - recent earnings, guidance, news, filings, analyst revisions, macro calendar
   - sector peers, ETFs, options/volatility, positioning, and sentiment when relevant
3. Apply the Serenity lens:
   - What is the non-obvious bottleneck or demand shift?
   - Which obvious trade is crowded, and which beneficiary is more underpriced?
   - Is the demand material relative to the company's size or segment revenue?
   - Why might consensus, social chatter, or the instrument structure be missing it?
   - What catalyst can force repricing, and on what timeline?
   - What would invalidate the thesis?
4. Produce an investment-research output:
   - directional view with confidence level
   - bull case, bear case, and base case
   - catalyst map
   - financial materiality check
   - market-pricing / positioning read
   - key risks and invalidation signals
   - watchlist ranking when multiple tickers are provided

## Analysis Rules

- Browse or verify current data for time-sensitive market questions.
- Separate facts, assumptions, and inference.
- Prefer probabilistic language over certainty.
- Do not recommend position size unless the user explicitly asks for portfolio construction.
- Do not invent financials, analyst estimates, option data, or news.
- When data is missing, say what must be checked before the thesis is actionable.
- For broad index calls, connect macro catalysts to sector dispersion instead of only saying bullish or bearish.
- For ticker calls, explain why that ticker is a better or worse expression than peers, suppliers, customers, ETFs, or options.

## Output Formats

For a single ticker, use:

```text
View: Bullish / Bearish / Neutral / Watchlist
Confidence: Low / Medium / High
Timeframe: [days/weeks/months]

Thesis:
[one paragraph]

Serenity Lens:
- Bottleneck / demand shift:
- Hidden beneficiary:
- Materiality:
- Mispricing reason:
- Catalyst:

Cases:
- Bull:
- Base:
- Bear:

Risks / Invalidation:
- [risk]
- [what would prove the thesis wrong]

TLDR:
[one sentence]
```

For multiple tickers, rank them:

```text
1. [ticker] - [best expression / why]
2. [ticker] - [second-best / caveat]
3. [ticker] - [watch only / why]
Avoid / weak setup: [ticker] - [reason]
```

## Reference

Read `references/strategy-guide.md` for the detailed Serenity-derived strategy map, checklists, and scoring framework.
