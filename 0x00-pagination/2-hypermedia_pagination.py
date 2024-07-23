#!/usr/bin/env python3
"""
Hypermedia pagination class.
"""

import csv
import math
from typing import List, Tuple, Dict, Any


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


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Get a specific page from the dataset.

        Args:
            page (int): The page number (1-indexed). Default is 1.
            page_size (int): The number of items per page. Default is 10.

        Returns:
            List[List]: The rows for the requested page, or an empty list
            if the page is out of range.
        """
        # Validate the inputs
        assert isinstance(page, int) and page > 0, (
            "Page must be a positive integer"
        )
        assert isinstance(page_size, int) and page_size > 0, (
            "Page size must be a positive integer"
        )

        # Get the dataset
        dataset = self.dataset()

        # Get the index range for the requested page
        start_index, end_index = index_range(page, page_size)

        # Return the appropriate page of the dataset
        return dataset[start_index:end_index]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Get a specific page from the dataset with additional pagination information.

        Args:
            page (int): The page number (1-indexed). Default is 1.
            page_size (int): The number of items per page. Default is 10.

        Returns:
            Dict[str, Any]: A dictionary containing pagination information.
        """
        # Get the current page data
        data = self.get_page(page, page_size)

        # Calculate total pages
        total_items = len(self.dataset())
        total_pages = math.ceil(total_items / page_size)

        # Calculate next and previous pages
        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        return {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': total_pages
        }
