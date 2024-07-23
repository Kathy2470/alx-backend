#!/usr/bin/env python3
"""
LFUCache module
"""

from base_caching import BaseCaching
from collections import defaultdict, OrderedDict


class LFUCache(BaseCaching):
    """
    LFUCache class
    """

    def __init__(self):
        """
        Initialize the class
        """
        super().__init__()
        self.freq_data = defaultdict(int)
        self.order_data = defaultdict(OrderedDict)
        self.min_freq = 0

    def put(self, key, item):
        """
        Add an item to the cache
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            # Update item
            self.cache_data[key] = item
            self._update_freq(key)
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # Find the LFU item
            lfu_key = min(self.order_data[self.min_freq].keys())
            del self.cache_data[lfu_key]
            del self.order_data[self.min_freq][lfu_key]
            print(f"DISCARD: {lfu_key}")

        # Add new item
        self.cache_data[key] = item
        self.freq_data[key] = 1
        self.order_data[1][key] = None
        self.min_freq = 1

    def get(self, key):
        """
        Get an item from the cache
        """
        if key is None or key not in self.cache_data:
            return None

        self._update_freq(key)
        return self.cache_data[key]

    def _update_freq(self, key):
        """
        Update the frequency of an item
        """
        freq = self.freq_data[key]
        self.freq_data[key] += 1
        new_freq = freq + 1

        # Remove from old frequency list
        del self.order_data[freq][key]
        if not self.order_data[freq]:
            del self.order_data[freq]
            if self.min_freq == freq:
                self.min_freq += 1

        # Add to new frequency list
        self.order_data[new_freq][key] = None
