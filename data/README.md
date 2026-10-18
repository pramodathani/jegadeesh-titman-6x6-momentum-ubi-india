# Data

Downloaded and intermediate data, not kept in git. Each file is listed here with where it came from.
All pulled from UBI via tradingmachine's export tools on 2026-10-18.

| File | What | Source |
|---|---|---|
| instruments.parquet | 3,454 NSE equity instruments listed now (incl. 22 NSETEST symbols, not priced) | export_instruments nse/equities |
| equities_daily.parquet | 2,943,119 daily candles, 2,605 symbols, 2019-12-03 to 2026-10-16; split/bonus-adjusted, not dividend-adjusted; has `price_factor`; `oi` all empty | export_prices nse/equities, day, adjusted |
| nifty500_daily.parquet | NIFTY 500 price index, 1,932 daily bars, 2019-01-01 to 2026-10-16 (not total return) | export_prices nse/equity_indices |

## Coverage checks
- 827 of 3,432 asked symbols had no candles (mostly -RE rights/odd lots, new listings).
- Symbols with a bar per month: 1,310 in Dec 2019, 1,393 in Dec 2020, 1,999 in Dec 2024, 2,525 in Sep 2026.
- No duplicate (symbol, date) rows; no missing values apart from `oi`.
- Known limits (see shared gaps register 2, 4, 7, 12, 23): survivorship bias, renamed shares cut at the rename, no dividends, price-only index, still-listed shares with truncated history.
