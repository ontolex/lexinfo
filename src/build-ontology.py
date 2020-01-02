"""
Generates the LexInfo Ontology from the relevant CSV and Turtle Fragments
"""
from rdflib import Graph, RDF, RDFS, OWL, Literal, Namespace, BNode
import csv
import re
import sys
from glob import glob

g = Graph()

# Define namespaces
lexinfo = Namespace("http://www.lexinfo.net/ontology/3.0/lexinfo#")
ontolex = Namespace("http://www.w3.org/ns/lemon/ontolex#")
synsem = Namespace("http://www.w3.org/ns/lemon/synsem#")
vartrans = Namespace("http://www.w3.org/ns/lemon/vartrans#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
g.namespace_manager.bind("owl", OWL)
g.namespace_manager.bind("lexinfo", lexinfo)
g.namespace_manager.bind("ontolex", ontolex)
g.namespace_manager.bind("synsem", synsem)
g.namespace_manager.bind("vartrans", vartrans)
g.namespace_manager.bind("skos", SKOS)

def decamelcase(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1).lower()

with open("data/definitions.csv") as inp:
    reader = csv.reader(inp)
    next(reader)
    for row in reader:
        g.add((lexinfo[row[0]], RDF.type, OWL.ObjectProperty))
        g.add((lexinfo[row[0]], RDFS.label, Literal(decamelcase(row[0]), lang="en")))
        g.add((lexinfo[row[0]], RDFS.comment, Literal(row[1], lang="en")))
        g.add((lexinfo[row[0]], RDFS.subPropertyOf, SKOS.definition))

with open("data/frame_examples.csv") as inp:
    reader = csv.reader(inp)
    next(reader)
    for row in reader:
        g.add((lexinfo[row[0]], lexinfo.example, Literal(row[2], lang=row[1])))

with open("data/frames.csv") as inp:
    reader = csv.reader(inp)
    next(reader)
    for row in reader:
        g.add((lexinfo[row[0]], RDF.type, OWL.Class))
        g.add((lexinfo[row[0]], RDFS.label, Literal(decamelcase(row[0]), lang="en")))
        if row[1]:
            g.add((lexinfo[row[0]], RDFS.subClassOf, lexinfo[row[1]]))
        else:
            g.add((lexinfo[row[0]], RDFS.subClassOf, synsem.SyntacticFrame))
        if row[2]:
            g.add((lexinfo[row[0]], RDFS.comment, Literal(row[2], lang="en")))

g.parse("data/frames.ttl", format="turtle")
g.parse("data/misc.ttl", format="turtle")
g.parse("data/args.ttl", format="turtle")

with open("data/morphosyntactic_properties.csv") as inp:
    reader = csv.reader(inp)
    next(reader)
    for row in reader:
        g.add((lexinfo[row[0]], RDF.type, OWL.ObjectProperty))
        g.add((lexinfo[row[0]], RDFS.label, Literal(decamelcase(row[0]), lang="en")))
        if row[1]:
            g.add((lexinfo[row[0]], RDFS.comment, Literal(row[1], lang="en")))
        g.add((lexinfo[row[0]], RDFS.subPropertyOf, lexinfo.morphosyntacticProperty))

with open("data/relations.csv") as inp:
    reader = csv.reader(inp)
    next(reader)
    for row in reader:
        g.add((lexinfo[row[0]], RDF.type, OWL.ObjectProperty))
        g.add((lexinfo[row[0]], RDFS.label, Literal(decamelcase(row[0]), lang="en")))
        if row[1]:
            g.add((lexinfo[row[0]], RDFS.subPropertyOf, lexinfo[row[1]]))
        elif row[2] == "LexicalEntry":
            g.add((lexinfo[row[0]], RDFS.subPropertyOf, vartrans.lexicalRel))
        elif row[2] == "LexicalSense":
            g.add((lexinfo[row[0]], RDFS.subPropertyOf, vartrans.senseRel))
        if row[2]:
            g.add((lexinfo[row[0]], RDFS.domain, ontolex[row[2]]))
            g.add((lexinfo[row[0]], RDFS.range, ontolex[row[2]]))
        if row[3]:
            g.add((lexinfo[row[0]], RDFS.comment, Literal(row[3], lang="en")))

with open("data/representations.csv") as inp:
    reader = csv.reader(inp)
    next(reader)
    for row in reader:
        g.add((lexinfo[row[0]], RDF.type, OWL.DatatypeProperty))
        g.add((lexinfo[row[0]], RDFS.label, Literal(decamelcase(row[0]), lang="en")))
        g.add((lexinfo[row[0]], RDFS.subPropertyOf, ontolex.representation))
        if row[1]:
            g.add((lexinfo[row[0]], RDFS.comment, Literal(row[1], lang="en")))


with open("data/syntactic_arguments.csv") as inp:
    reader = csv.reader(inp)
    next(reader)
    for row in reader:
        classid = row[0][0].upper() + row[0][1:]
        g.add((lexinfo[row[0]], RDF.type, OWL.ObjectProperty))
        g.add((lexinfo[row[0]], RDFS.label, Literal(decamelcase(row[0]), lang="en")))
        g.add((lexinfo[classid], RDFS.label, Literal(decamelcase(row[0]), lang="en")))
        g.add((lexinfo[row[0]], RDFS.subPropertyOf, synsem.synArg))
        if row[1]:
            for t in row[1].split(","):
                g.add((lexinfo[row[0]], RDFS.subPropertyOf, lexinfo[t]))
                g.add((lexinfo[classid], RDFS.subClassOf, lexinfo[t[0].upper() + t[1:]]))
        else:
            g.add((lexinfo[row[0]], RDFS.subPropertyOf, synsem.synArg))
            g.add((lexinfo[classid], RDFS.subClassOf, synsem.SyntacticArgument))
        if row[2]:
            g.add((lexinfo[row[0]], RDFS.comment, Literal(row[2], lang="en")))
            g.add((lexinfo[classid], RDFS.comment, Literal(row[2], lang="en")))

with open("data/usages.csv") as inp:
    reader = csv.reader(inp)
    next(reader)
    for row in reader:
        g.add((lexinfo[row[0]], RDF.type, OWL.ObjectProperty))
        g.add((lexinfo[row[0]], RDFS.label, Literal(decamelcase(row[0]), lang="en")))
        if row[1]:
            g.add((lexinfo[row[0]], RDFS.comment, Literal(row[1], lang="en")))
        g.add((lexinfo[row[0]], RDFS.subPropertyOf, ontolex.usage))

non_leaf_poses = set()
pos_types = set()

for f in glob("data/values/*.csv"):
    classname = f[12:-4]
    with open(f) as inp:
        reader = csv.reader(inp)
        next(reader)
        for row in reader:
            g.add((lexinfo[row[0]], RDF.type, OWL.Thing))
            g.add((lexinfo[row[0]], RDFS.label, Literal(decamelcase(row[0]), lang="en")))
            g.add((lexinfo[row[0]], RDF.type, lexinfo[classname]))
            if row[1] and classname != "PartOfSpeech":
                g.add((lexinfo[row[0]], RDF.type, lexinfo[row[1]]))
            if row[2]:
                g.add((lexinfo[row[0]], RDFS.comment, Literal(row[2], lang="en")))
            if classname == "PartOfSpeech":
                if row[1]:
                    non_leaf_poses.add(row[1])
                pos_types.add(row[0])

with open("data/values/PartOfSpeech.csv") as inp:
    reader = csv.reader(inp)
    next(reader)
    for row in reader:
        classid = row[0][0].upper() + row[0][1:]
        g.add((lexinfo[classid], RDF.type, OWL.Class))
        g.add((lexinfo[classid], RDFS.label, Literal(decamelcase(row[0]), lang="en")))
        if row[1] == classid or row[1] == "":
            g.add((lexinfo[classid], RDFS.subClassOf, ontolex.Word))
        else:
            g.add((lexinfo[classid], RDFS.subClassOf, lexinfo[row[1]]))
        if classid in non_leaf_poses:
            g.add((lexinfo[classid + "POS"], RDF.type, OWL.Class))
            g.add((lexinfo[classid + "POS"], RDFS.label, Literal(decamelcase(row[0]), lang="en")))
            if row[1] == classid:
                g.add((lexinfo[classid + "POS"], RDFS.subClassOf, lexinfo.PartOfSpeech))
            elif row[1]:
                g.add((lexinfo[classid + "POS"], RDFS.subClassOf, lexinfo[row[1] + "POS"]))
            b = BNode()
            g.add((lexinfo[classid], OWL.equivalentClass, b))
            g.add((b, RDF.type, OWL.Restriction))
            g.add((b, OWL.onProperty, lexinfo.partOfSpeech))
            g.add((b, OWL.someValuesFrom, lexinfo[classid + "POS"]))
        else:
            b = BNode()
            g.add((lexinfo[classid], OWL.equivalentClass, b))
            g.add((b, RDF.type, OWL.Restriction))
            g.add((b, OWL.onProperty, lexinfo.partOfSpeech))
            g.add((b, OWL.hasValue, lexinfo[row[0]]))

sys.stdout.buffer.write(g.serialize(format="pretty-xml"))

