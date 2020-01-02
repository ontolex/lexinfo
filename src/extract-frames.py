"""
Extracts the frames from LexInfo 2

Run this as
python3 src/extract-frames.py | rapper -o turtle -I file: - > data/frames.ttl
"""
import fileinput
import csv

in_frame = 0
line_no = 0

frames = []
current_frame = {"examples":[]}

for line in fileinput.input("lexinfo2.owl"):
    line_no += 1
    if line_no < 34:
        print(line.rstrip())
    elif "<owl:Class" in line:
        if ("Frame" in line or "Control" in line or "RaisingSubject" in line) and "lemon" not in line:
            current_frame["id"] = line[35:-3]
            in_frame = 1
            print(line.rstrip())
        elif in_frame:
            in_frame += 1
            print(line.rstrip())
    elif "</owl:Class" in line:
        if in_frame > 0:
            print(line.rstrip())
            in_frame -= 1
            if in_frame == 0:
                frames.append(current_frame)
                current_frame = {"examples":[]}
    elif in_frame:
        if "subClassOf" in line:
            if "lemon" in line:
                current_frame["kind"] = ""
            else:
                current_frame["kind"] = line[48:-4]
        elif "example" in line:
            current_frame["examples"].append( {
                    "lang":line[27:29],
                    "example":line[31:-11]
            })
        elif "comment" in line:
            current_frame["defn"] = line[line.index(">")+1:line.rindex("<")]
        elif "isDefinedBy" not in line:
            print(line.rstrip())

print("</rdf:RDF>")

frames.sort(key=lambda x: x["id"])

with open("data/frames.csv","w") as out:
    writer = csv.writer(out)
    writer.writerow(["ID","Type","Definition"])
    for frame in frames:
        writer.writerow([frame["id"],frame["kind"],frame.get("defn","")])

with open("data/frame_examples.csv","w") as out:
    writer = csv.writer(out)
    writer.writerow(["Frame","Language","Example"])
    for frame in frames:
        for example in frame["examples"]:
            writer.writerow([frame["id"],example["lang"],example["example"]])
    
