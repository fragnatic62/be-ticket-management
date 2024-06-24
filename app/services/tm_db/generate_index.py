from typing import Callable, Sequence, Optional

from pymongo.collection import Collection


class MongoDBIndexService:
    """
    Service class for generating indexes for MongoDB collections.
    """
    _service_from_factory: Optional[Collection] = None

    def _generate_unique_index(self, indexes: Sequence):
        """
        Generates a unique index for the specified collection.

        Args:
            indexes : The indexes to be generated.
        """
        for index in indexes:
            self._service_from_factory.create_index(index, unique=True)

    def _generate_index(self, indexes: Sequence):
        """
        Generates an index for the specified collection.

        Args:
            indexes : The indexes to be generated.
        """
        self._service_from_factory.create_index(indexes)

    def _generate_composite_index(self, indexes: Sequence):
        """
        Generates a composite index for the specified collection.

        Args:
            indexes : The indexes to be generated.
        """
        self._service_from_factory.create_index(indexes, unique=True)

    def _unset_service(self):
        """
        Unset the service.
        """
        self._service_from_factory = None

    def generate_indexes(self, schema, service_from_factory):
        """
        Generates indexes for the specified collection.

        Args:
            schema : The class for which the indexes are to be generated.
            service_from_factory : The service from instantiated factory to get the MongoDB service.
        """

        if hasattr(schema, 'Config'):
            indexes = getattr(schema.Config, 'indexes', {})

            if indexes:
                collection_name: str = schema._collection.get_default()  # noqa
                self._service_from_factory = service_from_factory.get_mongodb_service_from_collection(collection_name)

                if indexes.get('index'):
                    self._generate_index(indexes.get('index'))
                if indexes.get('unique_index'):
                    self._generate_unique_index(indexes.get('unique_index'))
                if indexes.get('composite_index'):
                    self._generate_composite_index(indexes.get('composite_index'))

        self._unset_service()

        # Starting here, don't do anything
        def decorator(cls):
            return cls

        return decorator
