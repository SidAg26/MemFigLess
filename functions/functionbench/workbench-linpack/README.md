### Linpack Operation Function <br>
1. send input _payload_ with request body
2. invoke _function_ to assess and return 
(Function available at [GitRepo](https://github.com/ddps-lab/serverless-faas-workbench))

__NOTE:__ <br>
- PowerTools for AWS Lambda (Python) for distributed tracing, structured logging, metrics and event routing 

#### Architecture Diagram
![ArchitectureDiagram](../sebs-floatOperation/AWS-Float-Sleep-Linpack-Matmul-PyAES.svg)

#### AWS Lambda Power Tuning Tool Result
![PowerTuneResult](./power-tuning-linpack-(1-1000).png "Power Tuning")

__Note:__ <br>
 - this analysis was done on [AWS Lambda Power Tuning tool](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:451282441545:applications~aws-lambda-power-tuning) and the results were generated using payload - 1, 10, 100, 1000
 - the generated results are also available at [link](https://lambda-power-tuning.show/#gAAAAYABAAKAAgADgAMABIAEAAWABQAGgAYAB4AHAAiACAAJgAkACoAKAAuAC8AL;VVXSQ1VVWkMAAANDq6rEQlVVnUIAAIdCq6pcQquqSkKrqiZCVVUZQquqHkKrqgpCVVUVQquq+kGrqvJBq6riQVVV7UEAAPRBq6rOQauq2kGrqsZBVVWxQQAAzEGrqp5B;5FJtNS3odjUvil01HjtfNc6qXjXZ/mU14PlcNdn+ZTWFFVU1QNlbNcwIeDWUwmw1yzyLNUmLfDVJEIM1IciCNUi/jzW+Rp01yzyLNQ3XnTWd+ZM1qJ6ONfaMqDUQeYQ1) (might/might not be active)