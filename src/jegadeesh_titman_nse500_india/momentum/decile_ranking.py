"""Splits a universe into return deciles."""

import pandas as pd


class DecileRanking:
    """Finds the winner and loser deciles each month.

    Attributes:
        decile_count: How many groups to split into.
    """

    def __init__(self, decile_count: int = 10):
        """Sets the number of groups.

        Args:
            decile_count (int): How many groups.

        Raises:
            ValueError: decile_count is below 2.
        """
        if decile_count < 2:
            raise ValueError(f'{decile_count=} must be >= 2')
        self.decile_count = decile_count

    def rank(
        self,
        formation_returns: pd.DataFrame,
        members: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Picks winners and losers among the members of each month.

        Ties in return are broken by symbol, the earlier symbol ranking lower.

        Args:
            formation_returns (pd.DataFrame): Compounded returns, months by symbols.
            members (pd.DataFrame): Bools, True where a share is in the universe.

        Returns:
            tuple[pd.DataFrame, pd.DataFrame]: Bools for the losers and the winners, with the same shape as the inputs.
        """
        losers = pd.DataFrame(
            False,
            index=members.index,
            columns=members.columns,
        )
        winners = losers.copy()
        for month in members.index:
            chosen = members.loc[month]
            chosen = chosen[chosen].index
            scores = formation_returns.loc[month, chosen].dropna()
            group_size = len(scores) // self.decile_count
            if group_size < 1:
                continue
            table = scores.reset_index()
            table.columns = [
                'symbol',
                'score',
            ]
            table = table.sort_values(
                [
                    'score',
                    'symbol',
                ],
            )
            losers.loc[month, table['symbol'].head(group_size)] = True
            winners.loc[month, table['symbol'].tail(group_size)] = True
        return losers, winners
