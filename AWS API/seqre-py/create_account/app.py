import json, os
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
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
