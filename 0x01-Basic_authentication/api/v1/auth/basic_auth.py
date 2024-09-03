#!/usr/bin/env python3
"""basic authntefication Class module"""
from api.v1.auth.auth import Auth


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
