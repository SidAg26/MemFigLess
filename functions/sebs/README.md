# SEBS (Serverless Benchmark Suite) Functions

This directory contains a collection of serverless function benchmarks designed to test and measure performance characteristics of different workloads. Each benchmark focuses on a specific type of computation or workload pattern.

## Available Benchmarks

### sebs-sleepOperation
Sleep operation benchmark
- `lambda_function.py`: Main function implementation
- `requirements.txt`: Python dependencies
- `config.json`: Configuration settings
- `README.md`: Benchmark-specific documentation

### sebs-graph-pagerank
PageRank algorithm implementation
- `lambda_function.py`: Main function implementation
- `requirements.txt`: Python dependencies
- `config.json`: Configuration settings
- `README.md`: Benchmark-specific documentation

### sebs-graph-mst
Minimum Spanning Tree algorithm implementation
- `lambda_function.py`: Main function implementation
- `requirements.txt`: Python dependencies
- `config.json`: Configuration settings
- `README.md`: Benchmark-specific documentation

### sebs-graph-bfs
Breadth-First Search algorithm implementation
- `lambda_function.py`: Main function implementation
- `requirements.txt`: Python dependencies
- `config.json`: Configuration settings
- `README.md`: Benchmark-specific documentation

### sebs-floatOperation
Floating-point operation benchmark
- `lambda_function.py`: Main function implementation
- `requirements.txt`: Python dependencies
- `config.json`: Configuration settings
- `README.md`: Benchmark-specific documentation

### sebs-dynamic-html
Dynamic HTML generation benchmark
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
- The benchmarks cover various aspects of serverless performance including:
  - Computational performance (graph algorithms, float operations)
  - System behavior (sleep operations)
  - Web capabilities (dynamic HTML generation)

## Contributing

When adding new SEBS functions:
1. Create a new directory with the prefix `sebs-`
2. Include a README.md in the function directory
3. Follow the existing structure and naming conventions
4. Document any specific requirements or dependencies
