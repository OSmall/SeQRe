import boto3
import os
import json

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):

    primary_key_table = dynamodb.Table(os.environ['PRIMARY_KEY_TABLE'])

    keys = primary_key_table.scan()


    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps({
            "success": True,
            "keys": keys
        }),
        'headers': {
            "Content-Type" : "application/json",
            "Access-Control-Allow-Origin" : "*",
            "Allow" : "GET, OPTIONS, POST",
            "Access-Control-Allow-Methods" : "GET, OPTIONS, POST",
            "Access-Control-Allow-Headers" : "*"
        }
    }

