"""Monthly price returns from an export, with implausible daily moves removed."""

import pandas as pd


class CleanedMonthlyReturns:
    """Compounds daily returns into months after zeroing implausible days.

    Attributes:
        lower_limit: Daily returns below this are treated as unadjusted corporate actions.
        upper_limit: Daily returns above this are treated as unadjusted corporate actions.
        removed: Rows of symbol, date and return for each day that was set to zero.
    """

    def __init__(
        self,
        lower_limit: float = -0.5,
        upper_limit: float = 1.0,
    ):
        """Sets the limits.

        Args:
            lower_limit (float): The lowest daily return kept.
            upper_limit (float): The highest daily return kept.

        Raises:
            ValueError: The lower limit is not below the upper limit.
        """
        if lower_limit >= upper_limit:
            raise ValueError(f'{lower_limit=} must be below {upper_limit=}')
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.removed = pd.DataFrame(
            columns=[
                'symbol',
                'date',
                'daily_return',
            ],
        )

    def monthly_returns(
        self,
        daily_returns: pd.DataFrame,
        daily_has_close: pd.DataFrame,
    ) -> pd.DataFrame:
        """Compounds cleaned daily returns into calendar months.

        Args:
            daily_returns (pd.DataFrame): Daily returns, dates by symbols.
            daily_has_close (pd.DataFrame): Bools, True where the share had a close that day.

        Returns:
            pd.DataFrame: Monthly returns by PeriodIndex and symbol, NaN where the share did not trade in the month.

        Raises:
            ValueError: The two tables differ in shape.
        """
        if daily_returns.shape != daily_has_close.shape:
            raise ValueError('The two tables must have the same shape')
        too_low = daily_returns < self.lower_limit
        too_high = daily_returns > self.upper_limit
        implausible = too_low | too_high
        stacked = daily_returns.where(implausible).stack().dropna()
        self.removed = stacked.rename('daily_return').reset_index()
        self.removed.columns = [
            'date',
            'symbol',
            'daily_return',
        ]
        cleaned = daily_returns.mask(implausible, 0.0)
        months = cleaned.index.to_period('M')
        growth = 1.0 + cleaned.fillna(0.0)
        compounded = growth.groupby(months).prod() - 1.0
        traded = daily_has_close.groupby(months).any()
        return compounded.where(traded)
