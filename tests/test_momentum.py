"""Tests of the momentum components on small made-up data."""

import numpy as np
import pandas as pd

from jegadeesh_titman_nse500_india.data.cleaned_monthly_returns import (
    CleanedMonthlyReturns,
)
from jegadeesh_titman_nse500_india.momentum.decile_ranking import (
    DecileRanking,
)
from jegadeesh_titman_nse500_india.momentum.formation_returns import (
    FormationReturns,
)
from jegadeesh_titman_nse500_india.momentum.liquid_universe import (
    LiquidUniverse,
)
from jegadeesh_titman_nse500_india.momentum.momentum_strategy import (
    MomentumStrategy,
)


class TestMomentum:
    """Checks for the data cleaner and the momentum classes."""

    def make_panel(self, month_count: int = 14, share_count: int = 20):
        """Makes returns and traded values with known ordering.

        Args:
            month_count (int): Number of months.
            share_count (int): Number of shares.

        Returns:
            tuple[pd.DataFrame, pd.DataFrame]: Returns and traded values.
        """
        months = pd.period_range('2020-01', periods=month_count, freq='M')
        symbols = [f'S{number:02d}' for number in range(share_count)]
        returns = pd.DataFrame(index=months, columns=symbols, dtype=float)
        for number, symbol in enumerate(symbols):
            returns[symbol] = 0.001 * number
        values = pd.DataFrame(index=months, columns=symbols, dtype=float)
        for number, symbol in enumerate(symbols):
            values[symbol] = 100.0 + number
        return returns, values

    def test_monthly_compounding(self):
        """Two daily returns of 10% compound to 21% in the month."""
        dates = pd.to_datetime(['2020-01-01', '2020-01-02', '2020-01-03'])
        daily = pd.DataFrame({'A': [np.nan, 0.1, 0.1]}, index=dates)
        has_close = pd.DataFrame({'A': [True, True, True]}, index=dates)
        result = CleanedMonthlyReturns().monthly_returns(daily, has_close)
        assert abs(result.iloc[0, 0] - 0.21) < 1e-12

    def test_implausible_days_zeroed_and_listed(self):
        """A +300% day is set to zero and recorded."""
        dates = pd.to_datetime(['2020-01-01', '2020-01-02', '2020-01-03'])
        daily = pd.DataFrame({'A': [np.nan, 3.0, 0.1]}, index=dates)
        has_close = pd.DataFrame({'A': [True, True, True]}, index=dates)
        cleaner = CleanedMonthlyReturns()
        result = cleaner.monthly_returns(daily, has_close)
        assert abs(result.iloc[0, 0] - 0.1) < 1e-12
        assert len(cleaner.removed) == 1

    def test_untraded_month_is_nan(self):
        """A month with no close has no return."""
        dates = pd.to_datetime(['2020-01-02', '2020-02-03'])
        daily = pd.DataFrame({'A': [np.nan, np.nan]}, index=dates)
        has_close = pd.DataFrame({'A': [True, False]}, index=dates)
        result = CleanedMonthlyReturns().monthly_returns(daily, has_close)
        assert np.isnan(result.iloc[1, 0])

    def test_eligibility_needs_all_six_months(self):
        """A missing month makes a share ineligible for six months."""
        returns, values = self.make_panel()
        returns.loc[pd.Period('2020-03'), 'S05'] = np.nan
        eligible = LiquidUniverse(10, 6).eligible(returns)
        assert not eligible.loc[pd.Period('2020-08'), 'S05']
        assert eligible.loc[pd.Period('2020-09'), 'S05']
        assert not eligible.loc[pd.Period('2020-05'), 'S00']

    def test_top_size_by_traded_value(self):
        """The most traded shares are picked."""
        returns, values = self.make_panel()
        members = LiquidUniverse(5, 6).members(returns, values)
        chosen = members.loc[pd.Period('2020-08')]
        assert list(chosen[chosen].index) == [
            'S15',
            'S16',
            'S17',
            'S18',
            'S19',
        ]

    def test_no_look_ahead_in_selection(self):
        """Changing month t+1's data leaves month t's selection unchanged."""
        returns, values = self.make_panel()
        before = LiquidUniverse(5, 6).members(returns, values)
        changed = values.copy()
        changed.loc[pd.Period('2020-09'), 'S00'] = 1e9
        after = LiquidUniverse(5, 6).members(returns, changed)
        month = pd.Period('2020-08')
        assert before.loc[month].equals(after.loc[month])
        assert not before.loc[pd.Period('2020-09')].equals(
            after.loc[pd.Period('2020-09')]
        )

    def test_formation_return_compounds(self):
        """Six months of 1% compound to 1.01**6 - 1."""
        returns, values = self.make_panel()
        returns[:] = 0.01
        result = FormationReturns(6).compute(returns)
        assert abs(result.iloc[5, 0] - (1.01**6 - 1.0)) < 1e-12
        assert np.isnan(result.iloc[4, 0])

    def test_deciles_and_tie_break(self):
        """Deciles hold the extremes; ties go to the earlier symbol as loser."""
        returns, values = self.make_panel()
        members = pd.DataFrame(
            True, index=returns.index, columns=returns.columns
        )
        scores = returns.copy()
        scores['S00'] = 0.5
        scores['S01'] = 0.5
        losers, winners = DecileRanking(10).rank(scores, members)
        month = pd.Period('2020-08')
        assert list(losers.loc[month][losers.loc[month]].index) == [
            'S02',
            'S03',
        ]
        assert list(winners.loc[month][winners.loc[month]].index) == [
            'S00',
            'S01',
        ]

    def test_weights_sum_to_one_when_fully_formed(self):
        """Winner and loser weights sum to 1 in held months; spread to 0."""
        returns, values = self.make_panel(month_count=20)
        result = MomentumStrategy(20, 6, 6).weights(returns, values)
        winners = result['winners'].sum(axis=1)
        held = winners[winners > 0]
        assert len(held) > 0
        assert np.allclose(held, 1.0)
        assert np.allclose(result['losers'].sum(axis=1)[held.index], 1.0)
        assert np.allclose(result['buy_minus_sell'].sum(axis=1), 0.0)
        assert winners.iloc[:11].sum() == 0.0
        assert winners.iloc[11] > 0.0
