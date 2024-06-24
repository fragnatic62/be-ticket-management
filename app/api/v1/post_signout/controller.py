from http import HTTPMethod
from typing import List

from pymongo.collection import Collection

from app.api.v1.post_signout.models import SignOutUserRequest, SignOutUserResponse
from app.core.api.base_controller import BaseAPIController
from app.services.tm_db.provider import TMMongoDBServiceProvider


class APIController(
    BaseAPIController[SignOutUserRequest, SignOutUserResponse],
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
        return '/post_sign_out'

    def get_method(self) -> str:
        """
        return HTTP method intended
        """
        return HTTPMethod.POST

    def process_request(self, request: SignOutUserRequest) -> SignOutUserResponse:
        try:
            nosql_service: Collection = self.get_mongodb_service_from_collection(request.collection)
            user_cred = nosql_service.find_one({'auth_token': request.token})

            if not user_cred:
                raise Exception('Invalid token')

            nosql_service.update_one(
                {'auth_token': request.token},
                {'$set': {
                    'auth_token': 'NOT_SET',
                    'token_expires': 0.00,
                    'is_signed_in': False
                }}
            )

            return SignOutUserResponse(message=f'User {user_cred.get("email")} has been signed out.')
        except Exception as e:
            raise e

    def validate_request(self, request: SignOutUserRequest) -> bool:
        """
        Validate the email  field if it has record on Users and Auth collection.
        """
        return True
