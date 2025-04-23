
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Purpose
An AWS lambda function that analyzes documents with Amazon Textract.
"""
import json
import base64
import boto3
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext
from botocore.exceptions import ClientError

# Set up logging.
logger = Logger(service='text_analyser')
tracer = Tracer(service='text_analyser')

# Get the boto3 client.
textract_client = boto3.client('textract')
s3_client = boto3.client('s3')
@logger.inject_lambda_context(log_event=True)  
@tracer.capture_lambda_handler(capture_error=True, capture_response=True)
def lambda_handler(event: dict, context: LambdaContext):
    """
    Lambda handler function
    param: event: The event object for the Lambda function.
    param: context: The context object for the lambda function.
    return: The list of Block objects recognized in the document
    passed in the event object.
    """
    try:

        # Determine document source.
        if 'S3Object' in event.keys():
            # Decode the image
            image = {'S3Object':
                     {'Bucket':  event['S3Object']['Bucket'],
                      'Name': event['S3Object']['Name']}
                     }
        elif 'body' in event.keys():
            event = event['body']
            while type(event) is not dict:
                event = json.loads(event)
            image = {'S3Object':
                     {'Bucket':  event['S3Object']['Bucket'],
                      'Name': event['S3Object']['Name']}
                     }
        else:
            logger.exception("Value error in decoding the input body")
            raise ValueError(
                'Invalid source. Only image base 64 encoded image bytes or S3Object are supported.')


        # Analyze the document.
        response = textract_client.detect_document_text(Document=image)

        # Get the Blocks
        blocks = response['Blocks']
        metadata = float(s3_client.head_object(Bucket=event['S3Object']['Bucket'], Key=event['S3Object']['Name'])['ContentLength'])/(1024*1024)

        lambda_response = {
            "statusCode": 200,
            "body": json.dumps({"filesize": metadata})
        }

    except ClientError as err:
        error_message = "Couldn't analyze image. " + \
            err.response['Error']['Message']
        lambda_response = {
            'statusCode': 400,
            'body': {
                "Error": err.response['Error']['Code'],
                "ErrorMessage": error_message
            }
        }
        logger.error("Error function %s: %s",
            context.invoked_function_arn, error_message)

    except ValueError as val_error:
        lambda_response = {
            'statusCode': 400,
            'body': {
                "Error": "ValueError",
                "ErrorMessage": format(val_error)
            }
        }
        logger.error("Error function %s: %s",
            context.invoked_function_arn, format(val_error))
    logger.info(lambda_response)
    return lambda_response
