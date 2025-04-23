<!-- Build the Docker Image -->
docker build --platform linux/amd64 -t flask:first .

<!-- Deploying the Image -->
aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 030103857128.dkr.ecr.ap-southeast-2.amazonaws.com
<!-- Your password will be stored unencrypted in /home/ubuntu/.docker/config.json -->

<!-- Create a Registry in ECR service -->
aws ecr create-repository --repository-name flask-inference --region ap-southeast-2 --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE

<!-- Link of Repository  -->
030103857128.dkr.ecr.ap-southeast-2.amazonaws.com/flask-inference

<!-- Docker tag the Image to Amazon Registry -->
docker tag flask:first 030103857128.dkr.ecr.ap-southeast-2.amazonaws.com/flask-inference:latest

<!-- Push the image to Amazon ECR -->
docker push 030103857128.dkr.ecr.ap-southeast-2.amazonaws.com/flask-inference:latest

<!-- Create the ECS cluster -->
aws ecs create-cluster --cluster-name sklearn-inference-cluster --region ap-southeast-2

<!-- Create the Task Definition using JSON -->


<!-- Test Image locally -->
curl -X POST http://<your-public-ip-or-dns>:5000/predict -H "Content-Type: application/json" -d '{"payload": 100, "cpu_user_time": 50}'