"""DynamoDB implementation of domain repository ports.

This module provides the DynamoDB adapter for Client entity persistence,
strictly adhering to the ClientRepository interface defined in domain/ports.py.
"""

import logging
from typing import Any, Dict, Optional, Union
from uuid import UUID
from botocore.exceptions import ClientError

from domain.models import Client
from domain.ports import ClientRepository
from infrastructure.aws_config import get_dynamodb_table

logger = logging.getLogger(__name__)


class DynamoDBClientRepository(ClientRepository):
    """DynamoDB secondary adapter implementing the ClientRepository port."""

    def __init__(
        self,
        table_name: str = "Clients",
        table: Optional[Any] = None,
        dynamodb_resource: Optional[Any] = None,
    ) -> None:
        """Initialize DynamoDB repository with a target table or DynamoDB resource.

        Args:
            table_name (str): Name of the DynamoDB table. Defaults to 'Clients'.
            table (Optional[Any]): Injected boto3 Table resource (useful for testing/mocking).
            dynamodb_resource (Optional[Any]): Injected boto3 DynamoDB ServiceResource.
        """
        self.table_name = table_name
        self._table = table or get_dynamodb_table(
            table_name=table_name,
            dynamodb_resource=dynamodb_resource,
        )

    def _to_dynamodb_item(self, client: Client) -> Dict[str, Any]:
        """Serialize a domain Client model into a DynamoDB item dictionary.

        Converts UUIDs to strings, datetimes to ISO-8601 formatted strings,
        and excludes None values to maintain clean DynamoDB documents.

        Args:
            client (Client): Domain client entity.

        Returns:
            Dict[str, Any]: Formatted item dictionary for DynamoDB PutItem.
        """
        raw_dict = client.model_dump(mode="json")
        # Filter out None values to keep DynamoDB documents clean and efficient
        return {key: value for key, value in raw_dict.items() if value is not None}

    def _to_domain_entity(self, item: Dict[str, Any]) -> Client:
        """Deserialize a DynamoDB item dictionary back into a domain Client entity.

        Args:
            item (Dict[str, Any]): DynamoDB item response dictionary.

        Returns:
            Client: Validated domain Client entity.
        """
        return Client.model_validate(item)

    def save(self, client: Client) -> Client:
        """Persist a client domain entity to the DynamoDB table.

        Args:
            client (Client): The domain client model to save or update.

        Returns:
            Client: The saved client domain entity.

        Raises:
            ClientError: If an error occurs during the DynamoDB PutItem operation.
        """
        item = self._to_dynamodb_item(client)
        try:
            logger.info("Saving client with ID: %s to table '%s'", client.id, self.table_name)
            self._table.put_item(Item=item)
            return client
        except ClientError as error:
            logger.error(
                "Failed to save client %s in DynamoDB table '%s': %s",
                client.id,
                self.table_name,
                error.response.get("Error", {}).get("Message", str(error)),
            )
            raise error

    def get_by_id(self, client_id: Union[str, UUID]) -> Optional[Client]:
        """Retrieve a client domain entity from DynamoDB by its unique ID.

        Args:
            client_id (Union[str, UUID]): Unique identifier of the client.

        Returns:
            Optional[Client]: The client entity if found, otherwise None.

        Raises:
            ClientError: If an error occurs during the DynamoDB GetItem operation.
        """
        lookup_id = str(client_id)
        try:
            logger.info("Fetching client with ID: %s from table '%s'", lookup_id, self.table_name)
            response = self._table.get_item(Key={"id": lookup_id})
            item = response.get("Item")
            if not item:
                logger.info("Client with ID: %s not found in table '%s'", lookup_id, self.table_name)
                return None
            return self._to_domain_entity(item)
        except ClientError as error:
            logger.error(
                "Failed to get client %s from DynamoDB table '%s': %s",
                lookup_id,
                self.table_name,
                error.response.get("Error", {}).get("Message", str(error)),
            )
            raise error
