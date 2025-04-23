'''

This is the optimised version of the original code

# import boto3
# import pickle
# import io, json, os
# import numpy as np
# import pandas as pd
# import time, re
# import base64

# # Create an S3 client
# s3 = boto3.client('s3')
# rf_model = None  # Global variable to store the model
# model_name = None # Global variable to store the last model name
# required_constraint = None # Global variable to store the required constraint
# _tolerance = float(os.getenv('CONSTRAINT_TOLERANCE'))
# _duration_alpha = float(os.getenv('DURATION_ALPHA'))
# _pricing = None # Global variable to store the pricing information
# try:
#     with open('./price_per_memory.json', 'r') as f:
#         _pricing = json.load(f)
# except Exception as e:
#     print(f"Error loading pricing information: {e}")

# # Load the model from S3
# def load_model(bucket_name, model_key):
#     model_stream = io.BytesIO()
#     s3.download_fileobj(bucket_name, model_key, model_stream)
#     model_stream.seek(0)
#     model = pickle.load(model_stream)
#     return model

# def get_model_metadata(bucket_name, function_name):
#     model_metadata = s3.get_object(Bucket=bucket_name, Key=f'{function_name}-metadata.json')
#     model_metadata = json.loads(model_metadata['Body'].read().decode('utf-8'))
#     return model_metadata

# # Optimize memory list to use fewer steps
# def get_optimized_memory_list():
#     # Use larger steps for initial range
#     base_list = list(range(128, 1024, 128))  # 128MB steps until 1GB
#     mid_list = list(range(1024, 2048, 256))  # 256MB steps until 2GB
#     high_list = list(range(2048, 3009, 512))  # 512MB steps after 2GB
#     return base_list + mid_list + high_list

# # Cache Lambda versions to avoid repeated API calls
# _lambda_version_cache = {}

# def get_or_create_lambda_version(lambda_client, lambda_name, memory):
#     cache_key = f"{lambda_name}_{memory}"
#     if cache_key in _lambda_version_cache:
#         return _lambda_version_cache[cache_key]

#     try:
#         response = lambda_client.list_aliases(FunctionName=lambda_name)
#         for alias in response['Aliases']:
#             if alias['Name'] == f'RAM{memory}':
#                 _lambda_version_cache[cache_key] = alias['FunctionVersion']
#                 return alias['FunctionVersion']

#         # If not found, create new version
#         lambda_client.update_function_configuration(FunctionName=lambda_name, MemorySize=memory, Description=f'RAM{memory}')
#         time.sleep(5)  # Reduced wait time
#         publish_response = lambda_client.publish_version(FunctionName=lambda_name)
#         version = publish_response['Version']
#         lambda_client.create_alias(FunctionName=lambda_name, FunctionVersion=version, Name=f'RAM{memory}')
#         _lambda_version_cache[cache_key] = version
#         return version
#     except Exception as e:
#         print(f"Error in version management: {e}")
#         return None

# # Lambda handler function
# def lambda_handler(event, context):
#     function_name = event['lambdaARN'].split(':')[-1]
    
#     global rf_model  # Declare rf_model as global to modify it
#     global model_name # Declare model_name as global to modify it
#     global required_constraint # Declare required_constraint as global to modify it
#     global _tolerance
#     global _duration_alpha

#     _tolerance = event['tolerance'] if 'tolerance' in event else _tolerance
#     _duration_alpha = event['duration_alpha'] if 'duration_alpha' in event else _duration_alpha
#     # Define your S3 bucket and model key
#     bucket_name = 'sklearn-layer-model-training'
#     model_key = f'{function_name}-trained-model.pkl'
#     metadata = get_model_metadata(bucket_name, function_name)


#     lambda_name = event['lambda_name'] if 'lambda_name' in event else metadata['function_name']
#     deadline = event['deadline'] if 'deadline' in event else metadata['deadline']
#     deadline = deadline*1.5 # 50% increase in deadline
#     cost = event['cost'] if 'cost' in event else metadata['cost']
#     payload = event['payload']
#     min_payload = metadata['min_payload'] if 'min_payload' in metadata else 1
#     max_payload = metadata['max_payload'] if 'max_payload' in metadata else 1000
#     # memory_list = json.loads(os.environ['MEMORY_LIST'])
#     # memory_list = [i for i in range(128, 3008, 128)]
#     # memory_list = metadata['memory_list'] if 'memory_list' in metadata else [i for i in range(128, 2048, 128)]
#     # memory_list.append(3008)
#     memory_list = get_optimized_memory_list()
     
#     # Check if the model is already loaded
#     if model_name is None or model_name != model_key:
#         # Load the model
#         rf_model = load_model(bucket_name, model_key)
#         model_name = model_key
#     # if rf_model is None:
#     #     # Load the model
#     #     rf_model = load_model(bucket_name, model_key)

#     # If the payload is out of the model's range, return a default 3008 MB memory
#     if payload > max_payload:
#         return invoke_lambda(lambda_name, payload, 3008)
#     elif payload < min_payload:
#         payload = min_payload
#     # Make a prediction
#     # Generate predictions and check constraints
#     pareto_front = []
#     candidate = [] 
#     start = time.time()
#     # print("[['memory_utilisation', 'billed_duration', 'function_error']]")
#     # Use optimized memory list instead of full range
#     memory_list = get_optimized_memory_list()
    
#     # Optimize pareto front calculation
#     pareto_front = []
#     batch_size = 10  # Process predictions in batches
    
#     for i in range(0, len(memory_list), batch_size):
#         batch_memories = memory_list[i:i + batch_size]
#         features = pd.DataFrame([[mem, payload] for mem in batch_memories], 
#                               columns=['total_memory', 'payload'])
#         predictions = rf_model.predict(features)
        
#         for mem, pred in zip(batch_memories, predictions):
#             if not constraint_violation(pred, deadline, cost, mem):
#                 pareto_front.append((mem, pred))

#     prediction = None
#     if pareto_front != []:
#         # Identify Pareto optimal solutions
#         pareto_front = sorted(pareto_front, key=lambda x: x[0])
#         try:
#             # pareto = (mem, [utilisation, duration, error])
#             min = (_tolerance/100)*pareto_constraint(pareto_front[0][1], pareto_front[0][0])
#         except:
#             print("No solution found for input size", payload)  
            
            
#         for sol in pareto_front:
#             # pareto = (mem, [utilisation, duration, error])
#             # pareto_constraint(prediction, memory)
#             _tmp = (_tolerance/100)*pareto_constraint(sol[1], sol[0])
#             if _tmp < min:
#                 candidate.append(sol)
#                 min = _tmp
#                 required_constraint = min
#         prediction = candidate[0] if candidate else pareto_front[0]
#     best_mem = 128 # default value
#     if len(pareto_front) == 0:
#         # print("No solution found for input size", payload)
#         best_mem = 3008
#         prediction = rf_model.predict(pd.DataFrame([[best_mem, payload]], columns=['total_memory', 'payload']))[0]
#     else:
#         best_mem = prediction[0]
#     print(f"Best memory configuration for input size {payload} is {best_mem} MB")
#     print(f"Time taken for optimisation: {time.time()-start} seconds")
#     # print('Prediction:', prediction)import boto3


'''
"""
This is the optimised version of the Pareto Front calculation

def is_pareto_efficient(costs):
    is_efficient = np.ones(costs.shape[0], dtype=bool)
    for i, c in enumerate(costs):
        if is_efficient[i]:
            is_efficient[is_efficient] = np.any(costs[is_efficient] < c, axis=1)
            is_efficient[i] = True
    return is_efficient

def get_pareto_front(memory_list, payload, deadline, cost):
    solutions = []
    objectives = []
    
    for mem in memory_list:
        features = pd.DataFrame([[mem, payload]], columns=['total_memory', 'payload'])
        prediction = rf_model.predict(features)[0]
        
        if not constraint_violation(prediction, deadline, cost, mem):
            memory_util = prediction[0] * mem / 100
            duration = prediction[1]
            bill = memory_util * duration * _pricing[str(mem)]
            
            solutions.append((mem, prediction))
            objectives.append([duration, bill, memory_util])
    
    if not solutions:
        return []
        
    objectives = np.array(objectives)
    pareto_mask = is_pareto_efficient(objectives)
    pareto_front = [solutions[i] for i in range(len(solutions)) if pareto_mask[i]]
    
    return pareto_front
    
"""

