# Copyright (C) 2022, N3 Hub Limited
# All rights reserved.


class CeleryTask:

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
    PYTHON_WORKFLOW = "python-workflow"
    PYTHON_CODE_OPERATION = "python-code-operation"


class WorkflowTypes:
    SCHEDULE = "Schedule"
    ON_DEMAND = "OnDemand"
