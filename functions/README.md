# MemFigLess Functions

This directory contains all the functions used in the MemFigLess research project, encompassing monitoring, data collection, and AWS Lambda experimentation components.

## Directory Structure

### aws/
Contains AWS Lambda functions used for real-world serverless applications:
- `pdf2image-converter/`: PDF to image conversion function
- `aws-text-analyser/`: Text analysis function
- `aws-image-resizer/`: Image resizing function

### functionbench/
Contains benchmark functions for performance evaluation:
- `workbench-pyaes/`: AES encryption benchmark
- `workbench-matmul/`: Matrix multiplication benchmark
- `workbench-linpack/`: LINPACK benchmark
- `workbench-chameleon/`: Chameleon benchmark suite

### memfigless-rfr/
Contains the implementation of the MemFigLess Random Forest Regression model and related components:
- `sklearn-regression-training/`: Training pipeline for the Random Forest model
- `sklearn-regression-inference/`: Inference deployment for the trained model

### sebs/
Contains functions related to the Serverless Benchmark Suite (SEBS) implementation:
- `sebs-sleepOperation/`: Sleep operation benchmark function
- `sebs-graph-pagerank/`: Graph PageRank algorithm implementation
- `sebs-graph-mst/`: Graph Minimum Spanning Tree algorithm
- `sebs-graph-bfs/`: Graph Breadth-First Search algorithm
- `sebs-floatOperation/`: Floating-point operation benchmark
- `sebs-dynamic-html/`: Dynamic HTML generation benchmark

### lambda-utility/
Contains utility functions and helper tools for AWS Lambda function management and deployment:
- `log_collector.py`: Utility for collecting and processing Lambda function logs
- `constants.py`: Shared constants and configuration values
- `main.ipynb`: Main notebook for utility operations and demonstrations
- `__init__.py`: Package initialization file

## Purpose

This collection of functions serves three main purposes:

1. **Initial Monitoring**: Functions used to collect performance metrics and resource utilization data from serverless environments.
   - Utilizes `log_collector.py` for gathering performance data
   - Implements various benchmark functions across SEBS and functionbench suites

2. **Training Data Collection**: Functions designed to gather and process data used for training the MemFigLess prediction models.
   - Leverages benchmark results from both SEBS and functionbench
   - Processes data through the sklearn-regression-training pipeline

3. **AWS Lambda Experimentation**: Production-ready functions used for actual experimentation and validation of the MemFigLess approach on the AWS Lambda platform.
   - Real-world applications in the `aws/` directory
   - Model deployment through sklearn-regression-inference
   - Comprehensive benchmarking using SEBS and functionbench suites

## Usage

Each subdirectory contains its own README with specific instructions for deploying and using the functions within that category. The `lambda-utility` tools can be used to manage and monitor the deployment and execution of these functions.
