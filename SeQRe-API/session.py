import json, boto3, os

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    
    id = event['headers']['seqre-id']
    alias = event['headers']['seqre-alias']

    keys_table = dynamodb.Table(os.environ['KEYS_TABLE'])
    
    table_response = keys_table.get_item(Key={
        'id': id,
        'alias': alias
    }, ProjectionExpression='pubKey')
    
    if 'Item' not in table_response:
        return {
            'statusCode': 404,
            'body': json.dumps({
                'errorMessage': 'id and alias combination does not exist'
            })
        }

    pub_key = table_response['Item']['pubKey']

    # TODO return cAuth

    return {
        # TODO headers
        'statusCode': 200,
        'body': json.dumps({
                'event': event,
                'id': id,
                'alias': alias,
                'pubKey': table_response
            })
    }
