import json, random, os, boto3, time, base64
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
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
    
    id = event['headers']['seqre-id']
    alias = event['headers']['seqre-alias']

    # check body
    if event['body'] == None:
        return error(400, 'empty body')

    body = json.loads(event['body'])

    # tables
    accounts_table = dynamodb.Table(os.environ['ACCOUNTS_TABLE'])
    transactions_table = dynamodb.Table(os.environ['TRANSACTIONS_TABLE'])
    keys_table = dynamodb.Table(os.environ['KEYS_TABLE'])

    # check for account
    table_response = keys_table.get_item(Key={
        'id': id,
        'alias': alias
    }, ProjectionExpression='sessionKey, authenticated')
    if 'Item' not in table_response:
        return error(404, 'id and alias combination does not exist')

    # variables
    session_key = base64.b64decode(table_response['Item']['sessionKey'])
    authenticated = table_response['Item']['authenticated']

    # check if authenticated
    if authenticated == False:
        return error(400, 'session not authenticated')

    if ('type' not in body and 'tan' not in body) or \
    ('type' in body and 'tan' in body):
        return error(400, 'either type OR tan shall be present in the body')

    if 'type' in body:
        type = body['type']
        transaction_time = int(round(time.time() * 1000))
        
        if type == 'getBalance':
            # TODO check attributes of data
            pass

        elif type == 'transfer':
            # check recipient is in body
            if 'recipient' not in body:
                return error(400, 'missing recipient in body')
            recipient = body['recipient']
            # check recipient account exists
            table_response = accounts_table.get_item(Key={'id': recipient})
            if 'Item' not in table_response:
                return error(400, 'recipient account does not exist')

            # check amount is in body
            if 'amount' not in body:
                return error(400, 'missing amount in body')
            # check amount is a number
            try:
                amount = round(float(body['amount']), 2)
            except:
                return error(400, 'amount must be a number')
            # check amount is positive
            if amount <= 0:
                return error(400, 'amount must be positive')
            # check amount is less than balance
            table_response = accounts_table.get_item(Key={'id': id}, ProjectionExpression='balance')
            balance = table_response['Item']['balance']
            if amount > balance:
                return error(400, 'amount must not be more than current balance')

            transaction_data = {
                'type': type,
                'recipient': recipient,
                'amount': amount
            }
        else:
            return error(404, 'unexpected type')
        
        transaction_key = get_random_bytes(16)
        tan_length = random.randint(8, 10)

        # check that transaction won't collide
        table_response = transactions_table.get_item(Key={
            'userId': id,
            'transactionTime': transaction_time
        })
        if 'Item' in table_response:
            return error(409, 'transaction with this time already exists. Please wait and try again')
        
        aes_cipher = AES.new(session_key, AES.MODE_CBC)
        iv = base64.b64encode(aes_cipher.iv).decode()

        # store transaction
        table_response = transactions_table.put_item(Item={
            'userId': id,
            'transactionTime': transaction_time,
            'tanLength': tan_length,
            'transactionData': json.loads(json.dumps(transaction_data), parse_float=Decimal),
            'transactionKey': base64.b64encode(transaction_key).decode(),
            'iv': iv,
            'verified': False
        })

        # compute ct
        data = transaction_key + tan_length.to_bytes(1, 'big')
        ct = aes_cipher.encrypt(pad(data, AES.block_size)) # 32 bytes

        # create transaction_data to be sent through QR code
        transaction_data['time'] = transaction_time
        transaction_data['iv'] = iv
        transaction_data_bytes = json.dumps(transaction_data).encode()

        # compute ht
        data = transaction_data_bytes + id.encode() + ct
        ht = SHA256.new(data).digest() # 32 bytes

        # create response data
        qr_data = base64.b64encode(transaction_data_bytes + ct + ht).decode()

        return response(200, {'qrData': qr_data})


    elif 'tan' in body:
        pass


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