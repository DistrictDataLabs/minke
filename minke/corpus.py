# minke.corpus
# Corpus reader and parser object for accessing data on disk.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Apr 19 12:39:13 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: corpus.py [] benjamin@bengfort.com $

"""
Corpus reader and parser object for accessing data on disk.
"""

##########################################################################
## Imports
##########################################################################

import os
import bs4
import time
import json
import nltk
import codecs
import nltk.data

from nltk.tokenize import WordPunctTokenizer
from nltk.corpus.reader.api import CorpusReader
from nltk.corpus.reader.api import CategorizedCorpusReader


##########################################################################
## Module Constants
##########################################################################

DOC_PATTERN = r'(?!\.)[a-z_\s]+/[a-f0-9]+\.json'
CAT_PATTERN = r'([a-z_\s]+)/.*'


##########################################################################
## BaleenCorpusReader
##########################################################################

class BaleenCorpusReader(CategorizedCorpusReader, CorpusReader):

    # Tags to extract as paragraphs from the HTML text
    TAGS = [
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p', 'li'
    ]

    def __init__(self, root, fileids=DOC_PATTERN, tags=None,
                 word_tokenizer=WordPunctTokenizer(),
                 sent_tokenizer=nltk.data.LazyLoader(
                    'tokenizers/punkt/english.pickle'),
                 encoding='utf8', **kwargs):
        """
        Initialize the corpus reader.  Categorization arguments
        (``cat_pattern``, ``cat_map``, and ``cat_file``) are passed to
        the ``CategorizedCorpusReader`` constructor.  The remaining arguments
        are passed to the ``CorpusReader`` constructor.
        """
        # Add the default category pattern if not passed into the class.
        if not any(key.startswith('cat_') for key in kwargs.keys()):
            kwargs['cat_pattern'] = CAT_PATTERN

        CategorizedCorpusReader.__init__(self, kwargs)
        CorpusReader.__init__(self, root, fileids, encoding)

        self._word_tokenizer = word_tokenizer
        self._sent_tokenizer = sent_tokenizer
        self._good_tags = tags or self.TAGS

    def _resolve(self, fileids, categories):
        """
        Returns a list of fileids or categories depending on what is passed
        to each internal corpus reader function. This primarily bubbles up to
        the high level ``docs`` method, but is implemented here similar to
        the nltk ``CategorizedPlaintextCorpusReader``.
        """
        if fileids is not None and categories is not None:
            raise ValueError("Specify fileids or categories, not both")

        if categories is not None:
            return self.fileids(categories)
        return fileids

    def docs(self, fileids=None, categories=None):
        """
        Returns the complete JSON document for every file in the corpus.
        Note that I attempted to use the nltk ``CorpusView`` and ``concat``
        methods here, but was not getting memory safe iteration. Instead the
        simple Python generator by far did a better job of ensuring that file
        handles got closed and that not all data was loaded into memory at a
        time. In the future, I will try to re-implement the corpus view.
        """
        # Resolve the fileids and the categories
        fileids = self._resolve(fileids, categories)

        # Create a generator, loading one document into memory at a time.
        for path, enc, fileid in self.abspaths(fileids, True, True):
            with codecs.open(path, 'r', encoding=enc) as f:
                yield json.load(f)

    def fields(self, fields, fileids=None, categories=None):
        """
        Helper function to extract particular fields from the json documents.
        Fields can be a string or an iterable of fields. If just one field is
        passed in, then the values are returned, otherwise dictionaries of
        the requsted fields are returned.

        This method doesn't raise KeyErrors nor does it yield None values if
        the document doesn't contain a particular field.

        For example to get title and pubdate from the documents:

            corpus.fields(['title', 'pubdate'])

        Or to simply get all of the summaries:

            corpus.fields('summary')

        Note: there is not yet support for nested fields.
        """
        if isinstance(fields, basestring):
            fields = [fields,]

        if len(fields) == 1:
            for doc in self.docs(fileids, categories):
                if fields[0] in doc:
                    yield doc[fields[0]]

        else:
            for doc in self.docs(fileids, categories):
                yield {
                    key: doc.get(key, None)
                    for key in fields
                }

    def html(self, fileids=None, categories=None):
        """
        Returns the HTML content from each JSON document for every file in
        the corpus, ensuring that it exists. Note, this simply returns the
        HTML strings, it doesn't perform any parsing of the HTML.
        """
        return self.fields('content', fileids, categories)

    def paras(self, fileids=None, categories=None):
        """
        Uses BeautifulSoup to parse the paragraphs from the HTML.
        Currently, this just sends raw text, it does not do any segmentation
        or tokenization as the standard NLTK CorpusReader objects do.
        """
        for html in self.html(fileids, categories):
            soup = bs4.BeautifulSoup(html, 'lxml')
            for element in soup.find_all(self._good_tags):
                yield element.text

    def sents(self, fileids=None, categories=None):
        """
        Uses the built in sentence tokenizer to extract sentences from the
        paragraphs. Note that this method uses BeautifulSoup to parse HTML.
        """
        for paragraph in self.paras(fileids, categories):
            for sentence in self._sent_tokenizer.tokenize(paragraph):
                yield sentence

    def words(self, fileids=None, categories=None):
        """
        Uses the built in word tokenizer to extract tokens from sentences.
        Note that this method uses BeautifulSoup to parse HTML content.
        """
        for sentence in self.sents(fileids, categories):
            for token in self._word_tokenizer.tokenize(sentence):
                yield token

    def sizes(self, fileids=None, categories=None):
        """
        Returns a list of tuples, the fileid and the size on disk of the file.
        This function is used to detect oddly large files in the corpus.
        """
        # Resolve the fileids and the categories
        fileids = self._resolve(fileids, categories)

        # Create a generator, getting every path and computing filesize
        for path, enc, fileid in self.abspaths(fileids, True, True):
            yield fileid, os.path.getsize(path)

    def describe(self, fileids=None, categories=None):
        """
        Performs a single pass of the corpus and returns a dictionary with a
        variety of metrics concerning the state of the corpus.
        """
        # Structures to perform counting.
        counts  = nltk.FreqDist()
        tokens  = nltk.FreqDist()
        started = time.time()

        # Perform single pass over paragraphs, tokenize and count
        for para in self.paras(fileids, categories):
            counts['paras'] += 1

            for sent in self._sent_tokenizer.tokenize(para):
                counts['sents'] += 1

                for word in self._word_tokenizer.tokenize(sent):
                    counts['words'] += 1
                    tokens[word] += 1

        # Compute the number of files and categories in the corpus
        n_fileids = len(self._resolve(fileids, categories) or self.fileids())
        n_topics  = len(self.categories(self._resolve(fileids, categories)))

        # Return data structure with information
        return {
            'files':  n_fileids,
            'topics': n_topics,
            'paras':  counts['paras'],
            'sents':  counts['sents'],
            'words':  counts['words'],
            'vocab':  len(tokens),
            'lexdiv': float(counts['words']) / float(len(tokens)),
            'ppdoc':  float(counts['paras']) / float(n_fileids),
            'sppar':  float(counts['sents']) / float(counts['paras']),
            'secs':   time.time() - started,
        }

    def describes(self, fileids=None, categories=None):
        """
        Returns a string representation of the describe command.
        """
        return (
            "Baleen corpus contains {files} files in {topics} categories.\n"
            "Structured as:\n"
            "    {paras} paragraphs ({ppdoc:0.3f} mean paragraphs per file)\n"
            "    {sents} sentences ({sppar:0.3f} mean sentences per paragraph).\n"
            "Word count of {words} with a vocabulary of {vocab} "
            "({lexdiv:0.3f} lexical diversity).\n"
            "Corpus scan took {secs:0.3f} seconds."
        ).format(**self.describe(fileids, categories))
