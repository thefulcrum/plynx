# Copyright (C) 2022, N3 Hub Limited
# All rights reserved.

from typing import Any, List

from plynx.cdp.handlers.base import BaseHandler
from plynx.cdp.data import EventMessage, StreamData, WorkflowNode, OperationNode
from plynx.cdp.constants import WebhookEvents, NodeTypes, DataSource
from plynx.db.node import Node, Parameter, NodeClonePolicy
from plynx.utils.db_connector import get_db_connector
from plynx.constants import Collections, NodeStatus


class WebHookHandler(BaseHandler):
    def __init__(self, message: EventMessage):
        self._event = None
        self._message = message

    @property
    def event(self) -> Any:
        return self._event

    @property
    def message(self) -> EventMessage:
        return self._message


class RunWorkflowHandler(WebHookHandler):
    """Run the workflow with specific ID by update the status to in queue,
    similar to what has been done in the web endpoint
    """

    def __init__(self, message: EventMessage):

        super().__init__(message)
        self._event = WebhookEvents.RUN_WORKFLOW_EVENT

    def process(self):
        raise NotImplementedError("To be implemented in HUB3233.")


class StreamDataHandler(WebHookHandler):
    """Use the stream message in the payload to start the workflow which subscribes the topic"""

    def __init__(self, message: EventMessage):
        super().__init__(message)
        self._event = WebhookEvents.PROCESS_STREAM_EVENT

    def process(self) -> None:

        stream_data = StreamData(
            self.message.data["topic"],
            self.message.data["payload"],
            self.message.data["stream_queue_id"],
            self.message.data["stream_instance_name"],
        )

        # !temporary solution for MVP
        # !A decent table for plynx on cdp side should be created and used when a workflow created
        # !with stream consumer, the id should be saved in the db on cdp side

        workflows = get_db_connector()[Collections.TEMPLATES].find(
            {
                "$and": [
                    {"kind": NodeTypes.PYTHON_WORKFLOW},
                    {"node_status": NodeStatus.CREATED},
                ],
            }
        )

        # update the default payload with passed in payload value
        # and save the copy of the workflow in `runs` collection in mongoDB
        for workflow in workflows:

            workflow_to_run = None

            workflow: WorkflowNode = Node.from_dict(workflow)
            workflow = workflow.clone(NodeClonePolicy.NODE_TO_RUN)

            op_param: Parameter = workflow.parameters[0]
            assert (
                op_param.parameter_type == "list_node"
            ), "Parameter type `list_node` is missing in the workflow."

            import logging
            logging.info("--------------------------")
            logging.info(op_param)
            logging.info("--------------------------")


            operations: List[OperationNode] = op_param.value.value
            for op in operations:
                op_params: List[Parameter] = op.parameters

                is_stream, payload_updated, topic_matched, instance_matched = (
                    False,
                    False,
                    False,
                    False,
                )

                for p in op_params:

                    if p.name == "data_source" and p.value == DataSource.STREAM:
                        is_stream = True
                        continue

                    if p.name == "topic" and p.value == stream_data.topic:
                        topic_matched = True
                        continue

                    if p.name == "payload" and p.value.strip() == "":
                        p.value = stream_data.payload
                        payload_updated = True
                        continue

                    if (
                        p.name == "instance_name"
                        and p.value == stream_data.stream_instance_name
                    ):
                        instance_matched = True
                        continue

                    if all(
                        [is_stream, topic_matched, instance_matched, payload_updated]
                    ):
                        workflow_to_run = workflow
                        break

            if workflow_to_run is not None:
                workflow_to_run.save(collection=Collections.RUNS)
