from datetime import datetime
import pytz
import os
import sys
import logging
from src.CONSTANS import (
    LOGS_FOLDER_NAME, DBHANDLER_LOGS_FOLDER_NAME
)


class FlushFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()


class FlushStreamHandler(logging.StreamHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()


class TimezoneFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, timezone=None):
        super().__init__(fmt, datefmt)
        self.timezone = timezone

    def formatTime(self, record, datefmt=None):
        record_time = datetime.fromtimestamp(record.created, self.timezone)
        if datefmt:
            return record_time.strftime(datefmt)
        else:
            return record_time.isoformat()


def setup_dbhandler_logger() -> None:
    """Method used to setup dbhandler logger."""

    logs_folder_path = os.path.join(LOGS_FOLDER_NAME, DBHANDLER_LOGS_FOLDER_NAME)
    _setup_logger(logger_name='db_handler', logs_folder_path=logs_folder_path)


def get_logger(logger_name: str) -> logging.Logger:
    """Method used to return logger object.

    Args:
        logger_name (str): logger name to be retrived

    Returns:
        logging.Logger: logger object
    """
    return logging.getLogger(logger_name)


def _setup_logger(logger_name: str, logs_folder_path: str) -> None:
    """Private method used to setup logger.
    Each logger get by get_logger functin will be setup.

    Args:
        logger_name (str): name of a logger
        logs_folder_path (str): path to folder in which logs are to be stored
    """

    log_filename = f"{logger_name}" + ".log"

    log_path = os.path.join(logs_folder_path, log_filename)
    logger = get_logger(logger_name=logger_name)

    FORMAT = "[ %(asctime)s ] [ %(levelname)s ] %(message)s"
    logger.setLevel(logging.INFO)

    timezone = pytz.timezone('Europe/Warsaw')
    formatter = TimezoneFormatter(fmt=FORMAT, datefmt="%d-%m-%Y %H:%M:%S", timezone=timezone)

    if not os.path.exists(log_path):
        with open(log_path, 'w'):
            pass

    file_handler = logging.FileHandler(log_path, mode='a')
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
