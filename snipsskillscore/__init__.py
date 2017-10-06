# -*-: coding utf-8 -*-
""" snipsskillscore module """
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def get_default_logger():
    import logging
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    log_format = '\033[2m%(asctime)s\033[0m [%(levelname)s] %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(log_format, date_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

LOGGER = get_default_logger()
