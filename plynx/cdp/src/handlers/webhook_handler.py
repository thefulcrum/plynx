# Copyright (C) 2022, N3 Hub Limited
# All rights reserved.

from typing import Any, List

from plynx.cdp.src.handlers.base import BaseHandler
from plynx.cdp.src.data import EventMessage, StreamData, WorkflowNode, OperationNode
from plynx.cdp.src.constants import WebhookEvents, NodeTypes, DataSource, StreamDataFields
from plynx.db.node import Node, Parameter, NodeClonePolicy
from plynx.utils.db_connector import get_db_connector
from plynx.constants import Collections, NodeStatus


class WebHookHandler(BaseHandler):
    def __init__(self, message: EventMessage):
        super().__init__()

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
        self.stream_data = StreamData(
            self.message.data[StreamDataFields.TOPIC],
            self.message.data[StreamDataFields.PAYLOAD],
            self.message.data[StreamDataFields.STREAM_QUEUE_ID],
            self.message.data[StreamDataFields.INSTANCE_NAME],
        )

    def _retrieve_workflows(self):
        """Query target workflows by given criterias."""

        workflows = get_db_connector()[Collections.TEMPLATES].find(
            {
                "$and": [
                    {"kind": NodeTypes.PYTHON_WORKFLOW},
                    {"node_status": NodeStatus.CREATED},
                    {
                        "$and": [
                            {
                                "parameters.value.value": {
                                    "$elemMatch": {
                                        "parameters.name": StreamDataFields.DATA_SOURCE,
                                        "parameters.value": DataSource.STREAM,
                                    }
                                }
                            },
                            {
                                "parameters.value.value": {
                                    "$elemMatch": {
                                        "parameters.name": StreamDataFields.TOPIC,
                                        "parameters.value": self.stream_data.topic,
                                    }
                                }
                            },
                            {
                                "parameters.value.value": {
                                    "$elemMatch": {
                                        "parameters.name": StreamDataFields.INSTANCE_NAME,
                                        "parameters.value": self.stream_data.instance_name,
                                    }
                                }
                            },
                        ]
                    },
                ],
            }
        )

        return workflows

    def process(self) -> None:
        """Process the stream data event."""

        workflows = self._retrieve_workflows()
        for workflow in workflows:

            workflow: WorkflowNode = Node.from_dict(workflow)
            workflow_to_run = workflow.clone(NodeClonePolicy.NODE_TO_RUN)

            ops_node: Parameter = workflow_to_run.parameters[0]
            assert (
                ops_node.parameter_type == "list_node"
            ), "Parameter type `list_node` is missing in the workflow."

            operations: List[OperationNode] = ops_node.value.value
            for op in operations:

                op_params: List[Parameter] = op.parameters

                for p in op_params:
                    if p.name == StreamDataFields.PAYLOAD:
                        self.logger.info("Updating payload data with stream message.")

                        p.value = self.stream_data.payload
                        break

            self.logger.info("Saving the workflow in `runs` collection for execution.")
            workflow_to_run.save(collection=Collections.RUNS)
