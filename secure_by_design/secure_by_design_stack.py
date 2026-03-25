from aws_cdk import (
    Stack,
    aws_s3 as s3,
)
from constructs import Construct

class SecureByDesignStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an S3 bucket without security configurations to demonstrate the aspect warnings

        s3.Bucket(self, "SecureByDesignBucket",
            bucket_name="secure-by-design-poc",
        )

      