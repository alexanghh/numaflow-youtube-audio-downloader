import json
from pytube import Playlist
from pynumaflow.function import Messages, Message, Datum, UserDefinedFunctionServicer


def map_handler(key: str, datum: Datum) -> Messages:
    val = datum.value
    _ = datum.event_time
    _ = datum.watermark

    data = json.loads(val.decode("utf-8"))
    playlist_url = data['playlist_url']
    print('listing: ' + json.dumps(data))
    messages = Messages()
    try:
        p = Playlist(playlist_url)
        for url in p.video_urls:
            msg = {}
            msg['playlist'] = p.title
            msg['video_url'] = url
            messages.append(Message.to_vtx('success', str.encode(json.dumps(msg))))
    except Exception as e:
        print(e)
        data['exception'] = str(e)
        messages.append(Message.to_vtx('error', str.encode(json.dumps(data))))
    return messages


if __name__ == "__main__":
    grpc_server = UserDefinedFunctionServicer(map_handler)
    grpc_server.start()
