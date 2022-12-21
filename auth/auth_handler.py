# Stdlib Imports
from datetime import datetime, timedelta
from typing import Dict, Any, Union

# FastAPI Imports
from fastapi import HTTPException

# PyJWT Imports
import jwt

# Third Party Imports
from core.settings import ledger_settings


# JWT Env Definitions
JWT_SECRET = ledger_settings.JWT_SECRET_KEY
JWT_ALGORITHM = ledger_settings.JWT_ALGORITHM
TOKEN_LIFETIME = ledger_settings.TOKEN_LIFETIME


class AuthHandler:
    """
    Responsible for:

    - signing,
    - encoding/decoding of tokens
    """

    def __init__(
        self,
        secret: str = JWT_SECRET,
        algorithm: str = JWT_ALGORITHM,
        token_lifetime: int = TOKEN_LIFETIME,
    ):
        """
        This method initializes the class with the secret,
        algorithm, and token lifetime.

        :param secret: The secret key used to sign the JWT
        :type secret: str

        :param algorithm: The algorithm used to sign the token
        :type algorithm: str

        :param token_lifetime: The lifetime of the token in seconds
        :type token_lifetime: int
        """
        self.JWT_SECRET = secret
        self.JWT_ALGORITHM = algorithm
        self.TOKEN_LIFETIME = token_lifetime

    def sign_jwt(self, user_id: int) -> Dict[str, Any]:
        """
        This method creates a JWT token with a user_id and expiration date,
        signs it with a secret key, and returns a response with the token.

        :param user_id: The user's ID
        :type user_id: int

        :return: A dictionary with the token and the expiration time.
        """
        payload = {
            "user_id": user_id,
            "expires": str(
                datetime.now() + timedelta(minutes=self.TOKEN_LIFETIME)
            ),
        }
        token = jwt.encode(
            payload, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM
        )
        return {"access_token": token}

    def decode_jwt(self, token: str) -> Union[Dict, Exception]:
        """
        This method checks if the token is valid,
        return the decoded token, otherwise return an empty dictionary.

        :param token: The token to decode
        :type token: str

        :return: A dictionary of the decoded token | error message.
        """

        try:
            decoded_token = jwt.decode(
                token, self.JWT_SECRET, algorithms=self.JWT_ALGORITHM
            )
        except:
            raise HTTPException(403, {"message": "Token invalid."})

        if (
            datetime.strptime(decoded_token["expires"], "%Y-%m-%d %H:%M:%S.%f")
            >= datetime.now()
        ):
            return decoded_token
        raise HTTPException(400, {"message": "Token expired."})


authentication = AuthHandler()
