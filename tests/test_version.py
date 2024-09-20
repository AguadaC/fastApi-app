# -*- coding: utf-8 -*-
"""Version check test."""

import unittest
from challenge import version


class VersionTests(unittest.TestCase):
    """Version check tests"""

    def test_version_is_valid(self):
        """Unit version should be defined"""
        self.assertIsNotNone(version)


if __name__ == "__main__":
    unittest.main()
