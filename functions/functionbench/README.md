# Function Benchmarks

This directory contains a collection of serverless function benchmarks designed to test and measure performance characteristics of different workloads. Each benchmark focuses on a specific type of computation or workload pattern.

## Available Benchmarks

### workbench-pyaes
AES encryption/decryption benchmark using PyAES
- `lambda_function.py`: Main function implementation
- `requirements.txt`: Python dependencies
- `config.json`: Configuration settings
- `pyaes_layer.zip`: Pre-built layer for PyAES
- `python/`: Additional Python resources
- `README.md`: Benchmark-specific documentation

### workbench-matmul
Matrix multiplication benchmark
- `lambda_function.py`: Main function implementation
- `requirements.txt`: Python dependencies
- `config.json`: Configuration settings
- `README.md`: Benchmark-specific documentation

### workbench-linpack
Linear algebra benchmark
- `lambda_function.py`: Main function implementation
- `requirements.txt`: Python dependencies
- `config.json`: Configuration settings
- `deployment_package.zip`: Pre-built deployment package
- `package/`: Additional package resources
- `power-tuning-linpack-(1-1000).png`: Power tuning visualization
- `README.md`: Benchmark-specific documentation

### workbench-chameleon
Chameleon benchmark
- `lambda_function.py`: Main function implementation
- `requirements.txt`: Python dependencies
- `config.json`: Configuration settings
- `README.md`: Benchmark-specific documentation

## Common Structure

Each benchmark directory follows a similar structure:
- `lambda_function.py`: The main function code
- `requirements.txt`: Python dependencies
- `config.json`: Configuration settings
- `README.md`: Benchmark-specific documentation
- Additional resources and layers as needed

## Usage

1. Navigate to the specific benchmark directory you want to use
2. Review the benchmark-specific README for detailed instructions
3. Deploy the function using your preferred serverless platform
4. Run the benchmark and collect performance metrics

## Requirements

- Python 3.x
- Serverless platform (e.g., AWS Lambda, Azure Functions)
- Dependencies specified in each benchmark's requirements.txt

## Notes

- Each benchmark is designed to be self-contained and deployable independently
- Configuration can be modified through the config.json file
- Performance metrics and results should be collected according to your specific needs
- Some benchmarks include pre-built layers or deployment packages for convenience
