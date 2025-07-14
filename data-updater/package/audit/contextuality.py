from package.audit.utils import get_distributions, is_defined, count_defined


# dcat:CatalogRecord properties.
ISSUE_DATE = 'http://purl.org/dc/terms/issued'

# dcat:CatalogRecord & dcat:Distribution properties.
MODIFY_DATE = 'http://purl.org/dc/terms/modified'

# dcat:Distribution properties.
RIGHTS = 'http://purl.org/dc/terms/rights'
FILE_SIZE = 'http://www.w3.org/ns/dcat#byteSize'


def audit_contextuality(dataset):
    distributions = get_distributions(dataset)
    return {
        "rights": count_defined(distributions, RIGHTS),
        "file_size": count_defined(distributions, FILE_SIZE),
        "issue_date": is_defined(dataset, ISSUE_DATE),
        "modification_date": is_defined(dataset, MODIFY_DATE)
    }
