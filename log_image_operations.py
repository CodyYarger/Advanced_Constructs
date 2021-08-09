#!/usr/bin/env python3
# 06/25/2021
# Dev: Cody Yarger
# Assignment 09 - Advanced Language Constructs

'''
    Decorator for logging exceptions
'''
# pylint: disable=C0103
# pylint: disable=W1203

import functools
import logging
from datetime import datetime

log_file = datetime.now().strftime("image_%m_%d_%Y.log")
logging.basicConfig(filename=log_file, level=logging.INFO)
logger = logging.getLogger()


def log(func):
    '''
        Basic logger for logging exceptions the func arg method and its
        arguments
        param func: function wrapped by log and wrapper
    '''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        func_args = ", ".join(args_repr + kwargs_repr)
        logger.debug(f"function {func.__name__} called with args {func_args}")
        try:
            func_result = func(*args, **kwargs)
            return func_result
        except Exception as e:
            logger.exception(f"Exception raised in {func.__name__}. exception: {str(e)}")
            raise e
    return wrapper
