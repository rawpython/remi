#!/usr/bin/env python
"""
Tests for Python 3.13 / PyInstaller compatibility:
  - __version__ is always defined (even when package metadata is absent)
  - importlib.metadata path is used on Python 3.8+
  - pkg_resources fallback is used when importlib.metadata is unavailable
  - Hardcoded fallback is used when neither can find the package
  - server.py contains no invalid escape sequences (SyntaxWarning-free)
"""

import importlib
import py_compile
import os
import sys
import unittest
import warnings
from unittest.mock import patch, MagicMock

import remi

# Absolute path to server.py so tests run from any working directory
_SERVER_PY = os.path.join(os.path.dirname(__file__), '..', 'remi', 'server.py')
_SERVER_PY = os.path.normpath(_SERVER_PY)


class TestNoSyntaxWarnings(unittest.TestCase):
    """server.py must compile without any SyntaxWarning (e.g. invalid escape sequences)."""

    def test_server_py_no_syntax_warnings(self):
        """Compiling server.py raises no SyntaxWarning on Python 3.12+."""
        with warnings.catch_warnings():
            warnings.simplefilter("error", SyntaxWarning)
            try:
                py_compile.compile(_SERVER_PY, doraise=True)
            except py_compile.PyCompileError as exc:
                self.fail("server.py has a SyntaxWarning/SyntaxError: %s" % exc)


class TestVersionAlwaysDefined(unittest.TestCase):
    """remi.__version__ must always be a non-empty string."""

    def test_version_is_string(self):
        self.assertIsInstance(remi.__version__, str)

    def test_version_non_empty(self):
        self.assertTrue(len(remi.__version__) > 0)


class TestVersionImportlibMetadataPath(unittest.TestCase):
    """When importlib.metadata.version() succeeds, __version__ is taken from it."""

    def test_importlib_metadata_used(self):
        fake_version = "9999.01.01"
        with patch("importlib.metadata.version", return_value=fake_version):
            importlib.reload(remi)
        self.assertEqual(remi.__version__, fake_version)
        # Restore
        importlib.reload(remi)


class TestVersionPkgResourcesFallback(unittest.TestCase):
    """When importlib.metadata raises ImportError, pkg_resources provides the version."""

    def test_pkg_resources_fallback(self):
        fake_version = "8888.06.15"

        mock_dist = MagicMock()
        mock_dist.version = fake_version
        mock_pkg = MagicMock()
        mock_pkg.get_distribution.return_value = mock_dist
        mock_pkg.DistributionNotFound = Exception

        # Make importlib.metadata unavailable, supply a mock pkg_resources
        with patch.dict(sys.modules, {"importlib.metadata": None, "pkg_resources": mock_pkg}):
            importlib.reload(remi)

        self.assertEqual(remi.__version__, fake_version)
        # Restore
        importlib.reload(remi)


class TestVersionHardcodedFallback(unittest.TestCase):
    """When both importlib.metadata and pkg_resources cannot find the package,
    __version__ falls back to the hardcoded _FALLBACK_VERSION string."""

    def test_hardcoded_fallback_used(self):
        from importlib.metadata import PackageNotFoundError

        # importlib.metadata is importable but raises PackageNotFoundError
        with patch("importlib.metadata.version", side_effect=PackageNotFoundError("remi")):
            importlib.reload(remi)

        # __version__ must still be a non-empty string (the hardcoded fallback)
        self.assertIsInstance(remi.__version__, str)
        self.assertTrue(len(remi.__version__) > 0)
        self.assertEqual(remi.__version__, remi._FALLBACK_VERSION)
        # Restore
        importlib.reload(remi)

    def test_fallback_version_matches_setup(self):
        """_FALLBACK_VERSION in __init__.py must match the version in setup.py."""
        setup_py = os.path.join(os.path.dirname(__file__), '..', 'setup.py')
        setup_py = os.path.normpath(setup_py)
        with open(setup_py) as f:
            content = f.read()
        # Extract the version string from setup.py: 'version': '...'
        import re
        match = re.search(r"'version'\s*:\s*'([^']+)'", content)
        self.assertIsNotNone(match, "Could not find 'version' in setup.py")
        setup_version = match.group(1)
        self.assertEqual(
            remi._FALLBACK_VERSION,
            setup_version,
            "_FALLBACK_VERSION in __init__.py (%s) does not match setup.py (%s)"
            % (remi._FALLBACK_VERSION, setup_version),
        )


if __name__ == "__main__":
    unittest.main()
