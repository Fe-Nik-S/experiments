
import functools as ft
import types
import signal
import logging
import argparse


STR_TO_LOGGING = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARN": logging.WARNING,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}
def log_level(logging_str):
    """Convert string into logging level."""
    logging_str = logging_str.upper()
    logging_level = STR_TO_LOGGING.get(logging_str, None)
    if not logging_level:
        raise argparse.ArgumentTypeError(
            "invalid choice: {} "
            "(choose from 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')".format(logging_str)
        )
    return logging_level


class SingletonMeta(type):

    """Singleton metaclass (not thread-safe)."""

    def __new__(cls, name, bases, attrs):
        def singleton_method(func):
            @ft.wraps(func)
            def wrapper(_cls, *args, **kw):
                if _cls.__instance is None:
                    raise TypeError("{} singleton not initialized".format(name))
                return func(_cls.__instance, *args, **kw)
            return wrapper
        # Replace public methods with classmethods linked to singleton
        # instance
        for attr, item in attrs.items():
            if isinstance(item, types.FunctionType) and not attr.startswith("_"):
                attrs[attr] = classmethod(singleton_method(item))
        cls.__instance = None
        return type.__new__(cls, name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls.__instance


class TimeoutError(Exception):
    pass


class Timeout(object):

    """Context manager that allows to perform blocking operations with time limit.

    Usage:

    with Timeout(5):
        time.sleep(10)
    """

    def __init__(self, wait_seconds):
        self.wait_seconds = wait_seconds

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.alarm_handler)
        signal.alarm(self.wait_seconds)
        return self

    def __exit__(self, type, value, traceback):
        signal.alarm(0)

    def alarm_handler(self, *args):
        raise TimeoutError("Operation took longer than expected", self.wait_seconds)
