"""This is the root conftest.py file for the tests which includes the globally shared fixtures."""
import os
import pytest
from src.app import create_app
from pytest_mock import MockerFixture

if os.getenv("FLASK_ENV") == "production":
    TEST_REDIS_ADDRESS = "redis:6379"
else:
    TEST_REDIS_ADDRESS = "localhost:6379"


@pytest.fixture(scope="module")
def test_client():  # noqa: D103
    app = create_app({"TESTING": True})
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client


@pytest.fixture()
def get_test_redis_address():  # noqa: D103
    return TEST_REDIS_ADDRESS


@pytest.fixture()
def mocked_redis_address(mocker: MockerFixture):  # noqa: D103
    mocker.patch("src.proxy_web_service.controller.REDIS_ADDRESS", TEST_REDIS_ADDRESS)


@pytest.fixture()
def test_redis_client():  # noqa: D103
    from src.backing_redis import redis_client

    return redis_client(TEST_REDIS_ADDRESS)
