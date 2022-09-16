# pylint: disable=redefined-outer-name,unused-argument,wrong-import-order

"""Test config"""
import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import Session

import alembic
from alembic.config import Config
from app.server import get_app


@pytest.fixture
def apply_migrations() -> None:
    """Apply DB migrations in TESTING environment."""
    config = Config("alembic.ini")

    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@pytest.fixture
def app() -> FastAPI:
    """FastAPI application"""
    return get_app()


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    """Get lifecycle-managed AsyncClient"""
    async with AsyncClient(
        app=app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture
async def managed_app(app: FastAPI, apply_migrations: None) -> FastAPI:
    """FastAPI application with managed lifecycle"""
    async with LifespanManager(app):
        yield app


@pytest.fixture
def db(managed_app) -> Session:
    """Extract Session from app state"""
    # pylint: disable=protected-access
    return managed_app.state._db
