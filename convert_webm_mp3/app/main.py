import json
import boto3
import ffmpeg
import io
import os
from pynumaflow.function import Messages, Message, Datum, UserDefinedFunctionServicer


def map_handler(key: str, datum: Datum) -> Messages:
    val = datum.value
    _ = datum.event_time
    _ = datum.watermark

    data = json.loads(val.decode("utf-8"))
    webm_s3_bucket = data['webm_s3_bucket']
    webm_s3_key = data['webm_s3_key']

    print('downloading: ' + json.dumps(data))
    messages = Messages()
    try:
        # setup s3
        s3_client = boto3.client('s3',
                                 endpoint_url=os.environ['MINIO_URL'],
                                 aws_access_key_id=os.environ['MINIO_USER'],
                                 aws_secret_access_key=os.environ['MINIO_SECRET']
                                 )

        webm_buf = io.BytesIO()
        s3_client.download_fileobj(webm_s3_bucket, webm_s3_key, webm_buf)

        out, _ = (
            ffmpeg
            .input('pipe:', vn=None)
            .output('pipe:', format='mp3', metadata='title=' + webm_s3_key.split('/')[-1][:-4])
            .overwrite_output()
            .run(capture_stdout=True, input=webm_buf.getbuffer())
        )
        mp3_buf = io.BytesIO(out)

        mp3_s3_bucket = 'mp3'
        mp3_s3_key = webm_s3_key[:-4] + 'mp3'
        s3_client.upload_fileobj(mp3_buf, mp3_s3_bucket, mp3_s3_key)
        print('uploaded to {}/{}'.format(mp3_s3_bucket, mp3_s3_key))
        data['mp3_s3_bucket'] = mp3_s3_bucket
        data['mp3_s3_key'] = mp3_s3_key
        messages.append(Message.to_vtx('success', str.encode(json.dumps(data))))
    except Exception as e:
        print(e)
        data['exception'] = str(e)
        messages.append(Message.to_vtx('error', str.encode(json.dumps(data))))
    return messages


if __name__ == "__main__":
    grpc_server = UserDefinedFunctionServicer(map_handler)
    grpc_server.start()
