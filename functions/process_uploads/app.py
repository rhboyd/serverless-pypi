import boto3
import json
import os
from pkginfo import SDist
import re

DDB_TABLE_NAME = os.environ['DDB_TABLE_NAME']

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DDB_TABLE_NAME)


def normalize(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def lambda_handler(event, context):

    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        with open('/tmp/local.tar.gz', 'wb') as f:
            s3_client.download_fileobj(bucket_name, object_key, f)
        mypackage = SDist('/tmp/local.tar.gz')
        print(mypackage.name)
        print(mypackage.version)
        table.put_item(
            Item={
                'PartitionKey': mypackage.name,
                'SortKey': mypackage.version,
                'Location': "{}/{}".format(bucket_name, object_key),
                'PackageName': object_key
            }
        )
        table.put_item(
            Item={
                'PartitionKey': "Package",
                'SortKey': mypackage.name
            }
        )

    return {
        "statusCode": 200,
        "headers": {"content-type": "text/html"},
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
