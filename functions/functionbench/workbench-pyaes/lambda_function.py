from time import time
import random
import string
import pyaes
import json as json
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext


logger = Logger(service='pyaes', log_uncaught_exceptions=True)
tracer = Tracer(service='pyaes')
def generate(length):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext):
    try:
        # should always perform sanitisation check and parse JSON
        if "body" in event:
            # body is string
            # print((event["body"]))
            event = json.loads(event["body"])
    except Exception as e:
        logger.error(e)

    length_of_message = event['length_of_message']
    num_of_iterations = event['num_of_iterations']

    message = generate(length_of_message)

    # 128-bit key (16 bytes)
    KEY = b'\xa1\xf6%\x8c\x87}_\xcd\x89dHE8\xbf\xc9,'
    ciphertext_ = []
    plaintext_ = []
    start = time()
    try:
        for _ in range(num_of_iterations):
            aes = pyaes.AESModeOfOperationCTR(KEY)
            ciphertext = aes.encrypt(message)
            ciphertext_.append(ciphertext)
            # print(ciphertext)

            aes = pyaes.AESModeOfOperationCTR(KEY)
            plaintext = aes.decrypt(ciphertext)
            plaintext_.append(plaintext)
            # print(plaintext)
            aes = None
            latency = time() - start
    except Exception as e:
        logger.error(e)
        result = {"Error": str(e)}
    
    result = {
        "latency": latency,
        "num_of_iterations": num_of_iterations,
        "length_of_message": length_of_message
    }
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