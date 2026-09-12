"""Application services coordinating use cases for the CRM Core Service.

This module implements the core business use cases for Client management,
orchestrating interactions between domain entities and repository ports.
"""

from typing import Optional, Union
from uuid import UUID

from domain.models import Client, ClientStatus
from domain.ports import ClientRepository


class ClientService:
    """Application service for managing client-related use cases."""

    def __init__(self, client_repository: ClientRepository) -> None:
        """Initialize ClientService with a client repository port.

        Args:
            client_repository (ClientRepository): The repository port implementation.
        """
        self._client_repository = client_repository

    def create_client(
        self,
        coach_id: UUID,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Client:
        """Create and persist a new coaching client.

        Args:
            coach_id (UUID): Unique identifier of the assigned coach.
            first_name (str): Client first name.
            last_name (str): Client last name.
            email (str): Client email address.
            phone_number (Optional[str]): Contact phone number.
            notes (Optional[str]): Contextual coaching notes.

        Returns:
            Client: The newly created and persisted client domain entity.
        """
        client = Client(
            coach_id=coach_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            status=ClientStatus.ACTIVE,
            notes=notes,
        )
        return self._client_repository.save(client)

    def get_client(self, client_id: Union[str, UUID]) -> Optional[Client]:
        """Retrieve an existing client by unique identifier.

        Args:
            client_id (Union[str, UUID]): Unique identifier of the client.

        Returns:
            Optional[Client]: The client domain entity if found, otherwise None.
        """
        return self._client_repository.get_by_id(client_id)
