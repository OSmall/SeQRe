import json, os
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):

    body = json.loads(event['body'])
    id = body['id']
    alias = body['alias']
    pubKey = body['pubKey']

    primaryKeyTable = dynamodb.Table(os.environ['PRIMARY_KEY_TABLE'])
    output = event
    primaryKeyTable.put_item(Item={"id+alias": id + '.' + alias, "pubKey": pubKey})


    return {
        "statusCode": 200,
        "body": json.dumps({
            "success": True,
            "output": output
        }),
    }
