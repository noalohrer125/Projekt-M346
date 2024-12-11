#!/bin/bash
BUCKET_INPUT="csv-input-bucket"
BUCKET_OUTPUT="json-output-bucket"

# S3-Buckets erstellen
aws s3api create-bucket --bucket $BUCKET_INPUT --region us-east-1
aws s3api create-bucket --bucket $BUCKET_OUTPUT --region us-east-1

# Lambda-Bereitstellung
aws lambda create-function \
    --function-name CsvToJson \
    --runtime python3.8 \
    --role arn:aws:iam::123456789012:role/lambda-role \
    --handler lambda_function.lambda_handler \
    --code S3Bucket=my-deployment-bucket,S3Key=lambda.zip \
    --timeout 15

# Ereignisquelle hinzufügen
aws s3api put-bucket-notification-configuration \
    --bucket $BUCKET_INPUT \
    --notification-configuration file://notification.json
