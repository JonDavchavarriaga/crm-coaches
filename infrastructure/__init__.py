"""Infrastructure layer package initialization.

Contains concrete implementations of domain ports (e.g., database repositories,
external APIs, message brokers) and cloud configurations.
"""

from infrastructure.aws_config import (
    get_aws_access_key_id,
    get_aws_endpoint_url,
    get_aws_region,
    get_aws_secret_access_key,
    get_boto3_session,
    get_dynamodb_client,
    get_dynamodb_resource,
    get_dynamodb_table,
)
from infrastructure.dynamodb_repository import DynamoDBClientRepository

__all__ = [
    "get_aws_region",
    "get_aws_endpoint_url",
    "get_aws_access_key_id",
    "get_aws_secret_access_key",
    "get_boto3_session",
    "get_dynamodb_client",
    "get_dynamodb_resource",
    "get_dynamodb_table",
    "DynamoDBClientRepository",
]
