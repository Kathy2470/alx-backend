#!/usr/bin/env python3
"""
Module documentation goes here.
"""

import pandas as pd
import math


class Server:
    def __init__(self):
        self.data = pd.read_csv('Popular_Baby_Names.csv')

    def get_page(self, page: int = 1, page_size: int = 10) -> pd.DataFrame:
        """
        Get a page of the dataset.

        Args:
            page (int): The page number to retrieve.
            page_size (int): The number of rows per page.

        Returns:
            pd.DataFrame: The page of the dataset.
        """
        start = (page - 1) * page_size
        end = start + page_size
        return self.data.iloc[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """
        Get a page of the dataset with hypermedia links.

        Args:
            page (int): The page number to retrieve.
            page_size (int): The number of rows per page.

        Returns:
            dict: A dictionary containing the page data and hypermedia links.
        """
        data = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.data) / page_size)
        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None
        return {
            'page_size': page_size,
            'page': page,
            'data': data.values.tolist(),
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': total_pages
        }
