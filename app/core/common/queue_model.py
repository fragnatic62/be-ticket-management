from abc import ABC
from typing import Dict, Generic, TypeVar, Optional, Union, Sequence
from pydantic import BaseModel

from app.core.common.log_models import LogTypeOptions

IT = TypeVar('IT', bound=BaseModel)
OT = TypeVar('OT', bound=BaseModel)


class LoadDataAbstractResponse(ABC, BaseModel):
    """
    Abstract base class for data loading responses.

    Parameters:
    ----------
    limit (int): The maximum number of items returned in a single request.
    offset (int): The starting index of the data in the complete dataset.
    total (int): The total number of items available in the dataset.

    """
    limit: int
    offset: int
    total: int


class APIToLoadRequestModel(BaseModel):
    """
    Represents a request model for loading data via API.

    Attributes:
    - class_name (str): The name of the class.
    - controller_name (str): The name of the controller.
    - version (str): The version of the API.
    - payload (Dict): Additional payload data.
    """
    class_name: str
    controller_name: str
    request_model_path: str
    version: str
    payload: Dict


class LoadDataProcessReport(BaseModel, Generic[OT]):
    """
    Report class for data loading processes.

    Parameters:
    ----------
    status_code (int): The HTTP status code indicating the success or failure of the data loading process.
    request (Optional[LoadDataAbstractRequest]): The actual data loading request object.
    response (Optional[LoadDataAbstractResponse]): The actual data loading response object.
    message (Optional[str]): A descriptive message about the outcome of the data loading process.
    is_success (bool): A boolean indicator of whether the data loading process was successful.
    """
    request: Optional[IT]
    response: Optional[Union[OT, Sequence[OT]]]
    message: Optional[str]
    is_success: bool
    log_type: LogTypeOptions
    controller_name: str

