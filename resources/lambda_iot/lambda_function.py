import json
import boto3
import os

def lambda_handler(event, context):
    # TODO implement
    client = boto3.client('iot-data', region_name='us-east-1')

    try:
        photo_bucket = os.environ['PHOTOBUCKET']
    except:
        photo_bucket = "itiro-teste"
    
    response = client.publish(
        topic='photo',
        qos=1,
        payload=json.dumps({"photo":1,"photo_bucket":str(photo_bucket)})
    )

    return {
        'statusCode': 200,
        "body": json.dumps("Command sent to RaspberryPi")
    }