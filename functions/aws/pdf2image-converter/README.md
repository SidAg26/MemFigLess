<!-- Build the Docker Image -->
docker build --platform linux/amd64 -t pdf2image:first .

<!-- Deploying the Image -->
aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 030103857128.dkr.ecr.ap-southeast-2.amazonaws.com
<!-- Your password will be stored unencrypted in /home/ubuntu/.docker/config.json -->

<!-- Create a Registry in ECR service -->
aws ecr create-repository --repository-name pdf2image-lambda --region ap-southeast-2 --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE

<!-- Link of Repository  -->
030103857128.dkr.ecr.ap-southeast-2.amazonaws.com/pdf2image-lambda

<!-- Docker tag the Image to Amazon Registry -->
docker tag pdf2image:first 030103857128.dkr.ecr.ap-southeast-2.amazonaws.com/pdf2image-lambda:latest

<!-- Push the image to Amazon ECR -->
docker push 030103857128.dkr.ecr.ap-southeast-2.amazonaws.com/pdf2image-lambda:latest

<!-- Role for the function -->
arn:aws:iam::030103857128:role/TestDockerImage

<!-- Create the function from CLI with Role -->
aws lambda create-function \
  --function-name pdf2image-lambda \
  --package-type Image \
  --region ap-southeast-2 \
  --code ImageUri=030103857128.dkr.ecr.ap-southeast-2.amazonaws.com/pdf2image-lambda:latest \
  --role arn:aws:iam::030103857128:role/TestDockerImage


<!-- Update the function with a new image -->
aws lambda update-function-code \
  --function-name pdf2image-lambda \
  --region ap-southeast-2 \
  --image-uri 030103857128.dkr.ecr.ap-southeast-2.amazonaws.com/pdf2image-lambda:latest