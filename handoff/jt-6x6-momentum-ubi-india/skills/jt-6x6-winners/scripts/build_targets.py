"""Builds the month's target portfolio for the six-month winners strategy.

This program only writes a CSV of targets. It never places, changes or cancels orders.

Usage:
  python build_targets.py targets.csv
  python build_targets.py targets.csv --previous last_month.csv
  python build_targets.py targets.csv --prices export_prices_file.parquet
"""

import argparse
import datetime
import tempfile
from pathlib import Path

import pandas as pd
from brahmagupta.exported_prices import ExportedPrices
from jegadeesh_titman_nse500_india.data.cleaned_monthly_returns import (
    CleanedMonthlyReturns,
)
from jegadeesh_titman_nse500_india.momentum.momentum_strategy import (
    MomentumStrategy,
)

MONTHS_NEEDED = 14
BATCH_SIZE = 200
MASTER_PATH = '/api/instruments/master'
PRICES_PATH = '/api/instruments/prices'


class BuildTargetsApplication:
    """Builds and writes the target weights.

    Attributes:
        arguments: The parsed command line.
    """

    def __init__(self):
        """Reads the command line."""
        parser = argparse.ArgumentParser(
            description='Build the month\'s winners targets.',
        )
        parser.add_argument('output', type=Path)
        parser.add_argument('--previous', type=Path, default=None)
        parser.add_argument('--prices', type=Path, default=None)
        parser.add_argument(
            '--as-of',
            type=datetime.date.fromisoformat,
            default=None,
        )
        self.arguments = parser.parse_args()

    def run(self) -> None:
        """Builds the targets and writes them.

        Raises:
            ValueError: The prices do not reach the end of the last full month.
        """
        as_of = self.arguments.as_of or datetime.date.today()
        last_month_end = as_of.replace(day=1) - datetime.timedelta(days=1)
        with tempfile.TemporaryDirectory() as folder:
            prices_path = self.arguments.prices
            if prices_path is None:
                prices_path = Path(folder) / 'prices.parquet'
                self.fetch_from_ubi(prices_path, last_month_end)
            prices = ExportedPrices(prices_path)
            daily_closes = prices.daily_closes.loc[: str(last_month_end)]
            last_date = daily_closes.index.max().date()
            if (last_month_end - last_date).days > 5:
                raise ValueError(
                    f'Prices end {last_date}, not {last_month_end}'
                )
            cleaner = CleanedMonthlyReturns()
            returns = cleaner.monthly_returns(
                daily_closes.pct_change(fill_method=None),
                daily_closes.notna(),
            )
            values = prices.monthly_median_traded_values()
            values = values.loc[: returns.index[-1]]
        targets = MomentumStrategy().next_winner_weights(returns, values)
        self.write(targets, returns.index[-1])

    def fetch_from_ubi(self, path: Path, last_date: datetime.date) -> None:
        """Fetches adjusted daily candles for every NSE share from UBI.

        Args:
            path (Path): Where to write the candles as Parquet.
            last_date (datetime.date): The last day to fetch.
        """
        from tradingmachine.assets import instruments

        client = instruments.Instrument.shared_unified_broker_interface()
        rows = client.get(
            MASTER_PATH,
            params={
                'exchange': 'nse',
                'segment': 'equities',
            },
        )
        rows = [row for row in rows if 'NSETEST' not in row['symbol']]
        first_date = last_date - datetime.timedelta(days=31 * MONTHS_NEEDED)
        frames = []
        for start in range(0, len(rows), BATCH_SIZE):
            batch = rows[start : start + BATCH_SIZE]
            body = {
                'instruments': [
                    {
                        'instrument_id': row['instrument_id'],
                    }
                    for row in batch
                ],
                'interval': 'day',
                'from': first_date.isoformat(),
                'to': last_date.isoformat(),
                'adjusted': 'true',
            }
            response = client.post(PRICES_PATH, body=body)
            for result in response['results']:
                if result['status'] != 200 or not result['data']['candles']:
                    continue
                data = result['data']
                frame = pd.DataFrame(data['candles'], columns=data['columns'])
                frame['date'] = (
                    pd.to_datetime(frame['time'])
                    .dt.tz_convert('Asia/Kolkata')
                    .dt.tz_localize(None)
                    .dt.normalize()
                )
                frame['symbol'] = batch[result['request_index']]['symbol']
                frames.append(frame[['symbol', 'date', 'close', 'volume']])
        pd.concat(frames, ignore_index=True).to_parquet(path)

    def write(self, targets: pd.Series, last_month: pd.Period) -> None:
        """Writes the CSV and prints a summary.

        Args:
            targets (pd.Series): Weights by symbol.
            last_month (pd.Period): The last full month of prices used.
        """
        table = targets.sort_index().rename('weight').reset_index()
        table.columns = [
            'symbol',
            'weight',
        ]
        table.to_csv(self.arguments.output, index=False)
        print(
            f'Targets for the month after {last_month}: {len(table)} holdings, '
            f'largest weight {table["weight"].max():.4f}'
        )
        if self.arguments.previous is not None:
            before = set(pd.read_csv(self.arguments.previous)['symbol'])
            after = set(table['symbol'])
            print(f'Joiners: {sorted(after - before)}')
            print(f'Leavers: {sorted(before - after)}')


if __name__ == '__main__':
    BuildTargetsApplication().run()
