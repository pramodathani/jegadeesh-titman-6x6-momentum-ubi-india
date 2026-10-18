# Adversarial review: JT 1993 J=6 K=6 momentum, top-500 traded NSE shares

Reviewer: backtest_reviewer subagent, 2026-10-18. Work in progress; checks appended as done.

## 1. What was tested
Jegadeesh & Titman (1993) Table I Panel A, J=6 K=6, no skip. Universe: 500 shares with highest 6-month average of monthly median daily traded value (close x volume), must have returns in all 6 formation months. Deciles by compounded 6-month price return; equal-weight overlapping cohorts (brahmagupta OverlappingCohorts), cohort formed at end of t held t+1..t+6. Data: UBI daily closes (back-adjusted for splits/bonuses, not dividends) 2019-12 to 2026-10, months 2020-01..2026-09; daily moves < -50% or > +100% set to 0. Holding months Dec 2020 - Sep 2026 (70). Headline (no costs): buy-sell 1.23%/mo NW t 3.06; delivery costs 0.1% impact 1.08%.

## 2. Look-ahead (code reading)
- FormationReturns: rolling 6-month product ending at t (formation_returns.py). LiquidUniverse: rolling 6-month mean of traded value ending at t, eligibility = returns in t-5..t (liquid_universe.py). Both use only months <= t.
- OverlappingCohorts.weights: for holding period p uses cohorts p-K..p-1 (overlapping_cohorts.py), i.e. cohort formed at end of t first held in t+1. No skip, as specified. Correct.
- Known JT-style look-ahead: within a cohort, weight is split among members with a non-NaN return *in the holding month* (`has_return` of period p). The construction knows which shares trade in month p. A share that stops trading mid-holding drops out with its last partial month counted (a month is NaN only if no close at all), so the main bias is: shares with zero closes in a month are silently dropped and re-weighted. Impact quantified below.
- Truncation test: universe and scores at 2023-06 rebuilt from data cut at 2023-06 are identical to the full-sample ones. Rebuilt weights from the code match data/weights_buy_minus_sell.parquet exactly. No look-ahead in ranking or universe.
- Holding-month knowledge: 17 of 21,750 winner member-months and 50 of 21,750 loser member-months were dropped because the share had no return in that month (0.08% / 0.23%). Immaterial, and if anything it removes suspended losers the short side would have gained on.

