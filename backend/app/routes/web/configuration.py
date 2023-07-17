# pylint: disable=missing-function-docstring
"""The UI application configuration endpoint"""

from fastapi import APIRouter

from app.schemas.configuration_response import ConfigurationResponse
from app.settings import settings

router = APIRouter()


@router.get("/config", name="web:configuration", response_model=ConfigurationResponse)
async def config():
    return ConfigurationResponse(
        marketplace_url=settings.MARKETPLACE_BASE_URL,
        eosc_explore_url=settings.EOSC_EXPLORE_URL,
        eosc_commons_url=settings.EOSC_COMMONS_URL,
        eosc_commons_env=settings.EOSC_COMMONS_ENV,
    )
