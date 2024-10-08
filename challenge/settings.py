# -*- coding: utf-8 -*-
"""Settings of the project."""

import os


# ==================================================================================
# Unit particular configurations
LOG_DIR = os.environ.get("LOG_DIR", "/opt/chanllenge/logs/")

# ==================================================================================
# Unit internal configurations
DEBUG = os.environ.get("DEBUG", True)

# ==================================================================================
# Data Base configurations
POSTGRES_USER     = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB       = os.environ.get("POSTGRES_DB", "challenge_db")
POSTGRES_HOST     = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_ECHO     = os.environ.get("ECHO", "false").lower() in ('true', '1', 't')
