import json
from pytube import YouTube
import boto3
import io
import os
from pynumaflow.function import Messages, Message, Datum, UserDefinedFunctionServicer


def map_handler(key: str, datum: Datum) -> Messages:
    val = datum.value
    _ = datum.event_time
    _ = datum.watermark

    data = json.loads(val.decode("utf-8"))
    video_url = data['video_url']
    playlist = data['playlist']
    print('downloading: ' + json.dumps(data))
    messages = Messages()
    try:
        yt = YouTube(video_url)
        buf = io.BytesIO()
        yt.streams.filter(only_audio=True).desc().first().stream_to_buffer(buf)
        # yt.streams.filter(only_audio=True).desc().first().download(timeout=15, max_retries=3)
        # Reset read pointer. DOT NOT FORGET THIS, else all uploaded files will be empty!
        buf.seek(0)
        print('downloaded video: ' + yt.title)

        # upload to s3
        s3_bucket = 'webm'
        s3_key = playlist + "/" + yt.title + ".webm"
        s3 = boto3.resource('s3',
                            endpoint_url=os.environ['MINIO_URL'],
                            aws_access_key_id=os.environ['MINIO_USER'],
                            aws_secret_access_key=os.environ['MINIO_SECRET']
                            )
        # Get bucket object
        boto_bucket = s3.Bucket(s3_bucket)
        boto_bucket.upload_fileobj(buf, s3_key)
        print('uploaded to {}/{}'.format(s3_bucket, s3_key))
        data['webm_s3_bucket'] = s3_bucket
        data['webm_s3_key'] = s3_key
        messages.append(Message.to_vtx('success', str.encode(json.dumps(data))))
    except Exception as e:
        print(e)
        data['exception'] = str(e)
        messages.append(Message.to_vtx('error', str.encode(json.dumps(data))))
    return messages


if __name__ == "__main__":
    grpc_server = UserDefinedFunctionServicer(map_handler)
    grpc_server.start()
