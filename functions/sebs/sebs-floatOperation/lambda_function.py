import math
from time import time
import json as json
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_typing import events


logger = Logger(service='floatOperation', log_uncaught_exceptions=True)
tracer = Tracer(service='floatOperation')

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event: events.APIGatewayProxyEventV1, context: LambdaContext):
    # def lambda_handler(event: dict, context: LambdaContext): alternate declaration
    try:
        if 'body' in event.keys():
            data = json.loads(event['body'])
            n = int(data['n'])
        elif 'n' in event.keys():
            n = int(event['n'])
    except ValueError as e:
        logger.append_keys(input_size=n)
        logger.exception('ValueError exception caught.') # this will be logged by the framework
        raise e
    except Exception as e:
        logger.append_keys(input_size=n)
        logger.exception(e)
        raise e  # to send an error response back to API Gateway

    result = {'latency': float_operations(n),
              'input_size': n}
    logger.info(result)
    
    response = {
                  "isBase64Encoded": "false",
                  "statusCode": 200,
                  "body": json.dumps(result),
                  "headers": {
                    "content-type": "application/json"
                  }
                }
    return response

def float_operations(n):
    start = time()
    try:
        for i in range(0, n):
            _ = math.sin(i)
            _ = math.cos(i)
            _ = math.sqrt(i)
    except Exception as e:
        logger.append_keys(input_size=n)
        logger.exception(e)
        raise e
    latency = time() - start
    return latency

