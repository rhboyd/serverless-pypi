# serverlessPyPi

This is a sample template for serverlessPyPi - Below is a brief explanation of what we have generated for you:

```bash
S3Bucket=478921047804-staging
ProjectName=serverless-pypi
sam build --use-container -b ./build/ -t ./template.yaml \
&& sam package --s3-bucket $S3Bucket --template-file build/template.yaml --output-template-file build/packaged.yaml --profile pypi\
&& aws cloudformation deploy --template-file build/packaged.yaml --stack-name $ProjectName-base --capabilities CAPABILITY_IAM --profile pypi


sam build --use-container -b ./build/ -t ./acm.yaml \
&& sam package --s3-bucket $S3Bucket --template-file build/template.yaml --output-template-file build/packaged.yaml --profile pypi\
&& aws cloudformation deploy --template-file build/packaged.yaml --stack-name $ProjectName-acm --parameter-overrides STAGE=pypi DOMAIN=rboyd.dev --capabilities CAPABILITY_IAM --profile pypi

aws cloudformation deploy --template-file APIGateway.yaml --stack-name $ProjectName-api --capabilities CAPABILITY_IAM --parameter-overrides DOMAIN=rboyd.dev STAGE=pypi --profile pypi

## Testing 
sam local invoke -t ./build/template.yaml --event event.json HelloWorldFunction


python src/pip install richardexample -i https://pypi.rboyd.dev --verbose --no-cache-dir
```