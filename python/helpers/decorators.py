
import os
import errno
import signal
from functools import wraps
from .utils import TimeoutError


def debug(fun):
    def tmp(self, *args, **kwargs):
        try:
            str_args = str(args)
        except Exception as e:
            str_args = "Error args"

        try:
            str_kwargs = str(kwargs)
        except Exception as e:
            str_kwargs = "Error kwargs"

        try:
            self.log.debug(
                '|   > | %s.%s args: %s kwargs: %s',
                self.__class__.__name__, fun.__name__, str_args, str_kwargs)
        except Exception as e:
            self.log.debug(
                '|   > | %s.%s args: %s kwargs: %s',
                self.__class__.__name__, fun.__name__,
                str_args[:200], str_kwargs[:200])

        result = fun(self, *args, **kwargs)

        try:
            str_result = str(result)
        except Exception as e:
            str_result = "Error result"

        try:
            self.log.debug(
                '| <   | %s.%s result: %s'
                % (self.__class__.__name__, fun.__name__, str_result))
        except Exception as e:
            self.log.debug(
                '| <   | %s.%s result: %s'
                % (self.__class__.__name__, fun.__name__, str_result[:200]))

        return result
    return tmp


def timeout(seconds=10, error_message=os.strerror(errno.ETIMEDOUT)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator
