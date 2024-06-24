import hashlib
import bcrypt
from datetime import datetime
from http import HTTPMethod
from typing import List

from pymongo.collection import Collection

from app.api.public.post_refresh_token.models import RefreshTokenRequest, RefreshTokenResponse
from app.core.api.base_controller import BaseAPIController
from app.core.common.config import config
from app.services.tm_db.provider import TMMongoDBServiceProvider


class APIController(
    BaseAPIController[RefreshTokenRequest, RefreshTokenResponse],
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
        return '/post_refresh_token'

    def get_method(self) -> str:
        """
        return HTTP method intended
        """
        return HTTPMethod.POST

    @staticmethod
    def _generate_auth_token(token: bytes) -> str:
        return hashlib.sha256(token+bcrypt.gensalt()).hexdigest()

    def process_request(self, request: RefreshTokenRequest) -> RefreshTokenResponse:
        try:
            nosql_service: Collection = self.get_mongodb_service_from_collection(request.collection)
            user = nosql_service.find_one({'auth_token': request.token})

            if not user:
                raise Exception('Invalid token. Please sign in again.')

            auth_token = self._generate_auth_token(user.get('token'))
            token_expires = datetime.utcnow().timestamp() + config.AUTH_TOKEN_EXPIRY

            nosql_service.update_one(
                {'auth_token': request.token},
                {'$set': {
                    'auth_token': auth_token,
                    'token_expires': token_expires
                }}
            )
            return RefreshTokenResponse(auth_token=auth_token, token_expires=token_expires)
        except Exception as e:
            raise e

    def validate_request(self, request: RefreshTokenRequest) -> bool:
        """
        Validate the email  field if it has record on Users and Auth collection.
        """
        return True

