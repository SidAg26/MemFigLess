from numpy import matrix, linalg, random
from time import time
import json as json
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext


logger = Logger(service='linpack', log_uncaught_exceptions=True)
tracer = Tracer(service='linpack')

def linpack(n):
    # LINPACK benchmarks
    ops = (2.0 * n) * n * n / 3.0 + (2.0 * n) * n

    # Create AxA array of random numbers -0.5 to 0.5
    A = random.random_sample((n, n)) - 0.5
    B = A.sum(axis=1)

    # Convert to matrices
    A = matrix(A)
    B = matrix(B.reshape((n, 1)))

    # Ax = B
    start = time()
    x = linalg.solve(A, B)
    latency = time() - start

    mflops = (ops * 1e-6 / latency)

    result = {
        'mflops': mflops,
        'latency': latency
    }

    return result

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext):
    try:
        # should always perform sanitisation check and parse JSON
        if 'body' in event.keys():
            # body is string
            # print((event["body"]))
            n = json.loads(event['body'])
            n = int(n['n'])
        else:
            n = int(event['n'])
    except Exception as e:
        logger.exception(e)
    try:
        result = linpack(n)
    except Exception as e:
        logger.exception(e)
        result = {"Error": str(e)}
    response = {
        "isBase64Encoded": "false",
        "statusCode": 200,
        "body": str(result),
        "headers": {
        "content-type": "application/json"
        }
    }
    return response