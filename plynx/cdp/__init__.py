# Copyright (C) 2022, N3 Hub Limited
# All rights reserved.

import os
import logging
from typing import Dict, Any, Union

import yaml
from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

_logger = None
_cdp_config = None
_celery_app = None
_db_connection = None


def get_logger():
    """Create or return logger of cdp module."""

    global _logger

    if _logger is None:
        _logger = logging.getLogger(__name__)
    return _logger


def get_config(service: Union[str, None] = None) -> Dict[str, Any]:
    """Create or return config per service if specified, otherwise return the entire config."""

    global _cdp_config

    if _cdp_config is None:

        config_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "config.yaml"
        )
        with open(config_file) as f:
            _cdp_config = yaml.load(f, Loader=yaml.FullLoader)

    return _cdp_config[service] if service else _cdp_config


def get_celery_app() -> Celery:
    """Create or return the Celery app."""

    global _celery_app
    CELERY_APP_NAME = "cdp-plynx"

    if _celery_app is None:

        _celery_app = Celery(CELERY_APP_NAME, broker="redis://redis:6379")
        _celery_app.conf.update(get_config("celery"))

    return _celery_app


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
