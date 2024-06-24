import binascii
import os

import bcrypt
from pydantic import BaseModel, EmailStr

from app.core.schema.auth import PublicAuthInfo


class AuthCredentialCreateRequest(PublicAuthInfo):
    """
    Represents the public information of a user including the user's information.

    Attributes:
        email (EmailStr): The email address of the user.
        password (bytes): The hashed password of the user.
    """


class AuthCredentialCreateResponse(BaseModel):
    """
    Represents a response object for creating a new user.

    Attributes:
        message (str): The message indicating the success of the operation.
    """
    message: str
