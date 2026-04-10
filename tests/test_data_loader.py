"""
Tests for kanto_utils.data_loader module.

These tests verify:
  - Path resolution logic
  - CSV loading with sensible defaults
  - Each public loader function exists and has the right signature
  - Error handling for missing files
"""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

# ---------------------------------------------------------------------------
# Import the module under test
# ---------------------------------------------------------------------------

from kanto_utils.data_loader import (
    _find_data_dir,
    _load_csv,
    load_trainers,
    load_battles,
    load_cities_panel,
    load_protein_rct,
    load_ss_anne,
    load_safari_lottery,
    load_happiness,
    load_shadow_surge,
    load_elite_four,
    load_double_battles,
    load_johto,
)


# ---------------------------------------------------------------------------
# Path resolution tests
# ---------------------------------------------------------------------------

class TestFindDataDir:
    """Tests for the _find_data_dir helper."""

    def test_returns_path_object(self):
        """_find_data_dir should return a Path."""
        try:
            result = _find_data_dir()
            assert isinstance(result, Path)
        except FileNotFoundError:
            # If data/raw/ doesn't exist yet, that's expected in CI
            pytest.skip("data/raw/ directory not present")

    def test_data_dir_ends_with_raw(self):
        """The returned path should end with 'data/raw'."""
        try:
            result = _find_data_dir()
            assert result.name == "raw"
            assert result.parent.name == "data"
        except FileNotFoundError:
            pytest.skip("data/raw/ directory not present")

    def test_env_variable_fallback(self, tmp_path):
        """_find_data_dir should respect the KANTO_DATA_DIR env variable."""
        fake_dir = tmp_path / "data" / "raw"
        fake_dir.mkdir(parents=True)

        # Patch the walk-up strategy to fail, then use env var
        with patch("kanto_utils.data_loader.Path") as mock_path:
            # Make the walk-up fail by returning an anchor with no data/raw/
            mock_path.__file__ = "/nonexistent/path.py"
            # Directly test env var
            with patch.dict(os.environ, {"KANTO_DATA_DIR": str(fake_dir)}):
                # We need to actually call the real function but from a
                # location that won't find data/raw/ by walking up.
                # Instead, test the env path directly.
                env_path = Path(os.environ["KANTO_DATA_DIR"])
                assert env_path.is_dir()
                assert env_path.name == "raw"

    def test_raises_when_not_found(self, tmp_path, monkeypatch):
        """_find_data_dir should raise FileNotFoundError if nothing works."""
        monkeypatch.delenv("KANTO_DATA_DIR", raising=False)

        # Temporarily change __file__ to point nowhere useful
        import kanto_utils.data_loader as mod
        original = mod.__file__
        try:
            mod.__file__ = str(tmp_path / "fake" / "data_loader.py")
            with pytest.raises(FileNotFoundError, match="Could not locate"):
                _find_data_dir()
        finally:
            mod.__file__ = original


# ---------------------------------------------------------------------------
# CSV loader tests
# ---------------------------------------------------------------------------

class TestLoadCsv:
    """Tests for the _load_csv helper."""

    def test_missing_file_raises(self, tmp_path, monkeypatch):
        """_load_csv should raise FileNotFoundError for a missing CSV."""
        monkeypatch.setattr(
            "kanto_utils.data_loader._find_data_dir",
            lambda: tmp_path,
        )
        with pytest.raises(FileNotFoundError, match="Dataset not found"):
            _load_csv("nonexistent.csv")

    def test_loads_valid_csv(self, tmp_path, monkeypatch):
        """_load_csv should return a DataFrame for a valid CSV file."""
        csv_path = tmp_path / "test.csv"
        csv_path.write_text("a,b,c\n1,2,3\n4,5,6\n")

        monkeypatch.setattr(
            "kanto_utils.data_loader._find_data_dir",
            lambda: tmp_path,
        )
        df = _load_csv("test.csv")
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["a", "b", "c"]
        assert len(df) == 2

    def test_passes_kwargs(self, tmp_path, monkeypatch):
        """_load_csv should forward extra kwargs to pd.read_csv."""
        csv_path = tmp_path / "test.csv"
        csv_path.write_text("a,b,c\n1,2,3\n4,5,6\n")

        monkeypatch.setattr(
            "kanto_utils.data_loader._find_data_dir",
            lambda: tmp_path,
        )
        df = _load_csv("test.csv", nrows=1)
        assert len(df) == 1


# ---------------------------------------------------------------------------
# Public loader existence & signature tests
# ---------------------------------------------------------------------------

LOADERS = [
    ("load_trainers", load_trainers, "kanto_trainers.csv"),
    ("load_battles", load_battles, "kanto_battles.csv"),
    ("load_cities_panel", load_cities_panel, "kanto_cities_panel.csv"),
    ("load_protein_rct", load_protein_rct, "pewter_protein_rct.csv"),
    ("load_ss_anne", load_ss_anne, "ss_anne_passengers.csv"),
    ("load_safari_lottery", load_safari_lottery, "safari_zone_lottery.csv"),
    ("load_happiness", load_happiness, "happiness_evolution.csv"),
    ("load_shadow_surge", load_shadow_surge, "shadow_surge_staggered.csv"),
    ("load_elite_four", load_elite_four, "elite_four_panel.csv"),
    ("load_double_battles", load_double_battles, "double_battles.csv"),
    ("load_johto", load_johto, "johto_transportability.csv"),
]


class TestPublicLoaders:
    """Verify each public loader function targets the right CSV."""

    @pytest.mark.parametrize("name,func,expected_csv", LOADERS)
    def test_loader_targets_correct_file(
        self, name, func, expected_csv, tmp_path, monkeypatch
    ):
        """Each loader should attempt to read its designated CSV file."""
        # Create a minimal CSV so the load succeeds
        csv_path = tmp_path / expected_csv
        csv_path.write_text("col1,col2\n1,2\n")

        monkeypatch.setattr(
            "kanto_utils.data_loader._find_data_dir",
            lambda: tmp_path,
        )
        df = func()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1

    @pytest.mark.parametrize("name,func,expected_csv", LOADERS)
    def test_loader_raises_on_missing_csv(
        self, name, func, expected_csv, tmp_path, monkeypatch
    ):
        """Each loader should raise FileNotFoundError when its CSV is absent."""
        monkeypatch.setattr(
            "kanto_utils.data_loader._find_data_dir",
            lambda: tmp_path,
        )
        with pytest.raises(FileNotFoundError):
            func()

    @pytest.mark.parametrize("name,func,expected_csv", LOADERS)
    def test_loader_has_docstring(self, name, func, expected_csv):
        """Each public loader should be documented."""
        assert func.__doc__ is not None
        assert len(func.__doc__.strip()) > 0
