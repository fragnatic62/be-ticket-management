from pydantic import BaseModel

from app.core.schema.user import BaseUserModel


class UserCreateRequest(BaseUserModel):
    """
    Represents a request object for creating a new user.

    Attributes:
        _id (str): The unique identifier of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
    """


class UserCreateResponse(BaseModel):
    """
    Represents a response object for creating a new user.

    Attributes:
        id (str): The unique identifier of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
    """
    id: str
    first_name: str
    last_name: str
    email: str
