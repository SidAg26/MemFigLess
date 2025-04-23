### Matmul Operation Function <br>
1. send input _payload_ with request body
2. invoke _function_ to calculate and return 
(Function available at [GitRepo](https://github.com/ddps-lab/serverless-faas-workbench))

__NOTE:__ <br>
- PowerTools for AWS Lambda (Python) for distributed tracing, structured logging, metrics and event routing 

#### Architecture Diagram
![ArchitectureDiagram](../sebs-floatOperation/AWS-Float-Sleep-Linpack-Matmul-PyAES.svg)

#### AWS Lambda Power Tuning Tool Result
![PowerTuneResult](./power-tuning-matmul-(1-1000).png "Power Tuning")

__Note:__ <br>
 - this analysis was done on [AWS Lambda Power Tuning tool](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:451282441545:applications~aws-lambda-power-tuning) and the results were generated using payload - 1, 10, 100, 1000
 - the generated results are also available at [link](https://lambda-power-tuning.show/#gAAAAYABAAKAAgADgAMABIAEAAWABQAGgAYAB4AHAAiACAAJgAkACoAKAAuAC8AL;AKAGRACAgkMAgCdDq6r/QlVVv0IAAKlCAACRQlVVgUIAAF5CAABIQlVVM0Krqi5Cq6oeQgAAFkJVVQdCVVULQquq/kGrqu5Bq6r2QQAA9EGrqvZBAADsQVVV6UEAAOxB;yuuXNSUhkzVZDo41l0+QNZ5KhzVIv481bweQNdaQkjVZDo41uu2MNfOEizUU0pQ11pCSNbPylTVIv481DdedNZFUmTXxM5g1jwOmNWHArjUzfbc1mQa6NUN7wjWYtcY1) (might/might not be active)