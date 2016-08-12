# console.commands.preprocess
# A management command to engage the preprocessing in a meaningful way.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Aug 12 19:01:43 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: preprocess.py [] benjamin@bengfort.com $

"""
A management command to engage the preprocessing in a meaningful way.
"""

##########################################################################
## Imports
##########################################################################

from commis import Command
from minke.config import settings
from collections import OrderedDict
from minke.utils.timer import Timer
from minke.preprocess import Preprocessor
from minke.corpus import BaleenCorpusReader


##########################################################################
## Command
##########################################################################

class PreprocessCommand(Command):

    name = "preprocess"
    help = "transform an html corpus into a pickled preprocessed corpus"
    args = args = OrderedDict([
        (('-p', '--parallel'), {
            "action": "store_true",
            "default": settings.preprocess.parallel,
            "help": "run the preprocessing in parallel with multiprocessing",
        }),
        (('-t', '--tasks'), {
            "type": int,
            "default": settings.preprocess.tasks,
            "metavar": "CPUs",
            "help": "if parallel, specify the number of processes",
        }),
        ('--overwrite', {
            'action': 'store_true',
            'default': settings.preprocess.overwrite,
            'help': 'overwrite any existing files in the target',
        }),
        ('--no-skip', {
            'action': 'store_false',
            'dest': 'skip_exists',
            'default': settings.preprocess.skip_exists,
            'help': "don't skip any similarly named files in the target",
        }),
        ('corpus', {
            'nargs': 1,
            'help': 'the path to the html corpus to preprocess',
        }),
        ('target', {
            'nargs': 1,
            'help': 'the path to a directory to write the new corpus to',
        })
    ])

    def handle(self, args):
        """
        Handle the describe command.
        """
        # Create the common transformer keyword arguments
        kwargs = {
            'overwrite': args.overwrite,
            'skip_exists': args.skip_exists,
        }

        # Handle multiprocessing
        if args.parallel:
            raise NotImplementedError("Parallel prprocessing not implemented.")

        # Time and execute the transformation
        with Timer() as timer:
            corpus = BaleenCorpusReader(args.corpus[0])
            transformer = Preprocessor(corpus, args.target[0], **kwargs)

            docs = sum(1 for doc in transformer.transform())

        return "Preprocessed {} documents in {}".format(docs, timer)
