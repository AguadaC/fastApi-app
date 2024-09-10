# -*- coding: utf-8 -*-
"""Settings of the project."""

import os


# -----------------------------------------------------------------------------
# Unit particular configurations
LOG_DIR = os.environ.get("LOG_DIR", "/opt/chanllenge/logs/")

# -----------------------------------------------------------------------------
# Unit internal configurations
DEBUG = os.environ.get("DEBUG", False)
