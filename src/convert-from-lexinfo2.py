from rdflib import Graph, RDF, URIRef, RDFS
import csv

g = Graph()
g.parse("lexinfo2.owl")

LEXINFO = "http://www.lexinfo.net/ontology/2.0/lexinfo#"
LEMON = "http://lemon-model.net/lemon#"

ms_props = []
syn_args = []
relations = []
definitions = []
representations = []
values = {
        "Dating": [],
        "Animacy": [],
        "Aspect": [],
        "Case": [],
        "Cliticness": [],
        "Definiteness": [],
        "Degree": [],
        "Finiteness": [],
        "Gender": [],
        "ModificationType": [],
        "Mood": [],
        "Negative": [],
        "Number": [],
        "AdjectivePOS": [],
        "AdpositionPOS": [],
        "AdverbPOS": [],
        "ConjunctionPOS": [],
        "DeterminerPOS": [],
        "ArticlePOS": [],
        "FusedPrepositionPOS": [],
        "NounPOS": [],
        "NumeralPOS": [],
        "ParticlePOS": [],
        "PronounPOS": [],
        "SymbolPOS": [],
        "VerbPOS": [],
        "PartOfSpeech": [],
        "Person": [],
        "ReferentType": [],
        "Tense": [],
        "VerbFormMood": [],
        "Voice": [],
        "TermElement": [],
        "TermType": [],
        "AbbreviatedForm": [],
        "Frequency": [],
        "NormativeAuthorization": [],
        "Register": [],
        "TemporalQualifier": []
        }

subjs = set(g.subjects())

for subj in subjs:
    typed = False
    for typ in g.objects(subj, RDFS.subPropertyOf):
        if (typ == URIRef(LEXINFO + "formCaseVariant") or
                typ == URIRef(LEXINFO + "formDegreeVariant") or
                typ == URIRef(LEXINFO + "formMoodVariant") or
                typ == URIRef(LEXINFO + "formNumberVariant") or
                typ == URIRef(LEXINFO + "formPersonVariant") or
                typ == URIRef(LEXINFO + "formPositivityVariant") or
                typ == URIRef(LEXINFO + "formTenseVariant")):
            pass
        elif (typ == URIRef(LEMON + "synArg") or
                typ == URIRef(LEXINFO + "adjunct") or
                typ == URIRef(LEXINFO + "predicativeAdjunct") or
                typ == URIRef(LEXINFO + "clausalArg") or
                typ == URIRef(LEXINFO + "complement") or
                typ == URIRef(LEXINFO + "copulativeArg") or
                typ == URIRef(LEXINFO + "object") or
                typ == URIRef(LEXINFO + "adpositionalObject") or
                typ == URIRef(LEXINFO + "subject")):
            kind = str(typ)[len(LEXINFO):]
            if str(subj).endswith("copulativeSubject"):
                kind = "copulativeArg,subject"
            syn_args.append({
                "id": subj.n3()[(len(LEXINFO)+1):-1],
                "defn": str(next(g.objects(subj, RDFS.comment), "")),
                "range": str(next(g.objects(subj, RDFS.range), LEXINFO))[(len(LEXINFO)):],
                "kind": kind
                })
            typed = True
        elif (typ == URIRef(LEMON + "lexicalVariant") or
                typ == URIRef(LEXINFO + "derivedForm") or
                typ == URIRef(LEXINFO + "contractionFor")):
            if typ == URIRef(LEMON + "lexicalVariant"):
                kind = ""
            else:
                kind = str(typ)[len(LEXINFO):]
            relations.append({
                "id": subj.n3()[(len(LEXINFO)+1):-1],
                "defn": str(next(g.objects(subj, RDFS.comment), "")),
                "domain": "LexicalEntry",
                "range": "LexicalEntry",
                "kind": kind 
                })
            typed = True
        elif (typ == URIRef(LEMON + "broader") or
                typ == URIRef(LEMON + "equivalent") or
                typ == URIRef(LEMON + "incompatible") or
                typ == URIRef(LEMON + "narrower") or
                typ == URIRef(LEMON + "senseRelation") or
                typ == URIRef(LEXINFO + "partitiveRelation") or
                typ == URIRef(LEXINFO + "holonymTerm") or
                typ == URIRef(LEXINFO + "meronymTerm") or
                typ == URIRef(LEXINFO + "relatedTerm")):
            if typ == URIRef(LEMON + "senseRelation"):
                kind = ""
            else:
                kind = str(typ)[len(LEXINFO):]
            relations.append({
                "id": subj.n3()[(len(LEXINFO)+1):-1],
                "defn": str(next(g.objects(subj, RDFS.comment), "")),
                "domain": "LexicalSense",
                "range": "LexicalSense",
                "kind": kind
                })
            typed = True
        elif (typ == URIRef(LEMON + "definition")):
            definitions.append({
                "id": subj.n3()[(len(LEXINFO)+1):-1],
                "defn": str(next(g.objects(subj, RDFS.comment), ""))
                })
            typed = True
        elif (typ == URIRef(LEXINFO + "morphosyntacticProperty") or
                typ == URIRef(LEMON + "property")):
            ms_props.append({
                "id": subj.n3()[(len(LEXINFO)+1):-1],
                "defn": str(next(g.objects(subj, RDFS.comment), ""))
                })
            typed = True
        elif typ == URIRef(LEMON + "representation"):
            representations.append({
                "id": subj.n3()[(len(LEXINFO)+1):-1],
                "defn": str(next(g.objects(subj, RDFS.comment), ""))
                })
            typed = True
    for typ in g.objects(subj, RDF.type):
        if typ == URIRef('http://www.w3.org/2002/07/owl#Class'):
            typed = True
        elif (str(typ).startswith(LEXINFO) and str(typ)[len(LEXINFO):] in values):
            if str(typ).endswith("POS"):
                kind = str(typ)[len(LEXINFO):-3]
                if str(subj).endswith("Article") or str(subj) == LEXINFO + "article":
                    kind = "Article"
                val_id = subj.n3()[(len(LEXINFO)+1):-1]
                if [x for x in values["PartOfSpeech"] if x["id"] == val_id]:
                    [x for x in values["PartOfSpeech"] if x["id"] == val_id][0]["kind"] = kind
                else:
                    values["PartOfSpeech"].append({
                        "id": val_id,
                        "defn": str(next(g.objects(subj, RDFS.comment), "")),
                        "kind": kind
                        })
            elif str(typ).endswith("AbbreviatedForm"):
                kind = str(typ)[len(LEXINFO):]
                val_id = subj.n3()[(len(LEXINFO)+1):-1]
                if [x for x in values["TermType"] if x["id"] == val_id]:
                    [x for x in values["TermType"] if x["id"] == val_id][0]["kind"] = kind
                else:
                    values["TermType"].append({
                        "id": val_id,
                        "defn": str(next(g.objects(subj, RDFS.comment), "")),
                        "kind": kind
                        })

            else:
                val_id = subj.n3()[(len(LEXINFO)+1):-1]
                if not [x for x in values[str(typ)[len(LEXINFO):]] if x["id"] == val_id]:
                    values[str(typ)[len(LEXINFO):]].append({
                        "id": subj.n3()[(len(LEXINFO)+1):-1],
                        "defn": str(next(g.objects(subj, RDFS.comment), ""))
                        })
            typed = True

    if not typed and subj.n3().startswith("<" + LEXINFO):
        print("Could not understand " + subj.n3())

