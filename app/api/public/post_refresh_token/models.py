from pydantic import BaseModel

from app.core.schema.auth import BaseAuthCredential


class RefreshTokenRequest(BaseAuthCredential):
    """
    Represents the request object for the refresh token request.

    Attributes:
        token (str): The refresh token.
    """
    token: str


class RefreshTokenResponse(BaseModel):
    """
    Represents the response object for the sign-in request.

    Attributes:
        auth_token (str): The access token.
        token_expires (int): The token expiration time.
    """
    auth_token: str
    token_expires: float
