#!/usr/bin/env python3
"""encrypt password Module"""
import bcrypt


def hash_password(password: str) -> bytes:
    """return byte hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'),
                         bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """check password validation
    """
    return bcrypt.checkpw(password.encode('utf-8'),
                          hashed_password)
