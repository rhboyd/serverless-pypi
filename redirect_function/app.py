import boto3

s3_client = boto3.client('s3')


def lambda_handler(event, context):
    response = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': 'serverless-pypi-base-pypibucket-1priygfe8yxtu',
            'Key': event['version']
        },
        ExpiresIn=900
    )
    return {
        'location': response
    }
