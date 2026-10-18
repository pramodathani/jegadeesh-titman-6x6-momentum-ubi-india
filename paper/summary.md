# Jegadeesh and Titman (1993): summary for this study

## This study's scope

This study reproduces only the **6-month formation, 6-month holding strategy with no skip** (Table I, Panel A, J=6, K=6; p. 70). The target numbers are:

| 6/6, Panel A (no skip), Jan 1965 – Dec 1989, 300 months | Average monthly return | t-statistic |
|---|---|---|
| Sell (losers, lowest decile) | 0.0079 | 1.56 |
| Buy (winners, highest decile) | 0.0174 | 4.33 |
| Buy − sell | 0.0095 | 3.07 |

Checked for this study on 2026-10-18 against the page images and text of `paper/jegadeesh-titman93.pdf`:
- Table I (journal p. 70, PDF p. 7): the 6/6 row above matches exactly.
- Method (p. 68–69): stocks are ranked in ascending order, deciles are equally weighted, holding periods overlap, and returns come from portfolios rebalanced monthly. Buy-and-hold was "very similar" with slightly higher returns.
- Costs (p. 77, fn 12–13): 84.8% semiannual turnover (buy side 86.6%, sell side 83.1%), and 9.29% a year risk-adjusted return after a 0.5% one-way cost.

The full summary below was written by an earlier analyst (project phase3-check). It is reused as instructed, and its 6/6 figures were re-verified as listed above. Sections on other strategies (the rest of Table I, Tables II–IX) are kept for context only; this study does not reproduce them.

---

Jegadeesh, N. and Titman, S. (1993). "Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency." *Journal of Finance* 48(1), 65–91. Source: JSTOR copy in `paper/jegadeesh-titman93.pdf`.

Page references are **journal pages** (p. 65–91). In the PDF, journal page = PDF page + 63 (PDF page 1 is the JSTOR cover). Table I was checked against the page image, not only the extracted text.

## 1. The question and the main claim

**Question.** Do relative-strength strategies make money over 3- to 12-month horizons? These strategies buy stocks that did well over the past 3–12 months and sell those that did badly. If they do, is the profit pay for systematic risk, a lead-lag reaction to common factors, or a delayed reaction to firm-specific news? (p. 66–67)

**Main claim.**
- All 32 J/K strategies earn positive zero-cost returns on NYSE and AMEX stocks, 1965–1989. All except 3/3 without a skip are statistically significant (p. 69).
- The 6/6 strategy earns about 1% a month, which is "a compounded excess return of 12.01% per year" (p. 69, p. 89).
- The profits are not explained by beta or size. The winners-minus-losers portfolio has a slightly negative beta of −0.08 (Table II, p. 73).
- They are not explained by lead-lag effects either; the regression of profits on lagged squared market returns has a negative slope (p. 75).
- The authors read this as delayed reaction (underreaction) to firm-specific information.
- Part of the gain later reverses. Cumulative 6/6 profit peaks at 9.51% at month 12 and falls to 4.06% by month 36 (Table VII, p. 84).
- Returns around earnings announcements follow the same pattern (Table IX, p. 88).

## 2. Data

| Item | Paper | Page |
|---|---|---|
| Market | US: NYSE and AMEX common stocks | p. 67 |
| Return source | CRSP daily returns file, July 1962 – Dec 1989; monthly returns made by compounding daily returns | p. 68–69, fn 4 |
| Universe each month | "All stocks with available returns data in the J months preceding the portfolio formation date." No price, size or liquidity filter is stated | p. 69 |
| Main test period | Jan 1965 – Dec 1989, 300 months. 1965 is the first full year in which the 12/12 strategy can run, since it needs 23 months of lagged data | p. 69 fn 4, p. 70 |
| Back-test periods | 1927–1940 and 1941–1964 (6-month strategy, event time only) | p. 85 |
| Market proxy | CRSP value-weighted index (also the equal-weighted index in places) | p. 77 |
| Risk-free rate | 1-month Treasury bill | p. 77 |
| Size | Market capitalisation (Table II units not stated; probably $ millions) | p. 73 |
| Betas for subsamples | Scholes-Williams betas from daily returns in the calendar year before formation | p. 78 |
| Earnings dates | COMPUSTAT quarterly, 1980–1989; on average 429.2 announcements a month | p. 87 |

