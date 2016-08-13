# minke.utils.humanize
# Provides methods for humanizing values for better readability.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 06 16:51:02 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: humanize.py [3d75c52] benjamin@bengfort.com $

"""
Provides methods for humanizing values for better readability.
"""

##########################################################################
## Imports
##########################################################################

from dateutil.relativedelta import relativedelta


##########################################################################
## Format constants
##########################################################################

HUMAN_DATETIME   = "%a %b %d %H:%M:%S %Y %z"
HUMAN_DATE       = "%b %d, %Y"
HUMAN_TIME       = "%I:%M:%S %p"
JSON_DATETIME    = "%Y-%m-%dT%H:%M:%S.%fZ" # Must be UTC
ISO8601_DATETIME = "%Y-%m-%dT%H:%M:%S%z"
ISO8601_DATE     = "%Y-%m-%d"
ISO8601_TIME     = "%H:%M:%S"
COMMON_DATETIME  = "%d/%b/%Y:%H:%M:%S %z"


##########################################################################
## Humainze Functions
##########################################################################

def filesize(num, suffix='B'):
    """
    Returns a size in bytes (or other specified unit) in human readable form.
    """
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def timedelta(*args, **kwargs):
    """
    Wrapper around dateutil.relativedelta (same construtor args) and returns
    a humanized string representing the detla in a meaningful way.
    """
    if 'milliseconds' in kwargs:
        sec  = kwargs.get('seconds', 0)
        msec = kwargs.pop('milliseconds')
        kwargs['seconds'] = sec + (float(msec) / 1000.0)

    delta = relativedelta(*args, **kwargs)
    attrs = ('years', 'months', 'days', 'hours', 'minutes', 'seconds')
    parts = [
        '%d %s' % (getattr(delta, attr), getattr(delta, attr) > 1 and attr or attr[:-1])
        for attr in attrs if getattr(delta, attr)
    ]

    return " ".join(parts)
