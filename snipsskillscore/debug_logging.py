# -*-: coding utf-8 -*-
""" Logging utilities. """

import inspect

LOGGING_ENABLED = True

class LOG_LEVEL:
    
    WARNING, INFO, DEBUG, CRITICAL, ERROR = range(5)

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

LOG_COLORS = {
    LOG_LEVEL.WARNING: YELLOW,
    LOG_LEVEL.INFO: WHITE,
    LOG_LEVEL.DEBUG: BLUE,
    LOG_LEVEL.CRITICAL: YELLOW,
    LOG_LEVEL.ERROR: RED
}

# COLORS = {
#     'WARNING'  : YELLOW,
#     'INFO'     : WHITE,
#     'DEBUG'    : BLUE,
#     'CRITICAL' : YELLOW,
#     'ERROR'    : RED,
#     'RED'      : RED,
#     'GREEN'    : GREEN,
#     'YELLOW'   : YELLOW,
#     'BLUE'     : BLUE,
#     'MAGENTA'  : MAGENTA,
#     'CYAN'     : CYAN,
#     'WHITE'    : WHITE,
# }

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[%dm"
BOLD_SEQ = "\033[1m"
UNDERLINE_SEQ = "\033[4m"


# class TerminalColors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKGREEN = '\033[92m'
#     LIGHT = '\033[97m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'


def log_error(message):
    """ Print an error message.

    :param message: the message to print.
    """
    log(message, stack=inspect.stack(), log_level=LOG_LEVEL.ERROR)


def log_success(message):
    """ Print a success message.

    :param message: the message to print.
    """
    log(message, stack=inspect.stack(), color=GREEN)


def log_warning(message):
    """ Print a warning message.

    :param message: the message to print.
    """
    log(message, stack=inspect.stack(), log_level=LOG_LEVEL.WARNING)


def log_blue(message):
    """ Print a blue message.

    :param message: the message to print.
    """
    log(message, stack=inspect.stack(), color=BLUE)



def debug_log(message):
    """ Print a log message.

    :param message: the message to print.
    """
    log(message, stack=inspect.stack(), include_tag=True)


def debug_log_error(message):
    """ Print an error message.

    :param message: the message to print.
    """
    log(message, stack=inspect.stack(), log_level=LOG_LEVEL.ERROR, include_tag=True)


def debug_log_success(message):
    """ Print a success message.

    :param message: the message to print.
    """
    log(message, stack=inspect.stack(), color=GREEN, include_tag=True)


def debug_log_warning(message):
    """ Print a warning message.

    :param message: the message to print.
    """
    log(message, stack=inspect.stack(), log_level=LOG_LEVEL.WARNING, include_tag=True)


def debug_log_blue(message):
    """ Print a blue message.

    :param message: the message to print.
    """
    log(message, stack=inspect.stack(), color=BLUE, include_tag=True)

def log(message, stack=None, log_level=None, color=None, include_tag=False):
    """ Print a log message.

    :param message: the message to print.
    :param log_level: the log level.
    :param include_tag: include called tag.
    """
    return
    if not LOGGING_ENABLED or message is None:
        return

    tag = None
    if stack is not None and include_tag is True:
        frame = stack[1][0]
        caller = frame.f_locals.get('self', None)
        class_name = frame.f_locals.get('cls', None)
        
        if caller is not None:
            tag = caller.__class__.__name__
        elif class_name is not None:
            tag = class_name.__name__
        else:
            tag = "LOG"

        if tag is not None and len(tag) > 0:
            message = "[{}] {}".format(tag, message)

    if log_level is not None:
        color_code = COLOR_SEQ % (30 + LOG_COLORS[log_level])
    elif color is not None:
        color_code = COLOR_SEQ % (30 + color)
    else:
        color_code = COLOR_SEQ % (30 + WHITE)

    print("{}{}{}".format(color_code, message, RESET_SEQ))
