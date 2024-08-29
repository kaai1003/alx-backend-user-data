#!/usr/bin/env python3
"""filtred logger Module"""
import logging
from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """log message obfuscated"""
    obfus_msg = message
    for field in fields:
        pattern = r'({}=)[^{}]+'.format(field, separator)
        obfus_msg = re.sub(pattern,
                           r'\1{}'.format(redaction),
                           obfus_msg)
    return obfus_msg


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """class constructor

        Args:
            fields (List[str]): list of fields
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """message format func

        Args:
            record (logging.LogRecord): log record

        Returns:
            str: obfuscated message
        """
        return filter_datum(self.fields,
                            self.REDACTION,
                            super().format(record),
                            self.SEPARATOR)
