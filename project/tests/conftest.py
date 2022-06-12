import asyncio
import os
from typing import Iterator

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.test import finalizer, initializer

from main import create_app
from config import get_settings, Settings


def get_settings_override():
    return Settings(testing=1,
                    database_url=os.environ.get("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        yield test_client


# @pytest.fixture(scope="module")
# def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(scope="module")
def test_app_with_db():
    app = create_app()
    app.dependency_overrides[get_settings] = get_settings_override
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["models.user", "models.article"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    initializer(["models.user", "models.article"],
                db_url=os.environ.get("DATABASE_TEST_URL"))
    with TestClient(app) as test_client:
        yield test_client
    finalizer()
