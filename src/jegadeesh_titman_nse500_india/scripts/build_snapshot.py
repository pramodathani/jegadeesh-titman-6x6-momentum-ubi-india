"""Writes the companion site's data snapshot from derived results only.

Run with: python -m jegadeesh_titman_nse500_india.scripts.build_snapshot
"""

import json
from pathlib import Path


class BuildSnapshotApplication:
    """Reads the backtest result files and writes site/data/snapshot.json.

    Attributes:
        results_folder: The folder with one subfolder per backtest.
        output_path: The JSON file to write.
    """

    def __init__(
        self,
        results_folder: Path = Path('results'),
        output_path: Path = Path(
            'src/jegadeesh_titman_nse500_india/site/data/snapshot.json'
        ),
    ):
        """Sets the paths.

        Args:
            results_folder (Path): The results folder.
            output_path (Path): The snapshot file to write.
        """
        self.results_folder = results_folder
        self.output_path = output_path

    def load(self, name: str) -> dict:
        """Reads one backtest's result.json.

        Args:
            name (str): The backtest's folder name.

        Returns:
            dict: The parsed result.
        """
        path = self.results_folder / name / 'result.json'
        return json.loads(path.read_text())

    def run(self) -> None:
        """Builds and writes the snapshot."""
        rows = []
        for label, gross_name, net_name in [
            ('Sell (losers)', 'losers_nocosts', None),
            ('Buy (winners)', 'winners_nocosts', 'winners_costs'),
            (
                'Buy − sell',
                'buy_minus_sell_nocosts',
                'buy_minus_sell_costs',
            ),
        ]:
            gross = self.load(gross_name)['gross_summary']
            row = {
                'portfolio': label,
                'gross_mean': gross['mean'],
                'gross_t': gross['newey_west_t'],
                'gross_drawdown': gross['maximum_drawdown'],
                'periods': gross['periods'],
            }
            if net_name is not None:
                net = self.load(net_name)['net']['summary']
                row['net_mean'] = net['mean']
                row['net_t'] = net['newey_west_t']
                row['net_drawdown'] = net['maximum_drawdown']
            rows.append(row)
        winners = self.load('winners_costs')
        series = winners['net']['series']
        snapshot = {
            'table': rows,
            'periods': series['periods'],
            'winners_wealth': series['wealth'],
            'benchmark_wealth': series['benchmark_wealth'],
            'winners_compound': winners['net']['summary']['compound_annual'],
            'benchmark_compound': winners['net']['summary'][
                'benchmark_compound_annual'
            ],
            'winners_drawdown': winners['net']['summary']['maximum_drawdown'],
        }
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(json.dumps(snapshot))
        print(f'wrote {self.output_path}')


if __name__ == '__main__':
    BuildSnapshotApplication().run()