"""
CURRENT OPTIMIZATIONS:
1. Model Caching:
   - Caches loaded model across invocations
   - Only reloads when model changes
   
2. Lambda Version Management:
   - Caches function versions to avoid repeated API calls
   - Reuses existing versions with matching memory configurations
   
3. Memory Configuration:
   - Early exit for out-of-range payloads
   - Smart default handling for edge cases
   
4. Constraint Checking:
   - Efficient filtering of invalid configurations
   - Early termination for non-viable options
   
5. Payload Handling:
   - Automatic payload formatting based on function type
   - Standardized input processing
   
6. Response Processing:
   - Efficient log parsing with regex
   - Structured response formatting

POTENTIAL IMPROVEMENTS:
1. Version Cache Enhancement:
   TODO: Add TTL to version cache
   ```python
   _lambda_version_cache = {
       'versions': {},
       'timestamps': {}
   }
   CACHE_TTL = 3600  # 1 hour
   ```

2. Parallel Processing:
   TODO: Implement parallel prediction for memory configurations
   ```python
   from concurrent.futures import ThreadPoolExecutor
   
   def predict_batch(memory_configs):
       with ThreadPoolExecutor() as executor:
           return list(executor.map(predict_single_config, memory_configs))
   ```

3. Binary Search Optimization:
   TODO: Replace linear memory search with binary search
   ```python
   def binary_search_memory(min_mem=128, max_mem=3008):
       while min_mem <= max_mem:
           mid = (min_mem + max_mem) // 2
           if meets_constraints(mid):
               max_mem = mid - 1
           else:
               min_mem = mid + 1
       return min_mem
   ```

4. Prediction Result Caching:
   TODO: Cache prediction results for common payloads
   ```python
   _prediction_cache = {}
   PREDICTION_CACHE_SIZE = 100
   
   def get_cached_prediction(payload, memory):
       cache_key = f"{payload}_{memory}"
       return _prediction_cache.get(cache_key)
   ```

5. Batch Prediction Processing:
   TODO: Process predictions in larger batches
   ```python
   def process_memory_batch(memories, batch_size=50):
       return [predict_batch(memories[i:i+batch_size]) 
               for i in range(0, len(memories), batch_size)]
   ```

6. Smart Version Management:
   TODO: Implement smart version cleanup and management
   ```python
   def cleanup_old_versions(function_name, keep_latest=5):
       versions = list_versions(function_name)
       if len(versions) > keep_latest:
           remove_old_versions(versions[:-keep_latest])
   ```

7. Error Handling Enhancement:
   TODO: Add comprehensive error handling and retry logic
   ```python
   def invoke_with_retry(function_name, payload, max_retries=3):
       for attempt in range(max_retries):
           try:
               return invoke_lambda(function_name, payload)
           except RetryableError:
               continue
           except NonRetryableError:
               break
   ```

8. Metric Collection:
   TODO: Add performance metrics collection
   ```python
   def collect_metrics(start_time, end_time, memory, duration):
       metrics = {
           'optimization_time': end_time - start_time,
           'memory_configured': memory,
           'execution_duration': duration
       }
       # Store metrics for analysis
   ```

Note: Implementation details would need to be adjusted based on specific requirements and constraints.
"""



