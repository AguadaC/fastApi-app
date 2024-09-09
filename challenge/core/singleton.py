# -*- coding: utf-8 -*-
"""Module that defines Singleton metaclass."""
from typing import Dict


class Singleton(type):
    """Singleton Metaclass."""

    _instances: Dict = {}

    def __call__(cls, *args, **kwargs):
        """Generates an instance only if it's the first one."""

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
