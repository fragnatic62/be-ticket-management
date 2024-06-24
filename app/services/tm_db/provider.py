from pymongo.collection import Collection

from app.core.api.collections import DBCollectionEnum
from app.services.tm_db.service import TMMongoDBServicePool


class TMMongoDBServiceProvider:

    _tm_mongo_db_service_pool: TMMongoDBServicePool

    def get_mongodb_service_pool(self) -> TMMongoDBServicePool:
        """
        Get the TMMongoDBServicePool instance.

        Returns:
        - TMMongoDBServicePool: The TMMongoDBServicePool instance.
        """
        return self._tm_mongo_db_service_pool

    def set_mongodb_service_pool(self, pool: TMMongoDBServicePool):
        """
        Set the TMMongoDBServicePool instance.

        Parameters:
        - pool (TMMongoDBServicePool): The TMMongoDBServicePool instance to set.
        """
        self._tm_mongo_db_service_pool = pool

    def get_mongodb_service_from_collection(self, collection: str) -> Collection:
        """
        Get the MongoDB service from the TMMongoDBServicePool based on the collection.

        Parameters:
        - collection (str): The collection for which the MongoDB service is needed.

        Returns:
        - Collection: The MongoDB service for the specified collection.
        """
        return self._tm_mongo_db_service_pool.get_mongodb_service(collection)
