import base64, json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

session_key = 'qunAqmbGUycuZum+aZE6gw=='
session_key_bytes = base64.b64decode(session_key)

qr_data = 'eyJ0eXBlIjogInRyYW5zZmVyIiwgInJlY2lwaWVudCI6ICJ1c2VyMSIsICJhbW91bnQiOiAxMC4wNiwgInRpbWUiOiAxNjM1MzI4NTA0NjAxLCAiaXYiOiAidlpLbTNheWQzOFNNbXFpbWNwdUZWdz09In2MGVPvw8ZSgYE859H+y8BFkCZILyymW8fAYBV8Mnl5tNr9SFV+cfaWeoHYcrapZLCqXI7WM8GwQ7vETp2hPM+B'
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
tan = transaction_key[:length]


print(json.loads(transaction_data))
print('ct:', base64.b64encode(ct).decode())
print('ht:', base64.b64encode(ht).decode())
print('length:', length)
print('transaction key:', transaction_key)
print('tan:', tan)

