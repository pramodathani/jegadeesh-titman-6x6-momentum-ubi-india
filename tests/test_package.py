"""Checks that the package can be imported."""

import jegadeesh_titman_nse500_india


class TestPackage:
    """Tests for the package itself."""

    def test_package_has_docstring(self) -> None:
        """Checks that the package imports and documents itself.

        Returns:
            None.
        """
        assert jegadeesh_titman_nse500_india.__doc__
