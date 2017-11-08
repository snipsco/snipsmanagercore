# -*-: coding utf-8 -*-
""" Logging utilities. """

import sys

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

COLOR_VALUES = {
    'BLACK': BLACK,
    'RED': RED,
    'GREEN': GREEN,
    'YELLOW': YELLOW,
    'BLUE': BLUE,
    'MAGENTA': MAGENTA,
    'CYAN': CYAN,
    'WHITE': WHITE
}

RESET_SEQ = u'\033[0m'
BOLD_SEQ = u'\033[1m'
DIM_SEQ = u'\033[2m'
UNDERLINE_SEQ = u'\033[4m'
COLOR_SEQ = u'\033[%dm'

INDENT_SIZE = 2
INDENT_STR = INDENT_SIZE * ' '

CHECKMARK_SYMBOL=u'\u2714'
LIGHTNING_SYMBOL=u'\u21AF'
CHEVRON_SYMBOL=u'\u276F'
CROSS_SYMBOL=u'\u2718'
ARROW_SYMBOL=u'\u2794'
LIGHTBULB_SYMBOL=u'\U0001F4A1'
DOTS_SYMBOL=u'\u22EF'
QUESTION_SYMBOL='?'

silent = False

class ConsoleMessage:

    def __init__(self, message):
        self.message = message

    def start(self):
        psubmessage(self.message, prepend=DOTS_SYMBOL)

    def done(self):
        psubmessage(self.message, prepend=CHECKMARK_SYMBOL, overwrite_previous=True)

    def error(self):
        prepend = BOLD_SEQ + CROSS_SYMBOL + RESET_SEQ
        psubmessage(self.message, prepend=prepend, overwrite_previous=True)


def pheader(text):
    pprint(to_color_seq(BLUE) + BOLD_SEQ + UNDERLINE_SEQ + str(text) + RESET_SEQ)

def pheadersuccess(text):
    pprint(to_color_seq(GREEN) + BOLD_SEQ + UNDERLINE_SEQ + str(text) + RESET_SEQ)

def pquestion(text):
    pprint(to_color_seq(GREEN) + BOLD_SEQ + QUESTION_SYMBOL + ' ' + RESET_SEQ + BOLD_SEQ + str(text) + RESET_SEQ)

def psuccess(text):
    pprint(to_color_seq(GREEN) + BOLD_SEQ + CHECKMARK_SYMBOL + ' ' + RESET_SEQ + str(text) + RESET_SEQ)

def psubsuccess(text):
    psubmessage(text, prepend=CHECKMARK_SYMBOL, overwrite_previous=False)

def perror(text):
    pprint(to_color_seq(RED) + BOLD_SEQ + CROSS_SYMBOL + ' ' + str(text) + RESET_SEQ)

def pwarning(text):
    pprint(to_color_seq(YELLOW) + BOLD_SEQ + LIGHTNING_SYMBOL + ' ' + RESET_SEQ + str(text) + RESET_SEQ)

def phint(text):
    pprint(to_color_seq(YELLOW) + BOLD_SEQ + LIGHTBULB_SYMBOL + ' ' + RESET_SEQ + str(text) + RESET_SEQ)

def pcommand(text):
    pprint(to_color_seq(BLUE) + BOLD_SEQ + CHEVRON_SYMBOL + ' ' + RESET_SEQ + BOLD_SEQ + str(text) + RESET_SEQ)

def psubmessage(text, indent=False, prepend=None, overwrite_previous=False):
    text = DIM_SEQ + text
    text = text.replace("$RESET", RESET_SEQ + DIM_SEQ)
    for color_string, color_value in COLOR_VALUES.iteritems():
        text = text.replace("$" + color_string, to_color_seq(color_value))
    if indent is True:
        text = INDENT_STR + text
    if prepend is not None:
        text = prepend + " " + RESET_SEQ + text
    pprint(text + RESET_SEQ, overwrite_previous=overwrite_previous)

def preset():
    pprint(RESET_SEQ + '\r')

def pprint(message, overwrite_previous=False):
    if silent:
        return
    if overwrite_previous:
        sys.stdout.write("\033[F")
    print(message.encode('utf-8'))

def generate_user_input_string(text):
    return RESET_SEQ + INDENT_STR + text + ' ' + RESET_SEQ + to_color_seq(CYAN)

def to_color_seq(color):
    return COLOR_SEQ % (30 + color)
