"""Builds monthly returns, benchmark returns and strategy weights.

Run with: python -m jegadeesh_titman_nse500_india.scripts.build_weights
"""

from pathlib import Path

import pandas as pd
from brahmagupta.exported_prices import ExportedPrices

from jegadeesh_titman_nse500_india.data.cleaned_monthly_returns import (
    CleanedMonthlyReturns,
)
from jegadeesh_titman_nse500_india.momentum.momentum_strategy import (
    MomentumStrategy,
)


class BuildWeightsApplication:
    """Writes the files that the backtest reads.

    Attributes:
        data_folder: Where the exports and the outputs live.
        first_month: The first full month of data.
        last_month: The last full month of data.
    """

    def __init__(
        self,
        data_folder: Path = Path('data'),
        first_month: str = '2020-01',
        last_month: str = '2026-09',
    ):
        """Sets the folders and months.

        Args:
            data_folder (Path): The data folder.
            first_month (str): The first full month, as YYYY-MM.
            last_month (str): The last full month, as YYYY-MM.
        """
        self.data_folder = data_folder
        self.first_month = first_month
        self.last_month = last_month

    def run(self) -> None:
        """Builds and saves returns, benchmark and weights."""
        prices = ExportedPrices(self.data_folder / 'equities_daily.parquet')
        cleaner = CleanedMonthlyReturns()
        returns = cleaner.monthly_returns(
            prices.daily_returns(),
            prices.daily_closes.notna(),
        )
        values = prices.monthly_median_traded_values()
        returns = returns.loc[self.first_month : self.last_month]
        values = values.loc[self.first_month : self.last_month]
        cleaner.removed.to_csv(
            self.data_folder / 'removed_daily_returns.csv',
            index=False,
        )
        returns.to_parquet(self.data_folder / 'monthly_returns.parquet')
        strategy = MomentumStrategy()
        weights = strategy.weights(returns, values)
        for name, table in weights.items():
            table.to_parquet(self.data_folder / f'weights_{name}.parquet')
        self.save_benchmark(returns.index)
        print(
            f'{returns.shape=}, removed days={len(cleaner.removed)}, '
            f'held months={int((weights["winners"].sum(axis=1) > 0).sum())}'
        )

    def save_benchmark(self, months: pd.PeriodIndex) -> None:
        """Saves NIFTY 500 monthly price returns.

        Args:
            months (pd.PeriodIndex): The months to keep.
        """
        index = pd.read_parquet(self.data_folder / 'nifty500_daily.parquet')
        closes = index.set_index(pd.to_datetime(index['date']))['close']
        month_end = closes.groupby(closes.index.to_period('M')).last()
        monthly = month_end.pct_change()
        frame = monthly.loc[months[0] : months[-1]].to_frame('NIFTY 500')
        frame.to_parquet(self.data_folder / 'benchmark_returns.parquet')


if __name__ == '__main__':
    BuildWeightsApplication().run()
