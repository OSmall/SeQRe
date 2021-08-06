# SeQRe
CSIT321 Project - Secure QR code transaction system
- There are 3 components to this system
	- Mobile component: This component is an iOS or Android app that will authenticate codes
	- Webpage component: This component retrieves an encrypted authentication code from the AWS server, with valid credentials
	- API component: This component is an AWS server that services both frontend components


App-Android
- Mobile component of the system (Android)
- This code is not optimized to run for our MVP prototype
- No execution instructions provided (incomplete)

SeQRe API
- AWS API component of the system
- Written in Python 3
- This code is deployed to our AWS endpoint https://9gba6esvt9.execute-api.ap-southeast-2.amazonaws.com/Prod/
- No execution instructions provided (has been deployed to URL)

Desktop Website
- Webpage implementation of the system 
- Written with jQuery and Bootstrap
- The webpage is opened by navigating to 'Desktop-Website/index.html'
- Upon entering a valid userID / alias pair:
		- A POST request is made to the API
		- A JSON response containing an encrypted cAuth is provided
		- A QR containing the encrypted cAuth is displayed
		- In future iterations, this QR will be decrypted locally on a users primary device
- In the future, the webpage will be hosted on a server, but for now it is run locally and will access the remote AWS API. Simply open index.html in a browser.


NOTE: {userID: 'Oliver', alias: 'iPhone 11'} is a registered credential
NOTE: {userID: 'Oliver', alias: 'iPhone 12'} is a registered credential