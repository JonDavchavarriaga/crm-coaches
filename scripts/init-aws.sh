#!/bin/bash
set -euo pipefail

echo "Initializing LocalStack AWS resources for CRM Core Service..."

# Create DynamoDB Clients table
echo "Creating DynamoDB table 'Clients'..."
awslocal dynamodb create-table \
    --table-name Clients \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1

# Create SQS Client Onboarding Queue
echo "Creating SQS queue 'client-onboarding-queue'..."
awslocal sqs create-queue \
    --queue-name client-onboarding-queue \
    --region us-east-1

echo "LocalStack AWS resources initialized successfully."
