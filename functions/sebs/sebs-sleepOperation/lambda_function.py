from time import sleep
import json as json
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext


logger = Logger(service='sleepOperation', log_uncaught_exceptions=True)
tracer = Tracer(service='sleepOperation')

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext):
    sleep_time = 0
    try:
        if 'body' in event.keys():
            data = json.loads(event['body'])
            sleep_time = int(data['sleep_time'])
        elif 'sleep_time' in event.keys():
            sleep_time = int(event['sleep_time'])
    except ValueError as e:
        logger.append_keys(input_size=sleep_time)
        logger.exception('ValueError exception caught.') # this will be logged by the framework
        raise e
    except Exception as e:
        logger.append_keys(input_size=sleep_time)
        logger.exception(e)
        raise e  # to send an error response back to API Gateway
    # start timing
    result = {'latency': sleep(sleep_time),
              'input_size': sleep_time}
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