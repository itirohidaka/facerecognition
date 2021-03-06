
# Mask Recognition Demo

The Objective of this Repo is to create an repeatable Demo of the Mask Recognition solution using AWS services and AWS Rekognition API to detect the usage of PPE (Personal Protective Equipment).

## Architecture Overview

This section is intended to show us the Diagram with the solution component.

![alt text](img/facerecognition.jpg)

This is a project automated with AWS CDK (Python) and tested in AWS Cloud9 environment.

## How to create this solution on AWS
The component creation was automated using AWs CDK (Cloud Development Kit). To clone the code and to deploy the services, execute the following step by step: 

OBS: The deployment of this solution can incur in costs on your AWS monthly billing.


Open the terminal on Cloud9 and clone this repo using git commands.
``` bash
git clone https://github.com/itirohidaka/facerecognition.git
```

To manually create a virtualenv on Linux. 
``` bash
cd ~/environment/facerecognition
python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.
``` bash
source .venv/bin/activate
```

Once the virtualenv is activated, you can install the required dependencies.
``` bash
pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.
``` bash
cdk synth
```
Deploy the solution on your AWS environment.
``` bash
cdk deploy
```
To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

Useful CDK commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

## Configuring the Raspberry Pi/Rasbian (optional)

1. To activate the Camera Pi, access the Raspberry Pi using SSH and use the following commands:
``` bash
sudo apt-get update
sudo apt-get install python-picamera python3-picamera
```

2. Install the Node-Red on Raspian:
``` bash
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
```
To get more details on how to install Node-Red on Raspberry Pi click [here](https://nodered.org/docs/getting-started/raspberrypi).

3. To import the Flow, click on the Menu (Right top corner) and "Import". Copy the NodeRed/flow.json content and past to the NodeRed.

OBS: The MQTT and the S3 Nodes needs to be configured manually after the import.
