# Copyright (C) 2022, N3 Hub Limited
# All rights reserved.

from plynx import node as operator
from plynx.cdp.src.constants import DataSource, StreamDataFields


@operator.output(name="output", var_type=dict)
@operator.param(
    name=StreamDataFields.DATA_SOURCE, var_type=str, default=None
)  # TODO make a new decorator for this
@operator.param(name=StreamDataFields.INSTANCE_NAME, var_type=str)
@operator.param(name=StreamDataFields.TOPIC, var_type=str)
@operator.param(name=StreamDataFields.PAYLOAD, var_type=str, default=None)
@operator.operation(
    title="Stream Data Consumer",
    description="Receive stream data of specified topic from specified instance.",
)
def stream_processor(data_source, instance_name, topic, payload):
    """The stream data consumer on Plynx side will be used for receive the stream data from CDP.

    The param value of `payload` will be replaced with actual value when create the workflow run
    record in `runs` collection in MongoDB.
    """

    assert data_source in [
        DataSource.DB,
        DataSource.DB,
        DataSource.STREAM,
    ], "Value of data source is empty."
    assert instance_name, "Value of instance name is empty."
    assert topic, "Value of topic is empty."
    assert payload, "Value of payload is empty."

    return {
        "output": {
            StreamDataFields.DATA_SOURCE: data_source,
            StreamDataFields.INSTANCE_NAME: instance_name,
            StreamDataFields.TOPIC: topic,
            StreamDataFields.PAYLOAD: payload,
        }
    }


GROUP = operator.utils.Group(
    title="CDP Operations",
    items=[
        stream_processor,
    ],
)
