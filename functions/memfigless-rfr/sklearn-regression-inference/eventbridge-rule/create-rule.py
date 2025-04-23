# RULES CREATED VIA GUI - this file is unused

import boto3

eventbridge_client = boto3.client('events')

# Create an EventBridge rule with a cron expression to trigger every 2 hours
response = eventbridge_client.put_rule(
    Name='MyScheduledRule',
    ScheduleExpression='cron(0 */2 * * ? *)',
    State='ENABLED',
    Description='Trigger Lambda function every 2 hours'
)

# Add the Lambda function as the target of the rule
lambda_client = boto3.client('lambda')
rule_arn = response['RuleArn']

response = eventbridge_client.put_targets(
    Rule='MyScheduledRule',
    Targets=[
        {
            'Id': '1',
            'Arn': 'arn:aws:lambda:us-east-1:123456789012:function:MyScheduledLambdaFunction'
        }
    ]
)

# Grant EventBridge permission to invoke the Lambda function
lambda_client.add_permission(
    FunctionName='MyScheduledLambdaFunction',
    StatementId='MyScheduledRulePermission',
    Action='lambda:InvokeFunction',
    Principal='events.amazonaws.com',
    SourceArn=rule_arn
)

# cron(Minutes Hours Day-of-month Month Day-of-week Year)
# Editing the rule
# response = eventbridge_client.put_rule(
#     Name='MyScheduledRule',
#     ScheduleExpression='cron(0 */3 * * ? *)',
#     State='ENABLED',
#     Description='Trigger Lambda function every 3 hours'
# )

# Add the permission to the Lambda function for EventBridge Rule
import boto3

# Initialize the Lambda client
lambda_client = boto3.client('lambda')

# Define the Lambda function name and EventBridge rule ARN
function_name = 'MyScheduledLambdaFunction'
rule_arn = 'arn:aws:events:us-east-1:123456789012:rule/MyScheduledRule'

# Add permission to allow EventBridge to invoke the Lambda function
# response = lambda_client.add_permission(
#     FunctionName=function_name,
#     StatementId='MyScheduledRulePermission',
#     Action='lambda:InvokeFunction',
#     Principal='events.amazonaws.com',
#     SourceArn=rule_arn
# )

# JSON Inline policy how it looks
# {
#   "Sid": "MyScheduledRulePermission",
#   "Effect": "Allow",
#   "Principal": {
#     "Service": "events.amazonaws.com"
#   },
#   "Action": "lambda:InvokeFunction",
#   "Resource": "arn:aws:lambda:us-east-1:123456789012:function:MyScheduledLambdaFunction",
#   "Condition": {
#     "ArnLike": {
#       "AWS:SourceArn": "arn:aws:events:us-east-1:123456789012:rule/MyScheduledRule"
#     }
#   }
# }