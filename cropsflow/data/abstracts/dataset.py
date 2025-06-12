"""
Abstract base class for a generic dataset with CRUD operations.
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Dict, Optional, List

I = TypeVar('I')


class DataSet(Generic[I], ABC):
    """
    Generic abstract base class representing a dataset with CRUD methods.

    Attributes:
        name (str): The name identifier of the dataset.
    """

    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def find_one(self, query: Dict) -> Optional[Dict]:
        """
        Find a single record matching the query.

        Args:
            query (Dict): The search query.

        Returns:
            Optional[Dict]: The first matching record or None.
        """
        pass

    @abstractmethod
    def find_all(self, query: Dict) -> List[Dict]:
        """
        Find all records matching the query.

        Args:
            query (Dict): The search query.

        Returns:
            List[Dict]: List of all matching records.
        """
        pass

    @abstractmethod
    def save(self, data: Dict) -> None:
        """
        Save a new record.

        Args:
            data (Dict): The data to save.
        """
        pass

    @abstractmethod
    def delete(self, index: I) -> None:
        """
        Delete a record by its index.

        Args:
            index (I): The identifier of the record to delete.
        """
        pass

    @abstractmethod
    def update(self, index: I, data: Dict) -> None:
        """
        Update a record by its index.

        Args:
            index (I): The identifier of the record to update.
            data (Dict): The new data to update.
        """
        pass
