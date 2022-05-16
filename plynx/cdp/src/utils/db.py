# Copyright (C) 2022, N3 Hub Limited
# All rights reserved.

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

from plynx.cdp.src.utils.config import get_config

_db_connection = None


def get_hub_db_connection() -> Connection:
    """Create or return the Hub database connection."""

    global _db_connection

    if _db_connection is None:

        config = get_config("hub_db")
        _db_connection = create_engine(
            "{engine}://{user}:{password}@{host}:{post}/{database}".format(
                engine=config["engine"],
                user=config["user"],
                password=config["password"],
                host=config["host"],
                port=config["port"],
                database=config["database"],
            )
        ).connect()

    return _db_connection
