# minke.graph
# Extracts a Graph from keyphrases in the corpus.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri May 06 11:55:34 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: graph.py [] benjamin@bengfort.com $

"""
Extracts a Graph from keyphrases in the corpus.
"""

##########################################################################
## Imports
##########################################################################

import os
import networkx as nx

from minke.keyphrase import TFIDFScorer


##########################################################################
## Graph Extraction
##########################################################################



def graph(corpus, lookup, categories=None, verbose=True):
    """
    Returns a TF-IDF Graph of key terms to documents to feeds to categories.
    Temporarily this loads two corpora one that's already parsed and one that
    is used to lookup the requried JSON data from the corpus.
    """

    G = nx.Graph(name="Baleen Keyphrase Graph")

    # Create a Feed lookup table
    feeds = {
        feed['_id']['$oid']: feed for feed in corpus.feeds()
    }

    # Create category, feed, and document nodes
    if verbose: print("Creating category, feed, and document nodes")
    G.add_nodes_from(corpus.categories(), type='category')
    G.add_nodes_from([feed['title'] for feed in feeds.values()], type='feed')
    G.add_nodes_from(corpus.fileids(), type='document')

    # Create feed-category edges
    if verbose: print("Creating feed-category edges")
    G.add_edges_from([
        (feed['title'], feed['category']) for feed in feeds.values()
    ])

    # Create document-category edges
    if verbose: print("Creating document-category edges")
    G.add_edges_from([
        (fileid, corpus.categories(fileids=fileid)[0])
        for fileid in corpus.fileids(categories=categories)
    ])

    # Add document attributes from lookup and document-feed edges
    if verbose: print("Adding document attributes from lookup")
    for fileid in corpus.fileids(categories=categories):

        # Figure out the lookup file extension
        rawid, ext = os.path.splitext(fileid)
        rawid += ".json"

        # Load the document from the lookup
        doc = lookup.docs(fileids=rawid).next()

        # Set the node attributes
        G.node[fileid]['title'] = doc['title']
        G.node[fileid]['pubdate'] = doc.get('pubdate', {}).get('$date', 0)

        # Create the document-feed edge
        G.add_edge(fileid, feeds[doc['feed']['$oid']]['title'])


    # Perform the keyphrase extractions using TF-IDF Scores
    if verbose: print("Performing keyphrase extraction and scoring")
    phrases = TFIDFScorer(corpus)
    phrases.score(categories=categories)

    # Add the keyphrase-document edges
    if verbose: print("Adding keyphrase-document edges weighted by TF-IDF")
    for idx, doc in enumerate(phrases.tfidfs):
        fileid = phrases.fileids[idx]

        for wid, score in doc:
            word = phrases.lexicon[wid]
            G.add_edge(fileid, word, weight=score)

    return G


if __name__ == '__main__':
    import os
    from minke.corpus import BaleenCorpusReader, BaleenPickledCorpusReader

    PROJECT = os.path.join(os.path.dirname(__file__), "..")
    RCORPUS = os.path.join(PROJECT, "fixtures", "corpus")
    PCORPUS = os.path.join(PROJECT, "fixtures", "tagged_corpus")
    OUTFILE = os.path.join(PROJECT, "fixtures", "keyphrases.graphml")

    rcorpus = BaleenCorpusReader(RCORPUS)
    pcorpus = BaleenPickledCorpusReader(PCORPUS)

    categories = ['data science', 'books', 'cooking', 'politics', 'news', 'design', 'gaming', 'news', 'sports', 'tech']
    G = graph(pcorpus, rcorpus, categories=categories)
    print(nx.info(G))
    nx.write_graphml(G, OUTFILE)
