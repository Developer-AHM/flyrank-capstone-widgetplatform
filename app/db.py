import psycopg
from psycopg.rows import dict_row

from app import config


def connect():
    return psycopg.connect(config.DATABASE_URL, row_factory=dict_row)