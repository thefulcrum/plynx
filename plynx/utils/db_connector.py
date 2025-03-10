"""DB connector"""
import logging

import pymongo

from plynx.constants import Collections
from plynx.utils.config import get_db_config

_DB = None


def init_indexes():
    """Create DB indexes"""
    _DB[Collections.WORKER_STATE].create_index('insertion_date', expireAfterSeconds=5)

    _DB[Collections.RUNS].create_index('insertion_date')

    _DB[Collections.NODE_CACHE].create_index('key', unique=True)

    _DB[Collections.TEMPLATES].create_index('insertion_date')
    _DB[Collections.TEMPLATES].create_index([
        ('starred', pymongo.DESCENDING),
        ('insertion_date', pymongo.DESCENDING)
    ])
    _DB[Collections.TEMPLATES].create_index([('title', pymongo.TEXT), ('description', pymongo.TEXT)])

    _DB[Collections.RUNS].create_index('insertion_date')
    _DB[Collections.RUNS].create_index([('title', pymongo.TEXT), ('description', pymongo.TEXT)])

    _DB[Collections.USERS].create_index('username', unique=True)

    _DB[Collections.RUN_CANCELLATIONS].create_index('insertion_date', expireAfterSeconds=60)
    _DB[Collections.RUN_CANCELLATIONS].create_index('run_id')


def get_db_connector():
    """Create a connector lazily"""
    global _DB  # pylint: disable=global-statement
    if _DB is not None:
        return _DB
    connection_config = get_db_config()
    client = pymongo.MongoClient(connection_config.host, connection_config.port, read_preference=pymongo.read_preferences.PrimaryPreferred())
    _DB = client['plynx']
    if connection_config.user:
        _DB.authenticate(connection_config.user, connection_config.password)
    init_indexes()
    return _DB


def check_connection():
    """Check DB connection"""
    try:
        logging.info('Try db connection')
        get_db_connector().client.server_info()
    except pymongo.errors.ServerSelectionTimeoutError:
        logging.error('Connection failed')
        raise
