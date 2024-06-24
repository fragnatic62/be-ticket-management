import importlib
import os
import logging
from abc import ABC
from http import HTTPStatus
from fastapi import HTTPException
from typing import TypeVar, Generic, get_args, Optional, List, Union

from app.services.tm_db.provider import TMMongoDBServiceProvider
from app.core.common.base_schema import APIRequest, APIResponse, APIProcessReport
from app.core.api.base_delegate import BaseAPIControllerDelegate
from app.core.api.http_exceptions import (
    HTTP_CODE_424_EXCEPTION_LIST,
    HTTP_CODE_422_EXCEPTION_LIST,
    HTTP_CODE_500_EXCEPTION_LIST
)

logger = logging.getLogger('uvicorn')

IT = TypeVar('IT', bound=APIRequest)
OT = TypeVar('OT', bound=APIResponse)


# ApiController in class diagram
class BaseAPIController(Generic[IT, OT], ABC):
    """
    Base class for API controllers.

    Attributes:
        _full_dir (str): Full directory of the file, we will use this when
            determining the controller name later.
        delegate (APIControllerDelegate): The delegate responsible
            for handling API controller actions.
        is_cacheable (bool): Flag to determine if the response is cacheable.
        api_tags (List[str]): List of tags for the API controller.

    Methods:
        __init__(self, delegate: APIControllerDelegate) -> None:
                            Initialize the BaseAPIController with a delegate.
        get_request_type(self) -> IT:
                            Get the expected request type for the API controller.
        get_response_type(self) -> OT:
                            Get the expected response type for the API controller.
        get_controller(self) -> str:
                            Gets the name of the controller, done by getting the
                            current folder the file is stored on.
        get_path(self) -> str:
                            Get the API endpoint path handled by the controller.
        get_method(self) -> str:
                            Get the HTTP method associated with the API controller.
        process_request(request: IT) -> OT:
                            Process the API request and return the response.
        validate_request(request: IT) -> bool:
                            Validate the API request data.
        invoke(request: IT) -> OT:
                            Invoke the API request and return the response.

    Note:
        This class is intended to be used as a base class for specific API controllers,
        which should implement their own versions of the methods defined here.

    """
    _full_dir: str = __file__
    is_cacheable: bool = False
    api_tags: List[str] = []
    delegate: BaseAPIControllerDelegate

    def __init__(self, delegate: BaseAPIControllerDelegate) -> None:
        """
        Initialize the BaseAPIController with a delegate.

        Args:
            delegate (APIControllerDelegate): The delegate responsible for
            handling API controller actions.

        """
        self.delegate = delegate

    @classmethod
    def get_request_type(cls) -> IT:
        """
        Get the expected request type for the API controller.

        Returns:
            TypeVar: The type representing the expected request for the API controller.

        """
        return get_args(cls.__orig_bases__[0])[0]  # type: ignore

    @classmethod
    def get_response_type(cls) -> OT:
        """
        Get the expected response type for the API controller.

        Returns:
            TypeVar: The response type representing the expected response for the API controller.

        """
        return get_args(cls.__orig_bases__[0])[1]  # type: ignore

    def get_controller_name(self):
        full_path = os.path.realpath(self._full_dir)
        path, filename = os.path.split(full_path)
        return path.split(os.sep)[-1:][0]

    def get_api_tags(self) -> List[str]:
        """
        Get the tags for the API controller.

        Returns:
            Sequence[str]: The list of tags for the API controller.

        """
        return self.api_tags

    def get_path(self) -> str:
        """
        Get the API endpoint path handled by the controller.

        Returns:
            str: The API endpoint path associated with the controller.

        """
        raise NotImplementedError

    def get_method(self) -> str:
        """
        Get the HTTP method associated with the API controller.

        Returns:
            str: The HTTP method used for the API controller
            (e.g., 'GET', 'POST', 'PUT', 'DELETE').

        """
        raise NotImplementedError

    def process_request(self, request: IT) -> Union[List[OT], OT]:
        """
        Process the API request and return the response.

        Args:
            request (IT): The API request data.

        Returns:
            OT: The API response data.

        """
        raise NotImplementedError

    def validate_request(self, request: IT) -> bool:
        """
        Validate the API request data.

        Args:
            request (IT): The API request data.

        Returns:
            bool: True if the request data is valid; otherwise, False.

        """
        raise NotImplementedError

    @staticmethod
    def on_error(e: Exception) -> HTTPException:
        """
        Standardize return statement when api failed

        :param e:
        :return:
        """
        if isinstance(e, HTTP_CODE_424_EXCEPTION_LIST):
            return HTTPException(status_code=424, detail=str(e))

        elif isinstance(e, HTTP_CODE_422_EXCEPTION_LIST):
            return HTTPException(status_code=422, detail=str(e))

        elif isinstance(e, HTTP_CODE_500_EXCEPTION_LIST):
            return HTTPException(status_code=500, detail=str(e))

        else:
            return HTTPException(status_code=500, detail=str(e))

    def invoke(self, request: IT) -> Optional[Union[OT, List[OT]]]:
        """
        Invoke the API request and return the response.

        Args:
            request (IT): The API request data.

        Returns:
            OT: The API response data.

        """
        output: Optional[APIResponse] = None

        try:
            self.validate_request(request)

            output: Union[OT, List[OT]] = self.process_request(request)

            self.delegate.on_process_finished(
                APIProcessReport(
                    status_code=HTTPStatus.OK,
                    response=output,
                    message=None,
                    request=request
                )
            )

            return output

        except Exception as e:
            http_exception: HTTPException = self.on_error(e)
            self.delegate.on_process_failure(APIProcessReport(
                status_code=http_exception.status_code,
                response=output,
                message=str(e),
                request=request
            ))

            logger.warning(f'BaseController Exception(APIRequest body): {request.model_dump_json()}')
            logger.warning(f'BaseController Exception(Exception): {str(e)}')

            raise http_exception


class APIControllerFactory(TMMongoDBServiceProvider):
    _controller_map: dict[str, BaseAPIController] = {}

    @staticmethod
    def _build_delegate(name: str, version: str) -> BaseAPIControllerDelegate:
        module = importlib.import_module(
            f'app.api.{version.replace(".", "_")}.{name}.delegate'
        )
        return getattr(module, 'APIControllerDelegate')()

    @staticmethod
    def _build_controller(name: str,
                          version: str,
                          delegate: BaseAPIControllerDelegate) -> BaseAPIController:
        module = importlib.import_module(
            f'app.api.{version.replace(".", "_")}.{name}.controller'
        )
        return getattr(module, 'APIController')(delegate)

    def get_controller(self, name: str, version: str) -> BaseAPIController:
        identifier = f'{name}_{version}'

        if not self._controller_map.get(identifier):

            # Build the delegate
            delegate = self._build_delegate(name, version)

            # Build the controller
            controller = self._build_controller(name, version, delegate)

            self._controller_map[identifier] = controller

            if isinstance(controller, TMMongoDBServiceProvider):
                controller.set_mongodb_service_pool(self.get_mongodb_service_pool())

            return controller

        else:
            return self._controller_map[identifier]
