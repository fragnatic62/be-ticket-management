from pydantic import BaseModel, EmailStr


class FetchUserBaseModel(BaseModel):
    """
    Represents a base model for fetching user data.

    Attributes:
        _collection: collection name
    """
    _collection: str = 'Users'

    @property
    def collection(self) -> str:
        return self._collection


class FetchUserRequest(FetchUserBaseModel):
    """
    Represents a request model for fetching user data.

    Attributes:
        email: email of the user to fetch
    """
    email: EmailStr


class FetchUserResponse(BaseModel):
    """
    Represents a response model for fetching user data.

    Attributes:
        id: id of the user
        email: email of the user
        first_name: first name of the user
        last_name: last name of the user
    """
    id: str
    email: EmailStr
    first_name: str
    last_name: str
