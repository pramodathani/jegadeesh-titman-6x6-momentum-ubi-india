"""Picks the most traded shares of each formation month."""

import pandas as pd


class LiquidUniverse:
    """Chooses the shares that traded most over the formation months.

    Attributes:
        size: How many shares to keep.
        formation_months: How many months of returns and traded values to use.
    """

    def __init__(self, size: int = 500, formation_months: int = 6):
        """Sets the size of the universe.

        Args:
            size (int): How many shares to keep.
            formation_months (int): The ranking period J in months.

        Raises:
            ValueError: size or formation_months is below 1.
        """
        if size < 1 or formation_months < 1:
            raise ValueError(f'{size=} and {formation_months=} must be >= 1')
        self.size = size
        self.formation_months = formation_months

    def eligible(self, monthly_returns: pd.DataFrame) -> pd.DataFrame:
        """Says which shares had a return in every formation month.

        Args:
            monthly_returns (pd.DataFrame): Returns, months by symbols.

        Returns:
            pd.DataFrame: Bools, True at month t when months t-J+1 to t all have returns.
        """
        has_return = monthly_returns.notna().astype(int)
        counts = has_return.rolling(self.formation_months).sum()
        return counts == self.formation_months

    def members(
        self,
        monthly_returns: pd.DataFrame,
        monthly_traded_values: pd.DataFrame,
    ) -> pd.DataFrame:
        """Picks the top shares by average traded value over the formation months.

        Only months up to and including the formation month are used.

        Args:
            monthly_returns (pd.DataFrame): Returns, months by symbols.
            monthly_traded_values (pd.DataFrame): Monthly median traded values with the same shape.

        Returns:
            pd.DataFrame: Bools, True where a share is in the universe at that month's end.

        Raises:
            ValueError: The two tables differ in shape.
        """
        if monthly_returns.shape != monthly_traded_values.shape:
            raise ValueError('The two tables must have the same shape')
        eligible = self.eligible(monthly_returns)
        average_value = monthly_traded_values.rolling(
            self.formation_months,
            min_periods=self.formation_months,
        ).mean()
        average_value = average_value.where(eligible)
        members = pd.DataFrame(
            False,
            index=monthly_returns.index,
            columns=monthly_returns.columns,
        )
        for month in members.index:
            row = average_value.loc[month].dropna()
            row = row.reset_index()
            row.columns = [
                'symbol',
                'value',
            ]
            row = row.sort_values(
                [
                    'value',
                    'symbol',
                ],
                ascending=[
                    False,
                    True,
                ],
            )
            chosen = row['symbol'].head(self.size)
            members.loc[month, chosen] = True
        return members
