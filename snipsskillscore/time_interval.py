# -*-: coding utf-8 -*-
""" A representation of a time interval. """


# pylint: disable=too-few-public-methods
class TimeInterval:
    """ A representation of a time interval. """

    def __init__(self, start, end):
        """ Initialisation.

        :param start: the start of the time interval.
        :param end: the end of the time interval.
        """
        self.start = start
        self.end = end
