#!/usr/bin/env python3
"""basic authntefication Class module"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import Tuple, TypeVar
import base64


class BasicAuth(Auth):
    """Basic Auth class definition"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract base64 method"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if authorization_header.startswith('Basic '):
            return authorization_header[len('Basic '):]
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """base64 decode method"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            dec_str = base64.b64decode(base64_authorization_header)
            return dec_str.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str,
                                                               str]:
        """user & pwd from base64"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header,
                          str):
            return (None, None)
        if ':' in decoded_base64_authorization_header:
            cred = decoded_base64_authorization_header.split(':')
            return (cred[0], cred[1])
        return (None, None)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """user Object credentials method"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            filtred_users = User.search({'email': user_email})
        except Exception:
            return None
        for user in filtred_users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user method"""
        header_auth = self.authorization_header(request)

        if header_auth:
            b64_extract = self.extract_base64_authorization_header(
                header_auth
                )
            if b64_extract:
                user_cred = self.decode_base64_authorization_header(
                    b64_extract
                    )
                if user_cred:
                    email, pwd = self.extract_user_credentials(user_cred)
                    if email and pwd:
                        return self.user_object_from_credentials(
                            email, pwd
                            )
        return None
