# Baleen Corpora

Minke expects that you store the corpus you're trying to analyze in the fixtures directory of the project during development. However, as the Baleen corpus is rather large, we've obviously not included it on GitHub. Use the link below to download and extract the corpus.

> [Download Latest Baleen Corpus](http://bit.ly/baleen-corpus) (MD5 1d265ab6be866950cb4559ee008da88a)

As of April 19, 2016, the corpus ingested 373 feeds containing 180,342 posts in 13 categories. The download size is 8.1 GB and the decompressed size is 41.54 GB for 180,358 files.

## Category Counts

- politics: 9862 (1.4G, 519M pickled)
- books: 4506 (422M, 330M pickled)
- business: 22646 (2.8G, 607M pickled)
- cinema: 5680 (492M, 1.1G pickled)
- cooking: 1901 (198M, 84M pickled)
- data science: 2696 (160M, 100M pickled)
- design: 3164 (523M, 145M pickled)
- do it yourself: 6736 (480M, 142M pickled)
- essays: 966 (6.1G, N/A pickled)
- gaming: 8160 (865M, 271M pickled)
- news: 88865 (20G, 3.6G pickled)
- sports: 12974 (3.4G, 372M pickled)
- tech: 12186 (1.8G, 392M pickled)

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

The following data are complete scans of the corpus that describe the content
and structure of the corpus in a meaningful way.

### Raw JSON/HTML Corpus Scan

Baleen corpus contains 180342 files in 13 categories.

Structured as:

    27140803 paragraphs (150.496 mean paragraphs per file)
    98296455 sentences (3.622 mean sentences per paragraph).

Word count of 25308866993 with a vocabulary of 14306098 (1769.096 lexical diversity).

Corpus scan took 108546.756 (1 day, 6 hours, 9 minutes) seconds.

### Preprocessed Pickle Data Scan



**NOTE**: Preprocessing took 614 minutes 49.178 seconds before it was killed before using too much memory. It only completed 47,425 out of 180,342 documents (26%). I started the process again for the remaining categories except essays. The second phase took 703 minutes 48.559 seconds and moved the corpus to 179,472 (99.5%). Unfortunately it looks like there is a memory leak in the Essay category that can't be resolved. Whatever the problem is there is probably also in the Cinema category, which somehow gained data.

## Corpus MimeTypes

A survey of the corpus mime types revealed the following:

- unknown: 124550
- text/html: 50487
- text/plain: 5171
- application/xhtml+xml: 134

Which leads us to wonder what is in the unknown mimetype field.
