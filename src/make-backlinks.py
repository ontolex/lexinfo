"""
Generates all the backlinks to LexInfo v2 from the original ontology and the files
"""
from rdflib import Graph
import csv
from glob import glob

g = Graph()
g.parse("lexinfo2.owl")

LEXINFO_v2 = "http://www.lexinfo.net/ontology/2.0/lexinfo#"
LEXINFO_v3 = "http://www.lexinfo.net/ontology/3.0/lexinfo#"

v2_subjs = set(s.n3()[45:-1] for s in g.subjects() if s.n3()[1:].startswith(LEXINFO_v2))

v3_subjs = set()

form_variants = set()

for f in ["definitions","frame_examples","frames","morphosyntactic_properties","relations","representations","syntactic_arguments","usages"]:
    with open("data/" + f + ".csv") as inp:
        reader = csv.reader(inp)
        next(reader)
        for row in reader:
            v3_subjs.add(row[0])
            if f == "morphosyntactic_properties" and row[2] == "Yes":
                prop_name = "form%s%sVariant" % (row[0][0].upper(), row[0][1:])
                v3_subjs.add(prop_name)
                form_variants.add(row[0].lower())
            if f == "syntactic_arguments":
                classid = row[0][0].upper() + row[0][1:]
                v3_subjs.add(classid)

non_leaf_poses = set()

for f in glob("data/values/*.csv"):
    classname = f[12:-4]
    v3_subjs.add(classname)
    with open(f) as inp:
        reader = csv.reader(inp)
        next(reader)
        for row in reader:
            v3_subjs.add(row[0])
            if classname.lower() in form_variants:
                if row[0].endswith(classname):
                    prop_name = row[0] + "Form"
                elif classname == "Negative":
                    if row[0] == "yes":
                        prop_name = "positiveForm"
                    elif row[0] == "no":
                        prop_name = "negativeForm"
                else:
                    prop_name = row[0] + classname + "Form"
                v3_subjs.add(prop_name)
            if classname == "PartOfSpeech":
                if row[1]:
                    non_leaf_poses.add(row[1])
 

g.parse("data/frames.ttl", format="turtle")
g.parse("data/misc.ttl", format="turtle")
g.parse("data/args.ttl", format="turtle")

for s in g.subjects():
    if s.n3()[1:].startswith(LEXINFO_v3):
        v3_subjs.add(s.n3()[45:-1])

with open("data/values/PartOfSpeech.csv") as inp:
    reader = csv.reader(inp)
    next(reader)
    for row in reader:
        classid = row[0][0].upper() + row[0][1:]
        v3_subjs.add(classid)
        if classid in non_leaf_poses:
            v3_subjs.add(classid + "POS")


print("v2,v3")
v3_subjs  = list(v3_subjs)
v3_subjs.sort()
for s in v3_subjs:
    if s in v2_subjs:
        print(s + "," + s)
    else:
        print(s + ",?")

s = list(v2_subjs.difference(v3_subjs))
s.sort()
print(s)
 
