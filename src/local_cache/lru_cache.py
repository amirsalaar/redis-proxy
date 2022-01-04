"""This module implements a LRU cache using OrderedDict which is Map in other languages."""
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: str) -> any:
        """we return the value of the key
        that is queried in O(1) and return -1 if we
        don't find the key in out dict / cache.
        And also move the key to the beginning
        to show that it was recently used.

        Args:
            key (str): the key to be queried.

        Returns:
            any: the value of the key queried.
        """
        if key not in self.cache:
            return None
        else:
            self.cache.move_to_end(
                key, last=False
            )  # moves to the beginning due to last=False
            return self.cache[key]

    def set(self, key: str, value: any) -> None:
        """
        1. We add / update the key and value to the OrderedDict.
        2. We will also check whether the length of our
            ordered dictionary has exceeded our capacity,
            If so we remove the key from the beginning (least recently used)
        3. Move the key to the beginning to show that it was recently used.

        Args:
            key (str): the key to be added / updated.
            value (any): the value of the key to be added / updated.
        """
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
        self.cache.move_to_end(
            key, last=False
        )  # moves to the beginning due to last=False

    def remove(self, key: str) -> None:
        """
        Remove the key from the cache.
        """
        if key in self.cache:
            del self.cache[key]

    def get_all_keys(self) -> list:
        """
        Return all the keys in the cache.
        """
        return list(self.cache.keys())
