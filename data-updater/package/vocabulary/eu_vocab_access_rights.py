import json
from xml.etree import ElementTree as ET


TAG = r"{http://www.w3.org/2004/02/skos/core#}Concept"
IDENTIFIER = r"{http://purl.org/dc/elements/1.1/}identifier"


def update_vocabulary(in_filepath, out_filepath):
    tree = ET.parse(in_filepath)
    root = tree.getroot()
    vocabulary = [concept.find(IDENTIFIER).text for concept in root.findall(TAG)]
    with open(out_filepath, "w") as f:
        json.dump(vocabulary, f)


def read_vocabulary(out_filepath):
    with open(out_filepath, "r") as f:
        return json.load(f)
