# serverlessPyPi

This is a sample template for serverlessPyPi - Below is a brief explanation of what we have generated for you:

```bash
S3Bucket=478921047804-staging
ProjectName=serverless-pypi

BaseTemplateFile=https://s3.amazonaws.com/$S3Bucket/templates/$(uuidgen).yaml
ACMTemplateFile=https://s3.amazonaws.com/$S3Bucket/templates/$(uuidgen).yaml
APIGWTemplateFile=https://s3.amazonaws.com/$S3Bucket/templates/$(uuidgen).yaml

#Functions
sam build --use-container -b ./build/ -t ./templates/functions.yaml \
&& sam package --s3-bucket $S3Bucket --template-file build/template.yaml --output-template-file build/packaged.yaml --profile pypi \
&& aws s3 cp build/packaged.yaml $BaseTemplateFile --profile pypi

#ACM
sam build --use-container -b ./build/ -t ./templates/acm.yaml \
&& sam package --s3-bucket $S3Bucket --template-file build/template.yaml --output-template-file build/packaged.yaml --profile pypi \
&& aws s3 cp build/packaged.yaml $ACMTemplateFile --profile pypi

#APIGW
aws s3 cp ./templates/APIGateway.yaml $APIGWTemplateFile --profile pypi

aws cloudformation deploy \
--template-file serverless-pypi.yaml \
--stack-name $ProjectName \
--capabilities CAPABILITY_IAM \
--parameter-overrides DOMAIN=rboyd.dev STAGE=pypi \
--profile pypi

## Testing 
sam local invoke -t ./build/template.yaml --event event.json HelloWorldFunction


JWTProvider=$(aws cloudformation describe-stacks --stack-name $ProjectName-base --profile pypi | jq '."Stacks"[0]."Outputs"[] | select(.OutputKey | contains("JWTProviderFunctionArn"))."OutputValue"' -r)
AuthFunction=$(aws cloudformation describe-stacks --stack-name $ProjectName-base --profile pypi | jq '."Stacks"[0]."Outputs"[] | select(.OutputKey | contains("AuthorizerFunctionArn"))."OutputValue"' -r)


python src/pip install richardexample -i https://pypi.rboyd.dev --verbose --no-cache-dir
UserName=Richard
Password=[]
pip install richardexample -i https://$UserName:$Password@pypi.rboyd.dev/ --verbose --no-cache-dir
```