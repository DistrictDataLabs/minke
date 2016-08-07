# minke.utils.decorators
# Decorators for use wrapping functions with advanced funcationality.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 06 16:56:34 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: decorators.py [3d75c52] benjamin@bengfort.com $

"""
Decorators for use wrapping functions with advanced funcationality.
"""

##########################################################################
## Imports
##########################################################################

from functools import wraps
from minke.utils.timer import Timer


##########################################################################
## Descriptors
##########################################################################

def memoized(fget):
    """
    Return a property attribute for new-style classes that only calls its
    getter on the first access. The result is stored and on subsequent
    accesses is returned, preventing the need to call the getter any more.
    https://github.com/estebistec/python-memoized-property
    """
    attr_name = '_{0}'.format(fget.__name__)

    @wraps(fget)
    def fget_memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fget(self))
        return getattr(self, attr_name)

    return property(fget_memoized)


def setter(fset):
    """
    Returns a property attribute for new-style classes that defines behavior
    when setting the value, but not when getting it.
    """
    attr_name = '_{0}'.format(fset.__name__)

    def fget(self):
        """
        Returns the internal, wrapped property that is set automatically.
        """
        if not hasattr(self, attr_name):
            raise AttributeError(
                "No value for {} has been set!".format(fset.__name__)
            )
        return getattr(self, attr_name)

    @wraps(fset)
    def fset_setter(self, value):
        setattr(self, attr_name, fset(self, value))

    return property(fget, fset_setter)


##########################################################################
## Descriptors
##########################################################################

def timeit(func, wall_clock=True):
    """
    Returns the number of seconds that a function took along with the result
    """
    @wraps(func)
    def timer_wrapper(*args, **kwargs):
        """
        Inner function that uses the Timer context object
        """
        with Timer(wall_clock) as timer:
            result = func(*args, **kwargs)

        return result, timer
    return timer_wrapper
