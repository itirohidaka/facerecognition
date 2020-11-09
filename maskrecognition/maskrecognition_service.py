from aws_cdk import (core,
                     aws_apigateway as apigateway,
                     aws_s3 as s3,
                     aws_lambda as lambda_,
                     aws_iam as iam,
                     aws_dynamodb as dynamodb,
                     aws_cloudfront as cloudfront,
                     aws_cloudfront_origins as origins
)

class MaskService(core.Construct):
    def __init__(self, scope: core.Construct, id: str):
        super().__init__(scope, id)

        #Create a bucket to store the Lambda Code.
        bucket = s3.Bucket(self,"MaskStore",removal_policy=core.RemovalPolicy("DESTROY"))
        
        # Import Photo Bucket or Create a bucket if not exist
        try:
            bucket_photo = s3.Bucket.from_bucket_name(self, "BucketByName", "itiro-photo")
        except:
            bucket_photo = s3.Bucket(self,"itiro-photo",bucket_name="itiro-photo",removal_policy=core.RemovalPolicy("DESTROY"))

        # Import the dynamoDB table or create if not exist
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

        #API Gateway
        api = apigateway.RestApi(self, "mask-api",
                  rest_api_name="Mask Detection",
                  description="This service detect mask on photos.")

        get_mask_integration = apigateway.LambdaIntegration(handler,
                request_templates={"application/json": '{ "statusCode": "200" }'})

        api.root.add_method("GET", get_mask_integration)   # GET /
        
        #CDN
        oia = cloudfront.OriginAccessIdentity(self, 'OIA', comment="Created by CDK")
        bucket_origin = origins.S3Origin(bucket_photo,origin_access_identity=oia)
        
        cfdist = cloudfront.Distribution(self, "myDist",
            default_behavior={
                "origin": bucket_origin,
                "allowed_methods": cloudfront.AllowedMethods.ALLOW_ALL,
                "viewer_protocol_policy": cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            },
            additional_behaviors={
                "/images/*.jpg": {
                    "origin": bucket_origin,
                    "viewer_protocol_policy": cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
                }
            }
        )
        
        #IAM
        policystatement = iam.PolicyStatement()
        policystatement.add_actions('s3:GetBucket*')
        policystatement.add_actions('s3:GetObject*')
        policystatement.add_actions('s3:List*')
        policystatement.add_resources(bucket_photo.bucket_arn)
        policystatement.add_resources('${bucket_photo.bucket_arn}/*')
        policystatement.add_canonical_user_principal(oia.cloud_front_origin_access_identity_s3_canonical_user_id)
        
        if not bucket_photo.policy:
            #s3.BucketPolicy("bucketpolicy",bucket_photo)
            #new BucketPolicy(this, 'Policy', { bucket: testBucket }).document.addStatements(policyStatement)
            bucket_photo.add_to_resource_policy(policystatement)
        else:
            bucket_photo.policy.document.add_statements(policystatement)
        
        #bucket and dynamodb table permition
        bucket.grant_read_write(handler)
        table.grant_read_write_data(handler)  
        #bucket_photo.grant_read_write(oia)
        
