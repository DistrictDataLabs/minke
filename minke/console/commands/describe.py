# minke.console.commands.describe
# Command to describe a corpus for monitoring.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 06 16:45:51 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: describe.py [] benjamin@bengfort.com $

"""
Command to describe a corpus for monitoring.
"""

##########################################################################
## Imports
##########################################################################

import os

from commis import Command
from operator import itemgetter
from minke.corpus import BaleenCorpusReader
from minke.utils.humanize import filesize


##########################################################################
## Command
##########################################################################

class DescribeCommand(Command):

    name = "describe"
    help = "describe corpus properties for monitoring"
    args = {
        'corpus': {
            'nargs': 1,
            'help': 'the path to the corpus to describe',
        }
    }

    def handle(self, args):
        """
        Handle the describe command.
        """
        self.corpus = BaleenCorpusReader(args.corpus[0])
        return self.disk_usage()

    def disk_usage(self):
        """
        Returns disk usage properties of the corpus.
        """
        output = []

        # Global disk usage statement
        output.append(
            "{} documents in {} categories ({})".format(
                len(self.corpus.fileids()), len(self.corpus.categories()),
                filesize(sum(s[1] for s in self.corpus.sizes()))
            )
        )

        # Per category usage statement
        for cat in self.corpus.categories():
            csize = sum(size[1] for size in self.corpus.sizes(categories=cat))
            output.append(
                "  - {}: {} ({})".format(
                    cat, len(self.corpus.fileids(categories=cat)), filesize(csize)
                )
            )

        return "\n".join(output)
