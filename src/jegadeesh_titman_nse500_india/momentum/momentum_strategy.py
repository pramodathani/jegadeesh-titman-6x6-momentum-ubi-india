"""Builds the momentum portfolios' weights."""

import pandas as pd
from brahmagupta.overlapping_cohorts import OverlappingCohorts

from jegadeesh_titman_nse500_india.momentum.decile_ranking import (
    DecileRanking,
)
from jegadeesh_titman_nse500_india.momentum.formation_returns import (
    FormationReturns,
)
from jegadeesh_titman_nse500_india.momentum.liquid_universe import (
    LiquidUniverse,
)


class MomentumStrategy:
    """Six-month ranking, six-month holding momentum with no skip.

    Attributes:
        universe: Picks the most traded shares.
        formation: Computes ranking-period returns.
        ranking: Splits into deciles.
        holding_months: How many months each cohort is held.
    """

    def __init__(
        self,
        universe_size: int = 500,
        formation_months: int = 6,
        holding_months: int = 6,
    ):
        """Sets J and K.

        Args:
            universe_size (int): How many shares are ranked.
            formation_months (int): J, the ranking period.
            holding_months (int): K, the holding period.
        """
        self.universe = LiquidUniverse(universe_size, formation_months)
        self.formation = FormationReturns(formation_months)
        self.ranking = DecileRanking(10)
        self.holding_months = holding_months

    def weights(
        self,
        monthly_returns: pd.DataFrame,
        monthly_traded_values: pd.DataFrame,
    ) -> dict[str, pd.DataFrame]:
        """Builds weights for the winners, the losers and winners minus losers.

        Args:
            monthly_returns (pd.DataFrame): Returns, months by symbols.
            monthly_traded_values (pd.DataFrame): Median traded values, same shape.

        Returns:
            dict[str, pd.DataFrame]: Weights keyed by 'winners', 'losers' and 'buy_minus_sell'; each held month's winner and loser weights sum to 1.
        """
        members = self.universe.members(monthly_returns, monthly_traded_values)
        scores = self.formation.compute(monthly_returns)
        losers, winners = self.ranking.rank(scores, members)
        winner_weights = OverlappingCohorts(
            winners,
            self.holding_months,
        ).weights(monthly_returns)
        loser_weights = OverlappingCohorts(
            losers,
            self.holding_months,
        ).weights(monthly_returns)
        return {
            'winners': winner_weights,
            'losers': loser_weights,
            'buy_minus_sell': winner_weights - loser_weights,
        }
