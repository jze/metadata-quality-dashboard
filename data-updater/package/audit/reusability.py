from package.audit.utils import get_distributions, is_defined, count_defined, count_vocabulary_use
from package.paths import CONTROLLED_VOC
from package.vocabulary import dcat_ap_ch
from package.vocabulary import eu_vocab_access_rights

ACCESS_RAW = 'access-right-skos.rdf'
ACCESS_PREPROCESSED = 'access-rights_preprocessed.json'

# Load vocabulary lists.
LICENSE_VOCABULARY = dcat_ap_ch.VOCABULARY
ACCESS_RIGHT_VOCABULARY = eu_vocab_access_rights.read_vocabulary(CONTROLLED_VOC / ACCESS_PREPROCESSED)

# dcat:Distribution properties.
MEDIA_TYPE = 'http://www.w3.org/ns/dcat#mediaType'

# dcat:Resource properties.
CONTACT_POINT = 'http://www.w3.org/ns/dcat#contactPoint'
LICENSE = 'http://purl.org/dc/terms/license'
PUBLISHER = 'http://purl.org/dc/terms/publisher'

# dcat:Distribution & dcat:Resource properties.
ACCESS_RIGHT = 'http://purl.org/dc/terms/accessRights'


def audit_reusability(dataset):
    distributions = get_distributions(dataset)
    return {
        "license": count_defined(distributions, LICENSE),
        "license_vocabulary": count_vocabulary_use(distributions, LICENSE, LICENSE_VOCABULARY),
        # Opendata.swiss data structure has no access restriction. OGD team asked the value to be 100% by default.
        "access_restriction": True,
        "access_restriction_vocabulary": True,
        "contact_point": is_defined(dataset, CONTACT_POINT),
        "publisher": is_defined(dataset, PUBLISHER)
    }