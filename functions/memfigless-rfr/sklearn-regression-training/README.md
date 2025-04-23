<!-- Build the Docker Image -->
docker build --platform linux/amd64 -t sklearn:first .

<!-- Deploying the Image -->
aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 030103857128.dkr.ecr.ap-southeast-2.amazonaws.com
<!-- Your password will be stored unencrypted in /home/ubuntu/.docker/config.json -->

<!-- Create a Registry in ECR service -->
aws ecr create-repository --repository-name sklearn-training --region ap-southeast-2 --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE

<!-- Link of Repository  -->
030103857128.dkr.ecr.ap-southeast-2.amazonaws.com/sklearn-training

<!-- Docker tag the Image to Amazon Registry -->
docker tag sklearn:first 030103857128.dkr.ecr.ap-southeast-2.amazonaws.com/sklearn-training:latest

<!-- Push the image to Amazon ECR -->
docker push 030103857128.dkr.ecr.ap-southeast-2.amazonaws.com/sklearn-training:latest

<!-- Role for the function -->
arn:aws:iam::030103857128:role/TestDockerImage

<!-- Create the function from CLI with Role -->
aws lambda create-function \
  --function-name sklearn-regression-training \
  --package-type Image \
  --region ap-southeast-2 \
  --code ImageUri=030103857128.dkr.ecr.ap-southeast-2.amazonaws.com/sklearn-training:latest \
  --role arn:aws:iam::030103857128:role/TestDockerImage


<!-- Update the function with a new image -->
aws lambda update-function-code \
  --function-name sklearn-regression-training \
  --region ap-southeast-2 \
  --image-uri 030103857128.dkr.ecr.ap-southeast-2.amazonaws.com/sklearn-training:latest