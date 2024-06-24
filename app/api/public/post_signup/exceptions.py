from app.core.common.base_exception import BaseCustomException


class PostSignUpException(BaseCustomException):
    """
    Base exception for post_create_user
    """


class SignUpException(PostSignUpException):
    """
    Raise when error occurs during creating user.
    """