# <!-- Build the Docker Image -->
docker build --platform linux/amd64 -t inference:first .

# <!-- Docker tag the Image to Amazon Registry -->
docker tag inference:first 030103857128.dkr.ecr.ap-southeast-2.amazonaws.com/sklearn-inference:latest

# <!-- Push the image to Amazon ECR -->
docker push 030103857128.dkr.ecr.ap-southeast-2.amazonaws.com/sklearn-inference:latest

# <!-- Update the function with a new image -->
aws lambda update-function-code \
  --function-name sklearn-regression-inference \
  --region ap-southeast-2 \
  --image-uri 030103857128.dkr.ecr.ap-southeast-2.amazonaws.com/sklearn-inference:latest