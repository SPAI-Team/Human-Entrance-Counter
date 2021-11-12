import datetime.datetime
import requests
import time
import os
import sys
import logging
import traceback
from typing import Optional, Dict

from colorama import init, Fore, Style


class LoggerSetup:  # pylint: disable=too-few-public-methods
    """Set up the universal logging configuration"""

    def __init__(self) -> None:
        if os.name == "nt":
            init()

        formatter = ColoredFormatter(
            "{asctime} {name} {level_color} {levelname}"
            "{reset}: {msg_color} {message} {reset}",
            style="{",
            datefmt="%Y-%m-%d %H:%M:%S",
            colors={
                "DEBUG": Fore.RESET + Style.BRIGHT,
                "INFO": Fore.RESET + Style.BRIGHT,
                "WARNING": Fore.YELLOW + Style.BRIGHT,
                "ERROR": Fore.RED + Style.BRIGHT,
                "CRITICAL": Fore.RED + Style.BRIGHT,
            },
        )

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)

        self.logger = logging.getLogger()
        self.logger.handlers[:] = []
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        sys.excepthook = self.handle_exception

    def handle_exception(  # type:ignore
        self, exc_type, exc_value, exc_traceback
    ) -> None:
        """Use Python's logging module when showing errors"""

        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        error_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
        traceback_msg = " ".join([str(elem) for elem in error_list[:-1]])
        error_msg = str(error_list[-1])

        # Make the error type more obvious in terminal by separating these
        self.logger.error(traceback_msg)
        self.logger.error(error_msg)


class ColoredFormatter(logging.Formatter):
    """This class formats the color of logging messages"""

    def __init__(
        self, *args: str, colors: Optional[Dict[str, str]] = None, **kwargs: str
    ) -> None:
        """Initialize the formatter with specified format strings"""

        super().__init__(*args, **kwargs)

        self.colors = colors if colors else {}

    def format(self, record: logging.LogRecord) -> str:
        """Format the specified record as text."""

        record.level_color = self.colors.get(record.levelname, "")
        record.reset = Style.RESET_ALL
        record.msg_color = self.colors.get(record.levelname, "")

        return super().format(record)

