import http
from datetime import datetime
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from app.services.tm_db.service import TMMongoDBServicePool


header_auth_token = APIKeyHeader(name='X-API-Key', auto_error=False)


class AuthenticationService:
    _mongo_db_service_provider: TMMongoDBServicePool = None

    def __init__(self, mongo_db_service: TMMongoDBServicePool):
        self._mongo_db_service_provider = mongo_db_service

    def _token_is_valid(self, auth_token: str) -> bool:
        """
        Validate the authentication token.

        Parameters:
        - auth_token (str): The authentication token.

        Returns:
        - bool: A boolean indicator of whether the token is valid.
        """
        mongo_db_service = self._mongo_db_service_provider.get_mongodb_service('AuthCredentials')
        user = mongo_db_service.find_one({'auth_token': auth_token})

        # Check if the token has expired
        return bool(user and user.get('token_expires') > datetime.utcnow().timestamp())

    def authenticate(self, auth_token: str = Security(header_auth_token)) -> bool:
        """
        Authenticate the user using the provided authentication token.

        Parameters:
        - auth_token (str): The authentication token.

        Returns:
        - bool: A boolean indicator of whether the user is authenticated.
        """
        if not self._token_is_valid(auth_token):
            raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail='Invalid API key or the key has expired.')

        return True
