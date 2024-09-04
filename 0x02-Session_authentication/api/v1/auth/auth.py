#!/usr/bin/env python3
"""authntefication Class module"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class definition"""
    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """require auth method"""
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        for ex_path in excluded_paths:
            if ex_path.rstrip('/') == path.rstrip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """auth header method"""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """curr user method"""
        return None
