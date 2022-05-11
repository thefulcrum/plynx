# Copyright (C) 2022, N3 Hub Limited
# All rights reserved.

from typing import Dict, Any

from pydantic import validator
from pydantic.dataclasses import dataclass

from plynx.db.node import Node
from plynx.cdp.validators import check_empty


# Alias Node class
WorkflowNode = Node
OperationNode = Node


@dataclass(frozen=True)
class StreamData:
    # fields
    topic: str
    payload: str
    stream_queue_id: str
    instance_name: str

    # validators
    _check_topic = validator("topic", allow_reuse=True)(check_empty)
    _check_payload = validator("payload", allow_reuse=True)(check_empty)
    _check_stream_queue_id = validator("stream_queue_id", allow_reuse=True)(check_empty)
    _check_instance_name = validator("instance_name", allow_reuse=True)(
        check_empty
    )


@dataclass(frozen=True)
class EventMessage:
    # fields
    data: Dict[str, Any]

    # validators
    _check_data = validator("data", allow_reuse=True)(check_empty)
