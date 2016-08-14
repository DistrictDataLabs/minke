# minke.console.commands.sizes
# Computes the filesizes for each file in the corpus.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 13 21:42:54 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: sizes.py [] benjamin@bengfort.com $

"""
Computes the filesizes for each file in the corpus.
"""

##########################################################################
## Imports
##########################################################################

import os
import csv
import sys
import argparse

from tqdm import tqdm
from commis import Command
from minke.corpus import BaleenCorpusReader
from minke.utils.timer import Timer
from minke.utils.humanize import filesize as naturalsize


##########################################################################
## Command Description
##########################################################################

class SizesCommand(Command):

    name = 'sizes'
    help = 'creates a csv file with filesizes of documents in the corpus'
    args = {
        ('-H', '--humanize'): {
            'action': 'store_true',
            'default': False,
            'help': 'write file sizes in human readable units',
        },
        ('-o', '--output'): {
            'type': argparse.FileType('w'),
            'required': True,
            'metavar': 'PATH',
            'help': 'path to file to write CSV data out to',
        },
        'corpus': {
            'nargs': 1,
            'metavar': 'PATH',
            'help': 'path to the JSON corpus on disk',
        }
    }

    def handle(self, args):
        """
        Writes filesizes of the corpus to disk sequentially.
        """

        with Timer() as timer:

            # Create the CSV writer
            writer = csv.writer(args.output)
            corpus = BaleenCorpusReader(args.corpus[0])
            n_docs = len(corpus.fileids())
            paths  = corpus.abspaths(None, False, True)
            total  = 0

            # Begin writing the sizes
            for path, fileid in tqdm(paths, total=n_docs, unit='docs'):

                # Get the filesize and add to the total
                size = os.path.getsize(path)
                total += size

                # If we need to humanize, then do so
                if args.humanize:
                    size = naturalsize(size)

                # Get the category and the base name
                category = os.path.dirname(fileid)
                basename = os.path.basename(fileid)

                # Write the row to the CSV file
                writer.writerow((category, basename, size))

        # Return the final result
        return "Identified {} in {} documents in {}".format(
            naturalsize(total), n_docs, timer
        )
