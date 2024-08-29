#!/usr/bin/env python3
"""filtred logger Module"""
from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """log message obfuscated"""
    obfus_msg = message
    for field in fields:
        if field:
            pattern = r'({}=)[^{}]+'.format(field, separator)
            obfus_msg = re.sub(pattern,
                               r'\1{}'.format(redaction),
                               obfus_msg)
    return obfus_msg
