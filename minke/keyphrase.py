# minke.keyphrase
# Extracts keyphrases from the Baleen corpus.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue May 03 13:25:12 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: keyphrase.py [978bbb0] benjamin@bengfort.com $

"""
Extracts keyphrases from the Baleen corpus.
See: http://bdewilde.github.io/blog/2014/09/23/intro-to-automatic-keyphrase-extraction/
"""

##########################################################################
## Imports
##########################################################################

import nltk
import heapq
import gensim

from itertools import groupby
from operator import itemgetter
from nltk.chunk import tree2conlltags
from nltk.chunk.regexp import RegexpParser

from minke.normalize import Normalizer
from minke.normalize import STOPWORDS, PUNCT
from minke.corpus import BaleenPickledCorpusReader

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

    If the sentences are already tokenized and tagged, pass in: tagged=True
    Note: this function expects segmented sentences passed in to the method.
    """
    if chunks:
        return extract_candidate_chunks(sents, grammar, **kwargs)
    return extract_candidate_words(sents, tags, **kwargs)


# Alias for extract_candidates
candidates = extract_candidates


def extract_candidate_chunks(sents, grammar=GRAMMAR, tagged=False, **kwargs):
    """
    Extracts key chunks based on a grammar for a list of tokenized sentences.
    If the sentences are already tokenized and tagged, pass in: tagged=True
    """
    normalizer = Normalizer(**kwargs)
    chunker    = RegexpParser(grammar)

    for sent in sents:
        # Tokenize and tag sentences if necessary
        if not tagged:
            sent = nltk.pos_tag(nltk.wordpunct_tokenize(sent))

        # Parse with the chunker if we have a tagged sentence
        if not sent: continue
        chunks = tree2conlltags(chunker.parse(sent))

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


def extract_candidate_words(sents, tags=GOODTAGS, tagged=False, **kwargs):
    """
    Extracts key words based on a list of good part of speech tags.
    If the sentences are already tokenized and tagged, pass in: tagged=True
    """
    normalizer = Normalizer(**kwargs)

    for sent in sents:
        # Tokenize and tag sentences if necessary
        if not tagged:
            sent = nltk.pos_tag(nltk.wordpunct_tokenize(sent))

        # Identify only good words by their tag
        for token, tag in sent:
            if tag in tags:
                for token in normalizer.normalize([token]):
                    yield token


##########################################################################
## Key phrase by text scoring mechanisms
##########################################################################

class Scorer(object):
    """
    An base class for any key phrase scoring mechanism that we use. Scorers
    wrap a corpus object, and then can be used to get rankings for each
    individual document in the corpus by fileid.
    """

    def __init__(self, corpus):
        self.corpus = corpus

    def score(self, fileids=None, categories=None, chunks=True):
        """
        Fits the scorer to the specified fileids.
        """
        raise NotImplementedError("Subclasses must define scoring.")

    def keyphrases(self, N=20, fileids=None, categories=None):
        """
        Returns the N top key phrases per document.
        """
        raise NotImplementedError("Subclasses must implement rankings.")


class TFIDFScorer(Scorer):
    """
    Uses TF-IDF to score and rank key phrases.
    """

    def __init__(self, corpus):
        super(TFIDFScorer, self).__init__(corpus)
        self.lexicon = None
        self.tfidfs  = None
        self.fileids = None

    def score(self, fileids=None, categories=None, chunks=True):
        """
        Fits the TF-IDF model and creates the lexicon and scores.
        """
        # Resolve the fileids and the categories for doc specific selection.
        self.fileids = self.corpus._resolve(fileids, categories)

        # Determine if we have a tagged corpus or not
        tagged = isinstance(self.corpus, BaleenPickledCorpusReader)

        # Create the lexicon of candidate phrases per document.
        # TODO: generalize the candidate extraction to the scorer.
        self.lexicon = gensim.corpora.Dictionary(
            extract_candidates(
                self.corpus.sents(fileids=fileid), chunks=chunks, tagged=tagged
            ) for fileid in self.fileids
        )

        # Create the vectorized corpus for scoring
        # TODO: How do we not make multiple passes without memory loading?
        vectors     = [
            self.lexicon.doc2bow(
                extract_candidates(
                    self.corpus.sents(fileids=fileid), chunks=chunks, tagged=tagged
                )
            ) for fileid in self.fileids
        ]

        # Fit the TF-IDF model and compute the scores
        model  = gensim.models.TfidfModel(vectors)
        self.tfidfs = model[vectors]

        # Clean up the vectors and the mdoel
        del vectors
        del model

    def keyphrases(self, N=20, fileids=None, categories=None):
        """
        Returns the top N keyphrases grouped by document id.
        TODO: this currently ignores fileids/categories.
        """
        if not self.tfidfs or not self.lexicon or not self.fileids:
            raise ValueError("Must call the score method first!")

        for idx, doc in enumerate(self.tfidfs):
            fileid = self.fileids[idx]

            # Get the top N terms by TF-IDF score
            scores = [
                (self.lexicon[wid], score)
                for wid, score in heapq.nlargest(N, doc, key=itemgetter(1))
            ]

            yield fileid, scores


if __name__ == '__main__':
    import os

    PROJECT = os.path.join(os.path.dirname(__file__), "..")
    CORPUS  = os.path.join(PROJECT, "fixtures", "tagged_corpus")

    from corpus import BaleenPickledCorpusReader

    corpus = BaleenPickledCorpusReader(CORPUS)
    scorer = TFIDFScorer(corpus)
    scorer.score(categories=['data science'])

    for idx, (fileid, scores) in enumerate(scorer.keyphrases()):
        print u"Document '{}' keyphrases:".format(fileid)
        for word, score in scores:
            print u"{:0.3f}: {}".format(score, word)
        print

        if idx > 5: break
