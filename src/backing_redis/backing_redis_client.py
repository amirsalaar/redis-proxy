import re
from redis import Redis


class RedisClient:
    """A wrapper class around the initial Functional Programming style for this client."""

    def __init__(self, redis_address: str):
        self.redis_client = redis_client(redis_address)

    @property
    def instance(self):
        return self.redis_client

    def get(self, key: str) -> str:
        return get(key, self.redis_client)


def redis_client(redis_address: str) -> Redis:
    host, port = __extract_host_and_port(redis_address)
    r = Redis(host=host, port=port)

    try:
        if r.ping():
            return r.client()
    except Exception as e:
        raise ConnectionError(f"Connection to Backing Redis refused: {e}")


def __extract_host_and_port(redis_address: str) -> tuple:
    """Extract the host and port from the redis_address.

    Two expected formats for the redis_address are:
    1. "host:port": When the Backing Redis is on the same cluster as the Proxy server.
    2. "http(s)://host:port": When we are going to use a backling redis that is outside our cluster.

    Args:
        redis_address (str): The address of the Backing Redis.

    Raises:
        ProxyAppError

    Returns:
        tuple: The host and port of the Backing Redis.
    """
    if re.findall(r"[\w\d\.]+:[\d]+$", redis_address):
        # when the format is redis_address:port
        host, port = redis_address.split(":")
    else:
        # when an actual ip/host:port format is provided
        matched_regx = re.findall("http[s]?://(.*):(.*)", redis_address)

        if not matched_regx:
            raise ValueError("Invalid redis address format.")

        host, port = matched_regx[0]
        port: str = port.rstrip("/")

    return host, port


def get(key: str, redis_client: Redis):
    value = redis_client.get(key)
    return value.decode("utf-8") if value else None
