# Six-month momentum on liquid NSE shares

A short replication of the six-month ranking, six-month holding strategy (J=6, K=6, no skip) from Table I of Jegadeesh and Titman (1993), "Returns to Buying Winners and Selling Losers", *The Journal of Finance* 48(1), on the 500 most traded NSE shares, using UBI's daily prices from December 2019 and Indian delivery costs.

**In one line:** work in progress; no results yet.

## Repository layout

```
paper/      the paper (PDF not in git) and its summary
plan/       the plan for India, once approved
src/        the Python package jegadeesh_titman_nse500_india
tests/      unit tests that run without network access
results/    tables and summaries
data/       downloaded data, not in git
```

## Citation

See `CITATION.cff`. Please cite the original paper as well: Jegadeesh, N. and Titman, S. (1993), The Journal of Finance 48(1), 65-91, doi:10.1111/j.1540-6261.1993.tb04702.x.
