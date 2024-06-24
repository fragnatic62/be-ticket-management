from enum import Enum
from typing import Optional, TypeVar, Generic

from pydantic import BaseModel, Field


IT = TypeVar('IT', bound=BaseModel)
OT = TypeVar('OT', bound=BaseModel)


class DefaultAPIResponseStatus(Enum):
    """
    Enum class for default API response statuses.

    Attributes:
        OK (str): The 'OK' status.
        ENQUEUE (str): The 'ENQUEUE' status.
        ERROR (str): The 'ERROR' status.
    """
    OK: str = 'OK'
    ENQUEUE: str = 'ENQUEUE'
    ERROR: str = 'ERROR'


class APIRequest(BaseModel):
    """
    Base class for representing API requests.

    Note:
        This class inherits from the Pydantic BaseModel class, providing validation
        and serialization features
        for attributes defined in its subclasses.

    """
    company_code: str


class APIListRequest(BaseModel):
    """
    Represents a request object for API calls that involve pagination.

    Attributes:
        limit (int): The maximum number of items to retrieve in a single API call (default: 50).
        offset (int): The offset from the beginning of the list for pagination (default: 0).
    """
    limit: int = 50
    offset: int = 0


class APIResponse(BaseModel):
    """
    Base class for representing API responses.

    Note:
        This class inherits from the Pydantic BaseModel class, providing
        validation and serialization features
        for attributes defined in its subclasses.

    """
    error: Optional[str] = None
    status: DefaultAPIResponseStatus = Field(default=DefaultAPIResponseStatus.OK)


class APIListResponse(APIResponse):
    """
    Base class for representing API responses.

    Attributes:
        limit (int): The maximum number of items to retrieve in a single API call.
        offset (int): The offset from the beginning of the list for pagination.
        total (int): The total number of items in the list.

    """
    limit: int = 0
    offset: int = 0
    total: int = 0


class APIProcessReport(BaseModel, Generic[IT, OT]):
    """
    Represents a report of an API process.

    Attributes:
        status_code (int): The HTTP status code of the API response.
        response (APIResponse): APIResponse object representing the API response data.
        message (Optional[str]): An optional message associated with the process report.

    Properties:
        is_success (bool): A boolean indicating whether the API process was successful.

    Note:
        The 'is_success' property always returns True for this class.

    """

    status_code: int
    request: Optional[IT]
    response: Optional[OT]
    message: Optional[str]

    @property
    def is_success(self) -> bool:
        """
        Check if the API process was successful.

        Returns:
            bool: True, indicating the API process was successful.
        """
        return True
