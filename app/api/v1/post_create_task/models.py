from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.core.api.collections import DBCollectionEnum


class PostCreateTasksBaseModel(BaseModel):
    """
    Represents a base model for creating a company tasks.

    Attributes:
        _collection: collection name
    """
    _collection: str = DBCollectionEnum.TASKS.value

    @property
    def collection(self) -> str:
        return self._collection


class PostCreateTasksRequest(PostCreateTasksBaseModel):
    """
    Represents a request model for creating a company tasks.

    Attributes:
        name: task name
        description: task description
        position: task position
        board_id: board id
        date_created: date created
        date_updated: date updated
    """
    position: int
    name: str
    description: str
    board_id: str
    date_created: datetime = datetime.now()
    date_updated: Optional[datetime] = None


class PostCreateTaskResponse(BaseModel):
    """
    Represents a response model for creating a company tasks.

    Attributes:
        id: task id
        name: task name
        description: task description
        board_id: board id
        date_created: date created
        date_updated: date updated

    """
    id: str
    position: int
    name: str
    description: str
    board_id: str
    date_created: datetime
    date_updated: Optional[datetime] = None
