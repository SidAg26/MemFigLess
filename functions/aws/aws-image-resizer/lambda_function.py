import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
from PIL import Image
import json as json
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger(service='image_resizer')
tracer = Tracer(service='image_resizer')
s3_client = boto3.client('s3')
            
def resize_image(image_path, resized_path):
  try:
    with Image.open(image_path) as image:
      image.thumbnail(tuple(x / 2 for x in image.size))
      image.save(resized_path)
  except Exception as e:
      logger.exception("Failed to process the file")
      raise e
@logger.inject_lambda_context(log_event=True)  
@tracer.capture_lambda_handler(capture_error=True, capture_response=True)
def lambda_handler(event: dict, context: LambdaContext):
  download_bucket = None
  try:
    with open("config.json", "r") as jsonfile:
      download_bucket = json.load(jsonfile)["s3-download-bucket"]
  except Exception as e:
     logger.exception('Error reading the config file')
     raise e
  try:
    if 'body' in event.keys():
      event = event['body']
      while type(event) is not dict:
        event = json.loads(event)
        # image = {'S3Object':
        #           {'Bucket':  event['S3Object']['Bucket'],
        #           'Name': event['S3Object']['Name']}
        #           }
    bucket = event['S3Object']['Bucket']
    key = unquote_plus(event['S3Object']['Name'])
    download_bucket = event['S3Object']['Download_Bucket']
  except Exception as e:
     logger.exception(e)
     raise e

  tmpkey = key.replace('/', '')
  download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
  upload_path = '/tmp/resized-{}'.format(tmpkey)
  try:
    s3_client.download_file(bucket, key, download_path)
    metadata = float(s3_client.head_object(Bucket=bucket, Key=key)['ContentLength'])/(1024*1024)
    # print(upload_path, key, bucket)
  except Exception as e:
     logger.exception("Error in downloading file locally.", e)
     raise e
  try:
    resize_image(download_path, upload_path)
  except Exception as e:
     logger.exception(e)
     raise e
  try:
    s3_client.upload_file(upload_path, download_bucket, 'resized-{}'.format(key))
    lambda_response = {
            "statusCode": 200,
            "body": json.dumps({'file_size': metadata}),
            "requestId": context.aws_request_id,
            "memory_size": context.memory_limit_in_mb
        }
    logger.info(lambda_response)
    return lambda_response
  except Exception as e:
    logger.exception("Error with uploading", e)
    raise e
  # this is done to clear cache - raises No Space on device error
  finally:
    os.remove(download_path)
    os.remove(upload_path)