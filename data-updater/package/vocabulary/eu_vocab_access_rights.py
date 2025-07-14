import json
from os import getcwd
from pathlib import Path
from xml.etree import ElementTree as ET


IN_FILENAME = 'access-right-skos.rdf'
OUT_FILENAME = 'access-rights_preprocessed.json'
PATH = Path(getcwd() + '/data/controlled_vocabulary')


TAG = r'{http://www.w3.org/2004/02/skos/core#}Concept'
IDENTIFIER = r'{http://purl.org/dc/elements/1.1/}identifier'


def update_vocabulary(in_filepath=None, out_filepath=None):
    if not in_filepath:
        in_filepath = PATH/IN_FILENAME

    if not out_filepath:
        out_filepath = PATH/OUT_FILENAME

    tree = ET.parse(in_filepath)
    root = tree.getroot()
    vocabulary = [concept.find(
        IDENTIFIER).text for concept in root.findall(TAG)]
    with open(out_filepath, 'w') as f:
        json.dump(vocabulary, f)


def read_vocabulary(out_filepath=None):
    if not out_filepath:
        out_filepath = PATH/OUT_FILENAME

    with open(out_filepath, 'r') as f:
        return json.load(f)
