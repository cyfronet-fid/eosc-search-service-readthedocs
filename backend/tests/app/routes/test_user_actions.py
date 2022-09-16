# pylint: disable=missing-module-docstring,missing-function-docstring,redefined-outer-name,missing-class-docstring
import json
from time import sleep

import pytest
import stomp
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_303_SEE_OTHER
from stomp.utils import Frame

from app.config import (
    USER_ACTIONS_QUEUE_CLIENT_ID,
    USER_ACTIONS_QUEUE_HOST,
    USER_ACTIONS_QUEUE_PASSWORD,
    USER_ACTIONS_QUEUE_PORT,
    USER_ACTIONS_QUEUE_TOPIC,
    USER_ACTIONS_QUEUE_USERNAME,
)

Seconds = float


class TimeoutException(Exception):
    pass


class TestListener(stomp.ConnectionListener):
    """Test listener"""

    def __init__(self, timeout: Seconds = 10):
        self.timeout = timeout
        self.error = None
        self._last_message = None

    def on_error(self, frame: Frame):
        self.error = frame

    def on_message(self, frame: Frame):
        self._last_message = json.loads(frame.body)

    @property
    def last_message(self) -> dict:
        elapsed = 0
        while True:
            if elapsed >= self.timeout:
                raise TimeoutException
            if self.error:
                return self.error
            if self._last_message:
                return self._last_message
            sleep(1)
            elapsed += 1


@pytest.mark.integration
@pytest.mark.asyncio
async def test_redirects_to_the_target_url(app: FastAPI, client: AsyncClient):
    res = await client.get(
        app.url_path_for("web:register-navigation-user-action"),
        params={
            "url": "https://anothersite.org/",
            "resource_id": "123",
            "resource_type": "service",
            "page_id": "/search/all",
            "recommendation": "0",
        },
    )

    assert res.status_code == HTTP_303_SEE_OTHER


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sends_user_action_after_response(app: FastAPI, client: AsyncClient):
    conn = stomp.Connection(
        host_and_ports=[(USER_ACTIONS_QUEUE_HOST, USER_ACTIONS_QUEUE_PORT)]
    )
    listener = TestListener()
    conn.set_listener("test_listener", listener)
    conn.connect(USER_ACTIONS_QUEUE_USERNAME, USER_ACTIONS_QUEUE_PASSWORD, wait=True)
    conn.subscribe(USER_ACTIONS_QUEUE_TOPIC, USER_ACTIONS_QUEUE_CLIENT_ID, ack="auto")

    await client.get(
        app.url_path_for("web:register-navigation-user-action"),
        params={
            "url": "https://anothersite.org/",
            "resource_id": "123",
            "resource_type": "service",
            "page_id": "/search/all",
            "recommendation": "0",
        },
    )

    message = listener.last_message

    assert message["action"] == {"order": False, "text": "", "type": "browser action"}
    assert message["client_id"] == "search_service"
    assert message["source"]["page_id"] == "/search/all"
    assert message["source"]["root"] == {
        "resource_id": "123",
        "resource_type": "service",
        "type": "other",
    }
    assert message["source"]["visit_id"] is not None
    assert message["target"]["page_id"] == "https://anothersite.org/"
    assert message["target"]["visit_id"] is not None
    assert message["timestamp"] is not None
    assert message["unique_id"] is not None
