from typing import Dict, Union
from pymongo import MongoClient
from pymongo.database import Database
from cropsflow.common import service, InjectionScope
from cropsflow.data import DataSource

from .dataset import MongoDataSet


@service(scope=InjectionScope.DEFAULT)
class MongoDataSource(DataSource[MongoDataSet]):
    db: Database
    client: MongoClient

    def __init__(self):
        self.client: MongoClient = None
        self.db: Database = None

    def connect(self, uri: str, db: str) -> None:
        """
        Connect to the MongoDB server and select the specified database.
        """
        self.client = MongoClient(host=uri, connect=True)
        self.client.server_info()  # To raise an error if the connection fails
        self.db = self.client[db]

    def disconnect(self, **args) -> None:
        self.client.close()

    def get_dataset(self, name: str) -> Union[MongoDataSet, None]:
        """
        Retrieve a dataset (collection) by name.
        """
        if self.db is not None:
            collection = self.db.get_collection(name=name.strip())
            if collection is not None:
                return MongoDataSet(collection)
            else:
                raise Exception(f"Could not find Mongo collection name: '{name.strip()}'")
        else:
            raise Exception("Database connection is not established.")

    def get_datasets(self) -> Dict[str, MongoDataSet]:
        """
        Retrieve all datasets (collections) as a dictionary.
        The key is the collection name, and the value is the MongoDataSet.
        """
        datasets = {}
        if self.db:
            for collection_name in self.db.list_collection_names():
                datasets.setdefault(collection_name, self.db.create_collection(name=collection_name))
        return datasets

    def create_dataset(self, name: str) -> MongoDataSet:
        """
        Create a new dataset (collection) with the specified name.
        """
        if self.db is not None:
            collection = self.db.create_collection(name=name.strip())
            return MongoDataSet(collection)
        raise Exception("Database connection is not established.")

    def delete_dataset(self, name: str) -> bool:
        """
        Delete a dataset (collection) by name.
        """
        if self.db is not None:
            return True if self.db.drop_collection(name) else False
        else:
            raise Exception("Database connection is not established.")
