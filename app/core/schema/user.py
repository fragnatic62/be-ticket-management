from typing import Mapping, Optional, Sequence

from pydantic import BaseModel, EmailStr
from pymongo import ASCENDING

# Do not change the value of this constant.
# This is the collection name in the database.
USER_COLLECTION: str = 'Users'


class BaseUserModel(BaseModel):
    """
    Base class for representing user models.

    Attributes:
        _id (str): The unique identifier of the user.
        _collection (str): The collection/table name of the user.
    """
    _id: str
    _collection: str = USER_COLLECTION
    first_name: str
    last_name: str
    email: EmailStr

    @property
    def collection(self):
        return self._collection

    @property
    def id(self):
        return self._id

    class Config:
        """
        Pydantic model configuration.

        Attributes:
            indexes (List[str]): The list of fields to be indexed.
        """
        indexes: Mapping[str, Optional[Sequence]] = {
            'index': None,
            'unique_index': [[('email', ASCENDING)], ],
            'composite_index': None,
        }
