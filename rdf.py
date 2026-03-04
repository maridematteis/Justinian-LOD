import rdflib, csv, glob
from datetime import datetime
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import XSD, OWL, RDF, FOAF
from pathlib import Path

triple_graph = Graph()

# Namespace prefix mappings for the knowledge graph
prefix_map = {
    "sits" : Namespace("https://github.com/Iustinianus-LOD/Justinian-LOD.git"),
    "wd"   : Namespace("https://www.wikidata.org/wiki/"),
    "dbo"  : Namespace("https://dbpedia.org/ontology/"),
    "dcterms" : Namespace("http://purl.org/dc/terms/"),
    "crm"  : Namespace("https://cidoc-crm.org/html/cidoc_crm/"),
    "rdf"  : RDF,
    "owl"  : OWL,
    "skos" : Namespace("http://www.w3.org/2004/02/skos/core#"),
    "gndo" : Namespace("https://d-nb.info/standards/elementset/gnd#"),
    "gn"   : Namespace("http://www.geonames.org/ontology#"),
    "bf"   : Namespace("http://id.loc.gov/ontologies/bibframe/"),
    "bibo" : Namespace("http://purl.org/ontology/bibo/"),
    "rda"  : Namespace("http://rdaregistry.info/Elements/a/"),
    "metadigit" : Namespace("http://www.iccu.sbn.it/metaAG1"),
    "nmo"  : Namespace("http://nomisma.org/ontology#"),
    "nm"   : Namespace("http://nomisma.org/id/"),
    "foaf" : FOAF,
    "schema" : Namespace("https://schema.org/"),
    "viaf" : Namespace("https://viaf.org/en"),
    "tgm"  : Namespace("http://id.loc.gov/vocabulary/graphicMaterials/"),
    "mo"   : Namespace("http://purl.org/ontology/mo/"),
    "aat"  : Namespace("http://vocab.getty.edu/aat/")
}

# These prefixes are handled natively by rdflib and don't need manual binding
builtin_prefixes = ['foaf', 'rdf', 'owl']

for abbrev, uri_space in prefix_map.items():
    if abbrev not in builtin_prefixes:
        triple_graph.bind(abbrev, uri_space)


# Resolve CSV directory relative to this script's location
base_dir = Path(__file__).resolve().parent
# CSV files are located inside the repository under csv_files/Formal_language
data_dir = base_dir / "csv_files" / "Formal_language"

# Collect CSV paths first so we can warn if none are found
csv_paths = glob.glob(str(data_dir / '*.csv'))
if not csv_paths:
    print(f"Warning: no CSV files found in {data_dir}")

collected_rows = []

for filepath in csv_paths:
    with open(filepath, "r", encoding="utf-8") as csv_file:
        # DictReader reads the header row automatically; do not call next() here
        table = csv.DictReader(csv_file)

        for entry in table:
            collected_rows.append(entry)

            # Strip surrounding whitespace from each triple component
            raw_subj = entry.get('Subject', '').strip()
            raw_pred = entry.get('Predicate', '').strip()
            raw_obj  = entry.get('Object', '').strip()

            # Helper to resolve CURIEs or fall back to URIRef
            def resolve_term(token):
                token = token.strip()
                if not token:
                    return None
                # If the token contains multiple alternatives (e.g. "A - B"),
                # try to pick the part that looks like a CURIE or an http URI.
                for sep in [' - ', ';', '|', ',']:
                    if sep in token:
                        parts = [p.strip() for p in token.split(sep) if p.strip()]
                        # prefer a part that is a known CURIE or an http URI
                        for part in parts:
                            if (':' in part and part.split(':', 1)[0] in prefix_map) or part.startswith('http://') or part.startswith('https://'):
                                token = part
                                break
                        else:
                            token = parts[0]
                if ':' in token:
                    prefix, local = token.split(':', 1)
                    if prefix in prefix_map:
                        return prefix_map[prefix][local]
                    if token.startswith('http://') or token.startswith('https://'):
                        return URIRef(token)
                    # Unknown prefix and not an http(s) URI: cannot resolve
                    return None
                else:
                    # No colon; not a CURIE/URI we can resolve -> skip
                    return None

            # Resolve subject and predicate safely
            subj_uri = resolve_term(raw_subj)
            pred_uri = resolve_term(raw_pred)

            # If core components are missing, skip this row
            if subj_uri is None or pred_uri is None:
                continue

            # Attempt to resolve object as a URI if it contains a colon
            obj_node = None
            if ':' in raw_obj:
                try:
                    obj_prefix, obj_local = raw_obj.split(':', 1)
                    if obj_prefix in prefix_map:
                        obj_node = prefix_map[obj_prefix][obj_local]
                except ValueError:
                    pass

            # Fall back to Literal if no namespace match was found
            if obj_node is None:
                year_ceiling = datetime.now().year
                try:
                    parsed_num = int(raw_obj)
                    if 1000 <= parsed_num <= year_ceiling + 1:
                        obj_node = Literal(raw_obj, datatype=XSD.gYear)
                    else:
                        obj_node = Literal(parsed_num, datatype=XSD.integer)
                except ValueError:
                    obj_node = Literal(raw_obj)

            triple_graph.add((subj_uri, pred_uri, obj_node))


# Serialize the completed graph to Turtle format
output_file = base_dir / "full_dataset.ttl"
triple_graph.serialize(destination=str(output_file), format='turtle')
print(f"Wrote {len(triple_graph)} triples to {output_file}")