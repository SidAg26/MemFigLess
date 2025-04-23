import numpy as np
from time import time
import json as json
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext


logger = Logger(service='matmul', log_uncaught_exceptions=True)
tracer = Tracer(service='matmul')
def matmul(n):
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)

    start = time()
    C = np.matmul(A, B)
    latency = time() - start
    return latency


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext):
    try:
        # should always perform sanitisation check and parse JSON
        if "body" in event:
            # body is string
            # print((event["body"]))
            n = json.loads(event["body"])
            n = int(n["n"])
        else:
            n = int(event["n"])
    except Exception as e:
        logger.error(e)
    try:    
        result = matmul(n=n)
    except Exception as e:
        logger.error(e)
        result = {"Error": str(e)}

    response = {
        "isBase64Encoded": "false",
        "statusCode": 200,
        "body": str(result),
        "headers": {
        "content-type": "application/json"
        }
    }
    # print(response)
    return response