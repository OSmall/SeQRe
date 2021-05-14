# Methods required
# {url}/primary


## Create New Account
```
newAccount(pubKey, deviceName): userID
```
Create a new account.

1. Public and private key pair is computed on the phone. Private key is stored securely on the phone.
1. The public key is sent and stored on the server.
1. The device name is a string used to differentiate devices and is stored on the server. This is stored on the device too.
1. The server generates a User ID and sends back to the user.

Issues:
- People can spam the API and create a lot of accounts.

---
## Add New Device
```
    addNewDevice(userID, pubKey, newDeviceName, sigKey, signature): success
```
Add a new device to an account.

- userID:
- pubKey: might combine these two ^
- newDeviceName:
- sigKey: name of alias of key. Could either be a device key or a session key given to an untrusted computer


1. Public and private key pair is computed on the phone. Private key is stored securely on the phone.
1. The userID, pubKey, newDeviceName, sigKey are concatenated and signed with the stored private key.
1. Paramaters are sent to the server. Signature is verified with the publicKey and checked to see if matched with the parameters.
1. If it matches, the new device is added to the database and a success response is sent.

Issues:
- Might need to limit number of devices linked to an account.
---

## Get Session
```
getSession(userID)
```


---
# {url}/secondary