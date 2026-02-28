#!/usr/bin/env python3
"""
tei2rdf.py
Convert a TEI/XML file (text.xml) to RDF/Turtle and RDF/XML.
Usage:
    python3 tei2rdf.py text.xml
Outputs: text.ttl   text.rdf
Requires: lxml, rdflib
"""

import sys
import re
import uuid
from pathlib import Path
from lxml import etree
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, DCTERMS, FOAF, SKOS, OWL

# --- Configuration ---
TEI_NS = "http://www.tei-c.org/ns/1.0"
XML_NS = "http://www.w3.org/XML/1998/namespace"

BASE_URI = "https://example.org/procopius/"  
SCHEMA = Namespace("http://schema.org/")
BIBO = Namespace("http://purl.org/ontology/bibo/")

# --- Helpers ---
def qname_local(el):
    t = getattr(el, "tag", None)
    return etree.QName(t).localname if isinstance(t, str) else None

def xml_id(el):
    return el.get("{%s}id" % XML_NS) or el.get("id")

def slug(s: str) -> str:
    if not s:
        return str(uuid.uuid4())
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"[^A-Za-z0-9._~\-]", "", s)
    return s.lower() or str(uuid.uuid4())

def gather_text(el):
    if el is None:
        return ""
    return " ".join(t.strip() for t in el.itertext() if t and t.strip())

def extract_text_with_breaks(el, pb_template="[page {n}]"):
    if el is None:
        return ""
    parts = []
    if el.text:
        parts.append(el.text)
    for child in el:
        ln = qname_local(child)
        if ln == "lb":
            parts.append("\n")
        elif ln == "pb":
            n = child.get("n") or ""
            parts.append("\n" + (pb_template.format(n=n) if n else "[page]") + "\n")
        else:
            parts.append(extract_text_with_breaks(child, pb_template))
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)

def find_lang(el):
    cur = el
    while cur is not None:
        lang = cur.get("{%s}lang" % XML_NS)
        if lang:
            return lang
        cur = cur.getparent()
    return None

# --- RDF setup ---
g = Graph()
g.bind("dcterms", DCTERMS)
g.bind("foaf", FOAF)
g.bind("skos", SKOS)
g.bind("owl", OWL)
g.bind("schema", SCHEMA)
g.bind("bibo", BIBO)
g.bind("base", URIRef(BASE_URI))

# Work node
work_uri = URIRef(BASE_URI + "work/edizione-digitale")
g.add((work_uri, RDF.type, BIBO.Document))
g.add((work_uri, RDF.type, SCHEMA.CreativeWork))

seg_counters = {}

def next_uri(tag, hint=None):
    seg_counters.setdefault(tag, 0)
    seg_counters[tag] += 1
    base = slug(hint) if hint else tag
    return URIRef(BASE_URI + f"{tag}/{base}-{seg_counters[tag]}")

def map_node(node, parent_uri):
    tag = qname_local(node)
    if not tag:
        return

    xid = xml_id(node)
    hint = (gather_text(node)[:40] or tag)
    safe = slug(xid or hint)
    seg_uri = URIRef(BASE_URI + f"{tag}/{safe}")

    # link parent -> part
    g.add((parent_uri, DCTERMS.hasPart, seg_uri))

    # type & content extraction by tag
    if tag in {"teiHeader", "fileDesc", "sourceDesc"}:
        g.add((seg_uri, RDF.type, SCHEMA.CreativeWork))
    elif tag in {"div", "p", "head", "q", "quote", "lg", "l"}:
        g.add((seg_uri, RDF.type, SCHEMA.CreativeWork))
        txt = extract_text_with_breaks(node).strip()
        if txt:
            lang = find_lang(node)
            g.add((seg_uri, SCHEMA.text, Literal(txt, lang=lang)))
    elif tag in {"persName", "person"}:
        g.add((seg_uri, RDF.type, FOAF.Person))
        txt = gather_text(node)
        if txt:
            g.add((seg_uri, FOAF.name, Literal(txt)))
    elif tag in {"place", "placeName"}:
        g.add((seg_uri, RDF.type, SCHEMA.Place))
        label = gather_text(node)
        if label:
            g.add((seg_uri, RDFS.label, Literal(label)))
    elif tag in {"org", "orgName"}:
        g.add((seg_uri, RDF.type, FOAF.Organization))
        label = gather_text(node)
        if label:
            g.add((seg_uri, FOAF.name, Literal(label)))
    elif tag == "title":
        g.add((seg_uri, RDF.type, SCHEMA.CreativeWork))
        txt = gather_text(node)
        if txt:
            g.add((seg_uri, DCTERMS.title, Literal(txt)))
    else:
        g.add((seg_uri, RDF.type, SCHEMA.CreativeWork))

    # attributes -> notes / sameAs
    for (k, v) in node.items():
        if k == "{%s}id" % XML_NS:
            continue
        lname = etree.QName(k).localname
        if lname == "sameAs":
            # if sameAs is an URI, create owl:sameAs triple
            try:
                g.add((seg_uri, OWL.sameAs, URIRef(v)))
            except Exception:
                g.add((seg_uri, SKOS.note, Literal(f"sameAs (not URI)={v}")))
        else:
            g.add((seg_uri, SKOS.note, Literal(f"{lname}={v}")))

    # recursion
    for ch in list(node):
        map_node(ch, seg_uri)


# --- Main ---
def main(input_path):
    p = Path(input_path)
    if not p.exists():
        print("File not found:", input_path)
        return

    parser = etree.XMLParser(remove_blank_text=False, ns_clean=True, recover=True)
    tree = etree.parse(str(p), parser)
    root = tree.getroot()

    # Map teiHeader then text (preserve order)
    for child in root:
        if qname_local(child) == "teiHeader":
            map_node(child, work_uri)
    for child in root:
        if qname_local(child) == "text":
            map_node(child, work_uri)

    ttl_out = p.with_suffix(".ttl")
    rdf_out = p.with_suffix(".rdf")
    g.serialize(destination=str(ttl_out), format="turtle")
    g.serialize(destination=str(rdf_out), format="xml")

    print("Wrote:", ttl_out, rdf_out)
    print("Triples generated:", len(g))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 tei2rdf.py text.xml")
        sys.exit(1)
    main(sys.argv[1])
