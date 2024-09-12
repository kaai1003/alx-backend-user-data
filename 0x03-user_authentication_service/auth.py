#!/usr/bin/env python3
"""password encryption module"""
import bcrypt
from db import DB
from sqlalchemy.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """password encryption method"""
    encoded_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encoded_password, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """init method"""
        self._db = DB()

    def register_user(self,
                      email: str,
                      password: str) -> User:
        """register user method

        Args:
            email (str): user email
            password (str): user password

        Raises:
            ValueError: raise error

        Returns:
            User: registred user object
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            pass
        hashed = _hash_password(password)
        new_user = self._db.add_user(email, hashed)
        return new_user
