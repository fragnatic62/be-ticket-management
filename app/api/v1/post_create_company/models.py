from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.core.api.collections import DBCollectionEnum


class PostCreateCompanyBaseModel(BaseModel):
    """
    Represents a base model for creating a company.

    Attributes:
        _collection: collection name
    """
    _collection: str = DBCollectionEnum.COMPANIES.value

    @property
    def collection(self) -> str:
        return self._collection


class PostCreateCompanyRequest(PostCreateCompanyBaseModel):
    """
    Represents a request model for creating a company.

    Attributes:
        name: company name
        email: company email
        description: company description
        date_created: date created
        date_updated: date updated
    """
    name: str
    email: Optional[str] = None
    description: str
    date_created: datetime = datetime.now()
    date_updated: Optional[datetime] = None


class PostCreateCompanyResponse(BaseModel):
    """
    Represents a response model for creating a company.

    Attributes:
        id: company id
        name: company name
        email: company email
        description: company description
    """
    id: str
    name: str
    email: Optional[str] = None
    description: str
    date_created: datetime
    date_updated: Optional[datetime]
