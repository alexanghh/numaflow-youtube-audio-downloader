import json
import boto3
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
      s3 = boto3.resource('s3',
        endpoint_url = os.environ['MINIO_URL'],
        aws_access_key_id = os.environ['MINIO_USER'],
        aws_secret_access_key = os.environ['MINIO_SECRET']
      )
      
      # TODO: download from s3
      boto_webm_bucket = s3.Bucket(webm_s3_bucket)
      
      # TODO: convert webm to mp3 using ffmpeg
      

      # TODO: upload to mp3
      mp3_s3_bucket = 'mp3'
      mp3_s3_key = webm_s3_key[:-4] + '.mp3'
      # Get bucket object
      boto_bucket = s3.Bucket(mp3_s3_bucket)
      boto_bucket.upload_fileobj(buf, mp3_s3_key) # TODO: set mp3 file
      print('uploaded to {}/{}'.format(s3_bucket, s3_key))
      messages.append(Message.to_vtx('success', str.encode(json.dumps(data))))
    except Exception as e:
      print(e)
      data['exception'] = str(e)
      messages.append(Message.to_vtx('error', str.encode(json.dumps(data))))
    return messages


if __name__ == "__main__":
    grpc_server = UserDefinedFunctionServicer(map_handler)
    grpc_server.start()
