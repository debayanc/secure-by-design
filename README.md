
# Secure by Design POC

This is a sample CDK project that attempts to create an S3 bucket without blocking public access and without encryption.

Because the `secure-by-design-lib` security library is enabled in the application, running `cdk synth` will show warnings highlighting these security gaps.

### Sample Output

```
cdk synth
[Warning at /SecureByDesignStack/SecureByDesignBucket/Resource] S3 Bucket should have server-side encryption enabled
[Warning at /SecureByDesignStack/SecureByDesignBucket/Resource] S3 Bucket should have public access block enabled
Resources:
  SecureByDesignBucketEDC48776:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: secure-by-design-poc
```

