import os
import pytest
from src.app import create_app


@pytest.fixture(scope="module")
def test_client():
    app = create_app({"TESTING": True})
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client


@pytest.fixture()
def test_redis_client():
    from src.backing_redis import redis_client

    if os.getenv("FLASK_ENV") == "production":
        TEST_REDIS_ADDRESS = "redis:6379"
    else:
        TEST_REDIS_ADDRESS = "localhost:6379"

    return redis_client(TEST_REDIS_ADDRESS)
