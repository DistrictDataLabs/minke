# tests.test_utils.test_timer
# Tests for the timer module.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 06 21:30:41 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: test_timer.py [9eee771] benjamin@bengfort.com $

"""
Tests for the timer module.
"""

##########################################################################
## Imports
##########################################################################

import time
import unittest

from minke.utils.timer import Timer


##########################################################################
## Timer Tests
##########################################################################

class TimerTests(unittest.TestCase):
    """
    Basic Timer utility tests.
    """

    def test_timer(self):
        """
        Test the Timer context manager
        """
        with Timer() as t:
            time.sleep(1)

        self.assertGreater(t.finished, t.started)
        self.assertEqual(t.elapsed, t.finished-t.started)
        self.assertEqual(str(t), '1 seconds')

        data = t.serialize()
        for key in ('started', 'finished', 'elapsed'):
            self.assertIn(key, data)
