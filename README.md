# LexInfo

LexInfo is the data category ontology for 
[OntoLex-Lemon](https://www.w3.org/2016/05/ontolex/), which provides description
of lexicographic resources in RDF relative to ontologies

## Building

The ontology can be built with the following command

    python src/build-ontology.py

The most recent ontology is available at `ontology/3.0/lexinfo.owl`

## Editing

The ontology is generated from a selection of CSV and Turtle files:

### Morphosyntactic Properties

The list of the morphosyntactic properties is available in `data/morphosyntactic_properties.csv`.
The values for each of these properties are listed in individual CSV files in 
the `data/values` folder.

### Definitions

Properties for defining entries are listed in `data/definitions.csv`. These are
datatype properties whose range is assumed to be a lang-tagged literal.

### Representations

The representations are listed in `data/representations.csv`. These can be used
in place of the default `writtenRep` and `phoneticRep` properties in OntoLex

### Usages

The usages give usage restrictions on a sense and are listed in `data/usages.csv`.

### Arguments and Frames

These extend the synsem module of OntoLex

The arguments are listed in the file `data/syntactic_arguments.csv`, some extra
information about the arguments is added in the file `data/args.ttl`.

The frames are lists in the file `data/frames.csv` and further definition is
given in Turtle in `data/frames.ttl`. In addition, examples of the frames are
list in `data/frame_examples.csv`

### Relations

Relations extend the vartrans module of OntoLex

The relations are listed in the file `data/relations.csv`


