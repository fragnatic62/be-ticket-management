from pydantic import BaseModel


class SignOutUserBaseModel(BaseModel):
    """
    Represents a base model for fetching user data.

    Attributes:
        _collection: collection name
    """
    _collection: str = 'AuthCredentials'

    @property
    def collection(self) -> str:
        return self._collection


class SignOutUserRequest(SignOutUserBaseModel):
    """
    Represents a request model for fetching user data.

    Attributes:
        token: email of the user to fetch
    """
    token: str


class SignOutUserResponse(BaseModel):
    """
    Represents a response model for fetching user data.
    """
    message: str
