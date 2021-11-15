# coding: utf-8

from __future__ import annotations

import re  # noqa: F401
from datetime import date, datetime  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator  # noqa: F401

from app.generic.models.dump import Dump


class DumpResults(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    DumpResults - a model defined in OpenAPI

        dumps: The dumps of this DumpResults.
        next_cursor: The next_cursor of this DumpResults [Optional].
    """

    dumps: List[Dump]
    next_cursor: Optional[str] = None


DumpResults.update_forward_refs()