# minke.console.app
# Definition of the MinkeUtility app and commands.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 06 16:17:05 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: app.py [3d75c52] benjamin@bengfort.com $

"""
Definition of the MinkeUtility app and commands.
http://bbengfort.github.io/tutorials/2016/01/23/console-utility-commis.html
"""

##########################################################################
## Imports
##########################################################################

from commis import color
from commis import ConsoleProgram

from minke.version import get_version
from minke.console.commands import *

##########################################################################
## Utility Definition
##########################################################################

DESCRIPTION = "Run modeling and adminstrative commands on the Baleen corpus"
EPILOG      = "If there are any bugs or concerns, submit an issue on GitHub"
COMMANDS    = [
    SampleCommand,
    DescribeCommand,
    PreprocessCommand,
    SizesCommand,
    ManifestCommand,
]

##########################################################################
## The Minke CLI Utility
##########################################################################

class MinkeUtility(ConsoleProgram):

    description = color.format(DESCRIPTION, color.CYAN)
    epilog      = color.format(EPILOG, color.MAGENTA)
    version     = color.format("minke (sei) v{}", color.CYAN, get_version())

    @classmethod
    def load(klass, commands=COMMANDS):
        utility = klass()
        for command in commands:
            utility.register(command)
        return utility
