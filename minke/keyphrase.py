# minke.keyphrase
# Extracts keyphrases from the Baleen corpus.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue May 03 13:25:12 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: keyphrase.py [] benjamin@bengfort.com $

"""
Extracts keyphrases from the Baleen corpus.
See: http://bdewilde.github.io/blog/2014/09/23/intro-to-automatic-keyphrase-extraction/
"""

##########################################################################
## Imports
##########################################################################

import nltk
# import gensim

from itertools import groupby
from nltk.chunk import tree2conlltags
from nltk.chunk.regexp import RegexpParser

from minke.normalize import Normalizer
from minke.normalize import STOPWORDS, PUNCT

##########################################################################
## Module Constants
##########################################################################

GRAMMAR   = r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'
GOODTAGS  = set(['JJ','JJR','JJS','NN','NNP','NNS','NNPS'])

##########################################################################
## Key phrase extraction utilities
##########################################################################

def extract_candidates(sents, chunks=True, grammar=GRAMMAR, tags=GOODTAGS, **kwargs):
    """
    Entry point function for key phrase candidate extraction. If chunks is
    True than this uses `extract_candidate_chunks` otherwise uses the
    `extract_candidate_words` function. Also aliased as `candidates`.

    Note: this function expects tokenized sentences passed in to the method.
    """
    if chunks:
        return extract_candidate_chunks(sents, grammar, **kwargs)
    return extract_candidate_words(sents, tags, **kwargs)


# Alias for extract_candidates
candidates = extract_candidates


def extract_candidate_chunks(sents, grammar=GRAMMAR, **kwargs):
    """
    Extracts key chunks based on a grammar for a list of tokenized sentences.
    """
    normalizer = Normalizer(**kwargs)
    chunker    = RegexpParser(grammar)

    for sent in sents:
        # Tokenize and tag sentences, then parse with our chunker.
        tagged_sent = nltk.pos_tag(nltk.wordpunct_tokenize(sent))
        chunks = tree2conlltags(chunker.parse(tagged_sent))

        # Extract candidate phrases from our parsed chunks
        chunks = [
            " ".join(word for word, pos, chunk in group).lower()
            for key, group in groupby(
                chunks, lambda (word, pos, chunk): chunk != 'O'
            ) if key
        ]

        # Yield candidates that are not filtered by stopwords and punctuation.
        for chunk in normalizer.normalize(chunks):
            yield chunk


def extract_candidate_words(sents, tags=GOODTAGS, **kwargs):
    """
    Extracts key words based on a list of good part of speech tags.
    """
    normalizer  = Normalizer(**kwargs)

    for sent in sents:
        for token, tag in nltk.pos_tag(nltk.wordpunct_tokenize(sent)):
            if tag in tags:
                for token in normalizer.normalize([token]):
                    yield token

##########################################################################
## Key phrase by text scoring mechanisms
##########################################################################

# class Keyphrase

if __name__ == '__main__':
    import os

    PROJECT = os.path.join(os.path.dirname(__file__), "..")
    CORPUS  = os.path.join(PROJECT, "fixtures", "corpus")

    from corpus import BaleenCorpusReader

    corpus  = BaleenCorpusReader(CORPUS)
    cands = candidates(corpus.sents(categories=['data science']), True)

    for idx, cand in enumerate(cands):
        print cand
        if idx > 20: break
