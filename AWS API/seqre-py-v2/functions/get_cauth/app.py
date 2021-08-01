import json, os, base64, random
import boto3
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    
    try:
            
        body = json.loads(event['body'])
        id = body['id']
        alias = body['alias']

        primaryKeyTable = dynamodb.Table(os.environ['PRIMARY_KEY_TABLE'])
        pubKey = primaryKeyTable.get_item(Key={'id+alias': id + '.' + alias})['Item']['pubKey'].encode()
        # pubKey = b'MIIBojANBgkqhkiG9w0BAQEFAAOCAY8AMIIBigKCAYEAkQ8J6MhFNVIIx+eBm83FXFzGjqEB6LpS0eT/ToIA3B5bAXRyyTU8G32BqDnCX+Ku0djhmEtzjDHirjyk3icgv8gZdB0E5DLcZPB14Mu2W4SNP9HWnzr9rCyjGX77o71D/6bE+V4/wto4tYaYKpbfj8sDZQ+NMCy8tG03+vRvDPTZnPy1HJ2LC7pfEG5sG0iWL1BISmMfO+jLgI6foCrM4DIZElYBphlC+TWRKTK8kynnCm/YR3CMbEFbCmoi1GdEJ0ntz2ILE7c94mLAIWQHMq5V8r0NbCWY9KxWs4brvzaQ+SmWmbA6LEPgPEXXV08L0KA09SFs/UdMBSUHatx3mVg3ilpNt3S5fPRnMVm9U0pkJcZlnl4oRqeSEwuoWfRaOO5slZs5NzWqBIH7DVYZ3ca/iow5SVobMKHN//IrzcIAQgLjDOplhA/jeldffB5A1uImYEmukrmIohsvBzuTfxiS+9EPIKbbJJpU+jqdgpuMCg19cEdYEdX5NGXY5yyHAgMBAAE='
        pubKey = base64.b64decode(pubKey)

        session_key = get_random_bytes(16)
        # session_key = b'N\x03\xb7\xca\r\xa0|\x19\x12\xd2i\x16\xac\x14q~'
        rand = random.randint(8, 10)
        length = rand.to_bytes(1, 'big')

        sessionKeyTable = dynamodb.Table(os.environ['SESSION_KEY_TABLE'])
        sessionKeyTable.put_item(Item={
            "id": id,
            "key": base64.b64encode(session_key).decode('ascii'),
            "length": rand,
            "authenticated": False
            })


        rsa = RSA.import_key(pubKey)
        cipher_rsa = PKCS1_OAEP.new(rsa)

        c_auth = session_key + length
        c_auth = base64.b64encode(cipher_rsa.encrypt(c_auth)).decode('ascii')

        ret = base64.b64encode(rsa.export_key(format='DER')).decode('ascii')

        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            "body": json.dumps({
                "success": True,
                "cAuth": c_auth,
            }),
            'headers': {
                "Content-Type" : "application/json",
                "Access-Control-Allow-Origin" : "*",
                "Allow" : "GET, OPTIONS, POST",
                "Access-Control-Allow-Methods" : "GET, OPTIONS, POST",
                "Access-Control-Allow-Headers" : "*"
            }
        }

    except:
        return{
            "statuscode":500,
            "body": json.dumps({
                  "success": False
            })
        }