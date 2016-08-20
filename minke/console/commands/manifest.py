# minke.console.commands.manifest
# Generates a manifest of document-specific information from the JSON corpus.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Aug 18 10:33:59 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: manifest.py [] benjamin@bengfort.com $

"""
Generates a manifest of document-specific information from the JSON corpus.
"""

##########################################################################
## Imports
##########################################################################

import csv
import argparse
import multiprocessing as mp

from tqdm import tqdm
from commis import Command
from functools import reduce
from collections import OrderedDict

from minke.utils.timer import Timer
from minke.corpus import BaleenCorpusReader
from minke.utils.humanize import filesize as naturalsize

##########################################################################
## Manifest Fields
## TODO: Allow user to supply the fields somehow
##########################################################################

FIELDS = OrderedDict([
    ('document', '_id.$oid'),
    ('feed', 'feed.$oid'),
    ('title', 'title'),
    ('url', 'url'),
    ('pubdate', 'pubdate.$date'),
    ('created', 'created.$date'),
])

##########################################################################
## Command Description
##########################################################################

class ManifestCommand(Command):

    name = 'manifest'
    help = 'creates a csv or sqlite file with metadata from a corpus of JSON documents'
    args = {
        ('-o', '--output'): {
            'type': argparse.FileType('w'),
            'required': True,
            'metavar': 'PATH',
            'help': 'path to file to write CSV data out to',
        },
        'corpus': {
            'nargs': 1,
            'metavar': 'CORPUS',
            'help': 'path to the JSON corpus on disk',
        },
    }

    def handle(self, args):
        """
        Generates the manifest from a corpus of JSON documents.
        """
        with Timer() as timer:
            # Create reader and writer
            writer = csv.DictWriter(args.output, fieldnames=FIELDS.keys())
            corpus = BaleenCorpusReader(args.corpus[0])

            # Initialize output
            writer.writeheader()
            n_docs = len(corpus.fileids())

            # Iterate through all documents, generating the manifest.
            for idx,doc in enumerate(tqdm(corpus.docs(), total=n_docs, unit="Docs")):
                values = [self.nested_value(doc, field) for field in FIELDS.values()]
                row = dict(zip(FIELDS.keys(), values))
                writer.writerow(row)

        return "Generated {:,} manifest records in {}".format(idx+1, timer)

    def nested_value(self, doc, field):
        """
        Extracts a dot delimited key from a document and returns the key/val
        pair as follows. Given a key, created.$date, this method will return
        a timestamp that is the value doc["created"]["$date"].

        Note this method returns None for values that do not exist.
        """
        keys  = field.split(".")
        value = reduce(lambda d, k: d.get(k, {}), keys, doc)

        if not value:
            return None
        return value
