# SeQRe
CSIT321 Project - Secure QR code transaction system

--- AUTHORS ---------------------------------------------
- Hunter Riddle (6451159)
- Oliver Small (6443175)
- Luke Read-Bloomfield (6004581)
- Raisa Ryma (5766606)
--------------------------------------------------------------------------------------

--- OVERVIEW ---------------------------------------------
There are 3 components to this system
	- Webpage component: This component retrieves an encrypted authentication code from the AWS server (upon entry of valid credentials)
	- Mobile component: This component is an iOS or Android app that will decrypt and authenticate codes displayed on Webpage
	- API component: This component is an AWS server that services both frontend components
--------------------------------------------------------------------------------------

--- App-Android ---------------------------------------------
- Mobile component of the system (Android)
- Must be compiled using Android Studio, can be deployed to Android Lollipop 6.0.1 or higher
--------------------------------------------------------------------------------------


--- SeQRe AWS API ---------------------------------------------
- API component of the system
- Written in Python 3
- This code is deployed to our AWS endpoint https://9gba6esvt9.execute-api.ap-southeast-2.amazonaws.com/Prod/
- No execution instructions provided (has been deployed to URL)
--------------------------------------------------------------------------------------

--- Desktop Website ---------------------------------------------
- Webpage implementation of the API system 
- Written with jQuery and Bootstrap
- The webpage is opened by navigating to 'Desktop-Website/index.html'
	- Simply open index.html in a browser.
- Upon entering a valid userID / alias pair:
		- A POST request is made to the API
		- A JSON response containing an encrypted cAuth is provided
		- A QR containing the encrypted cAuth is generated and displayed
		- In future iterations, this QR will be decrypted locally on a users primary device
- In the future, the webpage will be hosted on a server, but for now it is run locally and will access the remote AWS API
--------------------------------------------------------------------------------------



NOTE: {userID: 'Oliver', alias: 'iPhone 11'} is a registered credential
NOTE: {userID: 'Oliver', alias: 'iPhone 12'} is a registered credential