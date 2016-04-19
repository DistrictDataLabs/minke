# tests
# Testing for the minke module
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Apr 19 11:06:59 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
Testing for the minke module
"""

##########################################################################
## Imports
##########################################################################

import unittest

##########################################################################
## Module Constants
##########################################################################

TEST_VERSION = "0.1" ## Also the expected version onf the package

##########################################################################
## Test Cases
##########################################################################

class InitializationTest(unittest.TestCase):

    def test_initialization(self):
        """
        Tests a simple world fact by asserting that 7**2 is 49
        """
        self.assertEqual(7**2, 49)

    def test_import(self):
        """
        Can import minke
        """
        try:
            import minke
        except ImportError:
            self.fail("Unable to import the minke module!")

    def test_version(self):
        """
        Assert that the version is sane
        """
        import minke
        self.assertEqual(TEST_VERSION, minke.__version__)
