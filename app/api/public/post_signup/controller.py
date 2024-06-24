import hashlib
from http import HTTPMethod
from typing import List

import bcrypt
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from app.api.public.post_signup.exceptions import PostSignUpException, SignUpException
from app.api.public.post_signup.models import AuthCredentialCreateRequest, AuthCredentialCreateResponse
from app.core.api.base_controller import BaseAPIController
from app.core.schema.auth import PrivateAuthInfo
from app.services.tm_db.provider import TMMongoDBServiceProvider


class APIController(
    BaseAPIController[AuthCredentialCreateRequest, AuthCredentialCreateResponse],
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
        return '/post_signup'

    def get_method(self) -> str:
        """
        return HTTP method intended
        """
        return HTTPMethod.POST

    @staticmethod
    def _generate_password(text_plain_password: bytes, salt: bytes) -> bytes:
        return bcrypt.hashpw(
            hashlib.pbkdf2_hmac('sha256', text_plain_password, salt, 14),
            bcrypt.gensalt(14)
        )

    def process_request(self, request: AuthCredentialCreateRequest) -> AuthCredentialCreateResponse:
        try:
            auth_request: PrivateAuthInfo = PrivateAuthInfo(**request.model_dump())

            nosql_service: Collection = self.get_mongodb_service_from_collection(auth_request.collection)
            auth_request.password = self._generate_password(auth_request.password, auth_request.salt)

            nosql_service.insert_one(auth_request.model_dump())

            return AuthCredentialCreateResponse(message='User created successfully')

        except DuplicateKeyError:
            raise PostSignUpException('User already exists.')

        except Exception as e:
            raise SignUpException(str(e)) from e

    def validate_request(self, request: AuthCredentialCreateRequest) -> bool:
        """
        Validate the email and user_id fields if it has record on Users collection.
        """
        nosql_service: Collection = self.get_mongodb_service_from_collection('Users')
        return bool(nosql_service.find_one({'email': request.email}))
