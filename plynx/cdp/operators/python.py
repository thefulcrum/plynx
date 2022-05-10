# Copyright (C) 2022, N3 Hub Limited
# All rights reserved.


from sqlalchemy import create_engine

import plynx.node
from plynx.cdp.utils import send_celery_task
from plynx.cdp.constants import DataSource

from plynx.constants import Collections


DB_USER = ""
hubdb_connection = create_engine(
    "postgresql+psycopg2://master:password@db:5432/fulcrum"
).connect()


@plynx.node.output(name="output", var_type=dict)
@plynx.node.param(
    name="data_source", var_type=str, default=None
)  # TODO make a new decorator for this
@plynx.node.param(name="instance_name", var_type=str)
@plynx.node.param(name="topic", var_type=str)
@plynx.node.param(name="payload", var_type=str, default=None)
@plynx.node.operation(
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
            "data_source": data_source,
            "instance_name": instance_name,
            "topic": topic,
            "payload": payload,
        }
    }


# def find_scheduler_id(sql):
#     result = hubdb_connection.execute(sql)
#     importer = next(iter(result), None)

#     if importer is None:
#         raise Exception("Batch importer not found.")

#     return importer.scheduler_id


# @plynx.node.output(name="status", var_type=str)
# @plynx.node.operation(
#     title="Start",
# )
# def start_stub():
#     return {"status": "ok"}


# @plynx.node.input(name="input", var_type=str)
# @plynx.node.output(name="output", var_type=str)
# @plynx.node.param(name="importer_name", var_type=str)
# @plynx.node.operation(title="Batch Importer", description="Batch importing task")
# def batch_import_operation(input, importer_name):
#     sql = """
#     SELECT sched.id AS scheduler_id
#     FROM cdp.schedulers sched
#     INNER JOIN cdp.data_importers di ON sched.schedule_to_id = di.id
#     INNER JOIN cdp.instances ins ON sched.instance_id = ins.id
#     WHERE di.name = '{importer_name}';
#     """.format(
#         importer_name=importer_name
#     )

#     send_celery_task(find_scheduler_id(sql))
#     return {"output": input}


# @plynx.node.input(name="input", var_type=str)
# @plynx.node.output(name="output", var_type=str)
# @plynx.node.param(name="exporter_name", var_type=str)
# @plynx.node.operation(title="Batch Exporter", description="Batch exporting task")
# def batch_exporter_operation(input, exporter_name):
#     sql = """
#     SELECT sched.id AS scheduler_id
#     FROM cdp.schedulers sched
#     INNER JOIN fulcrum.channels chan ON sched.schedule_to_id = chan.uuid
#     INNER JOIN cdp.instances ins ON sched.instance_id = ins.id
#     WHERE chan.name = '{exporter_name}';
#     """.format(
#         exporter_name=exporter_name
#     )

#     send_celery_task(find_scheduler_id(sql))
#     return {"output": input}


# @plynx.node.input(name="input", var_type=str)
# @plynx.node.output(name="output", var_type=str)
# @plynx.node.param(name="segment_name", var_type=str)
# @plynx.node.param(name="instance_name", var_type=str)
# @plynx.node.param(name="schedule_type", var_type=str)
# @plynx.node.operation(title="Segment Exporter", description="Segment exporting task")
# def segment_export_operation(input, segment_name, instance_name, schedule_type):

#     if not schedule_type in ("advanced", "manual"):
#         raise Exception("Schedule type needs to be either `advanced` or `manual`.")

#     sql = """
#     SELECT sched.id AS scheduler_id
#     FROM cdp.schedulers sched
#     INNER JOIN cdp.segments seg ON sched.schedule_to_id = seg.id
#     INNER JOIN cdp.instances ins ON sched.instance_id = ins.id
#     WHERE seg.name = '{segment_name}'
#     AND ins.name = '{instance_name}'
#     AND sched.schedule_type = '{schedule_type}'
#     AND sched.schedule_to_type = 'Segment';
#     """.format(
#         segment_name=segment_name,
#         instance_name=instance_name,
#         schedule_type=schedule_type,
#     )

#     send_celery_task(find_scheduler_id(sql))
#     return {"output": input}


GROUP = plynx.node.utils.Group(
    title="CDP Operations",
    items=[
        stream_processor,
        # start_stub,
        # batch_import_operation,
        # batch_exporter_operation,
        # segment_export_operation,
    ],
)
