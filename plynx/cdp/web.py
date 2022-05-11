# Copyright (C) 2022, N3 Hub Limited
# All rights reserved.

import json
from http import HTTPStatus

from flask import request, Blueprint

from plynx.cdp import get_logger
from plynx.cdp.data import EventMessage
from plynx.cdp.constants import WebhookEvents
from plynx.cdp.handlers import RunWorkflowHandler, StreamDataHandler

cdp_bp = Blueprint("cdp", __name__, url_prefix="/plynx/api/cdp")


@cdp_bp.route("/webhook", methods=("POST",))
# @requires_auth
def webhook():
    """Receive the webhook message to notify the listeners.

    Acceptable payload data structure:
    {
        "event": WebhookEvents.RUN_WORKFLOW_EVENT | WebhookEvents.PROCESS_STREAM_EVENT,
        "message": {}
    }

    Example of stream data processing event:
    {
        "event": WebhookEvents.PROCESS_STREAM_EVENT,
        "message": {
            "topic": "xxxxx",
            "payload: "xxxxx",
            "stream_queue_id": "xxxxx",
            "instance_name": xxxxx"
        }
    }
    """

    VALID_EVENTS = {
        WebhookEvents.RUN_WORKFLOW_EVENT: RunWorkflowHandler,
        WebhookEvents.PROCESS_STREAM_EVENT: StreamDataHandler,
    }
    logger = get_logger()

    if request.method == "POST":
        payload = json.loads(request.data)
        logger.info(f"Received stream data payload: {payload}.")

        event, message = payload.get("event"), payload.get("message")
        try:
            handler = VALID_EVENTS[event](EventMessage(message))
            handler.process()

        except KeyError:
            return (
                {"status": f"Invalid event type received: {event}."},
                HTTPStatus.BAD_REQUEST,
            )
        else:
            return {}, HTTPStatus.NO_CONTENT

    else:
        return (
            {"status": f"HTTP method not supported."},
            HTTPStatus.METHOD_NOT_ALLOWED,
        )
