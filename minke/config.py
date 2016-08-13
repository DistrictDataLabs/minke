# minke.config
# Configuration and settings from a YAML file using Confire.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 06 21:00:05 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: config.py [ad9c2f7] benjamin@bengfort.com $

"""
Configuration and settings from a YAML file using Confire.
"""

##########################################################################
## Imports
##########################################################################

import os
import multiprocessing as mp

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
    Email settings so that CloudScope can send email messages.
    Note, if using Gmail, you must set simple authentication.
    """

    username    = None  # Username to email service
    password    = None  # Password of email service
    email_host  = None  # Domain of the SMTP serivce
    email_port  = None  # Port that the SMTP service listens on
    fail_silent = True  # Whether to raise an error or not.


class PreprocessingConfiguration(Configuration):
    """
    Settings for preprocessing a corpus to another location
    """

    tasks       = mp.cpu_count() # Number of tasks to run in parallel
    parallel    = False # Parallelize the preprocessing with multiprocessing
    overwrite   = False # Overwrite existing files with new data
    skip_exists = True  # Skip any filenames that already exist in the target


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

    # Preprocessing parameters
    preprocess = PreprocessingConfiguration()


##########################################################################
## Generate Site Settings
##########################################################################

settings = MinkeConfiguration.load()

if __name__ == '__main__':
    print(settings)
