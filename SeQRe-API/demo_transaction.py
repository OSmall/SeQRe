import base64, json
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import unpad
from Crypto.Hash import SHA256


session_key = 'qunAqmbGUycuZum+aZE6gw=='
session_key_bytes = base64.b64decode(session_key)

qr_data = 'eyJpdiI6ICJZS3l5Zk9SYW9Ib0Jmay9HMW9YNWtRPT0iLCAidGltZSI6IDE2MzUzNTI4MDUxODYsICJ0eXBlIjogImdldEJhbGFuY2Uife1ctdjbWTap9fYfl4M8jGCXh6XU3LFEa0Cup/nozFHoyB4ISRy1wxmkZoB5TRF6fU7xmUr1rE3yDSDOKVkveLw='
qr_data_bytes = base64.b64decode(qr_data)

transaction_data = qr_data_bytes[:-64].decode()
transaction_obj = json.loads(transaction_data)
iv = base64.b64decode(transaction_obj['iv'])

ct = qr_data_bytes[-64:-32]
ht = qr_data_bytes[-32:]

aes_cipher = AES.new(session_key_bytes, AES.MODE_CBC, iv=iv)
ct_decrypted = unpad(aes_cipher.decrypt(ct), AES.block_size)
length = ct_decrypted[-1]
transaction_key = base64.b64encode(ct_decrypted[:-1]).decode()

data = transaction_data.encode() + ct_decrypted[:-1]
tan = base64.b64encode(SHA256.new(data).digest()).decode()[:length]


print(json.loads(transaction_data))
print('ct:', base64.b64encode(ct).decode())
print('ht:', base64.b64encode(ht).decode())
print('length:', length)
print('transaction key:', transaction_key)
print('tan:', tan)

