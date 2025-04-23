# Import necessary libraries
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.pipeline import make_pipeline
import pandas as pd
import re, csv, json
import pickle, io
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import NoCredentialsError
import boto3


pd.set_option('future.no_silent_downcasting', True)

def download_all_dynamodb_records(table_name):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table(table_name)
    
    all_records = []
    column_name = 'start_time'
    last_evaluated_key = None

    while True:
        if last_evaluated_key:
            response = table.scan(
                FilterExpression=Attr(column_name).exists(),
                ExclusiveStartKey=last_evaluated_key
            )
        else:
            response = table.scan(
                FilterExpression=Attr(column_name).exists()
            )

        all_records.extend(response['Items'])

        last_evaluated_key = response.get('LastEvaluatedKey')
        if not last_evaluated_key:
            break

    return all_records


def lambda_handler(event, context):
    # Example usage
    function_name = event['lambdaARN'].split(':')[-1]
    # Extract function name from lambda ARN
    # function_name = function_name.split(':')[-1]
    # Define the table name
    table_name = f'{function_name}_logs'
    all_records = download_all_dynamodb_records(table_name)
    df = pd.DataFrame(all_records)

    if function_name == 'workbench-matmul' or \
        function_name == 'workbench-linpack' or \
        function_name == 'sebs-floatOperation':
        # Define the regex pattern
        pattern = r"\{'n': (\d+)\}"
        # Replace the column value with the matched group
        df['payload'] = df['payload'].str.replace(pattern, r"\1", regex=True)
        df['payload'] = df['payload'].astype(float)

    elif function_name == 'workbench-pyaes':
        pattern = r"\{'length_of_message': (\d+), 'num_of_iterations': (\d+)\}"
        df['payload'] = df['payload'].str.replace(pattern, r"\1", regex=True)
        df['payload'] = df['payload'].astype(float)
        # df['payload2'] = 0
        # df['payload2'] = df['payload'].str.replace(pattern, r"\2", regex=True)
        # df['payload2'] = df['payload2'].astype(float)
    elif function_name == 'workbench-chameleon':
        pattern = r"\{'num_of_rows': (\d+), 'num_of_cols': (\d+)\}"
        df['payload'] = df['payload'].str.replace(pattern, r"\1", regex=True)
        df['payload'] = df['payload'].astype(float)
        # df['payload2'] = 0
        # df['payload2'] = df['payload'].str.replace(pattern, r"\2", regex=True)
        # df['payload2'] = df['payload2'].astype(float)
    else:
        # Define the regex pattern
        pattern = r"\{'n': (\d+)\}"
        # Replace the column value with the matched group
        df['payload'] = df['payload'].str.replace(pattern, r"\1", regex=True)
        df['payload'] = df['payload'].astype(float)
    
    # Drop rows with missing values
    df.dropna(subset=['payload'], inplace=True)
    df.dropna(subset=['memory_size'], inplace=True)
    
    if 'memory_used' in df.columns:
        df['memory_used'] = df['memory_used'].astype(float)
    if 'memory_size' in df.columns:
        df['memory_size'] = df['memory_size'].astype(float)
    if 'memory_utilisation' in df.columns:
        df['memory_utilisation'] = df['memory_utilisation'].astype(float)
    if 'total_memory' in df.columns:
        df['total_memory'] = df['total_memory'].astype(float)
    if 'duration' in df.columns:
        df['duration'] = df['duration'].astype(float)
    if 'billed_duration' in df.columns:
        df['billed_duration'] = df['billed_duration'].astype(float)
    else:
        df['billed_duration'] = df['duration']
    if 'function_error' in df.columns:
        df['function_error'] = df['function_error'].notna().astype(int)
    elif 'function_error' not in df.columns:
        df['function_error'] = 0
    # df = df.fillna(0)
    # df = df.drop(columns=['tmp_free', 'fd_use', 'tmp_max', 'rx_bytes','tmp_used', 'tx_bytes',
    #                     'threads_max', 'fd_max', 'memory_size', 
    #                     'total_network', 'agent_memory_avg', 'agent_memory_max', 
    #                     'insight_init_duration', 'shutdown', 'insights_duration', 'start_time'])
    # df = df[df['cold_start'] == 0]
    # df = df[df['cpu_user_time'] > 0]
    # avg_billed_duration = df['billed_duration'].mean()
    # avg_billed_mb_ms = df['billed_mb_ms'].mean()
    avg_billed_duration = df['duration'].mean()
    avg_billed_mb_ms =(df['duration']*df['memory_size']).mean()

    if 'total_memory' not in df.columns:
        df['total_memory'] = df['memory_size']
    if 'memory_utilisation' not in df.columns:
        df['memory_utilisation'] = (df['memory_used'] / df['memory_size']) * 100
    
    # Define the features and target variable
    X = df[['total_memory', 'payload']]
    if 'function_error' in df.columns:
        y = df[['memory_utilisation', 'billed_duration', 'function_error']]
    else:
        df['function_error'] = 0
    y = df[['memory_utilisation', 'billed_duration', 'function_error']]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    min_payload = X_train['payload'].min()
    max_payload = X_train['payload'].max()
    # Define a function to evaluate models
    def evaluate_model(model, X_train, y_train, X_test, y_test):
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        score = model.score(X_test, y_test)
        return predictions, score

    # Polynomial Regression
    poly = PolynomialFeatures(degree=2)
    poly_model = make_pipeline(poly, LinearRegression())
    poly_predictions, poly_score = evaluate_model(poly_model, X_train, y_train, X_test, y_test)
    print('Polynomial Regression R^2:', poly_score)

    # Decision Tree
    tree_model = DecisionTreeRegressor(random_state=42)
    tree_predictions, tree_score = evaluate_model(tree_model, X_train, y_train, X_test, y_test)
    print('Decision Tree R^2:', tree_score)

    # Random Forest
    rf_model = RandomForestRegressor(n_estimators=400, max_depth=10, max_features='sqrt',
                                     min_samples_leaf=1, min_samples_split=2, random_state=42)
    rf_predictions, rf_score = evaluate_model(rf_model, X_train, y_train, X_test, y_test)
    print('Random Forest R^2:', rf_score)

    # Neural Network
    nn_model = MLPRegressor(hidden_layer_sizes=(100,), max_iter=1000, random_state=42)
    nn_predictions, nn_score = evaluate_model(nn_model, X_train, y_train, X_test, y_test)
    print('Neural Network R^2:', nn_score)

    # Ridge Regression
    ridge_model = Ridge(alpha=1.0)
    ridge_predictions, ridge_score = evaluate_model(ridge_model, X_train, y_train, X_test, y_test)
    print('Ridge Regression R^2:', ridge_score)

    # Lasso Regression
    lasso_model = Lasso(alpha=0.1)
    lasso_predictions, lasso_score = evaluate_model(lasso_model, X_train, y_train, X_test, y_test)
    print('Lasso Regression R^2:', lasso_score)

    # Elastic Net
    elastic_model = ElasticNet(alpha=0.1, l1_ratio=0.5)
    elastic_predictions, elastic_score = evaluate_model(elastic_model, X_train, y_train, X_test, y_test)
    print('Elastic Net R^2:', elastic_score)

    # Random Forest
    # rf_model = RandomForestRegressor(n_estimators=400, max_depth=10, max_features='sqrt',
    #                                  min_samples_leaf=1, min_samples_split=2, random_state=42)
    rf_scores = cross_val_score(rf_model, X, y, cv=5)
    print('Random Forest Cross-Validation R^2:', rf_scores.mean())

    # Hyperparameter tuning
    # rf_model, rf_params = hyperparameter_tuning(rf_model, X_train, y_train, X_test, y_test)

    # Serialize the model to a byte stream
    model_stream = io.BytesIO()
    pickle.dump(rf_model, model_stream)  # Change this to the model you want to save
    model_stream.seek(0)
    # Upload the model to S3
    s3 = boto3.client('s3')
    bucket_name = 'sklearn-layer-model-training'
    s3_model_filename = f'{function_name}-trained-model.pkl'
    # Save the trained model to a file
    try:
        s3.upload_fileobj(model_stream, bucket_name, s3_model_filename)
        print(f'Model uploaded to S3 bucket {bucket_name} as {s3_model_filename}')
    except FileNotFoundError:
        print('The file was not found')
    except NoCredentialsError:
        print('Credentials not available')

    #  Upload the parameters to S3 for inference
    # Create a JSON object
    json_object = {
        "deadline": avg_billed_duration,
        "cost": avg_billed_mb_ms,
        "memory_list": event['powerValues'] if 'powerValues' in event else [i for i in range(128, 3008, 128)],
        "function_name": function_name,
        "min_payload": min_payload,
        "max_payload": max_payload
    }

    # Convert the JSON object to a string
    json_string = json.dumps(json_object)

    # Upload the JSON string to S3
    s3 = boto3.client('s3')
    s3_json_filename = f'{function_name}-metadata.json'

    try:
        s3.put_object(Bucket=bucket_name, Key=s3_json_filename, Body=json_string)
        print(f'JSON object uploaded to S3 bucket {bucket_name} as {s3_json_filename}')
    except FileNotFoundError:
        print('The file was not found')
    except NoCredentialsError:
        print('Credentials not available')
    


def hyperparameter_tuning(rf_model, X_train, y_train, X_test, y_test):
    # Hyperparameter tuning
    # Random Forest
    rf_param_grid = {
        'n_estimators': [i for i in range(100, 1001, 100)],
        'max_depth': [None, 10, 20, 30, 40, 50],
        'min_samples_split': [2, 5, 10, 20],
        'min_samples_leaf': [1, 2, 4, 8],
        'max_features': ['auto', 'sqrt', 'log2']
    }
    # Define a function to perform hyperparameter tuning using GridSearchCV
    def tune_model(model, param_grid, X_train, y_train):
        grid_search = GridSearchCV(model, param_grid, cv=5, scoring='r2', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        return grid_search.best_estimator_, grid_search.best_params_
    
    rf_model = RandomForestRegressor(random_state=42)
    best_rf_model, best_rf_params = tune_model(rf_model, rf_param_grid, X_train, y_train)
    rf_score = best_rf_model.score(X_test, y_test)
    print('Best Random Forest Params:', best_rf_params)
    print('Random Forest R^2:', rf_score)
    return best_rf_model, best_rf_params