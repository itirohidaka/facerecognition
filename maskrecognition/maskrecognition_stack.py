from aws_cdk import core
from . import maskrecognition_service

class MaskrecognitionStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        maskrecognition_service.MaskService(self, "Masks")