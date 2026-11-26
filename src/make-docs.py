"""
Generates a static HTML overview of a LexInfo build: the class hierarchy,
the property hierarchy and the values (individuals) of each value class.

    python src/make-docs.py build/3.1/lexinfo.ttl build/3.1/index.html
"""
from rdflib import Graph, RDF, RDFS, OWL, Namespace, URIRef
from html import escape
import sys

LEXINFO = "http://www.lexinfo.net/ontology/3.0/lexinfo#"
ONTOLOGY = URIRef("http://www.lexinfo.net/ontology/3.0/lexinfo")
DCT = Namespace("http://purl.org/dc/terms/")

STYLE = """
:root { --fg: #1d1d1f; --bg: #ffffff; --muted: #5f6368; --rule: #dadce0; --link: #1a5fb4; --code: #f3f4f6; }
@media (prefers-color-scheme: dark) {
  :root { --fg: #e8eaed; --bg: #1b1c1f; --muted: #a0a4a8; --rule: #3c4043; --link: #8ab4f8; --code: #2a2b2f; }
}
body { font: 16px/1.5 system-ui, sans-serif; color: var(--fg); background: var(--bg);
       max-width: 60rem; margin: 0 auto; padding: 1rem 16px 4rem; }
a { color: var(--link); }
h1 { margin-bottom: 0; }
h2 { border-bottom: 1px solid var(--rule); padding-bottom: .2rem; margin-top: 2.5rem; }
.meta, .muted { color: var(--muted); }
code { background: var(--code); padding: 0 .25rem; border-radius: 3px; overflow-wrap: anywhere; }
ul.tree, ul.tree ul { list-style: none; padding-left: 1.25rem; margin: 0; }
ul.tree { padding-left: 0; }
ul.tree li { margin: .15rem 0; }
.def { color: var(--muted); font-size: .9rem; }
dl.values { display: grid; grid-template-columns: max-content 1fr; gap: .15rem 1rem; }
dl.values dt { font-family: ui-monospace, monospace; }
dl.values dd { margin: 0; }
@media (max-width: 40rem) { dl.values { grid-template-columns: 1fr; } dl.values dd { margin-bottom: .5rem; } }
"""


def local(u):
    return str(u)[len(LEXINFO):] if str(u).startswith(LEXINFO) else None


def text(g, s, p):
    vals = [o for o in g.objects(s, p) if getattr(o, "language", None) in ("en", None)]
    return str(sorted(vals)[0]) if vals else ""


def curie(g, u):
    try:
        return g.namespace_manager.normalizeUri(u)
    except Exception:
        return str(u)


def term(g, u):
    name = local(u)
    if name is None:
        return "<code>%s</code>" % escape(curie(g, u))
    return '<a href="#%s"><code>lexinfo:%s</code></a>' % (escape(name), escape(name))


def tree(g, nodes, parent_pred, seen=None):
    """Render `nodes` (lexinfo terms) as nested lists using `parent_pred`."""
    nodes = set(nodes)
    children = {n: [] for n in nodes}
    roots = []
    for n in nodes:
        parents = [p for p in g.objects(n, parent_pred) if p in nodes and p != n]
        if parents:
            for p in parents:
                children[p].append(n)
        else:
            roots.append(n)

    def render(n, depth):
        if depth > 30:
            return ""
        name = local(n)
        out = ['<li id="%s"><code>lexinfo:%s</code>' % (escape(name), escape(name))]
        extra = []
        for p in g.objects(n, parent_pred):
            if p not in nodes:
                extra.append(term(g, p))
        if extra:
            out.append(' <span class="muted">&#8594; %s</span>' % ", ".join(sorted(extra)))
        if (n, OWL.deprecated, None) in g:
            out.append(' <strong>(deprecated)</strong>')
        d = text(g, n, RDFS.comment)
        if d:
            out.append('<div class="def">%s</div>' % escape(d))
        kids = sorted(children[n], key=str)
        if kids:
            out.append('<ul>%s</ul>' % "".join(render(k, depth + 1) for k in kids))
        out.append("</li>")
        return "".join(out)

    return '<ul class="tree">%s</ul>' % "".join(render(r, 0) for r in sorted(roots, key=str))


def main(src, dest):
    g = Graph().parse(src)
    version = text(g, ONTOLOGY, OWL.versionInfo) or "dev"
    modified = text(g, ONTOLOGY, DCT.modified)
    desc = text(g, ONTOLOGY, RDFS.comment)

    def lex(t):
        return {s for s in g.subjects(RDF.type, t) if local(s)}

    classes = lex(OWL.Class)
    obj_props = lex(OWL.ObjectProperty)
    data_props = lex(OWL.DatatypeProperty)
    # Value classes: lexinfo classes that have lexinfo individuals as instances
    value_classes = sorted(
        {c for c in classes
         if any(local(i) and (i, RDF.type, OWL.Thing) in g for i in g.subjects(RDF.type, c))},
        key=str)

    html = ["<!doctype html>", '<html lang="en"><head><meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            "<title>LexInfo %s</title><style>%s</style></head><body>" % (escape(version), STYLE),
            "<h1>LexInfo %s</h1>" % escape(version),
            '<p class="meta">Released %s &middot; namespace <code>%s</code></p>' % (escape(modified), LEXINFO),
            "<p>%s</p>" % escape(desc),
            '<p>Download: <a href="lexinfo.owl">RDF/XML</a> &middot; <a href="lexinfo.ttl">Turtle</a> &middot; '
            '<a href="lexinfo.nt">N-Triples</a> &middot; <a href="lexinfo.jsonld">JSON-LD</a></p>',
            "<p>Contents: <a href=\"#classes\">Classes</a> (%d) &middot; <a href=\"#object-properties\">Object properties</a> (%d)"
            " &middot; <a href=\"#datatype-properties\">Datatype properties</a> (%d) &middot; <a href=\"#values\">Values</a> (%d classes)</p>"
            % (len(classes), len(obj_props), len(data_props), len(value_classes)),
            '<h2 id="classes">Classes</h2>', tree(g, classes, RDFS.subClassOf),
            '<h2 id="object-properties">Object properties</h2>', tree(g, obj_props, RDFS.subPropertyOf),
            '<h2 id="datatype-properties">Datatype properties</h2>', tree(g, data_props, RDFS.subPropertyOf),
            '<h2 id="values">Values</h2>']
    for c in value_classes:
        name = local(c)
        html.append('<h3 id="values-%s"><a href="#%s"><code>lexinfo:%s</code></a></h3><dl class="values">'
                    % (escape(name), escape(name), escape(name)))
        for i in sorted((i for i in g.subjects(RDF.type, c) if local(i)), key=str):
            html.append('<dt id="value-%s">%s</dt><dd>%s</dd>'
                        % (escape(local(i)), escape(local(i)), escape(text(g, i, RDFS.comment))))
        html.append("</dl>")
    html.append("</body></html>")
    with open(dest, "w", encoding="utf-8") as out:
        out.write("\n".join(html))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
