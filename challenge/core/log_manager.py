# -*- coding: utf-8 -*-
"""LogManager module"""

import logging
import logging.config
import datetime

from logging.handlers import RotatingFileHandler
from pathlib import Path

from challenge import settings
from challenge import constants
from challenge.constants import TITLE
from challenge.core.singleton import Singleton


class LogManager(metaclass=Singleton):
    """Manages the logging configuration for the application using a singleton pattern.

    This class sets up the logging system, including the log directory, log level,
    and file rotation settings. It ensures that logging is properly initialized 
    and provides access to the logger instance.
    """

    def __init__(self) -> None:
        """Initializes the LogManager instance."""

        super().__init__()
        self._log_dir=settings.LOG_DIR
        self._timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self._log_level = (
            logging.DEBUG if settings.DEBUG else logging.INFO
        )
        self._create_log_dir_if_does_not_exist()
        self._initialize_logger()

    def _initialize_logger(self) -> None:
        """Configures the logger"""

        logging.basicConfig(
            level  = self._log_level,
            format = constants.LOG_FORMAT
        )
        self._logger = logging.getLogger(TITLE)

        log_filename = f"{self._log_dir}/{self._timestamp}_{TITLE}.log"
        file_handler = RotatingFileHandler(log_filename, maxBytes=10*1024*1024, backupCount=5)
        file_handler.setFormatter(logging.Formatter(constants.LOG_FORMAT))
        self._logger.addHandler(file_handler)

    def logger(self) -> logging.Logger:
        """Returns the configured logger instance."""

        return self._logger

    @staticmethod
    def _create_log_dir_if_does_not_exist() -> None:
        """Creates the log directory if it does not already exist."""

        Path(settings.LOG_DIR).mkdir(parents=True, exist_ok=True)
