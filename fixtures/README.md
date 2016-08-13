# Baleen Corpora

Minke expects that you store the corpus you're trying to analyze in the fixtures directory of the project during development. However, as the Baleen corpus is rather large, we've obviously not included it on GitHub. Use the link below to download and extract the corpus.

> [Download Latest Baleen Corpus](___) (MD5 ___ )

As of May 25, 2016, the corpus ingested 373 feeds containing 332,571 posts in 13 categories. In order to remove MP3 files from the download, we removed large files and the essays category. The download size is 12.13 GB and the decompressed size is 62.23 GB for 331,515 files.

## Category Counts

- books: 7921 (690.0MiB)
- business: 43420 (5.7GiB)
- cinema: 10544 (925.6MiB)
- cooking: 3230 (322.9MiB)
- data_science: 3812 (243.7MiB)
- design: 5863 (898.2MiB)
- do_it_yourself: 12495 (853.9MiB)
- gaming: 14235 (1.5GiB)
- news: 162937 (34.9GiB)
- politics: 18336 (2.6GiB)
- sports: 24045 (5.9GiB)
- tech: 24662 (3.6GiB)

## Corpus Access Times

The corpus is very large, and you can access it via the `BaleenCorpusReader` class in the `minke.corpus` package. The reader provides several methods to access the content, doing various levels of parsing. There is a hierarchy of access depending on what level you use:

- `docs()`: parses json
- `fields()`: selects specific fields from json
- `html()`: selects content from json
- `paras()`: parses html with BeautifulSoup
- `sents()`: segmentation with Punkt
- `words()`: tokenization with wordpunct

The two major parsing tasks are in `docs()` and `paras()`, though there is overhead to perform tokenization as well. For the current corpus the access times are as follows:

- Scanned ___ docs in ___ seconds (___ minutes, ___ seconds).
- Scanned ___ words in ___ seconds (___ hours ___ minutes ___ seconds)

## Corpus Describe

The following data are complete scans of the corpus that describe the content
and structure of the corpus in a meaningful way.

### Raw JSON/HTML Corpus Scan

Baleen corpus contains 180342 files in 13 categories.

Structured as:

    ___ paragraphs (___ mean paragraphs per file)
    ___ sentences (___ mean sentences per paragraph).

Word count of ___ with a vocabulary of ___ (___ lexical diversity).

Corpus scan took ___ seconds (___ day, ___ hours, ___ minutes ___ seconds).

### Preprocessed Pickle Data Scan



## Corpus MimeTypes

A survey of the corpus mime types revealed the following:


Which leads us to wonder what is in the unknown mimetype field.
