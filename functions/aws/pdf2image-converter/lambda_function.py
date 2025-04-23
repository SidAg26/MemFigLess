import json as json
import boto3
import uuid, os
import tempfile
import pymupdf # imports the pymupdf library

s3 = boto3.client('s3')

def pdf2image_conversion(from_path, to_path):
    try:
        doc = pymupdf.open(from_path) # open a document
        for page in doc: # iterate the document pages
            text = page.get_text() # get plain text encoded as UTF-8
    except Exception as e:
        print("error")  
        raise e

    return (text)


def lambda_handler(event, context):
    if 'S3Object' in event:
        if type(event) != "class <dict>":
            if 'body' in event:
                event = json.loads(event['body'])
                event = json.loads(event)
            else:
                event = event
        else:
            raise ValueError("Incorrect format for incoming object!!")
        
        _bucket = event['S3Object']['Bucket']
        _name = event['S3Object']['Name']
        

        tmpkey = _name.replace('/', '')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        upload_path = '/tmp/resized-{}'.format(tmpkey)
        s3.download_file(_bucket, _name, download_path)
        

        try:
            response = pdf2image_conversion(download_path, upload_path)
                # s3.upload_file(upload_path, _bucket, 'download/resized-{}'.format(_name))
            print("Success")
            response = json.dumps(response)
            response = {"status": "success", "text": response}
            return response
            
        except Exception as e:
            response = {"status": "failed"}
            response = json.dumps(response)
            return response
        finally:
            os.remove(download_path)
            # os.remove(upload_path)
           