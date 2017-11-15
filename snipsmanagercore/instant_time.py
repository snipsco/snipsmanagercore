# -*-: coding utf-8 -*-
""" A representation of a datetime with a given granularity (day, week). """


# pylint: disable=too-few-public-methods
class InstantTime:
    """ A representation of a datetime with a given granularity (day, week).
    """

    day, week = range(2)

    def __init__(self, datetime, granularity=None):
        """ Initialisation.

        :param datetime: the underlying datetime object
        :param granularity: granularity of the datetime, either
                            InstantTime.day or InstantTime.week.
        """
        self.datetime = datetime
        self.granularity = granularity or InstantTime.day

    @staticmethod
    def parse_grain(grain):
        """ Parse a string to a granularity, e.g. "Day" to InstantTime.day.

        :param grain: a string representing a granularity.
        """
        if not grain:
            return InstantTime.day
        if grain.lower() == 'week':
            return InstantTime.week
        return InstantTime.day
