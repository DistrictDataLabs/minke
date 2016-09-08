# minke.console.commands.describe
# Command to describe a corpus for monitoring.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 06 16:45:51 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: describe.py [3d75c52] benjamin@bengfort.com $

"""
Command to describe a corpus for monitoring.
"""

##########################################################################
## Imports
##########################################################################

import os

from commis import Command
from operator import itemgetter
from minke.corpus import READERS
from minke.utils.humanize import filesize


##########################################################################
## Command
##########################################################################

class DescribeCommand(Command):

    name = "describe"
    help = "describe corpus properties for monitoring"
    args = {
        ('-r', '--reader'): {
            'default': 'pickle',
            'choices': READERS.keys(),
            'help': 'the corpus reader to use and parse documents',
        },
        ('-d', '--disk-usage'): {
            'action': 'store_true',
            'default': False,
            'help': 'display disk usage of corpus by category and exit',
        },
        'corpus': {
            'nargs': 1,
            'help': 'the path to the corpus to describe',
        }
    }

    def handle(self, args):
        """
        Handle the describe command.
        """
        reader = READERS[args.reader]
        self.corpus = reader(args.corpus[0])

        if args.disk_usage:
            return self.disk_usage()

        return self.corpus.describes()

    def disk_usage(self):
        """
        Returns disk usage properties of the corpus.
        """
        output = []

        # Global disk usage statement
        output.append(
            "{:,} documents in {:,} categories ({})".format(
                len(self.corpus.fileids()), len(self.corpus.categories()),
                filesize(sum(self.corpus.sizes()))
            )
        )

        # Per category usage statement
        for cat in self.corpus.categories():
            csize = sum(self.corpus.sizes(categories=cat))
            output.append(
                "  - {}: {:,} ({})".format(
                    cat, len(self.corpus.fileids(categories=cat)), filesize(csize)
                )
            )

        return "\n".join(output)
