from abc import ABC, abstractmethod
from typing import Generic, Dict, TypeVar, Optional

from .dataset import DataSet

D = TypeVar('D', bound=DataSet)


class DataSource(Generic[D], ABC):
    """
    Abstract base class representing a generic data source
    that manages multiple datasets.
    """

    @abstractmethod
    def connect(self, **kwargs) -> None:
        """
        Establish connection to the data source.

        Args:
            **kwargs: Arbitrary keyword arguments for connection parameters.
        """
        pass

    @abstractmethod
    def disconnect(self, **kwargs) -> None:
        """
        Disconnect from the data source.

        Args:
            **kwargs: Arbitrary keyword arguments for disconnection parameters.
        """
        pass

    @abstractmethod
    def get_dataset(self, name: str) -> Optional[D]:
        """
        Retrieve a dataset by its name.

        Args:
            name (str): The dataset name.

        Returns:
            Optional[D]: The dataset instance or None if not found.
        """
        pass

    @abstractmethod
    def get_datasets(self) -> Dict[str, D]:
        """
        Retrieve all datasets managed by this data source.

        Returns:
            Dict[str, D]: Mapping of dataset names to dataset instances.
        """
        pass

    @abstractmethod
    def create_dataset(self, name: str) -> D:
        """
        Create a new dataset with the given name.

        Args:
            name (str): The name of the new dataset.

        Returns:
            D: The newly created dataset instance.
        """
        pass

    @abstractmethod
    def delete_dataset(self, name: str) -> bool:
        """
        Delete a dataset by its name.

        Args:
            name (str): The dataset name.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        pass
