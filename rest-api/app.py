import json
import os

from flask import Flask, render_template
from flask_restful import Resource, Api
from pathlib import Path


CONSTANT_PATH = Path("./data/constant/")
OPENDATA_DETAILS = CONSTANT_PATH / "opendata-swiss-details.json"

INPUT_PATH = Path("./data/output/" if "AUDIT_DEV" in os.environ else "/shared/")  # fmt: skip
INPUT_ORG_AUDIT = INPUT_PATH / "audit_organisation.json"
INPUT_TOTAL_AUDIT = INPUT_PATH / "audit_total.json"
DETAILED_LIST = INPUT_PATH / "detailed_organisation_list.json"
STATUS = INPUT_PATH / "status.json"

# HTTP Connection.
VERIFY = False
PROXY = {
    "http": os.environ.get("AUDIT_PROXY", None),
    "https": os.environ.get("AUDIT_PROXY", None),
}
print(f"INPUT_ORG_AUDIT = {INPUT_ORG_AUDIT}")
print(f"INPUT_TOTAL_AUDIT = {INPUT_TOTAL_AUDIT}")
print(f"PROXY = {PROXY}")

app = Flask(__name__)
api = Api(app)

# fmt: off
class OrganisationList(Resource):
    def get(self): return list(deserialize().keys())

class DetailedOrganisationList(Resource):
    def get(self): return deserialize(DETAILED_LIST)

class Overview(Resource):
    def get(self): return overview()

class Organisation(Resource):
    def get(self, id):
        data = get_organisation(id)
        if id == "all":
            details = deserialize(OPENDATA_DETAILS)        
        else:
            org_details = next(org for org in deserialize(DETAILED_LIST) if org["name"] == id)
            keys_to_include = {"image_display_url", "description", "display_name"}
            details = {key: org_details[key] for key in keys_to_include}
            
        data["total_score"] = get_total(data)  # fmt: skip
        data.update(details)
        return data

class OrganisationOverview(Resource):
    def get(self, id):
        data = get_organisation(id)
        scores = {key: value["score"] for key, value in data.items()}
        return organisation_overview(id, scores)

class OrganisationFindability(Resource):
    def get(self, id): return get_category(id,"findability")

class OrganisationAccessibility(Resource):
    def get(self, id): 
        ignore = ["access_url_valid", "download_url_valid"]
        return get_category(id, "accessibility", ignore=ignore)

class OrganisationReusability(Resource):
    def get(self, id): return get_category(id, "reusability")

class OrganisationContextuality(Resource):
    def get(self, id): return get_category(id,"contextuality")

class OrganisationInteroperability(Resource):
    def get(self, id): return get_category(id, "interoperability")

class OrganisationInteroperability(Resource):
    def get(self, id): return get_category(id, "interoperability")

class Status(Resource):
    def get(self): return status()

class Version(Resource):
    def get(self): return {key:val for key,val in status().items() if key in ("version", "version_last_update")}

@app.route("/")
def index(): return render_template("index.html")
# fmt: on

api.add_resource(OrganisationList, "/organisation-list")
api.add_resource(DetailedOrganisationList, "/detailed-organisation-list")
api.add_resource(Overview, "/overview")
api.add_resource(Organisation, "/organisation/<string:id>")
api.add_resource(OrganisationOverview, "/organisation/<string:id>/overview")
api.add_resource(OrganisationFindability, "/organisation/<string:id>/findability")
api.add_resource(OrganisationAccessibility, "/organisation/<string:id>/accessibility")
api.add_resource(OrganisationReusability, "/organisation/<string:id>/reusability")
api.add_resource(OrganisationContextuality, "/organisation/<string:id>/contextuality")
api.add_resource(OrganisationInteroperability, "/organisation/<string:id>/interoperability")  # fmt: skip
api.add_resource(Status, "/status")
api.add_resource(Version, "/version")


def deserialize(filepath=INPUT_ORG_AUDIT):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(fp=f)


def get_category(id: str, category: str, ignore=[]):
    org = get_organisation(id)[category]
    return format_response(id, org, ignore=ignore)


def get_organisation(id):
    if id == "all":
        return deserialize(INPUT_TOTAL_AUDIT)["opendata.swiss"]
    else:
        try:
            return deserialize()[id]
        except KeyError:
            msg = f"The organisation identifyer `{id}` does not exist. "
            msg += "Find an exhaustive list of all available identifyers under `/organisation-list`"
            raise KeyError(msg)


def format_response(id: str, data: dict, ignore=[]):
    return {
        "dataStatus": status().get("last_update_ok"),
        "organisation": id,
        "data": {key: select_format(key, value) for key, value in data.items() if key not in ignore},
    }


def overview():
    out = deserialize(INPUT_TOTAL_AUDIT)["opendata.swiss"]
    out["total_score"] = get_total(out)
    return out


def get_total(dataset):
    return round(sum(category["score"] for category in dataset.values()), 3)


def organisation_overview(id: str, data: dict):
    return {
        "dataStatus": status().get("last_update_ok"),
        "organisation": id,
        "data": [{"overview": data},]
    }


def select_format(key, value):
    if key == "score":
        return value
    # A sorted list of HTTP_status frequencies: [ {code: X, value: Y}, ... ]
    elif type(value) is dict:
        return [
            {"code": status, "value": round(freq * 100, 3)}
            for status, freq 
            in sorted(value.items(), key=lambda x: x[1], reverse=True)
            if round(freq * 100, 3) > 0
        ]
    else:
        return format_yesno(value)


def format_yesno(value_yes):
    yes = value_yes * 100
    no = (1.0 - value_yes) * 100
    return [
        {"category": "Yes", "value": round(yes, 3)},
        {"category": "No", "value": round(no, 3)},
    ]


def status():
    """ Return the most recent audit update time. """
    return deserialize(STATUS)


if __name__ == "__main__":
    app.run(debug=True)
