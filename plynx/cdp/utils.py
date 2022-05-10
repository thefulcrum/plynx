# Copyright (C) 2022, N3 Hub Limited
# All rights reserved.

from plynx.cdp import celery_app
from plynx.cdp.constants import CeleryTask


def send_celery_task(cdp_scheduler_id):

    celery_app.send_task(
        CeleryTask.TASK_NAME, args=(cdp_scheduler_id,), queue=CeleryTask.QUEUE_NAME
    )
