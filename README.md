# Six-month momentum on the 500 most traded NSE shares

**This is a short reproduction of one Jegadeesh and Titman (1993) strategy on UBI data from December 2019, made as a test of research-agent. It is not a full replication of the paper.** It reproduces only Table I, Panel A, J=6, K=6, no skip.

**In one line:** buy − sell earned 1.23% a month before costs (Newey-West t 3.06; paper 0.95%, t 3.07) and 1.08% after Indian costs, but over only 70 months (Dec 2020 – Sep 2026), with survivorship bias, price returns only, and a short leg that most NSE cash shares cannot take.

Companion page (after publication): https://pramodathani.github.io/jegadeesh-titman-6x6-momentum-ubi-india/

| Average monthly return (NW t) | Paper (US, 1965–89) | India, before costs | India, after costs |
|---|---|---|---|
| Sell | 0.0079 (1.56) | 0.0126 (1.68) | not run |
| Buy | 0.0174 (4.33) | 0.0249 (2.78) | 0.0242 (2.70) |
| Buy − sell | 0.0095 (3.07) | 0.0123 (3.06) | 0.0108 (2.69) |

Costs: brahmagupta NSE delivery costs with 0.1% impact per side. Universe: the 500 most traded shares, deciles of 50. Benchmark: NIFTY 500 price index.

## Caveats
- 70 months, against 300 in the paper, in a strong market for Indian mid and small caps.
- UBI lists today's shares only; delisted and renamed shares are missing. Prices exclude dividends.
- Buy − sell is a paper portfolio: most NSE cash shares cannot be shorted, and no borrowing fee is charged.
- UBI has no daily candles for any share from 2022-02-15 to 2022-03-07. Without March 2022, buy − sell is 1.11% a month.
- The effect fades across thirds of the sample (1.24%, 1.41%, 1.04% a month; the last third has t 1.31).
- Four planned variants were run as six backtests; nothing was tuned. An independent review (results/review/review.md) accepted the work with caveats.

Details: results/summary.md. Plan for India: plan/india_plan.md. The raw UBI data is not included; data/README.md says how it was exported.

## Reproducing
Export the data as in data/README.md, then:

```
pip install -e ".[test]"
python -m jegadeesh_titman_nse500_india.scripts.build_weights
python -m jegadeesh_titman_nse500_india.scripts.build_snapshot
pytest
```

The backtests were run with brahmagupta's run_backtest on the files in data/ (monthly, newey_west_lags=5, NIFTY 500 benchmark).

## Citation
See CITATION.cff. Author: Pramod Athani (pramod.athani@gmail.com, ORCID 0009-0002-0270-7045).
