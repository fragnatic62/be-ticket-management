from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.core.api.collections import DBCollectionEnum


class PostUpdateBoardBaseModel(BaseModel):
    """
    Represents a base model for creating a company.

    Attributes:
        _collection: collection name
    """
    _collection: str = DBCollectionEnum.BOARDS.value

    @property
    def collection(self) -> str:
        return self._collection


class PostUpdateBoardRequest(PostUpdateBoardBaseModel):
    """
    Represents a request model for creating a company task board.

    Attributes:
        position: board position
        name: board name
        description: board description
        date_created: date created
        date_updated: date updated
    """
    id: str
    position: int
    name: str
    description: str
    date_created: datetime = datetime.now()
    date_updated: Optional[datetime] = None


class PostUpdateBoardResponse(BaseModel):
    """
    Represents a response model for creating a company task board.

    Attributes:
        name: board name
        position: board position
        description: board description
        date_created: date created
        date_updated: date updated
    """
    id: str
    position: int
    name: str
    description: str
    company_id: str
    date_created: datetime
    date_updated: Optional[datetime] = None
