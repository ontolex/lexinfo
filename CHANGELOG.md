# Changelog

All notable changes to LexInfo. Every version is a
[GitHub release](https://github.com/ontolex/lexinfo/releases) and is published,
frozen, at `http://www.lexinfo.net/ontology/<version>/lexinfo`.

## [Unreleased]

### Added

- `lookupForm` term type, for variants that let an entry be found by search (#44, #45)
- IATE normative authorisations `historicalTerm`, `proposedTerm` and `abandonedTerm` (#42, #43)
- `supine` as a value of `mood` (#39, #40)
- Form variant properties for the new mood values: `conditionalMoodForm`, `gerundiveMoodForm`,
  `infinitiveMoodForm`, `participleMoodForm` and `supineMoodForm`
- Collocation metrics used by OntoLex FrAC, as sub-properties of `frac:cScore`: `relFreq`, `pmi`,
  `pmi2`, `pmi3`, `pmiLogFreq`, `dice`, `logDice`, `minSensitivity`, `logLikelihood`, `tScore`,
  `chi2`, `support`, `lift` and `conviction` (#50)
- Segmentation units `tokens`, `types` and `sentences` for `frac:unit` (#50)
- `reliabilityCode` usage with the IATE reliability codes `downgradedReliability`,
  `reliabilityNotVerified`, `minimumReliability`, `reliable` and `veryReliable` (#46)
- `LinguisticCategory`, the superclass of all classes of values, such as `PartOfSpeech` and `Case` (#1)

### Changed

- `verbFormMood` and `mood` are combined into `mood`, and `VerbFormMood` into `Mood` (#39, #40)
- `head` is defined as the syntactic head of a phrase (#41)
- The conceptual relations `relatedTerm`, `holonymTerm`, `meronymTerm` and their sub-properties are
  defined in terms of concepts, and `relatedTerm`, `holonymTerm`, `meronymTerm`, `associativeRelation`
  and `coordinateConcept` are labelled "related", "holonym", "meronym", "association" and
  "cohyponym" (#2)

### Deprecated

- `verbFormMood` and `VerbFormMood`, replaced by `mood` and `Mood`
- `confidence`, replaced by `ontolex:confidence` from the OntoLex core model (#49)

### Release process

- The ontology header now records `owl:versionIRI`, `owl:versionInfo`, `owl:priorVersion` and the
  release date
- Each release is published in RDF/XML, Turtle, N-Triples and JSON-LD, with an HTML overview of
  the classes, properties and values

## [3.0] - 2026-09-29

The first release made with the release workflow, built from commit `a5cba39`. It is the
LexInfo 3.0 that had been published on lexinfo.net (last deployed in September 2023), plus:

### Added

- `BaseType` values for `morph:baseType` from OntoLex-Morph: `aoristStem`, `futureStem`,
  `infinitiveStem`, `obliqueStem`, `pastParticipleStem`, `pastStem`, `perfectStem`,
  `presentStem`, `strongStem`, `thirdStem` and `weakStem` (#47, #48)

[Unreleased]: https://github.com/ontolex/lexinfo/compare/v3.0...HEAD
[3.0]: https://github.com/ontolex/lexinfo/releases/tag/v3.0
