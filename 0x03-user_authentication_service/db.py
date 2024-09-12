#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError, NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Dict
import logging

from user import Base, User

logging.disable(logging.WARNING)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self,
                 email: str,
                 hashed_password: str) -> User:
        """add user method

        Args:
            email (str): user email
            hashed_password (str): user password

        Returns:
            User: user object
        """
        session = self._session
        try:
            new_user = User(email=email,
                            hashed_password=hashed_password)
            session.add(new_user)
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        return new_user

    def find_user_by(self,
                     **kwargs: Dict[str, str]) -> User:
        """find user method

        Raises:
            NoResultFound: no user found
            InvalidRequestError: invalid input args

        Returns:
            User: user object found
        """
        session = self._session
        try:
            found = session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
        return found

    def update_user(self,
                    user_id: int,
                    **kwargs: Dict[str, str]) -> None:
        """update user method

        Args:
            user_id (int): user id

        Raises:
            ValueError: raise error value
        """
        user = self.find_user_by(id=user_id)
        session = self._session
        for key, value in kwargs.items():
            if hasattr(User, key):
                setattr(user, key, value)
            else:
                raise ValueError()
        session.commit()
