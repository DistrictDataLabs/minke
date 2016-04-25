# Baleen Corpora

Minke expects that you store the corpus you're trying to analyze in the fixtures directory of the project during development. However, as the Baleen corpus is rather large, we've obviously not included it on GitHub. Use the link below to download and extract the corpus.

> [Download Latest Baleen Corpus](http://bit.ly/baleen-corpus) (MD5 1d265ab6be866950cb4559ee008da88a)

As of April 19, 2016, the corpus ingested 373 feeds containing 180,342 posts in 13 categories. The download size is 8.1 GB and the decompressed size is 41.54 GB for 180,358 files.

## Category Counts

- politics: 9862 (1.4G)
- books: 4506 (422M)
- business: 22646 (2.8G)
- cinema: 5680 (492M)
- cooking: 1901 (198M)
- data science: 2696 (160M)
- design: 3164 (523M)
- do it yourself: 6736 (480M)
- essays: 966 (6.1G)
- gaming: 8160 (865M)
- news: 88865 (20G)
- sports: 12974 (3.4G)
- tech: 12186 (1.8G)

## Corpus Access Times

The corpus is very large, and you can access it via the `BaleenCorpusReader` class in the `minke.corpus` package. The reader provides several methods to access the content, doing various levels of parsing. There is a hierarchy of access depending on what level you use:

- `docs()`: parses json
- `fields()`: selects specific fields from json
- `html()`: selects content from json
- `paras()`: parses html with BeautifulSoup
- `sents()`: segmentation with Punkt
- `words()`: tokenization with wordpunct

The two major parsing tasks are in `docs()` and `paras()`, though there is overhead to perform tokenization as well. For the current corpus the access times are as follows:

- Scanned 180,341 docs in 1040.463 seconds (17 minutes 20.5 seconds).
- Scanned 25,308,866,993 words in 108546.756 seconds (30 hours 9 minutes 6.8 seconds)

## Corpus Describe

Baleen corpus contains 180342 files in 13 categories.

Structured as:

    27140803 paragraphs (150.496 mean paragraphs per file)

    98296455 sentences (3.622 mean sentences per paragraph).

Word count of 25308866993 with a vocabulary of 14306098 (1769.096 lexical diversity).

Corpus scan took 108546.756 seconds.

## Corpus MimeTypes

A survey of the corpus mime types revealed the following:

- unknown: 124550
- text/html: 50487
- text/plain: 5171
- application/xhtml+xml: 134

Which leads us to wonder what is in the unknown mimetype field.
