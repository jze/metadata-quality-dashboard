import asyncio
import json
import logging
import os
import traceback
import urllib3

from datetime import datetime
from pathlib import Path

from data_updater.api import opendata_catalog_jsonld as cat
from data_updater.api import opendata_ckan as ckan
from data_updater.audit import (
    audit_datasets,
    score_total,
    score_organisations,
    score_datasets,
)
import data_updater.config as c
from data_updater.utils import save_json, load_json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")  # fmt: skip
logger = logging.getLogger(__name__)


async def main() -> None:
    try:
        log_env_vars()
        ensure_output_files_exist()

        logger.info("Download all pages from DCAT catalog")
        requests = cat.request_all_pages()
        raw_data = cat.requests_to_json(requests)
        save_json(c.INPUT_FILE, list(raw_data))

        logger.info("Format the catalog.")
        catalog = cat.format_data(load_json(c.INPUT_FILE))

        logger.info("Audit all datasets.")
        audits = await audit_datasets(catalog, debug=True)

        # Ready for Future feature.
        # logger.info("Generate score by dataset.")
        # dataset_scores = score_datasets(audits)
        # logger.info(f"Save dataset audit to {c.OUTPUT_DATASET_AUDIT}.")
        # save_json(c.OUTPUT_DATASET_AUDIT, dataset_scores)

        logger.info("Generate score by organisation.")
        organisation_scores = score_organisations(audits)
        logger.info(f"Save organisation audit to {c.OUTPUT_ORG_AUDIT}.")
        save_json(c.OUTPUT_ORG_AUDIT, organisation_scores)

        logger.info("Generate total score.")
        total_score = score_total(audits)
        logger.info(f"Save DCAT catalog audit to {c.OUTPUT_TOTAL_AUDIT}.")
        save_json(c.OUTPUT_TOTAL_AUDIT, total_score)

        logger.info("Generate detailed organisation list.")
        detailed_org_list = ckan.generate_detailed_org_list(organisation_scores)

        logger.info(f"Save detailed organisation list to {c.OUTPUT_LIST}.")
        save_json(c.OUTPUT_LIST, detailed_org_list)
    except:
        save_status(c.OUTPUT_STATUS, "ERROR", traceback.format_exc())
    else:
        save_status(c.OUTPUT_STATUS, "OK", "")
    finally:
        logger.info(f"Save status to {c.OUTPUT_STATUS}.")

    logger.info(f"Audit complete!")


def save_status(file: Path, _status: str, error_message: str = "") -> None:
    now = datetime.now().strftime("%d.%m.%Y")

    if _status == "OK":
        last_ok = now
    elif file.exists():
        last_ok = load_json(file).get("last_update_ok")
    else:
        last_ok = "Never"

    status = dict(
        status="OK" if _status else "ERROR",
        message=error_message,
        last_update=now,
        last_update_ok=last_ok,
        version=c.VERSION,
        version_last_update=c.VERSION_DATE,
    )
    save_json(file, status)


def log_env_vars() -> None:
    logger.info(f"[env] AUDIT_DEV: {os.getenv(c.ENV_AUDIT_DEV, 'None')}")
    logger.info(f"[env] SHARED: {os.getenv(c.ENV_SHARED, 'None')}")
    logger.info(f"[env] AUDIT_HTTP_PROXY: {os.getenv(c.ENV_AUDIT_HTTP_PROXY, 'None')}")
    logger.info(f"[env] AUDIT_HTTPS_PROXY: {os.getenv(c.ENV_AUDIT_HTTPS_PROXY, 'None')}")


def ensure_output_files_exist():
    c.OUT.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output folder: {c.OUT}")
    for path in [
        c.OUTPUT_DATASET_AUDIT,
        c.OUTPUT_ORG_AUDIT,
        c.OUTPUT_TOTAL_AUDIT,
        c.OUTPUT_LIST,
        c.OUTPUT_STATUS,
    ]:
        path.touch()
        logger.debug(f"Ensured file exists: {path}")


asyncio.run(main())