CRSP includes delisted stocks, so the paper is survivorship-free. Delisting returns are not mentioned.

## 3. The method, step by step

**Strategy grid.** J ∈ {3, 6, 9, 12} months of formation and K ∈ {3, 6, 9, 12} months of holding give 16 strategies. Each is run twice: Panel A with no gap, and Panel B with a 1-week skip between formation and holding. That makes 32 strategies (p. 68).

For one J/K strategy:

1. **Monthly returns.** Compound CRSP daily returns into calendar-month returns for each stock (fn 4, p. 69).
2. **Eligibility.** At the start of month t, a stock is eligible if it has returns data for all J months t−J … t−1 (p. 69).
3. **Formation-period return.** Compute each eligible stock's cumulative return over months t−J to t−1.
4. **Ranking.** Sort ascending into ten deciles. The **lowest** decile (P1) is the *losers* or *sell* portfolio, and the **highest** (P10) is the *winners* or *buy* portfolio (Table I caption, p. 70).
5. **Weights.** Each decile is equally weighted (p. 68).
6. **Skip (Panel B only).** The portfolio is formed one week after the formation-period returns are measured (p. 68, p. 70). See ambiguity A3.
7. **Overlapping holdings.** In month t the strategy buys the winners and sells the losers formed at t, holds them K months, and closes the position opened at t−K. At any time it holds K overlapping cohorts formed at t, t−1, …, t−K+1, each with weight 1/K. So 1/K of the book is revised each month (p. 68).
8. **Rebalancing within cohorts.** The reported returns come from portfolios **rebalanced monthly to equal weights**. Buy-and-hold versions were "very similar", with slightly higher returns, and are not reported (p. 68).
9. **Strategy return for month t.** Average the K cohorts' returns for the buy side, do the same for the sell side, and take buy minus sell. This is the return per dollar long of a zero-cost portfolio (p. 69).
10. **Statistics.** Report the time-series average monthly return and its t-statistic over Jan 1965 – Dec 1989 (Table I). Bonferroni is used for the 32 tests (p. 69). Newey-West standard errors are used for the cumulative event-time returns (fn 16, p. 83).
11. **Risk adjustment.** The market-model regression is r_p − r_f = α + β(r_m − r_f) + ε, with the CRSP VW index and the 1-month T-bill. α is the abnormal return (eq. 9, p. 77).
12. **Costs.** Semiannual turnover for 6/6 is 84.8% (buy 86.6%, sell 83.1%). With a 0.5% one-way cost, the risk-adjusted return is 9.29% a year (p. 77, fn 12–13).

**Event-time study (Table VII).** Form 6-month-return deciles each month and track the zero-cost portfolio's return in each of the 36 months after formation. The t-statistics on cumulative returns use Newey-West (p. 83–84).

## 4. Table I: the 6/6 strategy (p. 70)

Average monthly returns with t-statistics in parentheses, January 1965 – December 1989.

| 6-month / 6-month | Panel A (no skip) | Panel B (1-week skip) |
|---|---|---|
| Sell (losers, P1) | 0.0079 (1.56) | 0.0068 (1.35) |
| Buy (winners, P10) | 0.0174 (4.33) | 0.0178 (4.41) |
| **Buy − sell** | **0.0095 (3.07)** | **0.0110 (3.61)** |

Context from the same table:
- The best strategy is 12/3: 1.31% (t 3.74) in Panel A and 1.49% (t 4.28) in Panel B (p. 69).
- The weakest is 3/3 in Panel A: 0.32% (t 1.10), the only one that is not significant (p. 69).

Checks elsewhere in the paper:
- Table III (p. 78) gives the "All" P10−P1 as 0.0095 (3.07), the same as Table I.
- Its market-model excess return is 0.0100 (3.23) (Table III Panel B, p. 79).
- With the equal-weighted index as benchmark, α = 0.0115 (t 3.84) (p. 77).

## 5. Robustness checks in the paper

