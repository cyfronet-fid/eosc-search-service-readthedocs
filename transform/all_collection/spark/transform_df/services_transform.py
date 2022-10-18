# pylint: disable=invalid-name, line-too-long, unbalanced-tuple-unpacking
"""Transform services"""

from typing import Dict
from pyspark.sql.functions import (
    lit,
    split,
    col,
)
from pyspark.sql.dataframe import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from transform.all_collection.spark.utils.join_dfs import join_different_dfs, create_df
from transform.all_collection.spark.utils.common_df_transformations import (
    create_open_access,
)
from transform.all_collection.spark.utils.utils import (
    drop_columns,
    add_columns,
)
from transform.all_collection.spark.schemas.input_col_name import (
    GEO_AV,
    RESOURCE_GEO_LOC,
)

COLS_TO_ADD = (
    "author_names",
    "author_pids",
    "code_repository_url",
    "content_type",
    "country",
    "document_type",
    "documentation_url",
    "duration",
    "eosc_provider",
    "format",
    "fos",
    "funder",
    "keywords",
    "level_of_expertise",
    "license",
    "programming_language",
    "publisher",
    "qualification",
    "research_community",
    "resource_type",
    "sdg",
    "size",
    "source",
    "subtitle",
    "target_group",
    "url",
)
COLS_TO_DROP = (GEO_AV, RESOURCE_GEO_LOC, "public_contacts")


def transform_services(services: DataFrame, spark: SparkSession) -> DataFrame:
    """
    Required transformations:
    1) type = service
    2) rename and cast columns
    3) Create open_access
    4) Simplify geographical_availabilities and resource_geographic_locations
    4) Add OAG + trainings specific columns
    """
    harvested_properties = {}

    services = services.withColumn("type", lit("service"))
    services = rename_and_cast_columns(services)
    create_open_access(services, harvested_properties, "best_access_right")
    simplify_geo_properties(services, harvested_properties)
    services = simplify_urls(services)

    services = drop_columns(services, COLS_TO_DROP)
    harvested_df = create_df(harvested_properties, spark)
    services = join_different_dfs((services, harvested_df))
    services = add_columns(services, COLS_TO_ADD)
    services = services.select(sorted(services.columns))

    return services


def rename_and_cast_columns(services: DataFrame) -> DataFrame:
    """Cast services columns"""
    services = (
        services.withColumn("description", split(col("description"), ","))
        .withColumn("id", services.id.cast(StringType()))
        .withColumnRenamed("created_at", "publication_date")
        .withColumnRenamed("order_type", "best_access_right")
        .withColumnRenamed("language_availability", "language")
        .withColumnRenamed("name", "title")
        .withColumn("publication_date", col("publication_date").cast("date"))
        .withColumn("last_update", col("last_update").cast("date"))
        .withColumn("synchronized_at", col("synchronized_at").cast("date"))
        .withColumn("updated_at", col("updated_at").cast("date"))
    )

    return services


def simplify_geo_properties(services: DataFrame, harvested_properties: Dict) -> None:
    """Extract most significant data from geographical_availabilities and resource_geographic_locations cols"""
    geo_av = services.select(GEO_AV).collect()
    res_geo_loc = services.select(RESOURCE_GEO_LOC).collect()

    geo_av_list = []
    for geo in geo_av:
        country_code = geo.geographical_availabilities[0].country_data_or_code
        geo_av_list.append(country_code)

    res_geo_loc_list = []
    for res_geo in res_geo_loc:
        try:
            country_code = res_geo.resource_geographic_locations[0].country_data_or_code
            res_geo_loc_list.append(country_code)
        except TypeError:
            res_geo_loc_list.append(None)

    harvested_properties[GEO_AV] = geo_av_list
    harvested_properties[RESOURCE_GEO_LOC] = res_geo_loc_list


def simplify_urls(df: DataFrame) -> DataFrame:
    """Simplify url columns - get only urls"""
    for urls in ("multimedia_urls", "use_cases_urls"):
        df = df.withColumn(urls, col(urls)["url"])
    return df