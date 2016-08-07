# minke.utils.statistics
# Helper functions for statistical computations.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 06 17:04:24 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: statistics.py [] benjamin@bengfort.com $

"""
Helper functions for statistical computations.
"""

##########################################################################
## Imports
##########################################################################

##########################################################################
## Statistical computation functions
##########################################################################

def mean(data):
    """
    TODO: if Numpy becomes a dependency, change this to a Numpy computation.
    """
    data = list(map(float, data))
    if data:
        return sum(data) / len(data)


def median(data, sort=True):
    """
    Finds the median in a list of numbers. If sort is False, this function
    expects the data to be presorted, or at least it won't be sorted again!
    Wanted to do this without the Numpy dependency, but if we bring Numpy in,
    then lets convert this function to creating a Numpy array then issuing
    the median function call.
    """
    if not data:
        return None

    num = len(data)
    if sort:
        data = sorted(data)

    if num & 1:
        # If num is odd, get the index simply by dividing it in half
        index = num / 2
        return data[index]

    # If num is even, average the two values at the center
    jdx = num / 2
    idx = jdx - 1
    return (data[idx] + data[jdx]) / 2.0
