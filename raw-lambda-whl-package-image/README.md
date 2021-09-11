## Deploying a Raw Lambda with Wheel Package as a Container

This spike explores deploying a Lambda that imports Python modules written separately for testability with the containe approach. This results in a wheel file that needs to installed in the container at deploy time. Considering the project layout below:

```
.
├── dist
│             ├── rest_helper-0.0.1-py3-none-any.whl
│             └── rest-helper-0.0.1.tar.gz
├── Dockerfile
├── ecr_repository_policy.json
├── functions
│             ├── getter.py
│             └── poster.py
├── LICENSE
├── packaged
│             ├── rest_helper
│             │             ├── __init__.py
│             │             └── rest_helper.py
├── pyproject.toml
├── setup.cfg
└── test
    └── test_rest_helper.py
```

- The Lambders are `poster.py` and `getter.py` in the `functions` folder. The `requests` library functionality of `POST` and `GET` are in the `rest_helper` folder in `packaged`. `pyproject.toml` and `setup.cfg` are for creating the package.
- Running `pip install -e .` in the `src` directory installs an editable dependency in the virtual environment with a sim link so that dependent python code in my tests and lambdas always has the latest in real time. 
- Running `python3 -m build` in `src` creates the wheel file in `dist`.
- The `Dockerfile` contains commands to copy the `.whl` file from `dist` into the image and install it (not necessary to involve pypi if used in the same repository). I tried parameterizing the Dockerfile with `ARG`s, but that flopped, so I need to tinker with that some more to make it reusable for any Lambda and wheel file(s) combination.
- This accomplishes:
  * the tests in test can access the package locally (with the sim link)
  * the lambda import statements work in vs code with dot notation as if using a pip installed package (with the sim link)
  * the lambdas themselves have access to the dependencies when running in their cloud environment (with the pip installed .whl file in the container).


### Instructions

1. Build the image with the `Dockerfile` in `src`:
```
docker build -t raw-lambda-wheel-image .
```

2. Login to ECR:
```
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin [AWS account number].dkr.ecr.us-west-2.amazonaws.com
```

3. Create a repository for the image:
```
aws ecr create-repository --repository-name raw-lambda-wheel-image --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
```

4. Tage the local Docker image:
```
docker tag  raw-lambda-wheel-image:latest [AWS account number].dkr.ecr.us-west-2.amazonaws.com/raw-lambda-wheel-image:latest
```

5. ...and push to the repository:
```
docker push [AWS account number].dkr.ecr.us-west-2.amazonaws.com/raw-lambda-wheel-image:latest
```

6. Set the repository policy for the repository (policy file in `src`):
```
aws ecr set-repository-policy \
    --repository-name raw-lambda-wheel-image \
    --policy-text file://ecr_repository_policy.json
```

7. Create an IAM Role for the Lambda:
```
$ aws iam create-role --role-name raw-lambda-wheel-image-role \
  --assume-role-policy-document file://raw_lambda_whl_image_trust_policy.json
```

8. Attach the Lambda execution role policy to the role:
```
$ aws iam attach-role-policy --role-name raw-lambda-wheel-image-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

9. Deploy the Lambda:
```
aws lambda create-function --region us-west-2 --function-name raw-lambda-wheel-image \
    --package-type Image  \
    --code ImageUri=[AWS account number].dkr.ecr.us-west-2.amazonaws.com/raw-lambda-wheel-image:latest   \
    --role arn:aws:iam::[AWS account number]:role/raw-lambda-wheel-image-role
```

### Clean Up

1. Delete the Lambda:
```
$ aws lambda delete-function --function-name raw-lambda-wheel-image
```

2. Detach Lambda Execution Role policy from the IAM role:
```
$ aws iam detach-role-policy --role-name raw-lambda-wheel-image-role \
--policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

3. Delete the IAM role:
```
$ aws iam delete-role --role-name raw-lambda-wheel-image-role
```