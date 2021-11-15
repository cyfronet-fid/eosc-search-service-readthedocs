# coding: utf-8

from typing import Dict, List  # noqa: F401

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

from app.generic.models.bad_request import BadRequest
from app.generic.models.dump_results import DumpResults
from app.generic.models.extra_models import TokenModel  # noqa: F401
from app.generic.models.forbidden import Forbidden
from app.generic.models.unauthorized import Unauthorized
from app.generic.security_api import get_token_main_security_scheme

router = APIRouter()


@router.get(
    "/dumps",
    responses={
        200: {"model": DumpResults, "description": "OK"},
        400: {"model": BadRequest, "description": "Bad request"},
        401: {"model": Unauthorized, "description": "Unauthorized"},
        403: {"model": Forbidden, "description": "Forbidden"},
    },
    tags=["default"],
    summary="Returns available dumps",
)
async def dumps_get(
    cursor: str = Query(None, description=""),
    rows: int = Query(None, description="", ge=0, le=100),
    token_main_security_scheme: TokenModel = Security(get_token_main_security_scheme),
) -> DumpResults:
    ...