## 3. Independent recomputation
- sum(W x R) by month from data/*.parquet: winners 2.492%, losers 1.264%, buy-sell 1.228%/month, NW(5) t 3.06, 70 months 2020-12..2026-09. Max abs difference against periods.csv 1.2e-16. Hand check 2023-06 (245 holdings): 0.0149835 vs periods.csv 0.0149835.
- Winner and loser weights each sum to 1 in every held month; buy-sell sums to 0, gross 1.88-1.91 (shares in both legs across cohorts net). periods_with_unpriced_weight = 0 in every result.json; unverified_rates = [].
- Tests: 10 pass with PYTHONPATH=src (they fail at import under the gateway venv without it, because the package isn't installed there; not a code fault).

## 4. Data
- **Market-wide gap: there are no candles for any share from 2022-02-15 to 2022-03-07** (trading dates jump 2022-02-14 -> 2022-03-08, 22 calendar days). The NIFTY 500 file does have those days. Effects: (a) the Feb 2022 stock returns cover only 1-14 Feb, and the 15 Feb-8 Mar move (the Ukraine sell-off) is booked to March 2022; (b) the March 2022 holding month, buy-sell +9.32% (3rd best of 70; winners +4.97%, losers -4.35%), includes two weeks earned before the end-Feb cohort was formed; (c) the benchmark is misaligned for those two months (NIFTY 500 Feb -4.11% / Mar +4.10% vs equal-weighted universe Feb -5.19% / Mar -0.42%). Dropping March 2022: mean 1.11%, t 2.75. Dropping Feb and Mar 2022: 1.12%, t 2.74. Smaller gaps: 2021-07-27 (5 days) and 2023-08-17 (6 days). This is not listed in tradingmachine_gaps.md.
- price_factor: across 450 factor changes the daily return is uncorrelated with the factor ratio (corr -0.006), so closes are generally back-adjusted. But 7 factor-change days still show the raw ratio (unadjusted); 5 of them fall just inside the -50% cut and were **not cleaned**: BHARATRAS 2025-12-12 -46.3%, GPIL 2021-10-26 -45.0%, MAANALU 2023-07-27 -47.5%, NAZARA 2025-09-26 -49.8%, POWERMECH 2024-10-08 -49.9% (all 1:1 bonus/2:1 split). EASEMYTRIP 2022-11-21 -40.0% (factor 0.125->0.5) looks partly adjusted.
- Held exposure to these: GPIL (winner, -0.75% of portfolio return in 2021-10), NAZARA (winner, -0.37% in 2025-09), EASEMYTRIP (winner, -0.35% in 2022-11). Demergers with no spin-off credit hit losers: PEL 2022-08-30 -44.8% (+0.13%), RAYMOND 2024-07-11 -36.6% (+0.22%). Net effect of the listed events on buy-sell: -1.13% in total, -0.016%/month. The errors mostly *reduce* the result. Non-factor -21% to -50% daily drops in held shares are real events (Adani Feb 2023, 4 June 2024 election day, INDUSINDBK, RBLBANK) or the 2022-03-08 gap.
- CUPID 2024-04-04 (-89.5%, factor 0.1->0.2, so the factor itself is wrong for a 1:10 split plus a bonus) was correctly zeroed. CUPID has zero weight in 2024-04.
- Held share-months beyond +100% (6) or below -50% (9): all checked ones are gradual moves at the circuit limit (max day ±20%) or real crashes (Adani Feb 2023), not data errors. DHANI 2022-03 (-51%) is the gap month.
- Survivorship: 79 of 2,605 symbols end before 2026-09. Merged or delisted names (HDFC, LTI, MINDTREE, IBULHSGFIN) are absent, and renamed shares restart at the rename (UNITDSPR from 2024-06, SAMMAANCAP from 2024-07, ETERNAL ends 2025-04). Both legs lose their history before the rename. Missing failed shares most plausibly flatter the losers leg's return (understating buy-sell); missing pre-rename histories cut universe eligibility. The direction for buy-sell is uncertain; size unknown without bhavcopy data.

## 5. Costs
- Delivery model: buy 0.2186%, sell 0.2036% including 0.1% impact; brokerage 0; no rates flagged unverified. Turnover 418% bought and 424% sold a year (one-way), so costs are 1.76%/year (0.147%/month). The long-short is costed on |Δw| of both legs, which is correct for weights netting to zero (gross 1.9). Missing: no securities-lending fee for the short leg (NSE SLB fees for mid/small caps can run to several %/year); the short leg is not implementable in the cash market for most of these shares. The first month carries an entry cost (0.40%); the final exit is not charged (minor).
- Rerun at double impact (0.2%, results/review/buy_minus_sell_impact02): 1.01%/month after costs, NW t 2.52, CAGR 11.92%, costs 2.60%/year, alpha 1.13% (t 2.42). Compare 1.08% (t 2.69) at 0.1% and 0.94% (t 2.34) at 0.3%.

## 6. Snooping and fragility
- 3 distinct portfolios (6 backtests); one J/K was specified in the plan, with no grid. Bonferroni x3 on t 3.06: p ≈ 0.009. It survives.
- Thirds: 2020-12..2022-10 1.24% (t 3.17); 2022-11..2024-09 1.41% (t 1.87); 2024-10..2026-09 1.04% (t 1.31). Significance is front-loaded, and the last third alone is not significant.
- Without 2024-01 (+14.6%, the best month; IFCI, IRFC, ELECTCAST, DBREALTY): 1.03% (t 2.76). Without the best 3 months: 0.78% (t 2.37).

## 7. Against the paper (JT 1993 Table I, 6/6)
| | Paper | India | Comment |
|---|---|---|---|
| Sell | 0.79% (1.56) | 1.26% (1.68) | Level reflects the 2020-26 Indian small/mid-cap bull market, not comparable |
| Buy | 1.74% (4.33) | 2.49% (2.78) | Same; also price-only (no dividends) |
| Buy-sell | 0.95% (3.07) | 1.23% (3.06) | The spread is comparable; the market difference is largely netted out. The 70-month sample makes the SE about 2x larger. Data issues above move it by < 0.15%/mo |
The paper's figures as quoted in summary.md match JT (1993) Table I as I know it. No code error explains the gap.

## Verdict: accept with caveats ("sound with caveats")

## Findings (most serious first)
1. **22-day market-wide data hole, 2022-02-15 to 2022-03-07** (trading dates jump 2022-02-14 -> 2022-03-08; the index file is complete). Two weeks of returns are booked to the wrong month. March 2022 (+9.32%, 3rd best month) earns returns from before its cohort was formed, and the benchmark is misaligned in Feb/Mar 2022. Dropping Mar 2022 gives 1.11% (t 2.75). Fix: fill from bhavcopy, or exclude Feb-Mar 2022 from formation and holding; add the hole to tradingmachine_gaps.md.
2. **Unadjusted bonuses/splits slip under the -50% threshold**: BHARATRAS, GPIL, MAANALU, NAZARA, POWERMECH (-45% to -50% on factor-change days), and EASEMYTRIP partly adjusted. GPIL, NAZARA and EASEMYTRIP were held as winners. Net effect on buy-sell -0.016%/month (conservative). Fix: flag days where the return ≈ pf_prev/pf - 1, rather than using a fixed threshold.
3. **Demergers without spin-off credit** (PEL 2022-08-30 -44.8%, RAYMOND 2024-07-11 -36.6%, both shorted) add +0.35% in total to buy-sell. Small, but in the favourable direction. Fix: use NSE corporate-action data for demerger ratios.
4. **Fragility in time**: the last third (2024-10..2026-09) is 1.04%, t 1.31; without the best 3 months, 0.78% (t 2.37). Report this alongside the halves.
5. **Short leg costs**: there is no borrow fee and the leg is not implementable. After 0.2% impact the result is 1.01% (t 2.52); a 3-5%/year SLB fee on the 0.95 short notional would take a further ~0.25-0.4%/month. State this as a paper result.
6. **Survivorship and renames** (79 early-ending symbols; HDFC, LTI, MINDTREE absent; UNITDSPR and SAMMAANCAP restart at the rename). The bias direction for buy-sell is unclear. Fix through the bhavcopy track.
7. Minor: the tests need PYTHONPATH=src (or an editable install) to run; there is no exit cost in the last month; and the NW t for the paper's numbers is not like-for-like (already noted).
