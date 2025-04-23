# AWS Functions

This directory contains AWS Lambda functions that are part of the MemFigLess application. Each function is designed to handle specific tasks in the application's workflow.

## Directory Structure

### 1. pdf2image-converter
A Lambda function that converts PDF files to images.
- `lambda_function.py`: Main function code
- `Dockerfile`: Container configuration
- `requirements.txt`: Python dependencies
- `config.json`: Function configuration
- `README.md`: Detailed documentation

### 2. aws-text-analyser
A Lambda function for text analysis using AWS services.
- `lambda_function.py`: Main function code
- `requirements.txt`: Python dependencies
- `config.json`: Function configuration
- `README.md`: Detailed documentation
- `AWS-Text-Analyser-Function.svg`: Architecture diagram
- `power-tuning-text-analyser.png`: Performance optimization results

### 3. aws-image-resizer
A Lambda function for image resizing operations.
- `lambda_function.py`: Main function code
- `requirements.txt`: Python dependencies
- `config.json`: Function configuration
- `README.md`: Detailed documentation
- `AWS-Image-Resizer-Workflow.svg`: Architecture diagram
- `AWS-Image-Resizer-Workflow.jpg`: Architecture diagram (JPG version)
- `power-tuning-result-image-resizer.png`: Performance optimization results
- `pillow_package/`: Directory containing Pillow library dependencies
- `pillow_package.zip`: Zipped Pillow library package

## Usage

Each function directory contains its own README.md with specific instructions for deployment and usage. Please refer to the individual function directories for detailed documentation.

## Deployment

To deploy these functions:
1. Navigate to the specific function directory
2. Follow the deployment instructions in the function's README.md
3. Ensure all dependencies are properly configured
4. Deploy using AWS SAM or AWS CLI

## Requirements

- AWS Account with appropriate permissions
- AWS CLI or AWS SAM CLI installed
- Python 3.x
- Docker (for containerized deployments)