with open("data/morphosyntactic_properties.csv", "w") as out:
    writer = csv.writer(out)
    writer.writerow(["ID","Definition"])
    ms_props.sort(key=lambda x: x["id"])
    for ms_prop in ms_props:
        if ms_prop["id"] != "morphosyntacticProperty":
            writer.writerow([ms_prop["id"],ms_prop["defn"]])

with open("data/syntactic_arguments.csv", "w") as out:
    writer = csv.writer(out)
    writer.writerow(["ID","Subproperty Of","Definition"])
    syn_args.sort(key=lambda x: x["id"])
    for syn_arg in syn_args:
        writer.writerow([syn_arg["id"],syn_arg["kind"],syn_arg["defn"]])

with open("data/relations.csv", "w") as out:
    writer = csv.writer(out)
    writer.writerow(["ID","Subproperty Of","Target","Definition"])
    relations.sort(key=lambda x: x["id"])
    for rel in relations:
        writer.writerow([rel["id"],rel["kind"],rel["domain"],rel["defn"]])

with open("data/definitions.csv", "w") as out:
    writer = csv.writer(out)
    writer.writerow(["ID","Definition"])
    definitions.sort(key=lambda x: x["id"])
    for defn in definitions:
        writer.writerow([defn["id"],defn["defn"]])

with open("data/representations.csv", "w") as out:
    writer = csv.writer(out)
    writer.writerow(["ID","Definition"])
    representations.sort(key=lambda x: x["id"])
    for rep in representations:
        writer.writerow([rep["id"],rep["defn"]])

for k,v in values.items():
    if len(v) > 0:
        with open("data/values/%s.csv" % k, "w") as out:
            writer = csv.writer(out)
            writer.writerow(["ID","Type","Definition"])
            v.sort(key=lambda x: x["id"])
            for w in v:
                writer.writerow([w["id"],w.get("kind",""),w["defn"]])


