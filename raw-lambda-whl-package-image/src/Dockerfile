FROM public.ecr.aws/lambda/python:3.8

# Copy function code
COPY functions/getter.py ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
# from your project folder
COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY dist/rest_helper-0.0.1-py3-none-any.whl .
RUN  pip3 install --no-index --find-links=./ rest_helper-0.0.1-py3-none-any.whl --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler
CMD [ "getter.handler" ]