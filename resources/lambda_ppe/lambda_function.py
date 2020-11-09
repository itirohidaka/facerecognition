import sys
from pip._internal import main

main(['install', '-I', '-q', 'boto3', '--target', '/tmp/', '--no-cache-dir', '--disable-pip-version-check'])
sys.path.insert(0,'/tmp/')

import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # TODO implement
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        filename = record['s3']['object']['key']
        print('## Bucket:' + bucket + " ## FileName: " + filename)
        print(boto3.__version__)
        
        client=boto3.client('rekognition')

        response = client.detect_protective_equipment(Image={'S3Object':{'Bucket':bucket,'Name':filename}})
        print (response)
        print(type(response))
        
        dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
        table = dynamodb.Table('photo')
        
        response["id"] = 1
        if "BodyParts" in response:
            print("Yes, 'BodyParts' is one of the keys in the thisdict dictionary")
        
        item={ 
            "id": response["id"],
            "persons": str(response["Persons"]),
            "photo": filename
        }
        print(type(item))

        resp = table.put_item( Item=item )

    return {
        'statusCode': 200,
    }