| Check | Result | Where |
|---|---|---|
| 1-week skip (Panel B) | Returns slightly higher than with no skip | Table I, p. 69–70 |
| WRSS (weights = past return minus the EW index) | 4.5% per semiannual period (t 2.99); correlation 0.95 with the decile strategy | p. 71 |
| Beta and size of the deciles | Losers have beta 1.36 and winners 1.28; P10−P1 beta −0.08; both extremes are smaller than average | Table II, p. 73 |
| Serial covariance | EW index 6-month serial covariance −0.0028; average residual serial covariance +0.0012 | p. 73–74 |
| Lead-lag test (profit on lagged squared market return) | θ = −2.29 (t −1.74); halves −2.55 (−2.65) and −1.83 (−2.52) | p. 75 |
| Size terciles S1/S2/S3 | P10−P1: 0.99%, 1.26%, 0.75% a month, all significant | Table III, p. 78 |
| Beta terciles | 0.62%, 0.79%, 1.08% | Table III, p. 78 |
| Market-model alphas | P10−P1 α = 1.00% (t 3.23); comes from the winners side | Table III B, p. 79; p. 77 |
| Transaction costs | 0.5% one-way cost → 9.29% a year risk-adjusted, still significant, also in each size group | p. 77 |
| Calendar months | January −6.86% (t −3.52); Feb–Dec +1.66% (t 6.67); April positive in 24 of 25 years | Tables IV–V, p. 80–81 |
| 5-year subperiods | Positive in 4 of 5; 1975–79 −0.44%, driven by small-firm Januaries | Table VI, p. 82 |
| Event time, 36 months | Cumulative 9.51% at month 12, 4.06% at month 36; month 1 −0.25% | Table VII, p. 84 |
| Back-test 1927–40 | Cumulative −40.81% by month 36; month 1 −4.95% | Table VIII A, p. 86 |
| Back-test 1941–64 | Similar to 1965–89; gain gone by month 24 | Table VIII B, p. 87 |
| Earnings announcements | Winners beat losers by about 0.7% around announcements in months 1–6, and lose in months 8–20 | Table IX, p. 88 |

## 6. Ambiguities a replication must decide

- **A1. Which decile is "top".** The text on p. 68 says stocks are ranked in ascending order and calls the "top decile" the losers. The Table I caption (p. 70) says the lowest decile is the sell portfolio. Both mean the same thing: **winners = highest past return**. Code it that way.
- **A2. Rebalanced versus buy-and-hold within a cohort.** The tables report monthly rebalancing to equal weights (p. 68). Turnover and costs would differ under buy-and-hold. Choose rebalanced and report both.
- **A3. The skip.** "1 week" in Panel B is not defined precisely: 5 trading days or 7 calendar days, and whether the holding period moves by a week or the return window does. Modern practice skips a full **month**, which is a different strategy. Decide and state it.
- **A4. How the t-statistics are computed.** Table I does not say whether they are plain OLS t-statistics or autocorrelation-adjusted. The overlapping cohorts make the monthly series autocorrelated. Only the event-time t-statistics are stated to be Newey-West (fn 16). Our rules require Newey-West, so the lag length has to be chosen (for example K−1).
- **A5. Eligibility and missing data.** The paper requires returns over the J formation months only. It does not say what happens when a holding-period stock delists or stops trading. Choose a rule, for example cash at 0 for the rest of the month or the last return, and decide on delisting returns.
- **A6. Deciles with ties and small cross-sections.** The method for decile breakpoints is not given. For India's smaller universe, decide how many stocks a decile needs and how to break ties.
- **A7. No filters.** The paper uses no price or size screen. In India a liquidity screen (minimum traded value, no illiquid or penny shares) will be needed. Report results with and without it.
- **A8. Dividends.** CRSP returns include dividends. Without dividend adjustment, returns are price-only.
- **A9. Calendar alignment.** "Beginning of month t" means using closes up to the last trading day of t−1 and trading on the first day of t. Execution-price conventions (close against next open) are not stated.
- **A10. "Excess return 12.01% a year"** (p. 89) is not derived explicitly. It seems to compound the 6/6 risk-adjusted monthly return. Treat it as a headline, not a target number.
- **A11. Costs.** The paper's 0.5% one-way cost is a flat assumption (p. 77). India requires the full cost stack (brokerage, STT, stamp duty, exchange, SEBI, GST, impact), as in ResearchRules.md.
- **A12. Short selling.** The paper assumes losers can be shorted for K months. That is not possible for retail in NSE cash shares beyond intraday; only F&O stocks can be shorted, through futures. The India version must say what the short leg means.
