import boto3
import pickle
import io, json, os
import numpy as np
import pandas as pd



s3 = boto3.client('s3')
bucket_name = 'your-bucket-name'
key = 'memory_configurations.json'

memory_configurations = [128, 256, 512, 1024, 2048, 3008]
memory_configurations_json = json.dumps(memory_configurations)

s3.put_object(Bucket=bucket_name, Key=key, Body=memory_configurations_json)

# Set the JOBLIB_TEMP_FOLDER environment variable
os.environ['JOBLIB_TEMP_FOLDER'] = '/tmp'
s3 = boto3.client('s3')
rf_model = None  # Global variable to store the model

# Load the model from S3
def load_model(bucket_name, model_key):
    model_stream = io.BytesIO()
    s3.download_fileobj(bucket_name, model_key, model_stream)
    model_stream.seek(0)
    model = pickle.load(model_stream)
    return model

# Load memory configurations from S3
def load_memory_configurations(bucket_name, key):
    response = s3.get_object(Bucket=bucket_name, Key=key)
    memory_configurations_json = response['Body'].read().decode('utf-8')
    memory_configurations = json.loads(memory_configurations_json)
    return memory_configurations

# Lambda handler function
def lambda_handler(event, context):
    global rf_model  # Declare rf_model as global to modify it

    # Define your S3 bucket and model key
    bucket_name = 'sklearn-layer-model-training'
    model_key = 'trained_model.pkl'
    memory_configurations_key = 'memory_configurations.json'

    # Check if the model is already loaded
    if rf_model is None:
        # Load the model
        rf_model = load_model(bucket_name, model_key)

    # Load memory configurations from S3
    memory_configurations = load_memory_configurations(bucket_name, memory_configurations_key)

    # Define the feature names used during training
    feature_names = ['total_memory', 'payload', 'cpu_user_time']

    # Initialize variables to store the best configuration and its prediction
    best_configuration = None
    best_prediction = None

    # Define your constraints
    cost_constraint = 0.5  # Example cost constraint
    deadline_constraint = 1000  # Example deadline constraint in milliseconds

    # Iterate over each memory configuration
    for memory in memory_configurations:
        # Extract features from the event and create a DataFrame
        features = pd.DataFrame([[memory, event['payload'], event['cpu_user_time']]], columns=feature_names)

        # Make a prediction
        prediction = rf_model.predict(features)[0]

        # Calculate the cost (example calculation, adjust as needed)
        cost = memory * 0.00001667  # Example cost per MB-second

        # Check if the prediction satisfies the constraints
        if cost <= cost_constraint and prediction <= deadline_constraint:
            best_configuration = memory
            best_prediction = prediction
            break  # Stop if a suitable configuration is found

    # If no suitable configuration is found, use the default configuration
    if best_configuration is None:
        best_configuration = memory_configurations[0]
        best_prediction = rf_model.predict(pd.DataFrame([[best_configuration, event['payload'], event['cpu_user_time']]], columns=feature_names))[0]

    # Based on the best prediction, invoke another Lambda function
    lambda_client = boto3.client('lambda', region_name='ap-southeast-2')

    payload = {'n': event['payload']}
    print('Best Configuration:', best_configuration)
    print('Best Prediction:', best_prediction)
    # Define the threshold for the prediction
    some_threshold = 10000
    if best_prediction < some_threshold:
        function_name = 'workbench-matmul'
    else:
        function_name = 'workbench-linpack'

    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        response_payload = json.loads(response['Payload'].read())
        print('Response Payload:', response_payload)

        # Check if the response indicates success
        if response_payload.get('statusCode') == 200:
            print('Function executed successfully.')
        else:
            print('Function execution failed. Adjusting invocation...')
            # Adjust the invocation logic here if needed
            # For example, you can retry with a different configuration or handle the error
    except Exception as e:
        print('Error invoking function:', e)
        # Handle the error and adjust the invocation logic here if needed

    return {
        'statusCode': 200,
        'body': json.dumps(response_payload)
    }