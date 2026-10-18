# Plan for India: 6-month/6-month momentum on the 500 most traded NSE shares

Status: **draft, awaiting Pramod's approval** (written 2026-10-18).

## 1. What is reproduced

Only Table I, Panel A, the J=6, K=6 row with no skip (p. 70): the average monthly return and t-statistic of the sell (losers) decile, the buy (winners) decile and buy − sell. In the paper these are 0.0079 (1.56), 0.0174 (4.33) and 0.0095 (3.07) over January 1965 – December 1989.

Two things beside it:
- Turnover against the paper's 84.8% a semiannual period (p. 77).
- The after-cost return, against the paper's flat 0.5% one-way cost (p. 77).

## 2. What changes for India, and why

| Item | Paper | India version | Why |
|---|---|---|---|
| Market and universe | All NYSE/AMEX stocks with J months of returns (p. 69) | Each month-end t−1, the **500 most traded NSE shares** among those with a return in all six formation months. "Most traded" means the highest average of the six monthly medians of daily traded value (close × volume), using only months t−6 … t−1 | The user asked for the 500 most traded. It also screens out illiquid and penny shares (ambiguity A7). UBI has no market cap or index constituents (gaps 10, 11) |
| Dates | Jan 1965 – Dec 1989, 300 months | UBI daily data starts 2019-12-03. Monthly returns run Jan 2020 – Sep 2026; partial Dec 2019 and Oct 2026 are dropped. The first cohort forms at the end of Jun 2020. With all six cohorts required, holding months run **Dec 2020 – Sep 2026, about 70 months** | UBI history starts in December 2019 (gap 1) |
| Returns | CRSP daily returns compounded to months, dividends included | UBI daily closes adjusted for splits and bonuses, compounded to calendar months with brahmagupta's `ExportedPrices`. **Price returns only.** Daily moves below −50% or above +100% are treated as unadjusted corporate actions, set to zero and listed | Gaps 6 and 7. Dividends mostly cancel in buy − sell but lower the long-only return by about 1–1.5% a year |
| Ranking and portfolios | Ascending sort into deciles, equal weights, K overlapping cohorts, rebalanced monthly (p. 68) | The same. Deciles of 50 shares each; ties broken by symbol. brahmagupta's `OverlappingCohorts` gives 1/6 to each cohort, split equally among members that have a return that month | It matches the paper |
| Timing and lag | Formed on returns through t−1 and held from the start of t | Signal uses closes through the last trading day of t−1; the holding return runs from that close. No skip | This is the paper's Panel A. Trading at the same close is an idealisation (A9) |
| Shares that stop trading | Not stated (A5) | A share with no return in a holding month drops out, and its cohort's money is split over the remaining members (brahmagupta's rule) | — |
| Short selling | Losers shorted for six months | NSE cash shares **cannot be shorted overnight** by retail; only about 200 F&O shares can be shorted, via futures. buy − sell is reported as the **paper portfolio**, not a tradable one. The **long-only winners** decile against the NIFTY 500 is reported as the investable version | Indian market rules (A12) |
| Costs | Flat 0.5% one-way (p. 77) | brahmagupta `delivery` costs: STT 0.1% each side, stamp duty 0.015% on buys, NSE and SEBI charges, GST, zero brokerage, **impact 0.1% per side**. Results are shown before and after costs. For buy − sell, the short side is costed as delivery as well, which only approximates futures or SLB costs | ResearchRules.md; the impact level brahmagupta suggests for the top 500 |
| Settlement and hours | — | T+1 settlement, monthly trading at the close. Not material at a monthly horizon | — |
| Benchmark | CRSP value-weighted index | **NIFTY 500 price index from UBI** (checked: daily closes 2019-01-01 to 2026-10-16) | UBI has it. It is not total-return (gap 12), which is consistent with our price-only share returns |
| Risk-free rate | 1-month T-bill | None. Table I needs only raw returns. Excess over the NIFTY 500 is reported for the winners; no alpha against a risk-free rate | No risk-free series in UBI (gap 15). Kept out to keep the study small |
| Statistics | t-statistics, method unstated (A4) | Newey-West t-statistics with **5 lags (K−1)** for the overlapping cohorts, the number of months, worst drawdown and two subperiods, all from brahmagupta | ResearchRules.md |

## 3. Data

All from UBI through tradingmachine; nothing else is downloaded.
1. `export_prices`, nse / equities, whole segment, daily, 2019-12-01 → 2026-10-16, to `data/nse_equities_daily.parquet`. An earlier survey (phase3-check, 2026-10-18) counted 2,605 shares with candles. Monthly cross-sections run from 1,310 shares (Dec 2019) to 2,525 (Sep 2026), so there are always more than 500 to choose from.
2. `export_prices`, nse / equity_indices, NIFTY 500, to `data/nifty500_daily.parquet`. Already saved during the check above.

I relied on that one-day-old survey and my own NIFTY 500 check rather than running data_scout again.

## 4. Where India cannot match the paper

- **Short sample.** About 70 months against 300. Standard errors will be wide; a t-statistic near 3 needs a large, steady premium. The window includes the 2020 crash and rebound, the episode Daniel & Moskowitz (2016) say hurts momentum. Here the first holding month is December 2020, so the March 2020 crash itself falls only in formation windows.
- **Survivorship bias inside the window.** UBI's master holds today's symbols only. Shares that delisted or were renamed after Dec 2019 and left the master, such as HDFC (merged in 2023), are missing; renamed shares restart under the new symbol (gaps 2, 4, 23). This mostly removes failures, which usually helps losers look better and so understates momentum, but the direction is not certain.
- **Price returns only.** Both the shares and the benchmark exclude dividends.
- **Not a tradable short leg** (see above).
- **Universe.** The paper uses all stocks; this uses 500 liquid ones, where momentum is often reported weaker.

## 5. Variants

Every variant will be reported, and each is counted:
1. buy − sell, before and after costs (the main result)
2. winners only, long-only, against the NIFTY 500
3. losers only (for the table)
4. one cost sensitivity: impact 0.3% per side

No parameter search will be done.

## 6. Code and tests

Package `jegadeesh_titman_nse500_india`:
- `data/`: a class that loads the export through brahmagupta's `ExportedPrices` and cleans implausible daily returns.
- `momentum/`:
  - `LiquidUniverse`: the top-500 selection.
  - `FormationReturns`: six-month compounded returns and eligibility.
  - `DecileRanking`: winners and losers.
  - `MomentumStrategy`: builds the weights with `OverlappingCohorts`.
- `scripts/`: one program for monthly returns, one for building weights, and a call to `run_backtest`. Results go to `results/`.

Tests, on small made-up data with no network:
- Monthly compounding of daily returns.
- Eligibility needs all six formation months.
- The top-N liquidity pick uses only months t−6 … t−1. **No look-ahead:** changing month t's data leaves the month-t selection unchanged.
- Deciles: the right members, ties broken by symbol.
- Implausible-return cleaning.
- The long and short weights each sum to 1 in a fully formed month.

Before reporting, the backtest_reviewer subagent checks the backtest.
