from typing import Dict

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.core.common.config import config


class TMMongoDBServicePool:
    """
    Pool for managing MongoDB instances for different clients.

    Attributes:
    - _service_pool (Dict[str, MongoClient]): Dictionary to store MongoClient instances for each client.
    """
    _service_pool: Dict[str, Collection] = {}

    @staticmethod
    def _get_mongodb_client() -> Database:
        """
        Get the MongoDB configuration based on the collection.

        Parameters:
        - collection (str): The collection for which the MongoDB configuration is needed.

        Returns:
        - Database: The MongoDB configuration.
        """
        _nosql_server: str = f'mongodb://{config.NOSQL_USER}:{config.NOSQL_PWD}@{config.NOSQL_URL}'

        return MongoClient(_nosql_server, config.NOSQL_PORT)[config.NOSQL_DB]

    def get_mongodb_service(self, collection: str) -> Collection:
        """
        Get the MongoDB instance for the specified collection.

        Parameters:
        - collection (str): The collection for which the MongoDB instance is needed.

        Returns:
        - Collection: The MongoDB instance for the specified collection.
        """
        if collection not in self._service_pool:
            self._service_pool[collection] = self._get_mongodb_client()[collection]

        return self._service_pool[collection]
