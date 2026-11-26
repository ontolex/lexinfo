# LexInfo

LexInfo is the data category ontology for 
[OntoLex-Lemon](https://www.w3.org/2016/05/ontolex/), which provides description
of lexicographic resources in RDF relative to ontologies

## Installing

Set up the Python environment as follows

    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt

For subsequent usages rerun the following command

    source env/bin/activate

## Building

The ontology can be built with the following command, which prints a
development build in RDF/XML

    python src/build-ontology.py

To write all formats (RDF/XML, Turtle, N-Triples and JSON-LD) for a given
version, plus an HTML overview of the classes, properties and values

    python src/build-ontology.py --version 3.1 --prior 3.0 -o build/3.1
    python src/make-docs.py build/3.1/lexinfo.ttl build/3.1/index.html

Before opening a pull request, run the checks that CI runs

    python src/check-release.py --base origin/master

## Versions

Every version of LexInfo is a [GitHub release](https://github.com/ontolex/lexinfo/releases)
and is published on lexinfo.net under its own path, which never changes after
release:

| URL | Contents |
| --- | --- |
| `http://www.lexinfo.net/ontology/3.0/lexinfo` | LexInfo 3.0, frozen |
| `http://www.lexinfo.net/ontology/3.1/lexinfo` | LexInfo 3.1, frozen |
| `http://www.lexinfo.net/ontology/latest/lexinfo` | the most recent release |

Each file is available as `lexinfo.owl`, `lexinfo.ttl`, `lexinfo.nt` and
`lexinfo.jsonld`, and `index.html` documents the release.

All 3.x releases share the namespace `http://www.lexinfo.net/ontology/3.0/lexinfo#`
and the ontology IRI `http://www.lexinfo.net/ontology/3.0/lexinfo`; each release
is identified by its `owl:versionIRI` (e.g. `http://www.lexinfo.net/ontology/3.1/lexinfo`)
and links to the release before it with `owl:priorVersion`. As the namespace
resolves to the frozen 3.0 file, terms added after 3.0 are only defined in the
later versioned files and in `latest`.

Within 3.x, changes are backwards compatible: terms may be added, and
definitions improved, but no term is removed or renamed. A term that should no
longer be used is marked `owl:deprecated true`, with `dct:isReplacedBy` its
replacement where there is one. CI enforces this against the latest release.
Removing terms requires a new major version with a new namespace.

Changes are listed in [CHANGELOG.md](CHANGELOG.md).

## Releasing

1. Move the "Unreleased" section of `CHANGELOG.md` to a new version heading,
   e.g. `## [3.2] - 2027-03-01`, and merge this into `master`.
2. Tag the release and push the tag

        git tag -a v3.2 -m "LexInfo 3.2"
        git push origin v3.2

3. The [release workflow](.github/workflows/release.yml) builds the release,
   creates the GitHub release with the built files attached and opens a pull
   request `release/3.2` that adds `docs/ontology/3.2/` and updates
   `docs/ontology/latest/`.
4. Merge that pull request. GitHub Pages then publishes it on lexinfo.net.

The published directories under `docs/ontology/` must never be edited by hand;
CI rejects pull requests that change them.

## Editing

The ontology is generated from a selection of CSV and Turtle files:

### Morphosyntactic Properties

The list of the morphosyntactic properties is available in `data/morphosyntactic_properties.csv`.
The values for each of these properties are listed in individual CSV files in 
the `data/values` folder. Each file defines a class of values (e.g. `Case` for
`data/values/Case.csv`), which is a subclass of `lexinfo:LinguisticCategory`.

### Definitions

Properties for defining entries are listed in `data/definitions.csv`. These are
datatype properties whose range is assumed to be a lang-tagged literal.

### Representations

The representations are listed in `data/representations.csv`. These can be used
in place of the default `writtenRep` and `phoneticRep` properties in OntoLex

### Usages

The usages give usage restrictions on a sense and are listed in `data/usages.csv`.

### Collocation Metrics

The collocation metrics are listed in `data/collocation_metrics.csv` (ID, label
and definition). They are datatype properties and sub-properties of the
collocation score property (`frac:cScore`) of the OntoLex module for Frequency,
Attestation and Corpus Information (FrAC).

### Arguments and Frames

These extend the synsem module of OntoLex

The arguments are listed in the file `data/syntactic_arguments.csv`, some extra
information about the arguments is added in the file `data/args.ttl`.

The frames are lists in the file `data/frames.csv` and further definition is
given in Turtle in `data/frames.ttl`. In addition, examples of the frames are
list in `data/frame_examples.csv`

### Relations

Relations extend the vartrans module of OntoLex

The relations are listed in the file `data/relations.csv`. The optional
`Label` column gives the English label where it differs from the one derived
from the ID (e.g. "holonym" for `holonymTerm`).


