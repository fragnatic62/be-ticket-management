from http import HTTPMethod
from typing import List

from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from app.api.public.post_create_user.exceptions import PostCreateUserException, CreateUserException
from app.api.public.post_create_user.models import UserCreateRequest, UserCreateResponse
from app.core.api.base_controller import BaseAPIController
from app.services.tm_db.provider import TMMongoDBServiceProvider


class APIController(
    BaseAPIController[UserCreateRequest, UserCreateResponse],
    TMMongoDBServiceProvider
):
    """
    **Synchronous API endpoint for fetching completeness summary**

    API request attributes:
        schedule_date (date): The date of the schedule.
        retailers (Array[str]): The list of retailers. e.g. ['amazon.com', 'walmart.com']

    """
    _full_dir: str = __file__
    api_tags: List[str] = ['Synchronous API']

    def get_path(self) -> str:
        return '/post_create_user'

    def get_method(self) -> str:
        """
        return HTTP method intended
        """
        return HTTPMethod.POST

    def process_request(self, request: UserCreateRequest) -> UserCreateResponse:
        try:
            nosql_service: Collection = self.get_mongodb_service_from_collection(request.collection)
            inserted_id: str = nosql_service.insert_one(request.model_dump()).inserted_id.__str__()

            return UserCreateResponse(
                id=inserted_id,
                first_name=request.first_name,
                last_name=request.last_name,
                email=request.email
            )
        except DuplicateKeyError:
            raise PostCreateUserException('User already exists.')

        except Exception as e:
            raise CreateUserException(str(e)) from e

    def validate_request(self, request: UserCreateRequest) -> bool:
        return True