import pickle
import io, json, os
import numpy as np
import pandas as pd
import time, re
import base64

# Create an S3 client
s3 = boto3.client('s3')
rf_model = None  # Global variable to store the model
model_name = None # Global variable to store the last model name
required_constraint = None # Global variable to store the required constraint
_tolerance = float(os.getenv('CONSTRAINT_TOLERANCE'))
_duration_alpha = float(os.getenv('DURATION_ALPHA'))
_pricing = None # Global variable to store the pricing information
try:
    with open('./price_per_memory.json', 'r') as f:
        _pricing = json.load(f)
except Exception as e:
    print(f"Error loading pricing information: {e}")

# Load the model from S3
def load_model(bucket_name, model_key):
    model_stream = io.BytesIO()
    s3.download_fileobj(bucket_name, model_key, model_stream)
    model_stream.seek(0)
    model = pickle.load(model_stream)
    return model

def get_model_metadata(bucket_name, function_name):
    model_metadata = s3.get_object(Bucket=bucket_name, Key=f'{function_name}-metadata.json')
    model_metadata = json.loads(model_metadata['Body'].read().decode('utf-8'))
    return model_metadata


# Lambda handler function
def lambda_handler(event, context):
    function_name = event['lambdaARN'].split(':')[-1]
    
    global rf_model  # Declare rf_model as global to modify it
    global model_name # Declare model_name as global to modify it
    global required_constraint # Declare required_constraint as global to modify it
    global _tolerance
    global _duration_alpha

    _tolerance = event['tolerance'] if 'tolerance' in event else _tolerance
    _duration_alpha = event['duration_alpha'] if 'duration_alpha' in event else _duration_alpha
    # Define your S3 bucket and model key
    bucket_name = 'sklearn-layer-model-training'
    model_key = f'{function_name}-trained-model.pkl'
    metadata = get_model_metadata(bucket_name, function_name)


    lambda_name = event['lambda_name'] if 'lambda_name' in event else metadata['function_name']
    deadline = event['deadline'] if 'deadline' in event else metadata['deadline']
    deadline = deadline*1.5 # 50% increase in deadline
    cost = event['cost'] if 'cost' in event else metadata['cost']
    payload = event['payload']
    min_payload = metadata['min_payload'] if 'min_payload' in metadata else 1
    max_payload = metadata['max_payload'] if 'max_payload' in metadata else 1000
    # memory_list = json.loads(os.environ['MEMORY_LIST'])
    # memory_list = [i for i in range(128, 3008, 128)]
    # memory_list = metadata['memory_list'] if 'memory_list' in metadata else [i for i in range(128, 2048, 128)]
    # memory_list.append(3008)
    memory_list = [i for i in range(128, 3009, 1)] # 128 to 3008 MB
     
    # Check if the model is already loaded
    if model_name is None or model_name != model_key:
        # Load the model
        rf_model = load_model(bucket_name, model_key)
        model_name = model_key
    # if rf_model is None:
    #     # Load the model
    #     rf_model = load_model(bucket_name, model_key)

    # If the payload is out of the model's range, return a default 3008 MB memory
    if payload > max_payload:
        return invoke_lambda(lambda_name, payload, 3008)
    elif payload < min_payload:
        payload = min_payload
    # Make a prediction
    # Generate predictions and check constraints
    pareto_front = []
    candidate = [] 
    start = time.time()
    # print("[['memory_utilisation', 'billed_duration', 'function_error']]")
    for mem in memory_list:
        features = pd.DataFrame([[mem, payload]], columns=['total_memory', 'payload'])
        prediction = rf_model.predict(features)[0]
        # Check if the prediction meets the deadline and cost constraints
        if not constraint_violation(prediction, deadline, cost, mem):
            pareto_front.append((mem, prediction))

    prediction = None
    if pareto_front != []:
        # Identify Pareto optimal solutions
        pareto_front = sorted(pareto_front, key=lambda x: x[0])
        try:
            # pareto = (mem, [utilisation, duration, error])
            min = (_tolerance/100)*pareto_constraint(pareto_front[0][1], pareto_front[0][0])
        except:
            print("No solution found for input size", payload)  
            
            
        for sol in pareto_front:
            # pareto = (mem, [utilisation, duration, error])
            # pareto_constraint(prediction, memory)
            _tmp = (_tolerance/100)*pareto_constraint(sol[1], sol[0])
            if _tmp < min:
                candidate.append(sol)
                min = _tmp
                required_constraint = min
        prediction = candidate[0] if candidate else pareto_front[0]
    best_mem = 128 # default value
    if len(pareto_front) == 0:
        # print("No solution found for input size", payload)
        best_mem = 3008
        prediction = rf_model.predict(pd.DataFrame([[best_mem, payload]], columns=['total_memory', 'payload']))[0]
    else:
        best_mem = prediction[0]
    print(f"Best memory configuration for input size {payload} is {best_mem} MB")
    print(f"Time taken for optimisation: {time.time()-start} seconds")
    # print('Prediction:', prediction)
    # Invoke the lambda
    _invoke_result = invoke_lambda(lambda_name, payload, best_mem)
    if _invoke_result:
        return {
            'minimum_constraint': required_constraint if required_constraint else deadline,
            'best_memory': best_mem,
            'billed_duration': _invoke_result['body']['BilledDuration'],
            'init_duration': _invoke_result['body']['InitDuration'],
            'memory_size': _invoke_result['body']['MemorySize'],
            'memory_used': _invoke_result['body']['MemoryUsed'],
            'function_error': _invoke_result['body']['FunctionError'],
            'predicted_memory_utilisation': prediction[1][0] if len(pareto_front) > 0 else prediction[0],
            'predicted_duration': prediction[1][1] if len(pareto_front) > 0 else prediction[1],
            'predicted_error': prediction[1][2] if len(pareto_front) > 0 else prediction[2]
        }
    return {
        'statusCode': 500,
        'body': 'Error invoking Lambda function'
    }

