import json, boto3, os, base64, random, time
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    
    # check headers
    if event['headers'] == None:
        return error(400, "'seqre-id' and 'seqre-alias' headers do not exist")
    if 'seqre-id' not in event['headers']:
        return error(400, "'seqre-id' header does not exist")
    if 'seqre-alias' not in event['headers']:
        return error(400, "'seqre-alias' header does not exist")
    
    # create variables
    id = event['headers']['seqre-id']
    alias = event['headers']['seqre-alias']
    keys_table = dynamodb.Table(os.environ['KEYS_TABLE'])

    if event['httpMethod'] == 'GET':
        # fetch pubKey from table
        table_response = keys_table.get_item(Key={
            'id': id,
            'alias': alias
        }, ProjectionExpression='pubKey')
        
        # error if id and alias combo does not exist
        if 'Item' not in table_response:
            return error(404, 'id and alias combination does not exist')

        # get components for cAuth
        pub_key = base64.b64decode(table_response['Item']['pubKey'])
        session_key = get_random_bytes(16)
        otp_length = random.randint(8, 10)

        # store session data
        table_response = keys_table.update_item(Key={
            'id': id,
            'alias': alias
        }, UpdateExpression='SET sessionKey=:session_key, authenticated=:authenticated, sessionKeyCreatedTime=:time, otpLength=:length',
        ExpressionAttributeValues={
            ':session_key': base64.b64encode(session_key).decode('ascii'),
            ':authenticated': False,
            ':time': int(round(time.time() * 1000)),
            ':length': otp_length
        })

        # create cAuth
        rsa = RSA.import_key(pub_key)
        cipher_rsa = PKCS1_OAEP.new(rsa)
        c_auth = session_key + otp_length.to_bytes(1, 'big')
        c_auth = base64.b64encode(cipher_rsa.encrypt(c_auth)).decode('ascii')

        return response(200, {'qrData': c_auth})
    
    if event['httpMethod'] == 'POST':
        if event['body'] == None:
            return error(400, 'empty body')
        
        body = json.loads(event['body'])

        # check body for otp
        if 'otp' not in body:
            return error(400, 'missing otp in body')
        
        otp = body['otp']

        table_response = keys_table.get_item(Key={
            'id': id,
            'alias': alias
        }, ProjectionExpression='sessionKey, otpLength, sessionKeyCreatedTime, authenticated')
        
        # error if id and alias combo does not exist
        if 'Item' not in table_response:
            return error(404, 'id and alias combination does not exist')
        
        # error if brand new account
        if 'sessionKey' not in table_response['Item'] or \
        'otpLength' not in table_response['Item'] or \
        'sessionKeyCreatedTime' not in table_response['Item'] or \
        'authenticated' not in table_response['Item']:
            return error(400, 'sessionKey is not initialized. A GET request needs to be made to /session first')

        authenticated = table_response['Item']['authenticated']
        # check if it has been authenticated already
        if authenticated:
            return response(200, {'message': 'already authenticated'})

        session_key = table_response['Item']['sessionKey']
        otp_length = int(table_response['Item']['otpLength'])
        key_created_time = int(table_response['Item']['sessionKeyCreatedTime'])

        session_key_hash = base64.b64encode(SHA256.new(base64.b64decode(session_key.encode('ascii'))).digest()).decode('ascii')

        # error if sessionKey is too old (30 seconds)
        if int(round(time.time() * 1000)) - key_created_time > 30000:
            return error(400, 'sessionKey timed out')
        # error if otp does not compute
        if otp != session_key_hash[:otp_length]:
            return error(401, 'otp does not authenticate')
        
        # -----Authenticated-----
        table_response = keys_table.update_item(Key={
            'id': id,
            'alias': alias
        }, UpdateExpression='SET authenticated=:authenticated',
        ExpressionAttributeValues={
            ':authenticated': True
        })

        return response(200, {'message': 'authenticated'})


def response(statusCode, body):
    return {
        'statusCode': statusCode,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body)
    }

def error(statusCode, errorMessage):
    return response(statusCode, {'errorMessage': errorMessage})