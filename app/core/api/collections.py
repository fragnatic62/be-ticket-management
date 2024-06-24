from enum import Enum


class DBCollectionEnum(Enum):
    """
    Enum class for collections in the database

    DO NOT EDIT THIS CLASS

    Notes:
        - Do not change the values of the enum members as they are used as collection names in the database
        - The values of the enum members should be unique
        - The values of the enum members should be in PascalCase

    Attributes:
        USERS: users collection
        AUTH_CREDENTIALS: auth credentials collection
        COMPANIES: companies collection
        BOARDS: boards collection
        TASKS: tasks collection
    """
    USERS: str = 'Users'
    AUTH_CREDENTIALS: str = 'AuthCredentials'
    COMPANIES: str = 'Companies'
    BOARDS: str = 'Boards'
    TASKS: str = 'Tasks'
