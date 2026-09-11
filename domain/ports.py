"""Domain port interfaces for secondary (driven) adapters.

This module defines repository and external service contracts following Hexagonal
and Clean Architecture principles.
"""

from abc import ABC, abstractmethod
from typing import Optional, Union
from uuid import UUID

from domain.models import Client


class ClientRepository(ABC):
    """Abstract port for managing client entity persistence and retrieval."""

    @abstractmethod
    def save(self, client: Client) -> Client:
        """Persist a client entity into the storage medium.

        Args:
            client (Client): The domain client model to create or update.

        Returns:
            Client: The persisted client entity.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, client_id: Union[str, UUID]) -> Optional[Client]:
        """Retrieve a client domain entity by its unique identifier.

        Args:
            client_id (Union[str, UUID]): Unique identifier of the client.

        Returns:
            Optional[Client]: The client entity if found, otherwise None.
        """
        raise NotImplementedError
