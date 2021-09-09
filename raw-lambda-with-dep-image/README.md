## Simple Deploy of Lambda Function With Dependencies Using a Container Image

`pip freeze > requirements.txt`

`docker build -t raw-lambda-image .`

`aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin [AWS account number].dkr.ecr.us-west-2.amazonaws.com`

`aws ecr create-repository --repository-name raw-lambda-with-dep --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE`

`docker tag  raw-lambda-with-dep:latest [AWS account number].dkr.ecr.us-west-2.amazonaws.com/raw-lambda-with-dep:latest`

`docker push [AWS account number].dkr.ecr.us-west-2.amazonaws.com/raw-lambda-with-dep:latest`

4. Set the repository policy for the repository
```
aws ecr set-repository-policy \
    --repository-name raw-lambda-with-dep \
    --policy-text file://ecr_repository_policy.json
```

5. Create an IAM Role for the Lambda:
```
$ aws iam create-role --role-name raw-lambda-with-dep-image-role \
  --assume-role-policy-document file://raw_lambda_with_dep_image_trust_policy.json
```

4. Attach the Lambda execution role policy to the role:
```
$ aws iam attach-role-policy --role-name raw-lambda-with-dep-image-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

5. Deploy the Lambda:
```
aws lambda create-function --region us-west-2 --function-name raw-lambda-with-dep-image \
    --package-type Image  \
    --code ImageUri=[AWS account number].dkr.ecr.us-west-2.amazonaws.com/raw-lambda-with-dep:latest   \
    --role arn:aws:iam::[AWS account number]:role/raw-lambda-with-dep-image-role
```

### Clean Up
1. Delete the Lambda:
```
$ aws lambda delete-function --function-name raw-lambda-no-dep-zip
```

2. Detach Lambda Execution Role policy from the IAM role:
```
$ aws iam detach-role-policy --role-name raw-lambda-no-dep-zip-role \
--policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

3. Delete the IAM role:
```
$ aws iam delete-role --role-name raw-lambda-no-dep-zip-role
```