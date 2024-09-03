#!/usr/bin/env python3
"""basic authntefication Class module"""
from api.v1.auth.auth import Auth
from typing import Tuple
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
