from http import HTTPMethod
from typing import List

from pymongo.collection import Collection

from app.api.v1.fetch_user_by_email.models import FetchUserRequest, FetchUserResponse
from app.core.api.base_controller import BaseAPIController
from app.services.tm_db.provider import TMMongoDBServiceProvider


class APIController(
    BaseAPIController[FetchUserRequest, FetchUserResponse],
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
        return '/fetch_user_by_email'

    def get_method(self) -> str:
        """
        return HTTP method intended
        """
        return HTTPMethod.POST

    def process_request(self, request: FetchUserRequest) -> FetchUserResponse:
        try:
            nosql_service: Collection = self.get_mongodb_service_from_collection(request.collection)
            user = nosql_service.find_one({'email': request.email})

            return FetchUserResponse(
                id=str(user.get('_id')),
                first_name=user.get('first_name'),
                last_name=user.get('last_name'),
                email=user.get('email')
            )
        except Exception as e:
            raise e

    def validate_request(self, request: FetchUserRequest) -> bool:
        """
        Validate the email  field if it has record on Users and Auth collection.
        """
        return True
