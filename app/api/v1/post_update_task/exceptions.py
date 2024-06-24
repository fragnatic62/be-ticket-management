from app.core.common.base_exception import BaseCustomException


class PostUpdateBoardException(BaseCustomException):
    """
    Base exception for post_create_user
    """


class UpdateBoardException(PostUpdateBoardException):
    """
    Raise when error occurs during creating user.
    """