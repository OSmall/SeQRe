import json, os
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):

    body = json.loads(event['body'])
    id = body['id']
    alias = body['alias']
    pub_key = body['pubKey']

    primary_key_table = dynamodb.Table(os.environ['PRIMARY_KEY_TABLE'])
    output = event
    primary_key_table.put_item(Item={"id+alias": id + '.' + alias, "pubKey": pub_key})


    return {
        "statusCode": 200,
        "body": json.dumps({
            "success": True,
            "output": output
        }),
    }
