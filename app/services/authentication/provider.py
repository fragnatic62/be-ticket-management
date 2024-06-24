from app.services.authentication.service import AuthenticationService


class AuthenticationServiceProvider:
    _auth_service: AuthenticationService

    def get_auth_service(self) -> AuthenticationService:
        """
        Get the AuthenticationService instance.

        Returns:
        - AuthenticationService: The AuthenticationService instance.
        """
        return self._auth_service

    def set_auth_service(self, service: AuthenticationService):
        """
        Set the AuthenticationService instance.

        Parameters:
        - service (AuthenticationService): The AuthenticationService instance to set.
        """
        self._auth_service = service
