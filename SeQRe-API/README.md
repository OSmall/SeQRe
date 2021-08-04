
<!-- Best results viewed with a Markdown previewer -->

# Pre-requisites

## Python 3.8.0 (exactly)

- The AWS Lambda functions use this runtime and so you must have this exact version installed
- This can be alongside your main one. For example, I have Python 3.9.5 as my main and then 3.8.0 is installed alongside it.

![](https://i.ibb.co/Qp7smTr/image.png)

- The PATH variable shall point to Python 3.8.0, but it doesn't need to be the first one (PATH matches the first one it can find). In this example, the `python --version` command results in `Python 3.9.5`. So basically, you just need it installed somewhere.

![](https://i.ibb.co/ygzXrHd/image.png)

## AWS CLI

- Follow [https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) to install AWS CLI v2
- Once installed, run `aws configure`. This is where you give the CLI programmatic access, set the region, and the output format.
- To gain programmatic access you need to generate a key from the AWS Console. Click on your username in the top-right and click on "My Security Credentials".

![](https://i.ibb.co/6yZf44V/image.png)

- Then 