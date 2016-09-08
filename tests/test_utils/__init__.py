# tests.test_utils
# Testing package for the utilities module.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 06 21:29:13 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: __init__.py [9eee771] benjamin@bengfort.com $

"""
Testing package for the utilities module.
"""

##########################################################################
## Imports
##########################################################################

import unittest

from minke.utils import *

##########################################################################
## Helper Function Tests
##########################################################################

class HelperFunctionTests(unittest.TestCase):

    def test_module_exists(self):
        """
        Test the module exists helper function
        """

        # These modules should be installed with requirements.txt
        self.assertTrue(module_exists('networkx'))
        self.assertTrue(module_exists('nltk.corpus'))

        # These modules do not exist
        self.assertFalse(module_exists('finkeybarbar'))
        self.assertFalse(module_exists('bar.fink.boo.bar.baz'))
