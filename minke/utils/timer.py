# minke.utils.timer
# Provides timing functionality for the Minke library.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 06 16:59:45 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: timer.py [3d75c52] benjamin@bengfort.com $

"""
Provides timing functionality for the Minke library.
"""

##########################################################################
## Imports
##########################################################################

import time

from minke.utils.humanize import timedelta as humanizedelta


##########################################################################
## Timer functions
##########################################################################

class Timer(object):
    """
    A context object timer. Usage:
        >>> with Timer() as timer:
        ...     do_something()
        >>> print timer.elapsed
    """

    def __init__(self, wall_clock=True):
        """
        If wall_clock is True then use time.time() to get the number of
        actually elapsed seconds. If wall_clock is False, use time.clock to
        get the process time instead.
        """
        self.wall_clock = wall_clock
        self.time = time.time if wall_clock else time.clock

        # Stubs for serializing an empty timer.
        self.started  = None
        self.finished = None
        self.elapsed  = 0.0

    def __enter__(self):
        self.started  = self.time()
        return self

    def __exit__(self, type, value, tb):
        self.finished = self.time()
        self.elapsed  = self.finished - self.started

    def __str__(self):
        return humanizedelta(seconds=self.elapsed)

    def serialize(self):
        return {
            'started':  self.started,
            'finished': self.finished,
            'elapsed':  humanizedelta(seconds=self.elapsed),
        }
