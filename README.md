# Jegadeesh and Titman (1993) six-month momentum on the 500 most traded NSE shares

Reproduces Table I, Panel A, J=6 K=6 (no skip) with UBI daily prices, Dec 2020 – Sep 2026.

**In one line:** buy − sell earned 1.23% a month before costs (Newey-West t 3.06; paper 0.95%, t 3.07) and 1.08% after Indian costs, but over only 70 months, with survivorship bias, price returns only, and a short leg that most NSE cash shares cannot take.

| | Paper | India, before costs | India, after costs |
|---|---|---|---|
| Sell | 0.0079 (1.56) | 0.0126 (1.68) | – |
| Buy | 0.0174 (4.33) | 0.0249 (2.78) | 0.0242 (2.70) |
| Buy − sell | 0.0095 (3.07) | 0.0123 (3.06) | 0.0108 (2.69) |

Full tables, drawdowns, checks and caveats: [results/summary.md](results/summary.md). Plan: [plan/india_plan.md](plan/india_plan.md). Six backtests were run from four planned variants.

## Reproducing
Export the data as in data/README.md, then `python -m jegadeesh_titman_nse500_india.scripts.build_weights`, and run brahmagupta's backtest on the files in data/ (newey_west_lags=5, NIFTY 500 benchmark). Tests: `pytest`.
