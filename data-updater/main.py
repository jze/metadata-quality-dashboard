import asyncio
import json
import logging
import os
import traceback
import urllib3

from datetime import datetime
from pathlib import Path

from package.api import opendata_catalog_jsonld as cat
from package.api import opendata_ckan as ckan
from package.audit import (
    audit_datasets,
    score_total,
    score_organisations,
    score_datasets,
)
from package.paths import DATA

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")  # fmt: skip
logger = logging.getLogger(__name__)

VERSION, VERSION_DATE = 0.8, "16.07.2025"

RAW_FILE = DATA / "input_raw" / "all_catalog.jsonld"
OUT = (
    DATA / "output" if os.getenv("AUDIT_DEV") else Path(os.getenv("SHARED", "/shared/"))
)

OUTPUT_DATASET_AUDIT = OUT / "audit_dataset.json"
OUTPUT_ORG_AUDIT = OUT / "audit_organisation.json"
OUTPUT_TOTAL_AUDIT = OUT / "audit_total.json"
OUTPUT_LIST = OUT / "detailed_organisation_list.json"
OUTPUT_STATUS = OUT / "status.json"


async def main() -> None:
    try:
        log_env_vars()
        ensure_output_files_exist()
        
        logger.info("Download all pages from opendata.swiss")
        requests = cat.request_all_pages()
        raw_data = cat.requests_to_json(requests)
        cat.save_pages(raw_data, RAW_FILE)

        logger.info("Format the catalog.")
        catalog = cat.format_data(cat.load_pages(RAW_FILE))

        logger.info("Audit all datasets.")
        audits = await audit_datasets(catalog)

        # Ready for Future feature.
        # logger.info("Generate score by dataset.")
        # dataset_scores = score_datasets(audits)
        # logger.info(f"Save dataset audit to {OUTPUT_DATASET_AUDIT}.")
        # with open(OUTPUT_DATASET_AUDIT, "w") as f:
        #     json.dump(dataset_scores, f, indent=4)

        logger.info("Generate score by organisation.")
        organisation_scores = score_organisations(audits)
        logger.info(f"Save organisation audit to {OUTPUT_ORG_AUDIT}.")
        with open(OUTPUT_ORG_AUDIT, "w") as f:
            json.dump(organisation_scores, f, indent=4)

        logger.info("Generate total score.")
        total_score = score_total(audits)
        logger.info(f"Save opendata.swiss audit to {OUTPUT_TOTAL_AUDIT}.")
        with open(OUTPUT_TOTAL_AUDIT, "w") as f:
            json.dump(total_score, f, indent=4)

        logger.info("Generate detailed organisation list.")
        detailed_org_list = ckan.generate_detailed_org_list(organisation_scores)

        logger.info(f"Save detailed organisation list to {OUTPUT_LIST}.")
        with open(OUTPUT_LIST, "w") as f:
            json.dump(detailed_org_list, f, indent=4)
    except:
        save_status(OUTPUT_STATUS, "ERROR", traceback.format_exc())
    else:
        save_status(OUTPUT_STATUS, "OK", "")
    finally:
        logger.info(f"Save status to {OUTPUT_STATUS}.")

    logger.info(f"Audit complete!")


def save_status(file: Path, _status: str, error_message: str = "") -> None:
    now = datetime.now().strftime("%d.%m.%Y")

    if _status == "OK":
        last_ok = now
    elif file.exists():
        with open(file, "r") as f:
            last_ok = json.load(f).get("last_update_ok")
    else:
        last_ok = "Never"

    status = dict(
        status="OK" if _status else "ERROR",
        message=error_message,
        last_update=now,
        last_update_ok=last_ok,
        version=VERSION,
        version_last_update=VERSION_DATE,
    )

    with open(file, "w") as f:
        json.dump(status, f)


def log_env_vars() -> None:
    logger.info(f"[env] AUDIT_DEV: {os.getenv('AUDIT_DEV', 'None')}")
    logger.info(f"[env] SHARED: {os.getenv('SHARED', 'None')}")
    logger.info(f"[env] AUDIT_PROXY: {os.getenv('AUDIT_PROXY', 'None')}")


def ensure_output_files_exist():
    OUT.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output folder: {OUT}")
    for path in [
        OUTPUT_DATASET_AUDIT,
        OUTPUT_ORG_AUDIT,
        OUTPUT_TOTAL_AUDIT,
        OUTPUT_LIST,
        OUTPUT_STATUS
    ]:
        path.touch(exist_ok=True)
        logger.debug(f"Ensured file exists: {path}")


asyncio.run(main())
