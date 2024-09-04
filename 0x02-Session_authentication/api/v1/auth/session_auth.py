#!/usr/bin/env python3
"""session authntefication Class module"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import Tuple, TypeVar


class SessionAuth(Auth):
    """session auth class definition"""
    