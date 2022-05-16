# Copyright (C) 2022, N3 Hub Limited
# All rights reserved.


class CeleryTask:
    """Celery task name and queue name used for processing tasks."""

    TASK_NAME = "scheduler_task_dispatcher"
    QUEUE_NAME = "scheduler_task_dispatcher_queue"


class DataSource:
    """Data resource types will be processed."""

    DB = "DB"
    DW = "DW"
    STREAM = "STREAM"


class StreamBroker:
    """Stream data brokers"""

    KAFKA = "KAFKA"
    REDIS = "REDIS"


class DataProcessType:
    """Data processing approach will be processed."""

    BATCH = "BATCH"
    STREAM = "STREAM"


class WebhookEvents:
    """The available webhook events."""

    RUN_WORKFLOW_EVENT = "RUN_WORKFLOW"
    PROCESS_STREAM_EVENT = "PROCESS_STREAM"


class NodeTypes:
    """Node types used for filtering data."""

    PYTHON_WORKFLOW = "python-workflow"
    PYTHON_CODE_OPERATION = "python-code-operation"


class WorkflowTypes:
    """Workflow types"""

    SCHEDULE = "Schedule"
    ON_DEMAND = "OnDemand"


class StreamDataFields:
    """Stream data fields."""

    DATA_SOURCE = "data_source"
    INSTANCE_NAME = "instance_name"
    TOPIC = "topic"
    PAYLOAD = "payload"
    STREAM_QUEUE_ID = "stream_queue_id"
