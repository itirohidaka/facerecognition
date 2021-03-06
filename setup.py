import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="maskrecognition",
    version="0.0.1",

    description="An empty CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "maskrecognition"},
    packages=setuptools.find_packages(where="maskrecognition"),

    install_requires=[
        "aws-cdk.core==1.71.0",
        "aws_cdk.aws_apigateway==1.71.0",
        "aws_cdk.aws_iam==1.71.0",
        "aws_cdk.aws_lambda==1.71.0",
        "aws_cdk.aws_s3==1.71.0",
        "aws_cdk.aws_dynamodb==1.71.0",
        "aws_cdk.aws_cloudfront==1.71.0",
        "aws_cdk.aws_cloudfront_origins==1.71.0",
        "aws_cdk.aws_lambda_event_sources==1.71.0",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
