import requests
from data_updater.api.opendata_catalog_jsonld import VERIFY, PROXY, HEADERS

CKAN_BASE = "https://opendata.schleswig-holstein.de"

def generate_detailed_org_list(organization_audits):
    org_list = list(organization_audits.keys())
    org_details = [get_organisation_details(org) for org in org_list]
    keys = {"name", "display_name", "description", "image_display_url", "package_count"}
    filter_keys = lambda org: {key: value for key, value in org.items() if key in keys}
    return [filter_keys(org) for org in org_details]


def get_organisation_details(id):
    if not id:
        return {"name":"unknown", "display_name": "unknown"}

    if '_:' in id:
        # The publisher was a blank note. Therefore, it will not be
        # possible to retrieve the details via API.
        return {"name":"unknown", "display_name": "unknown"}

    if 'https://' in id or 'http://' in id:
        # the 'name' of the organisation seems to be a URI
        # use the text after the last slash as id
        id = id.split('/')[-1]

    response = requests.get(
        f"{CKAN_BASE}/api/3/action/organization_show",
        verify=VERIFY,
        proxies=PROXY,
        headers=HEADERS,
        params={"id": id},
    ).json()

    return response.get("result")
