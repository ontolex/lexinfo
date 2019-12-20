from rdflib import Graph, RDF, URIRef, RDFS

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
        "Person": [],
        "ReferentType": [],
        "Tense": [],
        "VerbFormMood": [],
        "Voice": [],
        "TermElement": [],
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
            syn_args.append({
                "id": subj.n3()[(len(LEXINFO)+1):-1],
                "defn": str(next(g.objects(subj, RDFS.comment), "")),
                "range": str(next(g.objects(subj, RDFS.range), LEXINFO))[(len(LEXINFO)):],
                "kind": str(typ)[len(LEXINFO):]
                })
            typed = True
        elif (typ == URIRef(LEMON + "lexicalVariant") or
                typ == URIRef(LEXINFO + "derivedForm") or
                typ == URIRef(LEXINFO + "contractionFor")):
            if typ == URIRef(LEMON + "lexicalVariant"):
                kind = ""
            else:
                kind = str(type)[len(LEXINFO):]
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
                typ == URIRef(LEMON + "senseRelation")):
            if typ == URIRef(LEMON + "senseRelation"):
                kind = ""
            else:
                kind = str(type)[len(LEXINFO):]
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
            values[str(typ)[len(LEXINFO):]].append({
                "id": subj.n3()[(len(LEXINFO)+1):-1],
                "defn": str(next(g.objects(subj, RDFS.comment), ""))
                })
            typed = True



                


            


    if not typed and subj.n3().startswith("<" + LEXINFO):
        print("Could not understand " + subj.n3())

print(syn_args)
