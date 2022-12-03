# Stdlib Imports
import os
import hashlib

# Own Imports
from ledger.models import User


class PasswordHasher:
    """
    Responsible for the following:

    - generating a salt
    - hashing the password with the generated salt
    - check hashed password
    """

    def __init__(self, salt_length: int = 38, iterations: int = 10000) -> None:
        self.salt_length = salt_length
        self.iterations = iterations

    @property
    def generate_salt(self):
        """
        This method generates a random string of
        characters of length self.salt_length

        :return: A random string of bytes.
        """
        return os.urandom(self.salt_length)

    def hash_password(self, password: str) -> str:
        """
        This method takes a password,
        hashes it with a salt, and returns the hashed password.

        :param password: The password to hash
        :type password: str

        :return: The key is being returned.
        """
        key = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode("utf-8"),
            salt=self.generate_salt,
            iterations=self.iterations,
        )
        return key

    def check_password(self, password: str, user: User) -> bool:
        """
        This method take the password that the user entered,
        compare it to the hashed_password stored in the user table,
        and returns True if the password atches - otherwise False.

        :param password: The password to check
        :type password: str
        
        :param user: User
        :type user: User

        :return: A boolean value.
        """


        password_salt = user.password["salt"]
        password_key = user.password["key"]

        hashed_password = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode("utf-8"),
            salt=password_salt,
            iterations=self.iterations,
        )

        if hashed_password == password_key:
            return True
        return False
