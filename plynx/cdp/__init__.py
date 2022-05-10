# Copyright (C) 2022, N3 Hub Limited
# All rights reserved.

from celery import Celery


celery_app = None


def make_celery_app():

    # TODO make it read from global config

    CELERY_APP_NAME = "plynx"
    celery_config = {
        "CELERY_BROKER_URL": "redis://redis:6379",
        "CELERY_RESULT_BACKEND": "redis://redis:6379",
        "CELERY_TRACK_STARTED": True,
        "CELERY_SEND_EVENTS": True,
    }

    celery = Celery(CELERY_APP_NAME, broker="redis://redis:6379")
    celery.conf.update(celery_config)

    global celery_app
    celery_app = celery


def setup_cdp():
    make_celery_app()
