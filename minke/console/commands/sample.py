# minke.console.commands.sample
# An adminstrative script to perform a simple random sample of a corpus.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed May 25 11:24:20 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: sample.py [3d75c52] benjamin@bengfort.com $

"""
An adminstrative script to perform a simple random sample of a corpus.
"""

##########################################################################
## Imports
##########################################################################

import os
import minke
import shutil
import random

from commis import Command
from minke.utils.timer import Timer
from minke.corpus import BaleenCorpusReader
from collections import OrderedDict


##########################################################################
## Command Description
##########################################################################

class SampleCommand(Command):

    name = 'sample'
    help = 'creates a simple random sample of a corpus of documents'
    args = OrderedDict([
        (('-p', '--percent'), {
            'type': int,
            'default': 10,
            'metavar': '%',
            'help': 'the percent of the corpus to sample, default is 10%%'
        }),
        (('-C', '--by-corpus'), {
            'action': 'store_false',
            'dest': 'categorical',
            'default': True,
            'help': 'sample the corpus as a whole, not by category.'
        }),
        ('source', {
            'nargs': 1,
            'help': 'path to the directory containing the original corpus.',
        }),
        ('target', {
            'nargs': 1,
            'help': 'path to write the sampled corpus out to.'
        }),
    ])

    def handle(self, args):
        """
        Handles the sampling command.
        """
        self.source = args.source[0]
        self.target = args.target[0]
        self.percent = args.percent / 100.0
        self.categorical = args.categorical

        with Timer() as timer:
            sample, total = self.sample()

        return "Sampled {} of {} documents from {} to {} in {}".format(
            sample, total, self.source, self.target, timer
        )

    def copy_root_files(self):
        """
        Copies the root files from the source to the target.
        """
        # List the names inside the source directory.
        names = [
            name  for name in os.listdir(self.source)
            if not name.startswith('.')
        ]

        # Filter out directories and copy files
        for name in names:
            source = os.path.join(self.source, name)
            target = os.path.join(self.target, name)

            if os.path.isfile(source):
                shutil.copy(source, target)

    def sample(self, target=None):
        """
        Sample instantiates a BaleenCorpusReader on the source, then moves a
        subset of the files in the original corpus (specified by the percent) to
        the directory specified by target.

        Note: Specify the percent as an integer between 1-99.

        If categorical is true, it samples a percent of each category, otherwise
        samples a percent of the files in the entire corpus.

        The sampler performs the following steps:

            1. Creates the target directory if it doesn't already exist
            2. Copies any files in the root directory over
            3. Iterates over categories and creates category sub directories
            4. Selects files to move by the categorical flag
            5. Copies all files over to the target directory

        Note this may take a while for large corpora, but no files are read.
        """
        if target is not None:
            self.target = target

        if self.target is None:
            raise ValueError("Target must be a path to a directory")

        # Step zero: instantiate the corpus reader
        corpus  = BaleenCorpusReader(self.source)

        # Step one: create target directory
        if not os.path.exists(self.target):
            os.makedirs(self.target)

        # Step two: shutil over the root documents
        self.copy_root_files()

        # Step 3: create categorical subdirectories
        for category in corpus.categories():
            catdir = os.path.join(self.target, category)
            if not os.path.exists(catdir):
                os.makedirs(catdir)

        # Step 4: select fileids
        # TODO: implement categorical field.
        if not self.categorical:
            raise NotImplementedError("Sampling by corpus not yet supported!")

        docs = 0
        for category in corpus.categories():
            for fileid in corpus.fileids(categories=category):
                if random.random() <= self.percent:
                    docs += 1
                    source = os.path.join(self.source, fileid)
                    target = os.path.join(self.target, fileid)
                    shutil.copy(source, target)

        # Return the number of documents copied.
        return docs, len(corpus.fileids())
