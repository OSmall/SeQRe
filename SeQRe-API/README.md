
<!-- Best results viewed with a Markdown parser. If using VSCode, right click this tab and select "Open Preview" -->

# Pre-requisites

## Python 3.8.0 (exactly)

- The AWS Lambda functions use this runtime and so you must have this exact version installed.
- [https://www.python.org/downloads/release/python-380/](https://www.python.org/downloads/release/python-380/)
- This can be alongside your main one. For example, I have Python 3.9.5 as my main and then 3.8.0 is installed alongside it.

![](https://i.ibb.co/Qp7smTr/image.png)

- The PATH variable shall point to Python 3.8.0, but it doesn't need to be the first one (PATH matches the first one it can find). In this example, the `python --version` command returns "Python 3.9.5". So basically, you just need it installed somewhere but it doesn't need to be your main installation.

![](https://i.ibb.co/ygzXrHd/image.png)

## Pip Libraries

- `& 'C:\Program Files\Python38\python.exe' -m pip install boto3`
- `& 'C:\Program Files\Python38\python.exe' -m pip install pycryptodome`

## AWS CLI

- Follow [https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) to install AWS CLI v2 (Choose your OS, not Docker)

- To gain programmatic access to AWS, you need to generate a key from the AWS Console. Click on your username in the top-right and click on "My Security Credentials".

![](https://i.ibb.co/6yZf44V/image.png)

- Then click "Create access key". The secret key can only be retrieved once so put it straight into the next step to save it.

![](https://i.ibb.co/Sf0r1nZ/image.png)

- Run `aws configure` command. The _Access Key_ and _Secret Access Key_ will be entered here. The _Default region name_ is `ap-southeast-2` and the _Default output format_ is `json`. These settings are saved in a file located at __C:\Users\USERNAME\.aws__ (on Windows).

## Docker

- Docker is installed to can run and test the API locally before deploying. SAM runs the Lambda environment inside a container.
- Install Docker for your OS. Windows 10 instructions are listed here but it is similar for other OSs.
- Follow [https://docs.docker.com/docker-for-windows/install/](https://docs.docker.com/docker-for-windows/install/). WSL 2 backend is recommended. There are instructions there on how to enable WSL 2 if it isn't already enabled.
- Docker is running when the icon in the tray is steady, and Docker Desktop looks like this (the containers might not look exactly the same. As long as it's green in the bottom left).
- Confirm Docker is running in the command line with `docker ps`

![](https://i.ibb.co/YjRbkPR/image.png)

## AWS SAM (Serverless Application Model) CLI

- Follow [https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) to install the SAM CLI on your OS. We have already completed steps 1-3, so start at step 4. NOTE: if Docker was installed with the Hyper-V backend, there may be some additional setup for configuring shared drives as outlined in Step 3.

# Running SeQRe-API Locally

This must be done before deploying to AWS in order for testing to be completed locally to make sure that the API works as intended.

__DO NOT__ deploy to AWS before testing locally as this can create issues and delays for developers. Test the entirety of the endpoints.

__NOTE:__ running the API locally will mean that the lambda functions won't be altered on AWS, but __it still accesses the database on AWS and can alter any data stored there__. So, please take care when writing functions that alter the database. In the future, a debugging database will be created so that user data is not at risk.

- Navigate to the directory containing the __template.yaml__ file. This is the __SeQRe-API__ folder, and is considered the root for the SAM project.
- Run `sam build` to build the project. An __.aws-sam__ folder will be created with all the build data. This should already be .gitignored and hence, won't be commited to _origin_.
- Run `sam local start-api`. The API will be accessible locally. The default URL is _http://127.0.0.1:3000/_

# Testing

From here, testing shall proceed. [Postman](https://www.postman.com/) is a very useful tool in this where automated testing can be set up. There are no automated tests written as yet. The shared team Postman workspace is linked [here](https://app.getpostman.com/join-team?invite_code=9edb5fc37dc7b26a2099c0cc1b9aeb20&ws=933784ea-2202-4f07-8c33-88ed42243d71).

# Deploying SeQRe-API to AWS

- `sam build`
- The first time deploying, run `sam deploy --guided` which will take in options and save some to use later. Subsequent times, `sam deploy` can be used. Here are the inputs needed:

| Key | Value |
| ------ | ------ |
| Stack Name | SeQRe-API |
| AWS Region | ap-southeast-2 |
| Confirm changes before deploy | N |
| Allow SAM CLI IAM role creation | Y |
| XXXX may not have authorization defined, Is this okay? | Y (this will appear every time when deploying and is  an AWS security measure to make sure authorization is defined. For our purposes at the moment it is fine. Authorization can be added later to our functions so the error doesn't show.) |
| Save arguments to configuration file | Y |
| SAM configuration file | samconfig.toml |
| SAM configuration environment | default |

# Developing

## IDE

- Visual Studio Code was used for the majority of development. The only thing to note is to choose the correct Python interpreter in the lower-left to get code completion.

## Editing template.yaml

This is the document that defines the rules to creates the entire software stack on AWS. Editing this is useful when __creating another function__. Simply, copy one of the other functions and make the following changes.
- Name: please use correct naming conventions.
- CodeUri: create a new folder in the __functions__ folder that contains a __.py file__ and __requirements.txt__ which contains the pip library requirements for the function.
- Policies: apply the policies so the function can access the appropriate database tables. Principle of least privilege.
- Event name: similar to API endpoint.
- Path: API endpoint.

## Stuck?
The [AWS Serverless Application Model Developer Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide) has useful information.