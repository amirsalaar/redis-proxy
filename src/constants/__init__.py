"""This module includes the constants used in the application."""
from src.vars import env_vars_store

REDIS_ADDRESS = env_vars_store.get("REDIS_ADDRESS", "redis:6379")
GLOBAL_CACHE_EXPIRY = int(env_vars_store.get("GLOBAL_CACHE_EXPIRY", "60"))  # seconds
CACHE_CAPACITY = int(env_vars_store.get("CACHE_CAPACITY", "10"))
