import json, boto3, os, base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from mnemonic import Mnemonic

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # check headers
    if event['headers'] == None:
        return error(400, "'seqre-id' and 'seqre-alias' headers do not exist")
    if 'seqre-id' not in event['headers']:
        return error(400, "'seqre-id' header does not exist")
    if 'seqre-alias' not in event['headers']:
        return error(400, "'seqre-alias' header does not exist")
    
    # check body
    if event['body'] == None:
        return error(400, 'empty body')
        
    body = json.loads(event['body'])

    # create variables
    id = event['headers']['seqre-id']
    alias = event['headers']['seqre-alias']

    accounts_table = dynamodb.Table(os.environ['ACCOUNTS_TABLE'])
    keys_table = dynamodb.Table(os.environ['KEYS_TABLE'])

    # check if account already exists
    table_response = accounts_table.get_item(Key={'id': id})
    if 'Item' in table_response:
        return error(400, 'account already exists')
    
    # check body for pubKey
    if 'pubKey' not in body:
        return error(400, 'missing pubKey in body')
    
    pub_key = body['pubKey']

    # check pubKey validity
    try:
        rsa = RSA.import_key(base64.b64decode(pub_key))
    except:
        return error(400, 'pubKey is not a valid RSA public key')
    
    # TODO enforce minimum RSA security level
    
    # create mnemonic
    mnemonic_phrase = Mnemonic("english").generate(strength=128)
    mnemonic_hash = base64.b64encode(SHA256.new(mnemonic_phrase.encode()).digest()).decode()
    cipher_rsa = PKCS1_OAEP.new(rsa)
    mnemonic_encrypted = base64.b64encode(cipher_rsa.encrypt(mnemonic_phrase.encode())).decode()
    
    # create account
    table_response = accounts_table.put_item(Item={
        'id': id,
        'balance': 0,
        'mnemonicHash': mnemonic_hash
    })
    table_response = keys_table.put_item(Item={
        'id': id,
        'alias': alias,
        'authenticated': False,
        'pubKey': pub_key
    })

    return response(200, {'mnemonicPhrase': mnemonic_encrypted})


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