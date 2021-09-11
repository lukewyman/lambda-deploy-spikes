## Directly Deploying a Simple Lambda Function With Dependencies
Same as Spike 1, but this time adding the `requests` library as a dependency.

1. Create and activate a Python environment at the same level as `src` and activate it:

```
$ virtualenv lambda_env
$ source lambda_env/bin/activate
```

2. Install the requests library and deactivate the environment:
```
$ pip install requests
$ deactivate
```

3. Navigate to the `site-packages` directory in the Python environment, and create a zip file of it's contents in `src`:
```
$ cd lambda_env/lib/python3.8/site-packages/
$ zip -r ../../../../src/my-deployment-package.zip .
```

4. Navigate back to the `src` directory and add the Lambda function to the zip created in step 3.
```
$ cd ../../../../src
$ zip -g my-deployment-package.zip lambda_function.py
```

5. Create an IAM Role for the Lambda:
```
$ aws iam create-role --role-name raw-lambda-with-dep-zip-role \
  --assume-role-policy-document file://raw_lambda_with_dep_trust_policy.json
```

6. Attach the Lambda execution role policy to the role:
```
$ aws iam attach-role-policy --role-name raw-lambda-with-dep-zip-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

7. Deploy the zipped up Lambda:
```
$ aws lambda create-function --function-name raw-lambda-with-dep-zip \
  --zip-file fileb://my-deployment-package.zip \
  --handler lambda_function.lambda_handler --runtime python3.8 \
  --role arn:aws:iam::[AWS account number]:role/raw-lambda-with-dep-zip-role
```

### Clean Up

1. Delete the Lambda:
```
$ aws lambda delete-function --function-name raw-lambda-with-dep-zip
```

2. Detach Lambda Execution Role policy from the IAM role:
```
$ aws iam detach-role-policy --role-name raw-lambda-with-dep-zip-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

3. Delete the IAM role:
```
$ aws iam delete-role --role-name raw-lambda-with-dep-zip-role
```
