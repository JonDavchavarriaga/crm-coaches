"""Main entrypoint for CRM Core FastAPI microservice.

This module sets up HTTP routes, dependency injection for Clean Architecture layers,
and exposes RESTful APIs for managing clients and service health.
"""

import logging
from typing import Optional
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from application.services import ClientService
from domain.models import Client
from domain.ports import ClientRepository
from infrastructure.dynamodb_repository import DynamoDBClientRepository

# Configure standard application logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("crm-core-service")

# Initialize FastAPI application
app = FastAPI(
    title="CRM Core Service",
    description="Core CRM microservice for managing coaches, clients, sessions, and goals.",
    version="1.0.0",
)


# --- DTO Schemas ---

class CreateClientRequest(BaseModel):
    """Payload schema for creating a new client."""
    coach_id: UUID = Field(..., description="Unique identifier of the assigned coach")
    first_name: str = Field(..., min_length=1, max_length=100, description="Client first name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Client last name")
    email: str = Field(
        ...,
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        description="Client email address",
    )
    phone_number: Optional[str] = Field(default=None, max_length=20, description="Contact phone number")
    notes: Optional[str] = Field(default=None, max_length=2000, description="Initial coaching notes")


class HealthResponse(BaseModel):
    """Payload schema for service health status."""
    status: str = Field(default="ok", description="Service health state")


# --- Dependency Injection Providers ---

def get_client_repository() -> ClientRepository:
    """Dependency provider for the ClientRepository port adapter."""
    return DynamoDBClientRepository()


def get_client_service(
    repository: ClientRepository = Depends(get_client_repository),
) -> ClientService:
    """Dependency provider for the ClientService application layer."""
    return ClientService(client_repository=repository)


# --- API Routes ---

@app.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    tags=["System"],
    summary="Health check endpoint",
)
def health_check() -> HealthResponse:
    """Verify that the microservice is operational and healthy."""
    return HealthResponse(status="ok")


@app.post(
    "/clients/",
    response_model=Client,
    status_code=status.HTTP_201_CREATED,
    tags=["Clients"],
    summary="Create a new client",
)
def create_client(
    payload: CreateClientRequest,
    service: ClientService = Depends(get_client_service),
) -> Client:
    """Create and persist a new coaching client entity."""
    logger.info("Received request to create client with email: %s", payload.email)
    created_client = service.create_client(
        coach_id=payload.coach_id,
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        phone_number=payload.phone_number,
        notes=payload.notes,
    )
    return created_client


@app.get(
    "/clients/{client_id}",
    response_model=Client,
    status_code=status.HTTP_200_OK,
    tags=["Clients"],
    summary="Get client by ID",
)
def get_client(
    client_id: UUID,
    service: ClientService = Depends(get_client_service),
) -> Client:
    """Retrieve an existing client by their unique identifier."""
    logger.info("Received request to fetch client with ID: %s", client_id)
    client = service.get_client(client_id=client_id)
    if not client:
        logger.warning("Client with ID %s not found", client_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID '{client_id}' not found.",
        )
    return client
