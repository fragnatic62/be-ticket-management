from app.core.common.base_exception import BaseCustomException


class PostCreateBoardException(BaseCustomException):
    """
    Base exception for post_create_user
    """


class CreateBoardException(PostCreateBoardException):
    """
    Raise when error occurs during creating user.
    """