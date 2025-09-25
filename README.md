 # Made from AWS Python S3 Bucket Pulumi Template

 A minimal Pulumi template for provisioning a single AWS S3 bucket using Python.

 ## Overview

 This template provisions an S3 bucket (`pulumi_aws.s3.BucketV2`) in your AWS account and exports its ID as an output. It’s an ideal starting point when:
  - You want to learn Pulumi with AWS in Python.
  - You need a barebones S3 bucket deployment to build upon.
  - You prefer a minimal template without extra dependencies.

 ## Prerequisites

 - An AWS account with permissions to create S3 buckets.
 - AWS credentials configured in your environment (for example via AWS CLI or environment variables).
 - Python 3.6 or later installed.
 - Pulumi CLI already installed and logged in.

 ## About this project

This repository is a simple static CV created on S3 bucket.

- Once you run the pulumi up command, the output will should you the URL for the CV.
- URL format : http://<bucket_name>.s3-website-<aws-region>.amazonaws.com