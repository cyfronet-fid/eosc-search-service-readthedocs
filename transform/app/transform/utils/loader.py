# pylint: disable=line-too-long, wildcard-import
"""Load data"""
import os
import json
from datetime import date
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from app.services.s3.connect import connect_to_s3
from app.transform.schemas.output import *


SERVICE = "service"
DATASOURCE = "data source"
PROVIDER = "provider"
OFFER = "offer"
BUNDLE = "bundle"
GUIDELINE = "interoperability guideline"
TRAINING = "training"
OTHER_RP = "other"
SOFTWARE = "software"
DATASET = "dataset"
PUBLICATION = "publication"

DATASET_PATH = "DATASET_PATH"
PUBLICATION_PATH = "PUBLICATION_PATH"
SOFTWARE_PATH = "SOFTWARE_PATH"
OTHER_RP_PATH = "OTHER_RP_PATH"

MP_API_ADDRESS = "MP_API_ADDRESS"
MP_API_TOKEN = "MP_API_TOKEN"
GUIDELINE_ADDRESS = "GUIDELINE_ADDRESS"
TRAINING_ADDRESS = "TRAINING_ADDRESS"

INPUT_FORMAT = "INPUT_FORMAT"
OUTPUT_FORMAT = "OUTPUT_FORMAT"
OUTPUT_PATH = "OUTPUT_PATH"
OUTPUT_SCHEMA = "OUTPUT_SCHEMA"

SEND_TO_SOLR = "SEND_TO_SOLR"
SOLR_ADDRESS = "SOLR_ADDRESS"
SOLR_PORT = "SOLR_PORT"
SOLR_DATASET_COLS = "SOLR_DATASET_COLS"
SOLR_PUBLICATION_COLS = "SOLR_PUBLICATION_COLS"
SOLR_SOFTWARE_COLS = "SOLR_SOFTWARE_COLS"
SOLR_OTHER_RP_COLS = "SOLR_OTHER_RP_COLS"
SOLR_TRAINING_COLS = "SOLR_TRAINING_COLS"
SOLR_SERVICE_COLS = "SOLR_SERVICE_COLS"
SOLR_DATASOURCE_COLS = "SOLR_DATASOURCE_COLS"
SOLR_PROVIDER_COLS = "SOLR_PROVIDER_COLS"
SOLR_GUIDELINE_COLS = "SOLR_GUIDELINE_COLS"
SOLR_OFFER_COLS = "SOLR_OFFER_COLS"
SOLR_BUNDLE_COLS = "SOLR_BUNDLE_COLS"

SEND_TO_S3 = "SEND_TO_S3"
S3_ACCESS_KEY = "S3_ACCESS_KEY"
S3_SECRET_KEY = "S3_SECRET_KEY"
S3_ENDPOINT = "S3_ENDPOINT"
S3_BUCKET = "S3_BUCKET"
S3_CLIENT = "S3_CLIENT"
S3_DUMP_NAME = "S3_DUMP_NAME"

CREATE_LOCAL_DUMP = "CREATE_LOCAL_DUMP"
LOCAL_DUMP_PATH = "LOCAL_DUMP_PATH"

ALL_COLLECTION = "ALL_COLLECTION"
SOLR_COL_NAMES = "SOLR_COL_NAMES"
PATH = "PATH"
ADDRESS = "ADDRESS"

solr_all_col_mapping = {
    SERVICE: SOLR_SERVICE_COLS,
    DATASOURCE: SOLR_DATASOURCE_COLS,
    PROVIDER: SOLR_PROVIDER_COLS,
    OFFER: SOLR_OFFER_COLS,
    BUNDLE: SOLR_BUNDLE_COLS,
    GUIDELINE: SOLR_GUIDELINE_COLS,
    TRAINING: SOLR_TRAINING_COLS,
    OTHER_RP: SOLR_OTHER_RP_COLS,
    SOFTWARE: SOLR_SOFTWARE_COLS,
    DATASET: SOLR_DATASET_COLS,
    PUBLICATION: SOLR_PUBLICATION_COLS,
}

load_dotenv()


def load_file_data(
    spark: SparkSession, data_path: str, col_name: str, _format: str = "json"
):
    """Load data based on the provided data path"""
    if col_name in {SERVICE, DATASOURCE, PROVIDER, BUNDLE, OFFER}:
        return spark.read.format(_format).option("multiline", True).load(data_path)
    if col_name == TRAINING:
        return spark.read.json(
            spark.sparkContext.parallelize([json.dumps(data_path)])
        )  # TODO Depreciated
    return spark.read.format(_format).load(data_path)


def load_request_data(spark: SparkSession, data):
    """Load data based on the request response"""
    return spark.read.json(spark.sparkContext.parallelize([json.dumps(data)]))


