# minke.exceptions
# Exceptions hierarchy for the Minke library.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 06 17:07:10 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: exceptions.py [3d75c52] benjamin@bengfort.com $

"""
Exceptions hierarchy for the Minke library.
"""

##########################################################################
## Exception Hierarchy
##########################################################################

class MinkeError(Exception):
    """
    Something went wrong in Minke.
    """
    pass


class NotifyError(MinkeError):
    """
    Could not send an email notification.
    """
    pass


##########################################################################
## Warning Hierarchy
##########################################################################

class MinkeWarning(Warning):
    """
    Something non-terminating went wrong in Minke.
    """
    pass
