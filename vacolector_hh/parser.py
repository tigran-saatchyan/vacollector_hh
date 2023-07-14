"""Abstract base class for parsers modules."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests


class Parser(ABC):
    """
    Abstract base class for parsers.
    """

    __slots__ = (
        'keyword',
        'url',
        'headers',
        'per_page',
        'parameters'
    )

    @abstractmethod
    def parse_vacancies(
            self, keyword: str, count: int
    ) -> List[Dict[str, Any]]:
        """
        Parses vacancies based on the given keyword and count.

        Args:
            keyword (str): The keyword to search for.
            count (int): The number of vacancies to retrieve.

        Returns:
            List[Dict[str, Any]]: The parsed vacancies.
        """
        pass


class RequestMixin:
    """
    Mixin class for making HTTP requests.
    """

    @staticmethod
    def make_request(
            url: str, parameters: Dict[str, Any], headers: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Makes an HTTP GET request and returns the response as JSON.

        Args:
            url (str): The URL to make the request to.
            parameters (Dict[str, Any]): The request parameters.
            headers (Dict[str, str]): The request headers.

        Returns:
            Dict[str, Any]: The JSON response.
        """
        return requests.get(
            url,
            params=parameters,
            headers=headers
        ).json()
