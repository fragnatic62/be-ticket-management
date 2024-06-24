import binascii
import os
from typing import Mapping, Sequence, Optional

import bcrypt
from pydantic import EmailStr, BaseModel
from pymongo import ASCENDING


class BaseAuthCredential(BaseModel):
    """
    Represents a request object for creating a new user.

    Attributes:
        _id (str): The unique identifier of the user.
        _collection (str): The collection/table name.
    """
    _id: str
    _collection: str = 'AuthCredentials'

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
            indexes (Mapping[str, Optional[Sequence]]): The list of fields to be indexed.
        """
        indexes: Mapping[str, Optional[Sequence]] = {
            'index': [('user_id', ASCENDING), ('auth_token', ASCENDING)],
            'unique_index': [[('email', ASCENDING)], ],
            'composite_index': None,
        }


class PublicAuthInfo(BaseAuthCredential):
    """
    Represents the public information of a user including the user's information.

    Attributes:
        email (EmailStr): The email address of the user.
        password (bytes): The hashed password of the user.
    """
    email: EmailStr
    password: bytes


class PrivateAuthInfo(PublicAuthInfo):
    """
    Represents the private information of a user including the user's information.

    Attributes:
        salt (bytes): The salt used for hashing the password.
        token (bytes): The token used for authentication.
        auth_token (str): The access token used for authentication.
        token_expires (int): The token expiration time.
        is_signed_in (bool): The flag indicating if the user is signed in.
    """
    token: bytes = binascii.hexlify(os.urandom(20))
    salt: bytes = bcrypt.gensalt(14)
    auth_token: str = 'NOT_SET'
    token_expires: float = 0.00
    is_signed_in: bool = False
