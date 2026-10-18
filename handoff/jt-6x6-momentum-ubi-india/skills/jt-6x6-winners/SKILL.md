---
name: jt-6x6-winners
description: Use on the first trading day of each month to build the target portfolio of the long-only six-month winners decile of the 500 most traded NSE shares, a short test reproduction of Jegadeesh and Titman (1993) six-month momentum.
---

# Six-month winners (Jegadeesh and Titman 6x6), long only

## Strategy

At each month-end, take the 500 most traded NSE shares (highest average of the last six monthly medians of daily traded value, among shares with a return in all six months). Rank them on their compounded return over the same six months, with no skip month. The top decile, 50 shares, is that month's winners cohort. The portfolio holds the six most recent winners cohorts at once, each with one sixth of the money, split equally among its members. Each month the oldest cohort is dropped and the newest added, so about 120 to 150 different shares are held and the portfolio turns over roughly 200% a year one way.

It comes from Jegadeesh and Titman (1993), "Returns to Buying Winners and Selling Losers", Journal of Finance 48(1), Table I, J=6, K=6. This is a short reproduction on UBI daily prices from December 2019, made as a test of research-agent, and only the long winners leg is handed over: the paper's short leg cannot be traded in most NSE cash shares. Prices are adjusted for splits and bonuses but not dividends. Study and code: https://github.com/pramodathani/jegadeesh-titman-6x6-momentum-ubi-india

## Monthly target command

Needs Python with `pip install git+https://github.com/pramodathani/jegadeesh-titman-6x6-momentum-ubi-india`, which installs the study and brahmagupta, plus tradingmachine and a reachable UBI. Run it on the first trading day of the month, after the previous month's closing prices are in UBI:

    python scripts/build_targets.py targets.csv --previous last_targets.csv

It fetches about 14 months of adjusted daily candles for every NSE share from UBI (a few minutes), builds the six cohorts, and writes `targets.csv` with columns `symbol,weight`, weights adding to 1. It prints the month, the number of holdings, the largest weight and, with `--previous`, the joiners and leavers. It refuses to run if the prices stop more than five days before the last month-end. It never places or changes orders. Same prices give the same targets. `--prices <file>` reads an export_prices file instead of UBI.

## Risk limits

Suggestions for the user to put into TradingRules.md, not set by the study:
- Most per share: 3% of the portfolio (the strategy's own largest weight is 2%).
- Number of holdings: 100 to 160.
- Most per sector: 25%. UBI has no sector data, so trading-agent needs its own sector map; the study did not test any sector limit.
- Market exposure: the winners portfolio had a beta of 1.24 to the NIFTY 500, so expect larger swings than the index.
- Stop and review: the backtest's worst drawdown was −27.2% on monthly data; pause new buying for review at −35%.

## Capital minimum

Each share's smallest weight is 1/300 (0.33%), when it sits in one cohort of 50. On the latest targets (128 holdings, last closes from UBI), with whole shares only: ₹5 lakh leaves 21 of 128 holdings below one share and about 21% in cash; ₹10 lakh leaves 11 holdings below one share and 14% in cash; ₹20 lakh leaves 6 and 7%; ₹50 lakh leaves 1 and 3%. Suggested minimum: ₹10 lakh for a workable portfolio, ₹20 lakh for a faithful one. Add a depository charge on each share sold (about ₹15 per share sold; an assumption, check with the broker); brokerage is zero in the study's cost model.

## Backtest summary

Winners decile only, monthly, holding months Dec 2020 to Sep 2026 (70 months), price returns, after brahmagupta delivery costs with 0.1% impact per side. The benchmark is the NIFTY 500 price index.

| Measure | Value |
|---|---|
| Mean return a month, after costs | 2.42% (Newey-West t 2.70, 5 lags) |
| Mean return a month, before costs | 2.49% (t 2.78) |
| Compound annual return, after costs | 29.7% |
| NIFTY 500 compound annual return | 13.2% |
| Excess over the benchmark | 16.5% a year; monthly excess t 2.37 |
| Beta to the NIFTY 500 | 1.24 |
| Annual volatility | 23.8% |
| Sharpe ratio, no risk-free rate | 1.22 |
| Worst drawdown | −27.2% |
| Annual turnover, one way | 199% |
| Annual costs | 0.84% |
| Average holdings | 131 |

Independent review (backtest_reviewer): accept with caveats. Main caveats:
- Only 70 months, in a strong market for Indian mid and small caps. The result fades across the sample: the buy−sell spread was 1.24%, 1.41% and 1.04% a month in successive thirds.
- UBI lists today's shares only, so delisted and renamed shares are missing (survivorship bias, direction unclear).
- Price returns only; no dividends in the shares or the benchmark.
- UBI has no daily candles for any share between 2022-02-15 and 2022-03-07, which inflates March 2022.
- Some unadjusted splits and demergers slipped through the cleaning.
- The strategy is a high-beta, mid and small cap portfolio: most of its excess return over the NIFTY 500 comes with a beta of 1.24, and the alpha is 1.0% a month (t 1.85).
- Full numbers: references/backtest_summary.md and the study's results/summary.md.
