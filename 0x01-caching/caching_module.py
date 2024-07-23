#!/usr/bin/env python3
"""
Caching Module
"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    BasicCache class
    """

    def put(self, key, item):
        """
        Add an item in the cache
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """
        Get an item by key
        """
        return self.cache_data.get(key)


if __name__ == "__main__":
    my_cache = BasicCache()
    my_cache.put("A", "Hello")
    my_cache.put("B", "World")
    my_cache.print_cache()
    print("A:", my_cache.get("A"))
    print("B:", my_cache.get("B"))
