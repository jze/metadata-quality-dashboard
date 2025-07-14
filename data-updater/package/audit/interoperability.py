from package.audit.utils import (
    get_distributions,
    is_defined,
    is_vocabulary_used,
)
from package.vocabulary.eu_vocab_non_proprietary import NON_PROPRIETARY_VOCABULARY
from package.vocabulary.eu_vocab_machine_readable import MACHINE_READABLE_VOCABULARY
from package.vocabulary.eu_vocab_file_type import FILE_TYPE_VOCABULARY
from package.vocabulary.iana_media_types import MEDIA_TYPE_VOCABULARY
from package.audit.scoring import interoperability_score


FORMAT = "http://purl.org/dc/terms/format"
MEDIA_TYPE = "http://www.w3.org/ns/dcat#mediaType"


def audit_interoperability(dataset):
    """ 
        Only the distribution with the highest number of points is used to calculate the points. 
        Source: https://data.europa.eu/mqa/methodology?locale=en#inline-nav-6
    """
    distributions = get_distributions(dataset)
    audits = [audit_distribution(distribution) for distribution in distributions]
    return max(audits, key=interoperability_score) if len(audits) > 0 else audit_nothing()


def audit_distribution(distribution):
    """ Audit interoperability on a single distribution. """
    is_vocabulary_controlled = (
        is_vocabulary_used(distribution, FORMAT, FILE_TYPE_VOCABULARY) 
        and is_vocabulary_used(distribution, MEDIA_TYPE, MEDIA_TYPE_VOCABULARY)
    )

    return {
        "format": is_defined(distribution, FORMAT),
        "media_type": is_defined(distribution, MEDIA_TYPE),
        "controlled_vocabulary": is_vocabulary_controlled,
        "non_proprietary": is_vocabulary_used(distribution, FORMAT, NON_PROPRIETARY_VOCABULARY),
        "machine_readable": is_vocabulary_used(distribution, FORMAT, MACHINE_READABLE_VOCABULARY),
        # opendata.swiss/catalog.jsonld devs must validate their shapes. 
        #   https://data.europa.eu/mqa/shacl-validator-ui/data-provision
        #   https://data.europa.eu/api/mqa/shacl/
        # OGD team asked the value to be 100% by default.
        "dcat_ap_compliance": True,
    }


def audit_nothing():
    """ For the rare cases when there is no distribution for a given dataset. """
    return {
        "format": False,
        "media_type": False,
        "controlled_vocabulary": False,
        "non_proprietary": False,
        "machine_readable": False,
        "dcat_ap_compliance": False,
    }



