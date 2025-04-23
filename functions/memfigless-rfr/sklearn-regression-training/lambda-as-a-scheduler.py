import json
import boto3
import joblib
import io
import numpy as np

s3 = boto3.client('s3')

# Load the model from S3
def load_model(bucket_name, model_key):
    model_stream = io.BytesIO()
    s3.download_fileobj(bucket_name, model_key, model_stream)
    model_stream.seek(0)
    model = joblib.load(model_stream)
    return model

# Lambda handler function
def lambda_handler(event, context):
    # Define your S3 bucket and model key
    bucket_name = 'your-s3-bucket-name'
    model_key = 'models/trained_model.joblib'
    
    # Load the model
    model = load_model(bucket_name, model_key)
    
    # Extract features from the event
    features = np.array([event['total_memory'], event['payload'], event['cpu_user_time']]).reshape(1, -1)
    
    # Make a prediction
    prediction = model.predict(features)[0]
    
    # Based on the prediction, invoke another Lambda function
    lambda_client = boto3.client('lambda')
    
    if prediction < some_threshold:
        response = lambda_client.invoke(
            FunctionName='function_name_for_low_prediction',
            InvocationType='RequestResponse',
            Payload=json.dumps(event)
        )
    else:
        response = lambda_client.invoke(
            FunctionName='function_name_for_high_prediction',
            InvocationType='RequestResponse',
            Payload=json.dumps(event)
        )
    
    # Return the response from the invoked function
    response_payload = json.loads(response['Payload'].read())
    return {
        'statusCode': 200,
        'body': json.dumps(response_payload)
    }