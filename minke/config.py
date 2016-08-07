# minke.config
# Configuration and settings from a YAML file using Confire.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 06 21:00:05 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: config.py [] benjamin@bengfort.com $

"""
Configuration and settings from a YAML file using Confire.
"""

##########################################################################
## Imports
##########################################################################

import os

from confire import Configuration


##########################################################################
## Base Paths
##########################################################################

PROJECT  = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


##########################################################################
## Nested Configurations
##########################################################################

class NotifyConfiguration(Configuration):
    """
    Email settings so that CloudScope can send email messages
    """

    username    = None
    password    = None
    email_host  = None
    email_port  = None
    fail_silent = True


##########################################################################
## Minke Configuration
##########################################################################

class MinkeConfiguration(Configuration):

    CONF_PATHS = [
        '/etc/minke.yaml',
        os.path.expanduser('~/.minke.yaml'),
        os.path.abspath('conf/minke.yaml'),
        os.path.abspath('minke.yaml'),
        os.path.abspath('.minke.yaml'),
    ]

    debug      = False
    testing    = False

    # Notification parameters
    notify     = NotifyConfiguration()


##########################################################################
## Generate Site Settings
##########################################################################

settings = MinkeConfiguration.load()

if __name__ == '__main__':
    print(settings)
