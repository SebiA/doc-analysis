## AWS Requirements:
Create an S3 bucket for app hosting (static web hosting must be enabled for this bucket)
Create an S3 bucket for uploading PDF documents
Create a Lambda function that gets triggered on S3 file upload, and include this in the deployment package
Create a Lambda function that reads the output JSON file from app hosting bucket
Create an API via API Gateway that triggers the read output Lambda function
Get access to a Bedrock model


## Creating a deployment package for AWS Lambda (Linux):
1. cd [project_directory_name]
2. py -m venv my_virtual_env
3. source ./my_virtual_env/bin/activate
4. pip install -r requirements.txt
5. pip show [package_name]
6. deactivate
7. zip -r ../../../../my_deployment_package.zip
8. cd ../../../../
9. zip my_deployment_package.zip app.py

