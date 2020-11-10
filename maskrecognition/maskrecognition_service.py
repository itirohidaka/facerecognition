from aws_cdk import (core,
                     aws_apigateway as apigateway,
                     aws_s3 as s3,
                     aws_lambda as lambda_,
                     aws_iam as iam,
                     aws_dynamodb as dynamodb,
                     aws_cloudfront as cloudfront,
                     aws_cloudfront_origins as origins
)
from aws_cdk.aws_lambda_event_sources import S3EventSource

class MaskService(core.Construct):
    def __init__(self, scope: core.Construct, id: str):
        super().__init__(scope, id)

        #Create a bucket to store the Lambda Code.
        #bucket = s3.Bucket(self,"MaskStore",removal_policy=core.RemovalPolicy("DESTROY"))
        
        # Creating the Photo Bucket (bucket123) and CloudFront (CDN)
        bucket123 = s3.Bucket(self,"itiro-teste",bucket_name="itiro-teste",removal_policy=core.RemovalPolicy("DESTROY"))
        
        oai = cloudfront.OriginAccessIdentity(self, 'OIA', comment="access_to_s3")
        
        origin = origins.S3Origin(bucket123,origin_access_identity=oai)
        
        cfdist = cloudfront.Distribution(self, "myDist",
            default_behavior={
                "origin": origin,
                "allowed_methods": cloudfront.AllowedMethods.ALLOW_ALL,
                "viewer_protocol_policy": cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            }
        )
        
        policy = s3.BucketPolicy(self, "CDNBucketOAIAccess", bucket=bucket123)
        policy.document.add_statements(iam.PolicyStatement(
            resources=[bucket123.bucket_arn + '/*'],
            actions=['s3:GetObject'],
            principals=[
                iam.ArnPrincipal('arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity ' + oai.origin_access_identity_name)
            ]
        ))
        
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

        #API Gateway
        api = apigateway.RestApi(self, "mask-api",
                  rest_api_name="Mask Detection",
                  description="This service detect mask on photos.")
        
        #Lambda - Front End
        handler = lambda_.Function(self, "MaskHandler",
                    runtime=lambda_.Runtime.PYTHON_3_8,
                    code=lambda_.Code.asset("resources/lambda_photo"),
                    handler="photoapi.lambda_handler",
                    environment=dict(
                    BUCKET=bucket123.bucket_name,CDNDOMAIN=str(cfdist.distribution_domain_name),APIURL=str(api.rest_api_id))
                    )
        
        get_mask_integration = apigateway.LambdaIntegration(handler,request_templates={"application/json": '{ "statusCode": "200" }'})
        api.root.add_method("GET", get_mask_integration)   # GET /
        
        #Lambda - Using IOT to remote trigger Raspberry Pi
        my_role = iam.Role(self,"Role1",assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))

        handler1 = lambda_.Function(self, "IOTHandler",
                    runtime=lambda_.Runtime.PYTHON_3_8,
                    code=lambda_.Code.asset("resources/lambda_iot"),
                    handler="lambda_function.lambda_handler",
                    role=my_role,
                    environment=dict(
                    BUCKET=bucket123.bucket_name,PHOTOBUCKET=str(bucket123.bucket_name))
                    )
        
        get_mask_integration2 = apigateway.LambdaIntegration(handler1,request_templates={"application/json": '{ "statusCode": "200" }'})
        iotapi = api.root.add_resource("iotapi")
        iotapi.add_method("GET", get_mask_integration2)   # GET /
    
        #my_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        my_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))

        #Lambda - Triggered by S3 and call Rekognition to Detect PPE
        my_role2 = iam.Role(self,"Role2",assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))

        handler2 = lambda_.Function(self, "PPEHandler",
                    runtime=lambda_.Runtime.PYTHON_3_8,
                    code=lambda_.Code.asset("resources/lambda_ppe"),
                    handler="lambda_function.lambda_handler",
                    role=my_role2,
                    environment=dict(
                    BUCKET=bucket123.bucket_name)
                    )
        
        my_role2.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))

        bucket123.grant_read_write(handler2)
        
        handler2.add_event_source(S3EventSource(bucket123,
            events=[s3.EventType.OBJECT_CREATED]
        ))

        #bucket and dynamodb table permition
        bucket123.grant_read_write(handler)
        table.grant_read_write_data(handler)  