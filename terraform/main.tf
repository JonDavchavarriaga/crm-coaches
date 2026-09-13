# DynamoDB table for CRM client entities
resource "aws_dynamodb_table" "clients_table" {
  name         = "Clients"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Environment = "Local"
    Service     = "crm-core-service"
  }
}

# SQS queue for client onboarding event processing
resource "aws_sqs_queue" "client_onboarding_queue" {
  name = "client-onboarding-queue"

  tags = {
    Environment = "Local"
    Service     = "crm-core-service"
  }
}

# S3 bucket for storing client-related attachments and documents
resource "aws_s3_bucket" "crm_attachments_bucket" {
  bucket = "crm-attachments-bucket"

  tags = {
    Environment = "Local"
    Service     = "crm-core-service"
  }
}
