
# CDK Python - Face Recognition

Under Construction!!!!

![alt text](img/facerecognition.jpg)

This is a project automated with AWS CDK (Python) and tested in AWS Cloud9 environment.

# How to Create this solution on AWS:

Open the terminal on Cloud9 and clone this repo using git commands.
```
$ git clone https://github.com/itirohidaka/facerecognition.git
```

To manually create a virtualenv on Linux. 
```
$ cd ~/environment/facerecognition
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.
```
$ source .venv/bin/activate
```

Once the virtualenv is activated, you can install the required dependencies.
```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.
```
$ cdk synth
```
Deploy the solution on your AWS environment.
```
$ cdk deploy
```
To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful CDK commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

# Configuring the Raspberry Pi:
