# Copyright (C) 2022, N3 Hub Limited
# All rights reserved.

from celery import Celery

from plynx.cdp.src.utils.config import get_config
from plynx.cdp.src.constants import CeleryTask


_celery_app = None

def get_celery_app() -> Celery:
    """Create or return the Celery app."""

    global _celery_app
    CELERY_APP_NAME = "cdp-plynx"

    if _celery_app is None:

        _celery_app = Celery(CELERY_APP_NAME, broker="redis://redis:6379")
        _celery_app.conf.update(get_config("celery"))

    return _celery_app


def send_celery_task(cdp_scheduler_id):
    """Send celery task to fulcrum-cli celery instance."""

    get_celery_app.send_task(
        CeleryTask.TASK_NAME, args=(cdp_scheduler_id,), queue=CeleryTask.QUEUE_NAME
    )
