# minke.console.commands.graph
# Extract a keyphrase graph from the corpus.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Sep 02 12:14:41 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: graph.py [] benjamin@bengfort.com $

"""
Extract a keyphrase graph from the corpus.
"""

##########################################################################
## Imports
##########################################################################

import pickle
import networkx as nx

from commis import Command
from minke.graph import graph
from minke.corpus import READERS

##########################################################################
## Command
##########################################################################

class GraphCommand(Command):

    name = "graph"
    help = "extract a keyphrase graph from the corpus"
    args = {
        ('-r', '--reader'): {
            'default': 'pickle',
            'choices': READERS.keys(),
            'help': 'the corpus reader to use and parse documents',
        },
        ('-o', '--output'): {
            'metavar': 'PATH',
            'default': 'keyphrases.graphml',
            'help': 'name of file to write the graph out to',
        },
        ('-f', '--format'): {
            'default': 'graphml',
            'choices': ('graphml', 'pickle'),
            'help': 'the output format for the graph',
        },
        'corpus': {
            'nargs': 1,
            'help': 'the path to the corpus to describe',
        }
    }

    def handle(self, args):
        """
        Handle the graph command.
        """

        reader = READERS[args.reader]
        self.corpus = reader(args.corpus[0])

        # Construct the graph using the graph command
        G = graph(self.corpus)

        # Write out the graph to disk
        if args.format == 'graphml':
            # Currently this fails if there are any None values
            nx.write_graphml(G, args.output)

        elif args.format == 'pickle':
            with open(args.output, 'wb') as fobj:
                pickle.dump(G, fobj)

        return nx.info(G)
