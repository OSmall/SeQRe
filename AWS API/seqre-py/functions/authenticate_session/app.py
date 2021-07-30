import json, os, base64, random
import boto3
from boto3.dynamodb.conditions import Key
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256

"""Sample pure Lambda function

Parameters
----------
event: dict, required
    API Gateway Lambda Proxy Input Format

    Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

context: object, required
    Lambda Context runtime methods and attributes

    Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

Returns
------
API Gateway Lambda Proxy Output Format: dict

    Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
"""

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    
    body = json.loads(event['body'])
    id = body['id']
    otp = body['otp']

    output = ''

    sessionKeyTable = dynamodb.Table(os.environ['SESSION_KEY_TABLE'])

    # row = sessionKeyTable.query(KeyConditionExpression=Key('id').eq(id))['Items'][0]
    row = sessionKeyTable.get_item(Key={'id': id})['Item']


    sessionKey = row['key']
    length = int(row['length'])

    sha256 = base64.b64encode(SHA256.new(base64.b64decode(sessionKey.encode('ascii'))).digest()).decode('ascii')
    output = otp == sha256[:length]

    if output:
        sessionKeyTable.update_item(Key={"id": id}, UpdateExpression="set authenticated = :b", ExpressionAttributeValues={':b': True})

    return {
        "statusCode": 200,
        "body": json.dumps({
            "success": output
        }),
    }
