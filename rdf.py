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
data_dir = base_dir.parent / "csv_files" / "formal_language"

collected_rows = []

for filepath in glob.glob(str(data_dir / '*.csv')):
    with open(filepath, "r", encoding="utf-8") as csv_file:
        table = csv.DictReader(csv_file)
        next(table)  # Skip the header row

        for entry in table:
            collected_rows.append(entry)

            # Strip surrounding whitespace from each triple component
            raw_subj = entry['Subject'].strip()
            raw_pred = entry['Predicate'].strip()
            raw_obj  = entry['Object'].strip()

            # Resolve subject URI from its prefix:localname pair
            subj_prefix, subj_local = raw_subj.split(':')
            subj_uri = prefix_map[subj_prefix][subj_local]

            # Resolve predicate URI
            pred_prefix, pred_local = raw_pred.split(':')
            pred_uri = prefix_map[pred_prefix][pred_local]

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
triple_graph.serialize(destination=output_file, format='turtle')