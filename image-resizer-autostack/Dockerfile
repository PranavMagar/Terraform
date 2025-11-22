FROM public.ecr.aws/lambda/python:3.10

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code into the container
COPY app.py ${LAMBDA_TASK_ROOT}

# Command for Lambda
CMD ["app.lambda_handler"]

