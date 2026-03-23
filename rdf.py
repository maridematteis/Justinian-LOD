import rdflib, csv, glob
from datetime import datetime
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import XSD, OWL, RDF
from pathlib import Path

triple_graph = Graph()

# Namespace prefix mappings
prefix_map = {
    "sits"    : Namespace("https://github.com/Iustinianus-LOD/Justinian-LOD.git/"),
    "wd"      : Namespace("https://www.wikidata.org/wiki/"),
    "dbo"     : Namespace("https://dbpedia.org/ontology/"),
    "dcterms" : Namespace("http://purl.org/dc/terms/"),
    "crm"     : Namespace("http://www.cidoc-crm.org/cidoc-crm/"),
    "rdf"     : RDF,
    "owl"     : OWL,
    "skos"    : Namespace("http://www.w3.org/2004/02/skos/core#"),
    "bf"      : Namespace("http://id.loc.gov/ontologies/bibframe/"),
    "bibo"    : Namespace("http://purl.org/ontology/bibo/"),
    "nmo"     : Namespace("http://nomisma.org/ontology#"),
    "nm"      : Namespace("http://nomisma.org/id/"),
    "schema"  : Namespace("https://schema.org/"),
    "aat"     : Namespace("http://vocab.getty.edu/aat/")
}

for abbrev, uri_space in prefix_map.items():
    if abbrev not in {'rdf', 'owl'}:
        triple_graph.bind(abbrev, uri_space)


def clean_token(token: str) -> str:
    """
    Strip surrounding whitespace, angle brackets (<URI>),
    and surrounding double-quotes ("literal") from a token.
    """
    token = token.strip()
    if token.startswith('<') and token.endswith('>'):
        token = token[1:-1].strip()
    if token.startswith('"') and token.endswith('"') and len(token) >= 2:
        token = token[1:-1].strip()
    return token


def resolve_uri(token: str):
    """
    Resolve a CURIE (e.g. 'dcterms:title') or a full http(s) URI into a URIRef.
    Returns None if the token cannot be resolved.

    If the token contains multiple alternatives separated by ' - ', ';', '|', or ',',
    the first resolvable one is returned.
    """
    token = clean_token(token)
    if not token:
        return None

    for sep in [' - ', ';', '|', ',']:
        if sep in token:
            for part in [p.strip() for p in token.split(sep) if p.strip()]:
                result = resolve_uri(part)
                if result is not None:
                    return result
            return None

    if token.startswith('http://') or token.startswith('https://'):
        return URIRef(token)

    if ':' in token:
        prefix, local = token.split(':', 1)
        ns = prefix_map.get(prefix) or prefix_map.get(prefix.lower())
        if ns is not None:
            local = local.strip()
            if local and ' ' not in local and '"' not in local and ']' not in local:
                try:
                    return ns[local]
                except AttributeError:
                    pass

    return None


def resolve_object(raw_obj: str):
    """
    Resolve an object token to a URIRef when possible,
    otherwise return an appropriately typed Literal.
    """
    raw_obj = raw_obj.strip()
    cleaned = clean_token(raw_obj)

    if raw_obj.startswith('<') and raw_obj.endswith('>'):
        return URIRef(cleaned)

    uri = resolve_uri(cleaned)
    if uri is not None:
        return uri

    if raw_obj.startswith('"') and raw_obj.endswith('"'):
        return Literal(cleaned)

    year_ceiling = datetime.now().year
    try:
        parsed_num = int(cleaned)
        if 1000 <= parsed_num <= year_ceiling + 1:
            return Literal(cleaned, datatype=XSD.gYear)
        else:
            return Literal(parsed_num, datatype=XSD.integer)
    except ValueError:
        pass

    import re
    lang_match = re.match(r'^"?(.+?)"?@([a-z]{2,3})$', cleaned)
    if lang_match:
        text, lang = lang_match.group(1), lang_match.group(2)
        return Literal(text, lang=lang)

    return Literal(cleaned)


# ---------------------------------------------------------------------------
# Main processing loop
# ---------------------------------------------------------------------------
base_dir = Path(__file__).resolve().parent
data_dir = base_dir / "csv_files" / "Formal_language"

csv_paths = glob.glob(str(data_dir / '*.csv'))
if not csv_paths:
    print(f"WARNING: no CSV files found in {data_dir}")

skipped = []

for filepath in csv_paths:
    with open(filepath, "r", encoding="utf-8") as csv_file:
        for entry in csv.DictReader(csv_file):
            raw_subj = entry.get('Subject',   '').strip()
            raw_pred = entry.get('Predicate', '').strip()
            raw_obj  = entry.get('Object',    '').strip()

            subj_uri = resolve_uri(raw_subj)
            pred_uri = resolve_uri(raw_pred)

            if subj_uri is None or pred_uri is None:
                skipped.append(entry)
                continue

            obj_node = resolve_object(raw_obj)
            triple_graph.add((subj_uri, pred_uri, obj_node))

if skipped:
    print(f"\n--- {len(skipped)} row(s) skipped (unresolvable subject or predicate) ---")
    print("These likely have typos in the CSV. Check the prefix spelling carefully:\n")
    for row in skipped:
        print(f"  Subject  : {row.get('Subject')}")
        print(f"  Predicate: {row.get('Predicate')}")
        print(f"  Object   : {row.get('Object')}")
        print()

output_file = base_dir / "full_dataset.ttl"
triple_graph.serialize(destination=str(output_file), format='turtle')
print(f"Wrote {len(triple_graph)} triples to {output_file}")