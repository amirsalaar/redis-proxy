"""This service contains the logic to retrieve the data either from the local cache or from the Backing Redis."""
from dataclasses import dataclass

from src.backing_redis import RedisClient
from src.local_cache import LocalCache
from src.utilities import logger
from werkzeug.exceptions import NotFound


@dataclass
class Proxy:
    """A proxy holds reference to the Redis client and the LocalCache."""

    redis_client: RedisClient
    local_cache: LocalCache


class ProxyService:
    """This class is the ProxyService which includes the logic for calling backing redis or local cache."""

    def __init__(
        self, redis_full_address: str, in_memory_local_cache: LocalCache
    ) -> None:
        """Instantiate the ProxyService.

        Args:
            redis_full_address (str): The full address of the Backing Redis.
            in_memory_local_cache (LocalCache): The global in memory cache.
        """
        self.proxy = Proxy(
            redis_client=RedisClient(redis_full_address),
            local_cache=in_memory_local_cache,
        )

    def retrieve_value_for(self, key: str) -> str | None:
        """Handle the GET request.

        Logic:
            - if the key is in the local cache, return the value from the local cache
            - if the key is not in the local cache, check if the key is in the backing redis, if so:
                  - set the retrieved value in the local cache
                  - return the retrieved value

        Args:
            key (str): The key to be retrieved.
        Returns:
            The value of the key.
        """
        value_in_local_cache = self.proxy.local_cache.get(key)
        if not value_in_local_cache:
            value_in_backing_redis = self.proxy.redis_client.get(key)
            if value_in_backing_redis:
                self.proxy.local_cache.set(key, value_in_backing_redis)
                logger.info(
                    f"Retrieved value for key: {key} from the backing redis. Setting it in the local cache too."
                )
                return value_in_backing_redis

            raise NotFound("Key not found.")

        logger.info(f"Retrieved value for key: {key} from the local cache.")
        return value_in_local_cache
