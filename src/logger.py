from datetime import datetime
import pytz
import os
import sys
import logging
from logging.handlers import SMTPHandler
from src.models import (LogMailConfig)

from .CONSTANTS import (
    LOGS_FOLDER_NAME, CONSUMER_LOGS_FOLEDR_NAME, PRODUCER_LOGS_FOLDER_NAME, CONSUMERS_MANAGER_FOLDER_NAME,
    RETENTION_LOGS_FOLDER_NAME, AUDIT_LOGS_FOLDER_NAME
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


def setup_consumer_logger(topic_name: str, log_mail_config: LogMailConfig) -> None:
    """Method used to setup consumer logger.
    Logger for given topic_name will be consumer logger.

    Args:
        topic_name (str): name of consumer topic
    """
    logs_folder_path = os.path.join(LOGS_FOLDER_NAME, CONSUMER_LOGS_FOLEDR_NAME)
    _setup_logger(logger_name=topic_name, log_mail_config=log_mail_config, logs_folder_path=logs_folder_path)


def setup_producer_logger(topic_name: str, log_mail_config: LogMailConfig) -> None:
    """Method used to setup producer logger.
    Logger for given topic_name will be producer logger.

    Args:
        topic_name (str): name of producer topic
    """
    logs_folder_path = os.path.join(LOGS_FOLDER_NAME, PRODUCER_LOGS_FOLDER_NAME)
    _setup_logger(logger_name=topic_name, log_mail_config=log_mail_config, logs_folder_path=logs_folder_path)


def setup_consumers_manager_logger(manager_name: str) -> None:
    """Method used to setup consumers_manager logger.
    Logger for given manger_name will be consumers_manager logger.

    Args:
        manager_name (str): name of manger name
    """
    logs_folder_path = os.path.join(LOGS_FOLDER_NAME, CONSUMERS_MANAGER_FOLDER_NAME)
    _setup_consumers_manager_logger(manager_name=manager_name, logs_folder_path=logs_folder_path)


def setup_retention_logger(logger_name: str = "retention_logger") -> str:
    """Method used to setup retention cleaner logger.

    Args:
        logger_name (str, optional): name of logger. Defaults to "retention_logger".
    """
    timezone = pytz.timezone('Europe/Warsaw')
    curr_datetime = datetime.now(timezone)
    logs_folder_path = os.path.join(LOGS_FOLDER_NAME, RETENTION_LOGS_FOLDER_NAME)
    curr_date = datetime.strftime(curr_datetime.date(), "%Y_%m_%d")
    log_filename = f"{logger_name}_{curr_date}" + ".log"

    log_path = os.path.join(logs_folder_path, log_filename)
    logger = get_logger(topic_name=logger_name)

    FORMAT = "[ %(asctime)s ] [ %(levelname)s ] %(message)s"
    logger.setLevel(logging.INFO)

    formatter = TimezoneFormatter(fmt=FORMAT, datefmt="%d-%m-%Y", timezone=timezone)
    # formatter = logging.Formatter(FORMAT)

    new_file = True
    i = 0
    while new_file:
        if not os.path.exists(log_path):
            with open(log_path, 'w'):
                new_file = False
        else:
            file_name, extension = log_path.split(".")
            if "_v" in file_name:
                file_name, version = file_name.split("_v")
                file_name = f"{file_name}_v{int(version) + 1}"
                log_path = file_name + "." + extension
            else:
                log_path = file_name + "_v1." + extension
        i += 1
        if i > 100:
            break

    if not os.path.exists(log_path):
        with open(log_path, 'w'):
            pass

    file_handler = FlushFileHandler(log_path, mode='a')
    file_handler.setFormatter(formatter)

    stream_handler = FlushStreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return curr_datetime


def setup_audit_logger() -> logging.Logger:
    logger_name = "_audit_logger"
    _setup_logger(logger_name=logger_name, logs_folder_path=AUDIT_LOGS_FOLDER_NAME)
    logger = get_logger(logger_name)

    return logger


def get_logger(topic_name: str) -> logging.Logger:
    """Method used to return logger for given topic_name.

    Args:
        topic_name (str): name of topic for which logger has to be retrived

    Returns:
        logging.Logger: logger for given topic
    """
    return logging.getLogger(topic_name)


def _setup_consumers_manager_logger(manager_name: str, logs_folder_path: str) -> None:
    log_filename = f"{manager_name}_" + ".log"

    log_path = os.path.join(logs_folder_path, log_filename)
    logger = get_logger(topic_name=manager_name)

    FORMAT = "[ %(asctime)s ] [ %(levelname)s ] %(message)s"
    logger.setLevel(logging.INFO)

    timezone = pytz.timezone('Europe/Warsaw')
    formatter = TimezoneFormatter(fmt=FORMAT, datefmt="%d-%m-%Y %H:%M:%S", timezone=timezone)
    # formatter = logging.Formatter(FORMAT)

    if not os.path.exists(log_path):
        with open(log_path, 'w'):
            pass

    file_handler = FlushFileHandler(log_path, mode='a')
    file_handler.setFormatter(formatter)

    stream_handler = FlushStreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def _setup_logger(logger_name: str, logs_folder_path: str, log_mail_config: LogMailConfig = None) -> None:
    """Private method used to setup logger.
    Each logger get by get_logger functin will be setup.

    Args:
        topic_name (str): name of topic
        logs_folder_path (str): path to folder in which logs are to be stored, differente between consumer and producer
    """
    # curr_datetime = datetime.now(pytz.timezone('Europe/Warsaw'))

    log_filename = f"{logger_name}" + ".log"

    log_path = os.path.join(logs_folder_path, log_filename)
    logger = get_logger(topic_name=logger_name)

    FORMAT = "[ %(asctime)s ] [ %(levelname)s ] %(message)s"
    logger.setLevel(logging.INFO)

    timezone = pytz.timezone('Europe/Warsaw')
    formatter = TimezoneFormatter(fmt=FORMAT, datefmt="%d-%m-%Y %H:%M:%S", timezone=timezone)

    # formatter = logging.Formatter(FORMAT)

    if not os.path.exists(log_path):
        with open(log_path, 'w'):
            pass

    file_handler = logging.FileHandler(log_path, mode='a')
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    if log_mail_config is not None:
        _add_smtp_handler_to_logger(logger=logger, log_mail_config=log_mail_config)


def _add_smtp_handler_to_logger(logger: logging.Logger, log_mail_config: LogMailConfig) -> None:
    FORMAT_MAIL = f"[ %(asctime)s ] [ %(levelname)s ] [ {logger.name} ] %(message)s - zweryfikuj logi topicu!"
    formatter_mail = logging.Formatter(FORMAT_MAIL)
    smtp_handler = SMTPHandler(
        mailhost=(log_mail_config.mailhost, log_mail_config.port),
        fromaddr=log_mail_config.fromaddr,
        toaddrs=log_mail_config.toaddrs,
        subject=log_mail_config.subject
    )
    smtp_handler.setFormatter(formatter_mail)
    smtp_handler.setLevel(logging.ERROR)

    logger.addHandler(smtp_handler)
