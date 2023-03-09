import logging
import uuid
import datetime
import httpx
from starlette.status import HTTP_200_OK
from httpx import AsyncClient

from app.config import MAX_ITEMS_SORT_BY_RELEVANCE, RECOMMENDER_ENDPOINT
from app.routes.web.recommendation_utils.common import (
    RecommendationPanelId,
    RecommenderError,
    _get_panel,
    SolrRetrieveError,
)
from app.solr.operations import search
from app.schemas.session_data import SessionData

logger = logging.getLogger(__name__)


def _get_raw_candidates() -> dict:
    """Get raw candidates for sort by relevance.
    Note that data sources are not included because they are not supported"""
    return {
        "dataset": [],
        "publication": [],
        "software": [],
        "other": [],
        "training": [],
        "service": [],
    }


async def get_candidates(
    panel_id: RecommendationPanelId,
    q: str,
    qf: str,
    fq: list[str],
) -> [dict, list[dict]]:
    """Get candidates IDs for sort by relevance and whole documents to present later on"""
    if panel_id == "data-source":
        raise RecommenderError(
            message="Sorting by relevance for data sources cannot be performed"
        )

    if panel_id == "all":
        fq.append("-type:data\ source")  # Take all, but exclude data sources
    else:
        fq.append(f'type:("{panel_id}")')

    async with httpx.AsyncClient() as client:
        response = await search(
            client,
            "all_collection",
            q=q,
            qf=qf,
            fq=fq,
            sort=["id desc"],
            rows=MAX_ITEMS_SORT_BY_RELEVANCE,
        )
    if response.status_code != HTTP_200_OK:
        raise SolrRetrieveError(
            message="There are no search results or connection to solr failed"
        )

    docs: list = response.json()["response"]["docs"]

    if len(docs) == 0:
        raise ValueError("Search results are empty")

    candidates_ids = _get_raw_candidates()

    for doc in docs:
        # MP recommender requires IDs as integers
        _id = int(doc["id"]) if doc["type"] == "service" else doc["id"]
        candidates_ids[doc["type"]].append(_id)

    return candidates_ids, docs


async def perform_sort_by_relevance(
    client: AsyncClient,
    session: SessionData | None,
    panel_id: RecommendationPanelId,
    candidates_ids: dict,
):
    if panel_id == "all":  # TODO [#450] remove
        # Take candidates with the most IDs
        new_panel_id = max(candidates_ids, key=lambda x: len(candidates_ids[x]))
        candidates = candidates_ids[new_panel_id]
        panel_id = new_panel_id
    else:
        candidates = candidates_ids[panel_id]

    engine_version = (
        "NCFRanking" if panel_id == "service" else "content_visit_sort"
    )  # TODO [#450] remove

    try:
        request_body = {
            "unique_id": session.session_uuid if session else str(uuid.uuid4()),
            "timestamp": datetime.datetime.utcnow().isoformat()[:-3] + "Z",
            "visit_id": str(uuid.uuid4()),
            "page_id": "/search/" + panel_id,
            "panel_id": _get_panel(panel_id),
            "engine_version": engine_version,  # TODO [#450] change to "content_visit_sort" only
            "candidates": candidates,  # TODO [#450] pass the whole "candidates_ids"
            "search_data": {},
        }
        from pprint import pprint

        pprint(request_body)
        if session is not None:
            request_body["aai_uid"] = session.aai_id

        response = await client.post(
            RECOMMENDER_ENDPOINT,
            json=request_body,
        )

        if response.status_code != 200:
            raise RecommenderError(
                http_status=response.status_code,
                message=f"Recommender server status error: \n\n {response}",
            )

        parsed_response = response.json()

        if "recommendations" not in parsed_response:
            raise RecommenderError(message="No recommendations provided")

        if len(candidates) != len(
            parsed_response["recommendations"]
        ):  # TODO [#450] change candidates to include whole dict
            logger.warning(f"Not all candidates were returned by 'sort by relevance'")

        return parsed_response["recommendations"]

    except httpx.ConnectError as e:
        raise RecommenderError(message="Connection error") from e


async def sort_docs(uuids: list[str], docs: list[dict]) -> list[dict]:
    """Sort documents based on returned uuids by sorting by relevance"""
    sorted_docs = [doc for uuid in uuids for doc in docs if uuid == doc["id"]]

    return sorted_docs
