"""Seed module."""
from src.utilities.app_logger import logger
from src.constants import REDIS_ADDRESS
from src.backing_redis import redis_client


def seed_db():
    """Seed the Backing Redis with some data."""
    r = redis_client(redis_address=REDIS_ADDRESS)

    for i in range(1, 11):
        r.set(f"seeded_key{i}", f"seeded_value_{i}")

    logger.info("Seeded the Backing Redis with some data.")


def clean_db():
    """Clean the Backing Redis."""
    r = redis_client(redis_address=REDIS_ADDRESS)
    for i in range(1, 11):
        r.delete(f"seeded_key{i}")

    logger.info("Cleaned the Backing Redis.")
