"""Compounded returns over the ranking period."""

import pandas as pd


class FormationReturns:
    """Six-month (or J-month) compounded returns.

    Attributes:
        formation_months: The ranking period J in months.
    """

    def __init__(self, formation_months: int = 6):
        """Sets J.

        Args:
            formation_months (int): The ranking period in months.

        Raises:
            ValueError: formation_months is below 1.
        """
        if formation_months < 1:
            raise ValueError(f'{formation_months=} must be >= 1')
        self.formation_months = formation_months

    def compute(self, monthly_returns: pd.DataFrame) -> pd.DataFrame:
        """Compounds the last J monthly returns ending at each month.

        Args:
            monthly_returns (pd.DataFrame): Returns, months by symbols.

        Returns:
            pd.DataFrame: Compounded returns, NaN unless all J months have returns.
        """
        growth = 1.0 + monthly_returns
        product = growth.rolling(
            self.formation_months,
            min_periods=self.formation_months,
        ).apply(lambda values: values.prod(), raw=True)
        return product - 1.0
