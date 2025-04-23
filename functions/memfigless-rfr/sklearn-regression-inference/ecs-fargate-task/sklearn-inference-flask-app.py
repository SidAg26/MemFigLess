from flask import Flask, request, jsonify
import boto3
import pickle
import io, json, os
import numpy as np
import pandas as pd

app = Flask(__name__)

# Set up logging
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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

@app.route('/predict', methods=['POST'])
def predict():
    global rf_model  # Declare rf_model as global to modify it

    print("Received request: ", request.get_json())
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

    # Get the event data from the request
    event = request.get_json()

    # Log the input event
    logger.info(f"Received event: {event}")

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

    # Log the prediction result
    logger.info(f"Best Configuration: {best_configuration}, Best Prediction: {best_prediction}")

    return jsonify({
        'best_configuration': best_configuration,
        'best_prediction': best_prediction
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)