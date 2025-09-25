#imports
import pulumi
import pulumi_aws as aws
import json
import os
import mimetypes

# Create an AWS resource (S3 Bucket)
mybucket = aws.s3.Bucket(
    'my-bucket',
    
)

# turn the bucket into a website
mywebsite = aws.s3.BucketWebsiteConfiguration(
    "my_website",
    bucket=mybucket.id,
    index_document={"suffix" : "index.html"},
    )

#ownership
bucket_ownership_controls = aws.s3.BucketOwnershipControls(
    "my_bucket_ownership_controls",
    bucket=mybucket.id,
    rule={"object_ownership": "BucketOwnerPreferred"},
    )

#Public access block:
bucket_public_access_block = aws.s3.BucketPublicAccessBlock(
    "my_bucket_public_access_block",
    bucket=mybucket.id,
    block_public_acls=True,
    ignore_public_acls=True,
    block_public_policy=False,
    restrict_public_buckets=False,
)

# Public-read bucket policy (for website objects)
bucket_policy = aws.s3.BucketPolicy(
    "my_bucket_policy",
    bucket=mybucket.id,
    policy=mybucket.id.apply(lambda b: json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{b}/*"],
        }],
    })),
    opts=pulumi.ResourceOptions(
        depends_on=[bucket_ownership_controls, bucket_public_access_block]
    ),
)

# Upload website files
frontend_path = os.path.join(os.getcwd(), "frontend")

def crawl_directory(dir_path: str, bucket: aws.s3.Bucket):
    for root, _, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, dir_path)  # e.g. css/style.css
            content_type, _ = mimetypes.guess_type(file_path)

            aws.s3.BucketObjectv2(
                rel_path.replace("/", "-"),   # Pulumi resource name
                bucket=bucket.id,
                source=pulumi.FileAsset(file_path),
                key=rel_path,                 # Preserve folder structure in S3
                content_type=content_type or "application/octet-stream",
            )

crawl_directory(frontend_path, mybucket)

# Exports
pulumi.export("bucket_name", mybucket.id)
# website_endpoint is a property of the bucket, not the WebsiteConfiguration resource
#pulumi.export("URL", pulumi.Output.concat("http://", mybucket.website_endpoint))
pulumi.export("URL", pulumi.Output.concat("http://", mywebsite.website_endpoint))