import json
import boto3
from botocore.exceptions import ClientError
from ast import literal_eval

def lambda_handler(event, context):
    # Query DynamoDB
    dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
    table = dynamodb.Table('photo')
    
    response = table.get_item(Key={ 'id': 1 } )
    
    #Extract the photo filename from response
    photofilename = response["Item"]["photo"]
    print(photofilename)
    dict1 = literal_eval(response["Item"]["persons"])
    people = len(dict1)
    mask = len(dict1[0]["BodyParts"][0]["EquipmentDetections"])
    if mask == 0:
        usingmask = 'No'
        div3 = ''
    else:
        usingmask = 'Yes'
        try:
            blah = dict1[0]["BodyParts"][0]["EquipmentDetections"][0]["CoversBodyPart"]
            # key exists in dict
            face_percent = dict1[0]["BodyParts"][0]["EquipmentDetections"][0]["CoversBodyPart"]["Confidence"]
            div3 = '<div id=paragraph3> <BR><b>Confidence: </b>'+ str(face_percent) + '<BR></div>'        
        except KeyError:
            # key doesn't exist in dict
            div3 = ''
    
    print(type(dict1[0]))
    print(dict1[0])
    

        
    
    #print(type(res))
    #Prepare the HTML response
    #content = '<html><body><h1>Test</h1><BR><img id="imagem01" src="http://d10km6otpah3bu.cloudfront.net/' + photofilename + '" alt="Test" style="width:30%;height:auto;"></body></html>'
    initial_html = '<html> <body> <button type="submit" onclick="send()">Take a New Photo</button><BR><BR> <img src="http://d10km6otpah3bu.cloudfront.net/' + photofilename + '" alt="Test" style="width:30%;height:auto;"><BR>' 
    div1 = '<div id=paragraph1> <BR><b>People on Photo: </b>'+ str(people) + '<BR></div>'
    div2 = '<div id=paragraph2> <BR><b>Using Mask? </b>'+ usingmask + '</div>'
    
    final_html = '</body> </html>'
    js = '<script type="text/javascript" language="javascript"> function send(){var e=new XMLHttpRequest;e.open("POST","https://nh1drlqnu7.execute-api.us-east-1.amazonaws.com/test/python",!1),e.setRequestHeader("Content-Type","application/json"),e.send(null),alert(e.responseText)} </script>'
    content = initial_html + div1 + div2 + div3 + final_html + js

    #Return
    return {
        "statusCode": 200,
        "body": content,
        "headers": {
            'Content-Type': 'text/html',
            'Access-Control-Allow-Origin': '*'
        }
    }
