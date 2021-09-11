## Directly Deploying a Simple Lambda Function With No Dependencies

As a first step, this spike explores deploying a simple Lambda, without any dependencies, as a zip file. The instructions below are derived from [the AWS instructions](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html). Deployment uses the AWS CLI.

## Instructions

1. In the terminal, `cd` into the `src` directory.

2. Zip up the `lambda_function.py:
```
$ zip my-deployment-package.zip lambda_function.py
```

3. Create an IAM Role for the Lambda:
```
$ aws iam create-role --role-name raw-lambda-no-dep-zip-role \
  --assume-role-policy-document file://raw_lambda_no_dep_trust_policy.json
```

4. Attach the Lambda execution role policy to the role:
```
$ aws iam attach-role-policy --role-name raw-lambda-no-dep-zip-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

5. Deploy the zipped up Lambda:
```
$ aws lambda create-function --function-name raw-lambda-no-dep-zip \
  --zip-file fileb://my-deployment-package.zip \
  --handler lambda_function.lambda_handler \
  --runtime python3.8 \
  --role arn:aws:iam::[AWS account number]:role/raw-lambda-no-dep-zip-role
```
6. To test the Lambda from the AWS console, use `test-event.json` as your test data.

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