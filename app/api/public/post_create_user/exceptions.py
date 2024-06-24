from app.core.common.base_exception import BaseCustomException


class PostCreateUserException(BaseCustomException):
    """
    Base exception for post_create_user
    """


class CreateUserException(PostCreateUserException):
    """
    Raise when error occurs during creating user.
    """