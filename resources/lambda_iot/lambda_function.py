import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    client = boto3.client('iot-data', region_name='us-east-1')
    
    response = client.publish(
        topic='photo',
        qos=1,
        payload=json.dumps({"photo":1})
    )

    return {
        'statusCode': 200,
        "body": json.dumps("Command sent to RaspberryPi")
    }