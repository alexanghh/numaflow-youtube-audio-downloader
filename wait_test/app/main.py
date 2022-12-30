import json
import time
import os
from pynumaflow.function import Messages, Message, Datum, UserDefinedFunctionServicer


def map_handler(key: str, datum: Datum) -> Messages:
    val = datum.value
    _ = datum.event_time
    _ = datum.watermark

    wait_secs = int(os.environ['WAIT_DURATION_SECS'])
    time.sleep(wait_secs)
    print('sleep {} secs ok'.format(wait_secs))

    messages = Messages()
    messages.append(Message.to_vtx(key, val))
    return messages


if __name__ == "__main__":
    grpc_server = UserDefinedFunctionServicer(map_handler)
    grpc_server.start()
