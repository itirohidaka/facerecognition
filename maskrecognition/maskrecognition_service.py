from aws_cdk import (core,
                     aws_apigateway as apigateway,
                     aws_s3 as s3,
                     aws_lambda as lambda_,
                     aws_dynamodb as dynamodb)

class MaskService(core.Construct):
    def __init__(self, scope: core.Construct, id: str):
        super().__init__(scope, id)

        #Create a bucket to store the Lambda Code.
        bucket = s3.Bucket(self,"MaskStore",removal_policy=core.RemovalPolicy("DESTROY"))
        
        # import the dynamoDB table
        try:
            table = dynamodb.Table.from_table_arn(self, "ImportedTable", "arn:aws:dynamodb:us-east-1:016301331060:table/photo")
        except:
            table = dynamodb.Table(self,table_name="photo",partition_key=dynamodb.Attribute(name="id",type=dynamodb.AttributeType.NUMBER))

        #Lambda - Front End
        handler = lambda_.Function(self, "MaskHandler",
                    runtime=lambda_.Runtime.PYTHON_3_8,
                    code=lambda_.Code.asset("resources/lambda_photo"),
                    handler="photoapi.lambda_handler",
                    environment=dict(
                    BUCKET=bucket.bucket_name)
                    )
        
        #Lambda - Using IOT to remote trigger Raspberry Pi
        handler1 = lambda_.Function(self, "IOTHandler",
                    runtime=lambda_.Runtime.PYTHON_3_8,
                    code=lambda_.Code.asset("resources/lambda_iot"),
                    handler="lambda_function.lambda_handler",
                    environment=dict(
                    BUCKET=bucket.bucket_name)
                    )
                    
        #Lambda - Triggered by S3 and call Rekognition to Detect PPE
        handler2 = lambda_.Function(self, "PPEHandler",
                    runtime=lambda_.Runtime.PYTHON_3_8,
                    code=lambda_.Code.asset("resources/lambda_ppe"),
                    handler="lambda_function.lambda_handler",
                    environment=dict(
                    BUCKET=bucket.bucket_name)
                    )

        #bucket and dynamodb table permition
        bucket.grant_read_write(handler)
        table.grant_read_write_data(handler)  

        #API Gateway
        api = apigateway.RestApi(self, "mask-api",
                  rest_api_name="Mask Detection",
                  description="This service detect mask on photos.")

        get_mask_integration = apigateway.LambdaIntegration(handler,
                request_templates={"application/json": '{ "statusCode": "200" }'})

        api.root.add_method("GET", get_mask_integration)   # GET /