# tests.test_utils.test_decorators
# Tests for the function decorator utilities in Minke.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 06 21:28:53 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: test_decorators.py [] benjamin@bengfort.com $

"""
Tests for the function decorator utilities in Minke.
"""

##########################################################################
## Imports
##########################################################################

import time
import unittest

from minke.utils.decorators import *

try:
    from unittest import mock
except ImportError:
    import mock


##########################################################################
## Decorators Tests
##########################################################################

class DecoratorsTests(unittest.TestCase):
    """
    Basic decorators utility tests.
    """

    def test_memoized(self):
        """
        Test the memoized property
        """

        class Thing(object):

            @memoized
            def attr(self):
                return 42

        thing = Thing()
        self.assertFalse(hasattr(thing, '_attr'))
        self.assertEqual(thing.attr, 42)
        self.assertTrue(hasattr(thing, '_attr'))

    def test_timeit(self):
        """
        Test the timeit decorator
        """

        @timeit
        def myfunc():
            return 42

        output = myfunc()
        self.assertEqual(len(output), 2)
        result, timer = output
        self.assertEqual(result, 42)
        self.assertTrue(isinstance(timer, Timer))
