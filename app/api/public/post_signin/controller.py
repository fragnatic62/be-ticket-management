import hashlib
import bcrypt
from datetime import datetime
from http import HTTPMethod
from typing import List

from pymongo.collection import Collection

from app.api.public.post_signin.models import SignInRequest, SignInResponse, CollectionEnum
from app.core.api.base_controller import BaseAPIController
from app.core.common.config import config
from app.services.tm_db.provider import TMMongoDBServiceProvider


class APIController(
    BaseAPIController[SignInRequest, SignInResponse],
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
        return '/post_signin'

    def get_method(self) -> str:
        """
        return HTTP method intended
        """
        return HTTPMethod.POST

    @staticmethod
    def _password_match(text_plain_password: bytes, salt: bytes, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(
            hashlib.pbkdf2_hmac('sha256', text_plain_password, salt, 14),
            hashed_password
        )

    @staticmethod
    def _generate_auth_token(token: bytes) -> str:
        return hashlib.sha256(token+bcrypt.gensalt()).hexdigest()

    def process_request(self, request: SignInRequest) -> SignInResponse:
        try:
            nosql_service: Collection = self.get_mongodb_service_from_collection(CollectionEnum.AuthCredentials.value)
            user_cred = nosql_service.find_one({'email': request.email})

            if not self._password_match(
                    request.password.encode('utf-8'),
                    user_cred.get('salt'),
                    user_cred.get('password')
            ):
                raise Exception('Invalid password')

            auth_token = self._generate_auth_token(user_cred.get('token'))
            token_expires = datetime.utcnow().timestamp() + config.AUTH_TOKEN_EXPIRY

            nosql_service.update_one(
                {'email': request.email},
                {'$set': {
                    'auth_token': auth_token,
                    'token_expires': token_expires,
                    'is_signed_in': True
                }}
            )
            return SignInResponse(auth_token=auth_token, token_expires=token_expires)
        except Exception as e:
            raise e

    def validate_request(self, request: SignInRequest) -> bool:
        """
        Validate the email  field if it has record on Users and Auth collection.
        """
        nosql_service: Collection = self.get_mongodb_service_from_collection(CollectionEnum.Users.value)
        return bool(nosql_service.find_one({'email': request.email}))

