import boto3
import json
import base64
import os
import jwt
import uuid
import time

DDB_TABLE_NAME = os.environ['DDB_TABLE_NAME']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DDB_TABLE_NAME)


def generate_policy(principal_id, effect, method_arn):
    auth_response = dict()
    auth_response['principalId'] = principal_id

    if effect and method_arn:
        policy_document = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Sid': 'FirstStatement',
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': method_arn
                }
            ]
        }

        auth_response['policyDocument'] = policy_document

    return auth_response


def extract_jwt_from_basic_auth(auth: str):
    base64_token = auth[6:]
    base64_decoded_token = base64.b64decode(base64_token)
    cust_username, cust_token = base64_decoded_token.decode('utf-8').split(":")
    print("Username: {}".format(cust_username))
    print("Token: {}".format(cust_token))
    return cust_token


def custom_auth_handler(event, context):
    jwt_token = extract_jwt_from_basic_auth(event['authorizationToken'])
    try:
        jwt_object = jwt.decode(jwt_token, 'secret', algorithms=['HS256'])
        user_name = jwt_object['username']
        user_version = jwt_object['version']
        table.get_item(
            Key={
                'PartitionKey': user_name,
                'SortKey': user_version
            }
        )
        return generate_policy(user_name, 'Allow', event['methodArn'])
    except Exception as e:
        print(e)
        return generate_policy("denied", 'Deny', event['methodArn'])


def jwt_provider_handler(event, context):
    body = json.loads(event['body'])
    if 'user_name' in body:
        user_name = body['user_name']
        user_version = str(uuid.uuid4())
        encoded_jwt = jwt.encode(
            {
                'username': user_name,
                'version': user_version
            },
            'secret',
            algorithm='HS256')

    else:
        return {
            "statusCode": 403
        }
    seconds = int(time.time()) + 600

    table.put_item(
        Item={
            'PartitionKey': user_name,
            'SortKey': user_version,
            'Expires': seconds
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'username': user_name,
            'password': encoded_jwt.decode('utf-8')
        })
    }
