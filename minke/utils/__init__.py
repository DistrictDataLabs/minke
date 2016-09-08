# minke.utils
# Utility functions, decorators, timers, etc. for the Minke project.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 06 16:50:13 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: __init__.py [3d75c52] benjamin@bengfort.com $

"""
Utility functions, decorators, timers, etc. for the Minke project.
"""

##########################################################################
## Imports
##########################################################################


##########################################################################
## Helper Functions
##########################################################################

def module_exists(name):
    """
    Checks if the module with the given name exists and can be imported.
    """
    try:
        __import__(name)
    except ImportError:
        return False
    else:
        return True
