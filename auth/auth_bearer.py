# FastAPI Imports
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Own Imports
from auth.auth_handler import AuthHandler


# Initialize auth handler
authentication = AuthHandler()


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        """
        The method __init__() is a constructor of the class JWTBearer

        :param auto_error: If True, the middleware will raise an error if the token is invalid. If
        False, the middleware will return a 401 response, defaults to True

        :type auto_error: bool (optional)
        """
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """
        This method checks if the credentials are valid,
        return the credentials. If not, raise an exception.

        :param request: The request object
        :type request: Request

        :return: The token
        """
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(403, {"message": "Invalid authentication scheme."})

            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(403, {"message": "Invalid token or expired token."})

            return credentials.credentials
        else:
            raise HTTPException(403, {"message": "Invalid authorization code."})

    def verify_jwt_token(self, token: str) -> bool:
        """
        This method takes a JWT token as an argument, decodes it and returns a boolean value.

        :param token: The token that you want to verify
        :type token: str

        :return: A boolean value.
        """
        is_token_valid: bool = False
        payload = authentication.decode_jwt(token)

        if payload:
            is_token_valid = True
            return is_token_valid
        return is_token_valid