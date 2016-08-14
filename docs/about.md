# About     

The [Baleen](https://github.com/bbengfort/baleen) ingestion tool is used to create a corpus of web articles and blogs from RSS feeds. Minke extends Baleen with a library to perform text analysis and perform graph extraction on the exported corpora.

Baleen means &ldquo;whale bone&rdquo; and particularly refers to the straining bones that whales of the mysticeti suborder have. These bones filter food from water as the Baleen ingestion engine filters content from the web. [Minke whales](https://en.wikipedia.org/wiki/Minke_whale) are a specific species of [rorqual whales](https://seaworld.org/Animal-Info/Animal-InfoBooks/Baleen-Whales/Scientific-Classification), one of the shortest in fact. This library is named to indicate it's a short version of the larger Baleen codebase.

## Contributing

Minke is open source, and I'd love your help. If you would like to contribute, you can do so in the following ways:

1. Add issues or bugs to the bug tracker: [https://github.com/bbengfort/minke/issues](https://github.com/bbengfort/minke/issues)
2. Work on a card on the dev board: [https://waffle.io/bbengfort/minke](https://waffle.io/bbengfort/minke)
3. Create a pull request in Github: [https://github.com/bbengfort/minke/pulls](https://github.com/bbengfort/minke/pulls)

Note that labels in the Github issues are defined in the blog post: [How we use labels on GitHub Issues at Mediocre Laboratories](https://mediocre.com/forum/topics/how-we-use-labels-on-github-issues-at-mediocre-laboratories).

If you are a member of the District Data Labs Faculty group, you have direct access to the repository, which is set up in a typical production/release/development cycle as described in _[A Successful Git Branching Model](http://nvie.com/posts/a-successful-git-branching-model/)_. A typical workflow is as follows:

1. Select a card from the [dev board](https://waffle.io/bbengfort/minke) - preferably one that is "ready" then move it to "in-progress".

2. Create a branch off of develop called "feature-[feature name]", work and commit into that branch.

        ~$ git checkout -b feature-myfeature develop

3. Once you are done working (and everything is tested) merge your feature into develop.

        ~$ git checkout develop
        ~$ git merge --no-ff feature-myfeature
        ~$ git branch -d feature-myfeature
        ~$ git push origin develop

4. Repeat. Releases will be routinely pushed into master via release branches, then deployed to the server.

## Contributors

Thank you for all your help contributing to make Minke and Baleen great projects!

### Maintainers

- Benjamin Bengfort: [@bbengfort](https://github.com/bbengfort/)

### Contributors

_Be the first to have your name listed here!_

## Changelog

The release versions that are sent to the Python package index (PyPI) are also tagged in Github. You can see the tags through the Github web application and download the tarball of the version you'd like. Additionally PyPI will host the various releases of Minke (eventually).

The versioning uses a three part version system, "a.b.c" - "a" represents a major release that may not be backwards compatible. "b" is incremented on minor releases that may contain extra features, but are backwards compatible. "c" releases are bug fixes or other micro changes that developers should feel free to immediately update to.

### Version 0.1

* **tag**: [v0.1](https://github.com/bbengfort/minke/releases/tag/v0.1)
* **deployment**: August 12, 2016
* **commit**: [e41e858](https://github.com/bbengfort/minke/commit/e41e8583f1386dbad5249aad740343c984832f1e)

This is the initial release for Minke that provides preprocessing support for raw HTML/JSON exports from Baleen. This version provides `CorpusReader` subclasses for reading a Baleen corpus while engaging NLTK preprocessing techniques. Further a transformer has been created to preprocess the original corpus into a pickled, preprocessed corpus for faster loading and reading. Preprocessing has been operationalized with a console utility (that also has stub commands for sampling and description) that provides progress indication, start and restart commands, as well as multiprocessing to speed things up.
