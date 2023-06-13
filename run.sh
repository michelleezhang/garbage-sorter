# Build the docker image
#docker build -t  recycle_aws_lambda .

# Create a ECR repository
#aws ecr create-repository --repository-name recycle_aws_lambda --image-scanning-configuration scanOnPush=true --region us-east-2

# Tag the image to match the repository name
#docker tag recycle_aws_lambda:latest 2086-9852-1732.dkr.ecr.us-east-2.amazonaws.com/recycle_aws_lambda:latest

# Register docker to ECR
#docker login -u AWS -p $(aws ecr get-login-password --region us-east-2) 2086-9852-1732.dkr.ecr.us-east-2.amazonaws.com
#echo $(aws ecr get-login-password)|docker login --password-stdin --username AWS ${aws_account}.dkr.ecr.us-west-2.amazonaws.com

#echo "Hello World!"
# Push the image to ECR
#docker push 2086-9852-1732.dkr.ecr.us-east-2.amazonaws.com/recycle_aws_lambda:latest

aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 208698521732.dkr.ecr.us-east-2.amazonaws.com 

docker build -t recycle_aws_lambda .

docker tag recycle_aws_lambda:latest 208698521732.dkr.ecr.us-east-2.amazonaws.com/recycle_aws_lambda:latest 

docker push 208698521732.dkr.ecr.us-east-2.amazonaws.com/recycle_aws_lambda:latest