from datetime import datetime
from typing import Optional, Sequence, List

from pydantic import BaseModel


class Task(BaseModel):
    """
    Represents a request model for creating a company tasks.

    Attributes:
        name: task name
        description: task description
        position: task position
        date_created: date created
        date_updated: date updated
    """
    position: int
    name: str
    description: str
    board_id: str
    date_created: datetime = datetime.now()
    date_updated: Optional[datetime] = None


class Board(BaseModel):
    """
    Represents a board model.

    Attributes:
        position: board position
        name: board name
        description: board description
        date_created: date created
        date_updated: date updated
        tasks: tasks
    """
    position: int
    name: str
    description: str
    company_id: str
    date_created: datetime = datetime.now()
    date_updated: Optional[datetime] = None
    tasks: Sequence[Task] = []


class Company(BaseModel):
    """
    Represents a company model.

    Attributes:
        id: company id
        name: company name
        email: company email
        description: company description
        date_created: date created
        date_updated: date updated
        boards: boards
    """
    id: str
    name: str
    email: Optional[str] = None
    description: str
    date_created: datetime
    date_updated: Optional[datetime] = None
    boards: Sequence[Board] = []


class FetchCompaniesRequest(BaseModel):
    """
    Represents a request model for fetching companies.

    Attributes:
        page: page
        page_size: page size
    """
    page: int = 1
    page_size: int = 10


class FetchCompaniesResponse(BaseModel):
    """
    Represents a response model for fetching companies and company data.

    Attributes:
        results: results
        page: page
        page_size: page size
        total_count: total count
    """
    results: List[Company] = []
    page: int
    page_size: int
    total_count: int
