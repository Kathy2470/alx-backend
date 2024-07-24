#!/usr/bin/env python3
"""
This module provides methods to paginate a dataset and retrieve pagination
metadata.
"""

import csv
import math
from typing import List, Dict, Any, Optional


class Dataset:
    DATA_FILE = 'Popular_Baby_Names.csv'

    def __init__(self):
        self.__dataset = None

    def load_data(self):
        """Loads the dataset from the CSV file."""
        if self.__dataset is None:
            with open(self.DATA_FILE, newline='') as csvfile:
                reader = csv.reader(csvfile)
                self.__dataset = list(reader)[1:]  # Skip header row

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List[str]]:
        """
        Retrieves a page from the dataset.

        Args:
            page (int): The page number to retrieve.
            page_size (int): The number of items per page.

        Returns:
            List[List[str]]: The dataset page.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        self.load_data()

        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return self.__dataset[start_index:end_index]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Retrieves a page from the dataset along with pagination metadata.

        Args:
            page (int): The page number to retrieve.
            page_size (int): The number of items per page.

        Returns:
            Dict[str, Any]: A dictionary containing pagination metadata and
            the dataset page.
        """
        data = self.get_page(page, page_size)
        total_items = len(self.__dataset)
        total_pages = math.ceil(total_items / page_size)

        next_page: Optional[int] = page + 1 if page < total_pages else None
        prev_page: Optional[int] = page - 1 if page > 1 else None

        return {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': total_pages
        }


def main():
    dataset = Dataset()
    hyper_data = dataset.get_hyper(1, 10)
    print(hyper_data)


if __name__ == "__main__":
    main()
