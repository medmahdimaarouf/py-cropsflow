from typing import Union, List, Dict, Optional

from bson import ObjectId
from cropsflow.data import DataSet
from cropsflow.data.abstracts.dataset import I
from pymongo.collection import Collection


class MongoDataSet(DataSet):
    collection: Collection = None

    def __init__(self, collection: Collection):
        super().__init__(name=collection.name)
        self.collection = collection

    def find_one(self, query: dict[any, any]) -> Optional[Dict]:
        """
       Retrieve a document by its index (_id or custom index).
       """
        document = self.collection.find_one(query=query)
        return document.__dict__ if document is not None else None

    def find_all(self, query: dict[any, any]) -> list[Dict]:
        """
        Find documents matching the query.
        """
        documents = list(self.collection.find(query))
        return [doc.__dict__ for doc in documents]

    def save(self, data: Dict) -> None:
        """
        Save a DataModel instance to the collection.
        If the data has an _id, it will update the existing document.
        Otherwise, it will insert a new document.
        """
        return self.collection.insert_one(document=data)

    def update(self, index: I, data: Dict) -> None:
        """
        Update an existing document by its index (_id).
        """
        return self.collection.find_one_and_update(
            {"_id": ObjectId(index) if isinstance(index, str) else index},
            {"$set": data},
            return_document=True
        )

    def delete(self, index: I) -> None:
        """
        Delete a document by its index (_id).
        """
        return self.collection.find_one_and_delete({"_id": ObjectId(index) if isinstance(index, str) else index})
