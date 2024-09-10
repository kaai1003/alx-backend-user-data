#!/usr/bin/env python3
"""password encryption module"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """password encryption method"""
    encoded_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encoded_password, salt)
