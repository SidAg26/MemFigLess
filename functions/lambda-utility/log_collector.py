import boto3
from botocore import exceptions
import datetime
import time
import constants



class LogCollector():
    def __init__(self, function_name:str, file_name:str, start_time:datetime.datetime, end_time:datetime.datetime) -> None:
        """
        Initializes a LogCollector object.

        Args:
            function_name (str): The name of the Lambda function.
            file_name (str): The filepath to store the retrieved logs.
            start_time (datetime.datetime): The start time of the time range.
            end_time (datetime.datetime): The end time of the time range.
        """
        # Create a CloudWatch logs client
        self.cloudwatch_logs = boto3.client(service_name='logs',
                                            region_name=constants.AWS_REGION,
                                            aws_access_key_id=constants.ACCESS_KEY_ID,
                                            aws_secret_access_key=constants.SECRET_ACCESS_KEY)
        
        # Name of Lambda function
        self.lambda_function_name = function_name

        # Filepath to store the retrieved logs
        self.file_path = file_name

        # Log group name for the Lambda function
        self.log_group_name = '/aws/lambda/' + self.lambda_function_name

        # Start and end of the time range
        self.start_time = start_time
        self.end_time = end_time
        # Convert the start and end times to milliseconds since the epoch
        self.start_time = int(time.mktime(start_time.timetuple())) * 1000
        self.end_time = int(time.mktime(end_time.timetuple())) * 1000

        self.response = None
        self.list_of_log_streams = None


    def get_response_stream(self):
         return self.response
    def get_list_of_log_streams(self):
         return self.list_of_log_streams


    def get_cloudwatch_logs(self):
            """
            Retrieves and prints the log events from CloudWatch Logs within the specified time range.

            Returns:
                None
            """
            # Get the log streams for the Lambda function
            self.list_of_log_streams = self.cloudwatch_logs.describe_log_streams(logGroupName=self.log_group_name,
                                                                                 orderBy='LogStreamName',
                                                                                 descending=True,
                                                                                 limit=50)

            # Loop through each log stream
            for log_stream in self.list_of_log_streams['logStreams']:
                log_stream_name = log_stream['logStreamName']

                # Initialise next_token for manual pagination
                next_token = None
                while True:
                    if next_token:
                        # Get all the log events from the log stream in the specified time range
                        self.response = self.cloudwatch_logs.get_log_events(logGroupName=self.log_group_name, 
                                                                            logStreamName=log_stream_name, 
                                                                            startTime=self.start_time, 
                                                                            endTime=self.end_time,
                                                                            nextToken=next_token)
                    else:
                         self.response = self.cloudwatch_logs.get_log_events(logGroupName=self.log_group_name,
                                                                            logStreamName=log_stream_name,
                                                                            startTime=self.start_time,
                                                                            endTime=self.end_time)
                    
                    # Loop through each log event
                    for log_event in self.response['events']:
                        # Get the message from the log event
                        message = log_event['message']
                        # print(message)

                        # Filter the logs (replace 'Error' with your filter)
                        if 'Error' in message:
                            print(message)
                    # Check if there are more log events to retrieve
                    if 'nextForwardToken' in self.response:
                        # Set the next token to retrieve the next page of results
                        next_token = self.response['nextForwardToken']
                    else:
                        # All log events have been retrieved
                        break
            # return self.response, self.list_of_log_streams


