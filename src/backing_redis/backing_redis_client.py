from redis import Redis


def redis_client(redis_address: str) -> Redis:
    if len(redis_address.split(":")) != 2:
        raise ValueError("redis_address must be in the format of `host:port`")

    redis_host, redis_port = redis_address.split(":")
    r = Redis(host=redis_host, port=redis_port)

    try:
        if r.ping():
            return r.client()
    except Exception as e:
        raise ConnectionError(f"Connection to Backing Redis refused: {e}")


def get(key: str, redis_client: Redis):
    value = redis_client.get(key)
    return value.decode("utf-8") if value else None
