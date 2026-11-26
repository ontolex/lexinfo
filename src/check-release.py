"""
Checks run by CI on every pull request and push:

1. The ontology builds and every output format parses.
2. Compatibility: no LexInfo term declared in the latest release
   (docs/ontology/latest/lexinfo.ttl) has disappeared. Within 3.x, terms may be
   added or deprecated (owl:deprecated true) but never removed or renamed.
3. Immutability: published releases under docs/ontology/<version>/ are frozen.
   A change may only add a new release directory or update docs/ontology/latest/.

    python src/check-release.py [--base origin/master] [--release VERSION]

--release VERSION allows (re)writing docs/ontology/VERSION/, which only the
release workflow's pull request should do.
"""
from rdflib import Graph, RDF, OWL, Literal
import argparse
import os
import subprocess
import sys
import tempfile

LEXINFO = "http://www.lexinfo.net/ontology/3.0/lexinfo#"
PUBLISHED = "docs/ontology/"
FORMATS = {"owl": "xml", "ttl": "turtle", "nt": "nt", "jsonld": "json-ld"}

errors = []


def summary(text):
    print(text)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a") as out:
            out.write(text + "\n")


def declared_terms(g):
    """LexInfo IRIs that are the subject of an rdf:type triple."""
    return {s for s in g.subjects(RDF.type, None) if str(s).startswith(LEXINFO)}


def check_build():
    out = tempfile.mkdtemp()
    subprocess.run([sys.executable, "src/build-ontology.py", "--version", "check", "-o", out],
                   check=True, stderr=subprocess.DEVNULL)
    graphs = {}
    for ext, fmt in FORMATS.items():
        try:
            graphs[ext] = Graph().parse(os.path.join(out, "lexinfo." + ext), format=fmt)
        except Exception as e:
            errors.append("lexinfo.%s does not parse: %s" % (ext, e))
    sizes = {ext: len(g) for ext, g in graphs.items()}
    if len(set(sizes.values())) > 1:
        errors.append("Output formats differ in size: %s" % sizes)
    summary("Build OK: %d triples" % sizes.get("ttl", 0))
    return graphs.get("ttl")


def check_compat(built):
    # Before the first release through this pipeline there is no latest/ yet
    candidates = [os.path.join(PUBLISHED, d, "lexinfo.ttl") for d in ("latest", "3.0")]
    latest = next((c for c in candidates if os.path.exists(c)), None)
    if built is None or latest is None:
        summary("No published release found, skipping the compatibility check")
        return
    summary("Comparing with %s" % latest)
    old = Graph().parse(latest, format="turtle")
    old_terms, new_terms = declared_terms(old), declared_terms(built)
    removed = sorted(old_terms - new_terms)
    added = sorted(new_terms - old_terms)
    deprecated = sorted(s for s in new_terms
                        if (s, OWL.deprecated, Literal(True)) in built
                        and (s, OWL.deprecated, Literal(True)) not in old)
    short = lambda s: "`lexinfo:%s`" % str(s)[len(LEXINFO):]
    summary("\n### Changes since the latest release\n")
    summary("- Added (%d): %s" % (len(added), ", ".join(map(short, added)) or "none"))
    summary("- Deprecated (%d): %s" % (len(deprecated), ", ".join(map(short, deprecated)) or "none"))
    summary("- Removed (%d): %s" % (len(removed), ", ".join(map(short, removed)) or "none"))
    if removed:
        errors.append("%d terms of the latest release were removed; deprecate them "
                      "with owl:deprecated instead: %s" % (len(removed), ", ".join(map(short, removed))))


def check_frozen(base, release):
    if not base:
        return
    diff = subprocess.run(["git", "diff", "--name-status", base + "...HEAD", "--", PUBLISHED],
                          check=True, capture_output=True, text=True).stdout
    for line in diff.splitlines():
        status, path = line.split("\t")[0], line.split("\t")[-1]
        rel = path[len(PUBLISHED):]
        top = rel.split("/")[0] if "/" in rel else None
        if top == "latest" or (release and top == release):
            continue
        if status.startswith("A") and top is not None:
            existing = subprocess.run(["git", "ls-tree", "-d", "--name-only", base, PUBLISHED + top],
                                      capture_output=True, text=True).stdout.strip()
            if not existing:
                continue  # a new release directory
        errors.append("%s is part of a published release and must not change (%s)" % (path, status))


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", help="Git ref to diff against for the immutability check")
    parser.add_argument("--release", help="Version being released, whose directory may be written")
    args = parser.parse_args()

    built = check_build()
    check_compat(built)
    check_frozen(args.base, args.release)
    if errors:
        for e in errors:
            print("::error::" + e)
        sys.exit(1)
    print("All checks passed")


if __name__ == "__main__":
    main()
