from enum import Enum

from pydantic import BaseModel, EmailStr


class CollectionEnum(Enum):
    """
    CollectionEnum is a class that represents the collection names.

    Attributes:
        AuthCredentials (str): The AuthCredentials collection name.
        Users (str): The Users collection name.
    """
    AuthCredentials = 'AuthCredentials'
    Users = 'Users'


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class SignInResponse(BaseModel):
    """
    Represents the response object for the sign-in request.

    Attributes:
        auth_token (str): The access token.
        token_expires (int): The token expiration time.
    """
    auth_token: str
    token_expires: float
