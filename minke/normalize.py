# minke.normalize
# Utilities and helpers for cleaning and normalizing text data.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue May 03 14:19:14 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: normalize.py [] benjamin@bengfort.com $

"""
Utilities and helpers for cleaning and normalizing text data.
"""

##########################################################################
## Imports
##########################################################################

import nltk
import string

from nltk.corpus import wordnet as wn


##########################################################################
## Module Constants
##########################################################################

PUNCT     = set(string.punctuation)
STOPWORDS = set(nltk.corpus.stopwords.words('english'))


##########################################################################
## Lemmatizer
##########################################################################

class Lemmatizer(object):
    """
    Wraps the nltk.WordNetLemmatizer to provide added functionality like the
    discovery of the part of speech of the word to lemmatize.
    """

    def __init__(self):
        self._wordnet = nltk.WordNetLemmatizer()
        self._cache   = {}

    def tagwn(self, tag):
        """
        Returns the WordNet tag from the Penn Treebank tag.
        """

        return {
            'N': wn.NOUN,
            'V': wn.VERB,
            'R': wn.ADV,
            'J': wn.ADJ
        }[tag[0]]

    def poswn(self, word):
        """
        Computes the part of speech for the given word.
        """
        return self.tagwn(nltk.pos_tag([word])[0][1])

    def lemmatize(self, word, tag=None):
        """
        Lemmatizes the word; if no tag is given, then computes the tag.
        """
        if (word, tag) in self._cache:
            return self._cache[(word, tag)]

        tag   = self.tagwn(tag) if tag else self.poswn(word)
        lemma = self._wordnet.lemmatize(word, tag)

        self._cache[(word, tag)] = lemma
        return lemma

##########################################################################
## Normalizer
##########################################################################

class Normalizer(object):
    """
    Performs normalization of text by applying string operations (lowercase),
    excluding stopwords and punctuation, and by lemmatizing words.
    """

    def __init__(self, stopwords=STOPWORDS, punctuation=PUNCT,
                 lemmatize=True, lower=True, strip=True):
        self.stopwords = stopwords
        self.punct = punctuation
        self.lemmatize = lemmatize
        self.lower = lower
        self.strip = strip

        # Initialize lemmatizer
        self.lemmatizer = Lemmatizer() if self.lemmatize else None

    def normalize(self, words):
        """
        Normalizes a list of words.
        """
        # Add part of speech tags to the words
        words = nltk.pos_tag(words)

        for word, tag in words:
            if self.lower: word = word.lower()
            if self.strip: word = word.strip()

            if word not in self.stopwords:
                if not all(c in self.punct for c in word):
                    if self.lemmatize:
                        word = self.lemmatizer.lemmatize(word, tag)

                    yield word

    def tokenize(self, text):
        """
        Performs tokenization in addition to normalization.
        """
        return self.normalize(nltk.wordpunct_tokenize(text))


if __name__ == '__main__':
    norm = Normalizer()
    print list(norm.tokenize((
        'Sometimes, technically minded people feel they are not'
        ' good candidates for leadership positions.'
    )))
