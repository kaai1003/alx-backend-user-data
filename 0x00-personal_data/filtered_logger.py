#!/usr/bin/env python3
"""filtred logger Module"""
import logging
import mysql.connector
from mysql.connector.connection import MySQLConnection
import os
from typing import List
import re


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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


def get_logger() -> logging.Logger:
    """create logger func"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """return db connector"""

    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    pwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(user,
                                   pwd,
                                   host,
                                   db)


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


def main():
    """retrieve users and
    display filtred result"""

    logger = get_logger()
    con = get_db
    cur = con.cursor()
    cur.execute('SELECT * FROM users;')

    result = cur.fetchall()

    for row in result:
        log = "; ".join([f"{key}={value}" for key,
                         value in row.items()])
    cur.close()
    con.close()


if __name__ == "__main__":
    main()
