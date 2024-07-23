#!/usr/bin/env python3
"""
Simple helper function to calculate index range for pagination.
"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate the range of indexes for pagination.

    Args:
        page (int): The current page number (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing the start and end indexes.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)