def load_env_vars() -> dict:
    """Retrieve .env variables"""
    env_vars = {
        MP_API_TOKEN: os.environ.get(MP_API_TOKEN),
        OUTPUT_PATH: os.environ.get(OUTPUT_PATH, "output/"),
        INPUT_FORMAT: os.environ.get(INPUT_FORMAT, "JSON"),
        OUTPUT_FORMAT: os.environ.get(OUTPUT_FORMAT, "JSON"),
        SEND_TO_SOLR: os.environ.get(SEND_TO_SOLR, True).lower() in ("true", "1", "t"),
        SEND_TO_S3: os.environ.get(SEND_TO_S3, False).lower() in ("true", "1", "t"),
        CREATE_LOCAL_DUMP: os.environ.get(CREATE_LOCAL_DUMP, False).lower()
        in ("true", "1", "t"),
    }
    if not env_vars[MP_API_TOKEN]:
        raise ValueError("MP_API_TOKEN needs to be specified.")

    if not (
        env_vars[SEND_TO_SOLR] or env_vars[SEND_TO_S3] or env_vars[CREATE_LOCAL_DUMP]
    ):
        raise ValueError(
            "Data needs to be send to SOLR or/and to S3. Otherwise, program will not have any effect"
        )

    load_config(env_vars)

    return env_vars


def load_config(env_vars: dict) -> None:
    """Load Solr config"""
    env_vars[ALL_COLLECTION] = load_vars_all_collection(env_vars[SEND_TO_SOLR])
    current_date = str(date.today())

    if env_vars[SEND_TO_SOLR]:
        env_vars[SOLR_ADDRESS] = os.environ.get(SOLR_ADDRESS, "http://127.0.0.1")
        env_vars[SOLR_PORT] = os.environ.get(SOLR_PORT, 8983)

    if env_vars[SEND_TO_S3]:
        env_vars[S3_DUMP_NAME] = current_date
        for var in (S3_ACCESS_KEY, S3_SECRET_KEY, S3_ENDPOINT, S3_BUCKET):
            env_vars[var] = os.environ.get(var)
            assert env_vars[
                var
            ], f"Sending to S3 was enabled. Specify: {S3_ACCESS_KEY}, {S3_SECRET_KEY}, {S3_ENDPOINT}, {S3_BUCKET}"
        env_vars[S3_CLIENT] = connect_to_s3(
            env_vars[S3_ACCESS_KEY], env_vars[S3_SECRET_KEY], env_vars[S3_ENDPOINT]
        )

    if env_vars[CREATE_LOCAL_DUMP]:
        env_vars[LOCAL_DUMP_PATH] = os.environ.get(LOCAL_DUMP_PATH, current_date)


def load_vars_all_collection(solr_flag: bool) -> dict:
    """Load variables for all collection"""
    final_mp_api = os.environ.get(
        MP_API_ADDRESS, "https://beta.marketplace.eosc-portal.eu"
    )
    final_mp_api = final_mp_api + "/api/v1/ess/"

    collections = {
        SERVICE: {
            ADDRESS: final_mp_api + "services",
            OUTPUT_SCHEMA: service_output_schema,
        },
        DATASOURCE: {
            ADDRESS: final_mp_api + "datasources",
            OUTPUT_SCHEMA: data_source_output_schema,
        },
        PROVIDER: {
            ADDRESS: final_mp_api + "providers",
            OUTPUT_SCHEMA: provider_output_schema,
        },
        OFFER: {
            ADDRESS: final_mp_api + "offers",
            OUTPUT_SCHEMA: offer_output_schema,
        },
        BUNDLE: {
            ADDRESS: final_mp_api + "bundles",
            OUTPUT_SCHEMA: bundle_output_schema,
        },
        GUIDELINE: {
            ADDRESS: os.environ.get(
                GUIDELINE_ADDRESS,
                "https://beta.providers.eosc-portal.eu/api/public/interoperabilityRecord/all?catalogue_id=all&active=true&quantity=10000",
            ),
            OUTPUT_SCHEMA: guideline_output_schema,
        },
        TRAINING: {
            ADDRESS: os.environ.get(
                TRAINING_ADDRESS,
                "https://beta.providers.eosc-portal.eu/api/public/trainingResource/all?catalogue_id=all&active=true&quantity=10000",
            ),
            OUTPUT_SCHEMA: training_output_schema,
        },
        OTHER_RP: {
            PATH: os.environ.get(OTHER_RP_PATH, "input_data/other_rp/"),
            OUTPUT_SCHEMA: other_rp_output_schema,
        },
        SOFTWARE: {
            PATH: os.environ.get(SOFTWARE_PATH, "input_data/software/"),
            OUTPUT_SCHEMA: software_output_schema,
        },
        DATASET: {
            PATH: os.environ.get(DATASET_PATH, "input_data/dataset/"),
            OUTPUT_SCHEMA: dataset_output_schema,
        },
        PUBLICATION: {
            PATH: os.environ.get(PUBLICATION_PATH, "input_data/publication/"),
            OUTPUT_SCHEMA: publication_output_schema,
        },
    }
    if solr_flag:
        load_solr_cols_name(collections, solr_all_col_mapping)

    return collections


def load_solr_cols_name(collections: dict, solr_mapping: dict) -> None:
    """Load solr collections name"""
    for col_name, col_val in collections.items():
        col_val[SOLR_COL_NAMES] = os.environ.get(solr_mapping[col_name])

    if any(
        (not bool(env_var) for col in collections.values() for env_var in col.values())
    ):
        raise ValueError(
            f"Not all necessary .env variables were passed. Env = {collections}"
        )