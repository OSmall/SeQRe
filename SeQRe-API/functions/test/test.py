import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):

    primary_key_table = dynamodb.Table(os.environ['PRIMARY_KEY_TABLE'])

    keys = primary_key_table.scan()

    print("test")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": os.environ['PRIMARY_KEY_TABLE'],
            "keys": keys
        }),
    }