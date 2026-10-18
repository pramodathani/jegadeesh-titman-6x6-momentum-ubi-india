# Results: 6-month ranking, 6-month holding momentum on the 500 most traded NSE shares

Holding months: Dec 2020 to Sep 2026 (70 months). Price returns only. Four planned variants, run as six backtests (buy − sell with and without costs, winners with and without costs, losers without costs, buy − sell at 0.3% impact). Nothing was tuned.

## Table I, Panel A, J=6 K=6: paper against India

Average monthly return, Newey-West t-statistic (5 lags) in brackets, before costs.

| Portfolio | Paper (US, 1965–89, 300 months) | India (Dec 2020 – Sep 2026, 70 months) |
|---|---|---|
| Sell (losers) | 0.0079 (1.56) | 0.0126 (1.68) |
| Buy (winners) | 0.0174 (4.33) | 0.0249 (2.78) |
| Buy − sell | 0.0095 (3.07) | 0.0123 (3.06) |

The paper's t-statistics are as printed; their method is not stated. Ours are Newey-West.

## After Indian costs (brahmagupta delivery costs: STT, stamp, charges, GST, no brokerage)

| Portfolio | Impact per side | Mean/month after costs | NW t | Compound annual | Worst drawdown | One-way turnover a year | Costs a year |
|---|---|---|---|---|---|---|---|
| Buy − sell, before costs | – | 1.23% | 3.06 | 14.84% | −12.88% | 418% | 0 |
| Buy − sell, after costs | 0.1% | 1.08% | 2.69 | 12.85% | −13.54% | 418% | 1.76% |
| Buy − sell, after costs | 0.3% | 0.94% | 2.34 | 11.00% | −14.15% | 418% | 3.44% |
| Winners only, before costs | – | 2.49% | 2.78 | 30.79% | −26.87% | 199% | 0 |
| Winners only, after costs | 0.1% | 2.42% | 2.70 | 29.72% | −27.18% | 199% | 0.84% |
| NIFTY 500 price index | – | – | – | 13.18% | – | – | – |

The losers' compound annual return is 13.23%, against 13.18% for the NIFTY 500 (before costs).

Winners only, after costs, beat the NIFTY 500 by 16.5% a year (t of the monthly excess return 2.37) with a beta of 1.24. Buy − sell, after costs, has a compound annual return 0.33% below the NIFTY 500; it is a market-neutral paper portfolio, not a comparison with the index. Its alpha is 1.20% a month (t 2.57).

## Checks

- Both halves positive: first 35 months 1.27% a month (t 2.78), last 35 months 1.19% (t 1.88).
- The best five contributors out of 926 shares ever held: without them, buy − sell falls from 1.23% to 1.00% a month.
- By year, buy − sell: 2020 −0.9%, 2021 +1.6%, 2022 +0.7%, 2023 +1.5%, 2024 +1.7%, 2025 −0.1%, 2026 +2.4% a month. 2020 has only December.
- Turnover is not comparable with the paper's 84.8% per six-month period. Ours is a one-way annual figure of 418% for the long-short and 199% for winners only.
- 68 daily moves beyond −50% or +100% were set to zero (data/removed_daily_returns.csv). The largest influence is CUPID (−89.5% on 2024-04-04, a probable unadjusted split) and it is also the largest single contributor, at about 0.06% a month. The cleaning sets that day to zero, so its true return that day is lost, not invented.

## Caveats

- Short sample: 70 months against 300. The t-statistic for buy − sell is similar to the paper's, but 70 months of a bull market is a thin base. Winners' and losers' returns of 2.5% and 1.3% a month sit well above the paper's because Indian mid and small caps rose strongly in this window. Their level is not comparable.
- Survivorship: UBI's list holds today's symbols only, so shares that were delisted or renamed after December 2019 are missing (gaps 2, 4, 23). 79 still-listed shares have history ending before Sep 2026 and drop out as if delisted.
- Price returns only, for both the shares and the NIFTY 500 (gaps 7, 12).
- The short leg cannot be traded for most NSE cash shares; buy − sell is a paper portfolio, and its short side is costed as delivery.
- Trading is assumed at the close of the formation month.
- The backtest_reviewer subagent ran out of steps before returning a report. Its partial remark was that fragility checks had been run and the CUPID split was under examination. I ran the checks above myself instead: contributor concentration, subperiods, year by year and the series names in the universe (two hyphenated names, BAJAJ-AUTO and NAM-INDIA, are real shares). This is not an independent review. Say whether you want it rerun.
