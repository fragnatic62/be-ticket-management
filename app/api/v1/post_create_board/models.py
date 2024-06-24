from datetime import datetime
from typing import Optional, Sequence, Mapping

from pydantic import BaseModel
from pymongo import ASCENDING

from app.core.api.collections import DBCollectionEnum


class PostCreateBoardBaseModel(BaseModel):
    """
    Represents a base model for creating a company.

    Attributes:
        _collection: collection name
    """
    _collection: str = DBCollectionEnum.BOARDS.value

    @property
    def collection(self) -> str:
        return self._collection

    class Config:
        """
        Pydantic model configuration.

        Attributes:
            indexes (List[str]): The list of fields to be indexed.
        """
        indexes: Mapping[str, Optional[Sequence]] = {
            'index': None,
            'unique_index': None,
            'composite_index': [
                ('name', ASCENDING),
                ('company_id', ASCENDING),
                ('position', ASCENDING)
            ],
        }


class PostCreateBoardRequest(PostCreateBoardBaseModel):
    """
    Represents a request model for creating a company task board.

    Attributes:
        position: board position
        name: board name
        description: board description
        date_created: date created
        date_updated: date updated
    """
    position: int
    name: str
    description: str
    company_id: str
    date_created: datetime = datetime.now()
    date_updated: Optional[datetime] = None


class PostCreateBoardResponse(BaseModel):
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
