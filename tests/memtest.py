#!/usr/bin/env python
# tests.memtest
# Short script to exercise the corpus reader memory usage.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Apr 19 16:38:28 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: memtest.py [] benjamin@bengfort.com $

"""
Short script to exercise the corpus reader memory usage. Basically the script
runs through every document in the corpus and prints information about the
document to see how much memory is being used.
"""

##########################################################################
## Imports
##########################################################################

import os
import time
import argparse

from nltk import FreqDist
from functools import partial
from minke.corpus import BaleenCorpusReader

##########################################################################
## Static Variables
##########################################################################

PROJECT = os.path.join(os.path.dirname(__file__), "..")
CORPUS  = os.path.join(PROJECT, "fixtures", "corpus")


def main(args):
    """
    Runs a sequential scan over the corpus, for the given method, allowing
    you to check Activity Monitor to ensure that memory isn't being overused.
    """
    # Construct the corpus and fetch reader method
    corpus = BaleenCorpusReader(args.corpus)

    # If describe, print describe and exit
    if args.describe:
        print(corpus.describes(categories=args.categories))
        return

    # Find the method and set up counting
    method = getattr(corpus, args.method)
    counts = FreqDist()
    start  = time.time()

    # Create the partial closure for the fields
    if args.method == 'fields':
        method = partial(method, (args.fields))

    # Begin the sequential scan
    for idx, item in enumerate(method(categories=args.categories)):
        if args.limit is not None and idx >= args.limit:
            break

        try:

            if args.method == 'docs':
                if not args.quiet:
                    print(u"{: >7}: {}".format(idx+1, item['title']))

            elif args.method == 'fields':
                if not args.quiet:
                    print(u"{: >7}: {}".format(idx+1, item))

            elif args.method == 'html':
                if not args.quiet:
                    print(u"{}\n\n".format(item))

            elif args.method == 'sizes':
                print(u"{},{}".format(*item))

            elif args.method in ('words',):
                counts[item] += 1

            if args.method in ('paras', 'sents', 'words'):
                if not args.quiet:
                    if (idx + 1) % 1000 == 0:
                        print(u"{} {} scanned".format(idx+1, args.method))

        except KeyboardInterrupt:
            break

    # Print out the time and effort
    print(u"Scanned {} {} in {:0.3f} seconds.".format(
        idx, args.method, time.time() - start
    ))

    # Print out counts if we're doing that
    if args.method == 'words':
        for item in counts.most_common(100):
            print(u"    {}: {}".format(*item))

if __name__ == '__main__':

    # Command line arguments
    args = {
        ('--describe',): {
            'action': 'store_true',
            'help': 'describe the corpus and exit',
        },
        ('-Q', '--quiet'): {
            'action':'store_true',
            'help': 'limit the amount of output being printed'
        },
        ('-c', '--categories'): {
            'default': None,
            'nargs': '*',
            'metavar': 'CAT',
            'help': 'specify the categories to stream over',
        },
        ('-f', '--fields'): {
            'default': None,
            'nargs': '*',
            'metavar': 'FIELD',
            'help': 'for the fields method, specify the desired fields'
        },
        ('-n', '--limit'): {
            'type': int,
            'default': None,
            'metavar': 'N',
            'help': 'limit the number of rows scanned in the corpus'
        },
        ('-d', '--corpus'): {
            'type': str,
            'default': CORPUS,
            'help': 'change the place to look for the corpus root'
        },
        ('method',): {
            'nargs': '?',
            'type': str,
            'default': 'docs',
            'choices': ['docs', 'fields', 'html', 'paras', 'sents', 'words', 'sizes'],
            'help': 'specify the scanning method to use',
        }
    }

    # Create the parser
    parser  = argparse.ArgumentParser()
    for pargs, kwargs in args.items():
        parser.add_argument(*pargs, **kwargs)

    # Parse the arguments and execute main
    options = parser.parse_args()
    main(options)
