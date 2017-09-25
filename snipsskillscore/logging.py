# -*-: coding utf-8 -*-
""" Logging utilities. """

import inspect

LOGGING_ENABLED = True


class TermincalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def log(message):
    """ Print a log message.

    :param message: the message to print.
    """
    __log(inspect.stack(), message)


def log_error(message):
    """ Print an error message.

    :param message: the message to print.
    """
    __log(inspect.stack(), message, TermincalColors.FAIL)


def log_success(message):
    """ Print a success message.

    :param message: the message to print.
    """
    __log(inspect.stack(), message, TermincalColors.OKGREEN)


def log_warning(message):
    """ Print a warning message.

    :param message: the message to print.
    """
    __log(inspect.stack(), message, TermincalColors.WARNING)


def log_blue(message):
    """ Print a blue message.

    :param message: the message to print.
    """
    __log(inspect.stack(), message, TermincalColors.OKBLUE)



def debug_log(message):
    """ Print a log message.

    :param message: the message to print.
    """
    __log(inspect.stack(), message, None, True)


def debug_log_error(message):
    """ Print an error message.

    :param message: the message to print.
    """
    __log(inspect.stack(), message, TermincalColors.FAIL, True)


def debug_log_success(message):
    """ Print a success message.

    :param message: the message to print.
    """
    __log(inspect.stack(), message, TermincalColors.OKGREEN, True)


def debug_log_warning(message):
    """ Print a warning message.

    :param message: the message to print.
    """
    __log(inspect.stack(), message, TermincalColors.WARNING, True)


def debug_log_blue(message):
    """ Print a blue message.

    :param message: the message to print.
    """
    __log(inspect.stack(), message, TermincalColors.OKBLUE, True)

def __log(stack, message, color=None, include_tag=False):
    """ Print a message, optionally in a given color.

    :param message: the message to print.
    :param color: the color of the message.
    """
    if not LOGGING_ENABLED or message is None:
        return

    frame = stack[1][0]
    caller = frame.f_locals.get('self', None)
    class_name = frame.f_locals.get('cls', None)
    
    if caller is not None:
        tag = caller.__class__.__name__
    elif class_name is not None:
        tag = class_name.__name__
    else:
        tag = "LOG"

    if include_tag and tag is not None and len(tag) > 0:
        message = "[{}] {}".format(tag, message)

    if not color:
        print(message)
    else:
        print("{}{}{}".format(color, message, TermincalColors.ENDC))
