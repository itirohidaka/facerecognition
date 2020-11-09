#!/usr/bin/env python3

from aws_cdk import core

from maskrecognition.maskrecognition_stack import MaskrecognitionStack


app = core.App()
MaskrecognitionStack(app, "maskrecognition")

app.synth()
