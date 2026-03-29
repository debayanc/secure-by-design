import aws_cdk as core
import aws_cdk.assertions as assertions

from secure_by_design.secure_by_design_stack import SecureByDesignStack


def test_debug_print_template():
    app = core.App()
    stack = SecureByDesignStack(app, "secure-by-design")
    template = assertions.Template.from_stack(stack)
    import json
    print(json.dumps(template.to_json(), indent=2))  # shows everything you can assert on

def test_s3_bucket_created():
    app = core.App()
    stack = SecureByDesignStack(app, "secure-by-design")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::S3::Bucket", {
        "BucketName": "secure-by-design-poc"
    })

def test_s3_bucket_public_access_block():
    app = core.App()
    stack = SecureByDesignStack(app, "secure-by-design")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::S3::Bucket", {
        "PublicAccessBlockConfiguration": {
            "BlockPublicAcls": True,
            "BlockPublicPolicy": True,
            "IgnorePublicAcls": True,
            "RestrictPublicBuckets": True
        }
    })

def test_s3_bucket_encryption():
    app = core.App()
    stack = SecureByDesignStack(app, "secure-by-design")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::S3::Bucket", {
        "BucketEncryption": {
            "ServerSideEncryptionConfiguration": [
                {
                    "ServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "AES256"
                    }
                }
            ]
        }
    })

def test_s3_bucket_has_lifecycle_policy():
    app = core.App()
    stack = SecureByDesignStack(app, "secure-by-design")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::S3::Bucket", {
        "LifecycleConfiguration": {
            "Rules": assertions.Match.array_with([
                assertions.Match.object_like({
                    "Status": "Enabled",
                    "Transitions": assertions.Match.array_with([
                        assertions.Match.object_like({
                            "StorageClass": "GLACIER",
                            "TransitionInDays": 30
                        })
                    ])
                })
            ])
        }
    })