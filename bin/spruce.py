import os
from minke.corpus import BaleenCorpusReader
from operator import itemgetter

corpus = BaleenCorpusReader("fixtures/corpus")

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

for cat in corpus.categories():
    sizes = list(corpus.sizes(categories=cat))
    docs  = len(sizes)
    total = sum(size[1] for size in sizes)
    print("- {}: {} ({})".format(cat, docs, sizeof_fmt(total)))


docs = len(corpus.fileids())
cats = len(corpus.categories())
size = sum(s[1] for s in corpus.sizes())
print("{} documents in {} categories {}".format(docs, cats, sizeof_fmt(size)))
