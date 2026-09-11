"""AWS configuration module for initializing boto3 clients and resources.

This module provides centralized, configurable AWS connectivity optimized for both
production environments and local development environments (e.g., LocalStack).
"""

import os
from typing import Any, Optional
import boto3
from botocore.config import Config


def get_aws_region() -> str:
    """Retrieve the configured AWS region."""
    return os.getenv("AWS_REGION", "us-east-1")


def get_aws_endpoint_url() -> Optional[str]:
    """Retrieve the configured AWS endpoint URL (useful for LocalStack)."""
    return os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")


def get_aws_access_key_id() -> str:
    """Retrieve the configured AWS access key ID."""
    return os.getenv("AWS_ACCESS_KEY_ID", "test")


def get_aws_secret_access_key() -> str:
    """Retrieve the configured AWS secret access key."""
    return os.getenv("AWS_SECRET_ACCESS_KEY", "test")


def get_boto3_session() -> boto3.Session:
    """Create and return a configured boto3 Session instance."""
    return boto3.Session(
        aws_access_key_id=get_aws_access_key_id(),
        aws_secret_access_key=get_aws_secret_access_key(),
        region_name=get_aws_region(),
    )


def get_dynamodb_resource(
    endpoint_url: Optional[str] = None,
    region_name: Optional[str] = None,
) -> Any:
    """Instantiate and return a boto3 DynamoDB ServiceResource.

    Args:
        endpoint_url (Optional[str]): Custom endpoint URL, defaults to AWS_ENDPOINT_URL env.
        region_name (Optional[str]): AWS region name, defaults to AWS_REGION env.

    Returns:
        boto3 DynamoDB ServiceResource.
    """
    resolved_endpoint = endpoint_url or get_aws_endpoint_url()
    resolved_region = region_name or get_aws_region()

    session = get_boto3_session()
    return session.resource(
        "dynamodb",
        endpoint_url=resolved_endpoint,
        region_name=resolved_region,
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


def get_dynamodb_client(
    endpoint_url: Optional[str] = None,
    region_name: Optional[str] = None,
) -> Any:
    """Instantiate and return a low-level boto3 DynamoDB Client.

    Args:
        endpoint_url (Optional[str]): Custom endpoint URL, defaults to AWS_ENDPOINT_URL env.
        region_name (Optional[str]): AWS region name, defaults to AWS_REGION env.

    Returns:
        boto3 DynamoDB Client.
    """
    resolved_endpoint = endpoint_url or get_aws_endpoint_url()
    resolved_region = region_name or get_aws_region()

    session = get_boto3_session()
    return session.client(
        "dynamodb",
        endpoint_url=resolved_endpoint,
        region_name=resolved_region,
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


def get_dynamodb_table(
    table_name: str,
    dynamodb_resource: Optional[Any] = None,
) -> Any:
    """Retrieve a DynamoDB Table resource given a table name.

    Args:
        table_name (str): Name of the DynamoDB table.
        dynamodb_resource (Optional[Any]): Existing DynamoDB resource; created if None.

    Returns:
        boto3 DynamoDB Table resource.
    """
    resource = dynamodb_resource or get_dynamodb_resource()
    return resource.Table(table_name)
