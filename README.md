# serverlessPyPi

This is a sample template for serverlessPyPi - Below is a brief explanation of what we have generated for you:

```bash
S3Bucket=478921047804-staging
ProjectName=serverless-pypi

FunctionsTemplateFile=$(uuidgen).yaml
ACMTemplateFile=$(uuidgen).yaml
APIGWTemplateFile=$(uuidgen).yaml

#Functions
sam build --use-container -b ./build/ -t ./templates/functions.yaml \
&& sam package --s3-bucket $S3Bucket --template-file build/template.yaml --output-template-file build/packaged.yaml --profile pypi \
&& aws s3 cp build/packaged.yaml s3://$S3Bucket/templates/$FunctionsTemplateFile --profile pypi

#ACM
sam build --use-container -b ./build/ -t ./templates/acm.yaml \
&& sam package --s3-bucket $S3Bucket --template-file build/template.yaml --output-template-file build/packaged.yaml --profile pypi \
&& aws s3 cp build/packaged.yaml s3://$S3Bucket/templates/$ACMTemplateFile --profile pypi

#APIGW
aws s3 cp ./templates/APIGateway.yaml s3://$S3Bucket/templates/$APIGWTemplateFile --profile pypi

aws cloudformation deploy \
--template-file serverless-pypi.yaml \
--stack-name $ProjectName \
--capabilities CAPABILITY_IAM \
--parameter-overrides Domain=rboyd.dev Stage=pypi FunctionStackURL="https://$S3Bucket.s3.amazonaws.com/templates/$BaseTemplateFile" ACMStackURL="https://$S3Bucket.s3.amazonaws.com/templates/$ACMTemplateFile" APIGWStackURL="https://$S3Bucket.s3.amazonaws.com/templates/$APIGWTemplateFile" \
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