# minke.preprocess
# Converts a raw text corpus into a part of speech tokenized corpus.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed May 04 15:46:02 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: preprocess.py [] benjamin@bengfort.com $

"""
Converts a raw text corpus into a part of speech tokenized corpus.
"""

##########################################################################
## Imports
##########################################################################

import os
import nltk
import shutil
import pickle

##########################################################################
## Preprocessor
##########################################################################

class Preprocessor(object):
    """
    The preprocessor wraps a corpus object (usually a `BaleenCorpusReader`)
    and manages the stateful tokenization and part of speech tagging into a
    directory that is stored in a format that can be read by the
    `BaleenPickledCorpusReader`. This format is more compact and necessarily
    removes a variety of fields from the document that are stored in the JSON
    representation dumped from the Mongo database. This format however is more
    easily accessed for common parsing activity.
    """

    def __init__(self, corpus, target=None):
        """
        The corpus is the `BaleenCorpusReader` to preprocess and pickle.
        The target is the directory on disk to output the pickled corpus to.
        """
        self.corpus = corpus
        self.target = target

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, path):
        if path is not None:
            # Normalize the path and make it absolute
            path = os.path.expanduser(path)
            path = os.path.expandvars(path)
            path = os.path.abspath(path)

            if os.path.exists(path):
                if not os.path.isdir(path):
                    raise ValueError(
                        "Please supply a directory to write preprocessed data to."
                    )

        self._target = path

    def fileids(self, fileids=None, categories=None):
        """
        Helper function access the fileids of the corpus
        """
        fileids = self.corpus._resolve(fileids, categories)
        if fileids:
            return fileids
        return self.corpus.fileids()

    def abspath(self, fileid):
        """
        Returns the absolute path to the target fileid from the corpus fileid.
        """
        # Find the directory, relative from the corpus root.
        parent = os.path.relpath(
            os.path.dirname(self.corpus.abspath(fileid)), corpus.root
        )

        # Compute the name parts to reconstruct
        basename  = os.path.basename(fileid)
        name, ext = os.path.splitext(basename)

        # Create the pickle file extension
        basename  = name + '.pickle'

        # Return the path to the file relative to the target.
        return os.path.normpath(os.path.join(self.target, parent, basename))

    def tokenize(self, fileid):
        """
        Segments, tokenizes, and tags a document in the corpus. Returns a
        generator of paragraphs, which are lists of sentences, which in turn
        are lists of part of speech tagged words.
        """
        for paragraph in self.corpus.paras(fileids=fileid):
            yield [
                nltk.pos_tag(nltk.wordpunct_tokenize(sent))
                for sent in nltk.sent_tokenize(paragraph)
            ]

    def process(self, fileid):
        """
        For a single file does the following preprocessing work:

            1. Checks the location on disk to make sure no errors occur.
            2. Gets all paragraphs for the given text.
            3. Segements the paragraphs with the sent_tokenizer
            4. Tokenizes the sentences with the wordpunct_tokenizer
            5. Tags the sentences using the default pos_tagger
            6. Writes the document as a pickle to the target location.

        This method is called multiple times from the transform runner.
        """
        # Compute the outpath to write the file to.
        target = self.abspath(fileid)
        parent = os.path.dirname(target)

        # Make sure the directory exists
        if not os.path.exists(parent):
            os.makedirs(parent)

        # Make sure that the parent is a directory and not a file
        if not os.path.isdir(parent):
            raise ValueError(
                "Please supply a directory to write preprocessed data to."
            )

        # Ensure that we are not overwriting existing data
        if os.path.exists(target):
            raise ValueError(
                "Path at '{}' already exists!".format(target)
            )

        # Create a data structure for the pickle
        document = list(self.tokenize(fileid))

        # Open and serialize the pickle to disk
        with open(target, 'wb') as f:
            pickle.dump(document, f, pickle.HIGHEST_PROTOCOL)

        # Clean up the document
        del document

        # Return the target fileid
        return target

    def transform(self, fileids=None, categories=None, target=None):
        """
        Transform the wrapped corpus, writing out the segmented, tokenized,
        and part of speech tagged corpus as a pickle to the target directory.

        This method will also directly copy files that are in the corpus.root
        directory that are not matched by the corpus.fileids()
        """
        # Add the new target directory
        if target: self.target = target

        # Make the target directory if it doesn't already exist
        if not os.path.exists(self.target):
            os.makedirs(self.target)

        # First shutil.copy anything in the root directory.
        names = [
            name  for name in os.listdir(self.corpus.root)
            if not name.startswith('.')
        ]

        # Filter out directories and copy files
        for name in names:
            source = os.path.abspath(os.path.join(self.corpus.root, name))
            target = os.path.abspath(os.path.join(self.target, name))

            if os.path.isfile(source):
                shutil.copy(source, target)

        # Resolve the fileids to start processing
        fileids = self.fileids(fileids, categories)
        return map(self.process, fileids)


if __name__ == '__main__':

    PROJECT = os.path.join(os.path.dirname(__file__), "..")
    CORPUS  = os.path.join(PROJECT, "fixtures", "sample")
    TARGET  = os.path.join(PROJECT, "fixtures", "tagged")

    from corpus import BaleenCorpusReader

    corpus = BaleenCorpusReader(CORPUS)
    transformer = Preprocessor(corpus, TARGET)
    docs = transformer.transform()
    print(len(list(docs)))
