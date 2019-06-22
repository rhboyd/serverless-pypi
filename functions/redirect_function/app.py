import boto3
import os

bucket_name = os.environ['BUCKET_NAME']
s3_client = boto3.client('s3')


def lambda_handler(event, context):
    if "package_id" in event['pathParameters']:
        key = event['pathParameters']['package_id']
    else:
        return {
            'statusCode': 404,
            'body': "Package Not Found"
        }
    response = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name,
            'Key': key
        },
        ExpiresIn=900
    )
    return {
        'statusCode': 301,
        'headers': {
            'location': response
        }
    }