# Define the Pareto constraint function
def pareto_constraint(prediction, memory):
    global _tolerance
    global _duration_alpha
    global _pricing
    used_memory_max = prediction[0]*memory/100
    duration = prediction[1]
    error = prediction[2]
    bill = used_memory_max*duration*_pricing[str(memory)]
    # duration and cost
    result = ((1-_duration_alpha)*bill) + (_duration_alpha*duration)
    return result

# Define the constraint violation function
def constraint_violation(prediction, deadline, cost, memory):
    global _pricing
    mean_price = np.mean(list(_pricing.values()))
    used_memory_max = prediction[0]*memory/100
    duration = prediction[1]
    error = prediction[2]
    bill = used_memory_max*duration*_pricing[str(memory)]
    cost = cost*mean_price
    if bill > cost or duration > deadline \
          or used_memory_max > memory or error > 0.5:
        return True
    return False

def invoke_lambda(lambda_name, payload, memory):
    lambda_client = boto3.client('lambda', region_name='ap-southeast-2')

    # Check if there exists a version with the desired memory configuration
    try:
        response = lambda_client.list_versions_by_function(FunctionName=lambda_name)
        versions = [v['Version'] for v in response['Versions']]
        version_with_best_mem = None

        for version in versions:
            if version == '$LATEST':
                continue
            config = lambda_client.get_function_configuration(FunctionName=lambda_name, Qualifier=version)
            if config['MemorySize'] == memory:
                version_with_best_mem = version
                break

        if version_with_best_mem:
            print(f"Version {version_with_best_mem} of Lambda function {lambda_name} with memory {memory} exists.")
        else:
            print(f"No version of Lambda function {lambda_name} with memory {memory} exists. Creating version...")
            lambda_client.update_function_configuration(FunctionName=lambda_name, MemorySize=memory, Description=f'RAM{memory}')
            # wait for the configuration to be updated
            time.sleep(10)
            publish_response = lambda_client.publish_version(FunctionName=lambda_name)
            version_with_best_mem = publish_response['Version']
            lambda_client.create_alias(FunctionName=lambda_name, FunctionVersion=version_with_best_mem, Name=f'RAM{memory}')
            print(f"Version {version_with_best_mem} of Lambda function {lambda_name} created with memory {memory}.")
    except Exception as e:
        print(f"Error checking or creating Lambda function version: {e}")
        return

    # Invoke the Lambda function version
    try:
        if lambda_name == 'workbench-chameleon':
            payload = {
                    "num_of_rows": payload,
                    "num_of_cols": 25
                }
        elif lambda_name == 'workbench-pyaes':
            payload = {
                    "length_of_message": payload,
                    "num_of_iterations": 10
            }
        else:
            payload = {'n': payload}
        response = lambda_client.invoke(
            FunctionName=lambda_name,
            Qualifier=version_with_best_mem,
            LogType='Tail',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        print(f"Lambda function {lambda_name} version {version_with_best_mem} invoked.")
        request_id = response['ResponseMetadata']['RequestId']
        print(f'PAYLOAD\tRequestId:\t{request_id}\tQualifier:\t{version_with_best_mem}\tInput:\t{payload}\n')
        # Get the Billed duration from response
        _log_result = base64.b64decode(response.get('LogResult')).decode('utf-8')
        billed_duration = extract_duration(_log_result)
        init_duration = extract_init_duration(_log_result)
        memory_size = extract_memory_size(_log_result)
        memory_used = extract_memory_used(_log_result)
        function_error = extract_function_error(_log_result)
    
        # return response['ResponseMetadata']['RequestId']
        return {
            'statusCode': 200,
            'body':{
                'RequestId': response['ResponseMetadata']['RequestId'],
                'BilledDuration': billed_duration,
                'InitDuration': init_duration,
                'MemorySize': memory_size,
                'MemoryUsed': memory_used,
                'FunctionError': function_error
            }
        }


    except Exception as e:
        print(f"Error invoking Lambda function version: {e}")
        return
    
def extract_function_error(log):
    regex = r'Error (?P<Error>.*)|'\
            r'Exception (?P<Exception>.*)|'\
            r'error (?P<error>.*)|'\
            r'Status (?P<Status>.*)'
    match = re.search(regex, log, re.IGNORECASE)
    if match:
        if match.group('Error'):
            return match.group('Error')
        elif match.group('Exception'):
            return match.group('Exception')
        elif match.group('error'):
            return match.group('error')
        elif match.group('Status'):
            return match.group('Status')
    return None

def extract_request_id(log):
    regex = r'^REPORT RequestId:\s+([a-f0-9-]+)'
    match = re.search(regex, log)
    if match:
        return match.group(1)
    return None

def extract_duration(log):
    regex = r'Billed Duration: (\d+) ms'
    match = re.search(regex, log)
    if match:
        return int(match.group(1))
    return None

def extract_init_duration(log):
    regex = r'Init Duration: (\d+)'
    match = re.search(regex, log)
    if match:
        return int(match.group(1))
    return None

def extract_memory_size(log):
    regex = r'Memory Size: (\d+) MB'
    match = re.search(regex, log)
    if match:
        return int(match.group(1))
    return None

def extract_memory_used(log):
    regex = r'Memory Used: (\d+) MB'
    match = re.search(regex, log)
    if match:
        return int(match.group(1))
    return None
