# Source: https://www.iana.org/assignments/media-types/media-types.xhtml

from os import getcwd
from pathlib import Path
from xml.etree import ElementTree as ET


IANA_MEDIA_TYPE = "http://www.iana.org/assignments/media-types"
REGISTRY = r"{http://www.iana.org/assignments}registry"
RECORD = r"{http://www.iana.org/assignments}record"
FILE = r"{http://www.iana.org/assignments}file"

FILEPATH = Path(getcwd(), "data/controlled_vocabulary/Media Types.xml")

tree = ET.parse(FILEPATH)
root = tree.getroot()
# A templateis composed of a context and a data type.
# Example of a template: [context]/[type] -> application/csv.
templates = {
    file.text
    for registry in root.findall(REGISTRY)
    for record in registry.findall(RECORD)
    if (file := record.find(FILE)) is not None
}

MEDIA_TYPE_VOCABULARY = {f"{IANA_MEDIA_TYPE}/{template}" for template in templates}
