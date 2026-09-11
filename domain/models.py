"""Domain models representing core business entities.

This module defines pure domain models for the CRM system using Pydantic,
enforcing domain invariants, relationships, and business typing.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict, Field


def get_current_utc() -> datetime:
    """Returns the current UTC datetime."""
    return datetime.now(timezone.utc)


class ClientStatus(str, Enum):
    """Lifecycle status of a coaching client."""
    LEAD = "lead"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class SessionStatus(str, Enum):
    """Lifecycle status of a coaching session."""
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class GoalStatus(str, Enum):
    """Progress status of a client goal."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    ACHIEVED = "achieved"
    CANCELLED = "cancelled"


class DomainEntity(BaseModel):
    """Base domain model entity containing common audit and identification fields."""
    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    created_at: datetime = Field(default_factory=get_current_utc, description="Record creation timestamp")
    updated_at: datetime = Field(default_factory=get_current_utc, description="Record last update timestamp")

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        frozen=False,
    )


class Coach(DomainEntity):
    """Represents a professional coach within the CRM."""
    first_name: str = Field(..., min_length=1, max_length=100, description="Coach first name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Coach last name")
    email: str = Field(
        ...,
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        description="Unique email address",
    )
    phone_number: Optional[str] = Field(default=None, max_length=20, description="Contact phone number")
    specialization: Optional[str] = Field(default=None, max_length=150, description="Area of coaching expertise")
    is_active: bool = Field(default=True, description="Whether the coach account is currently active")

    @property
    def full_name(self) -> str:
        """Returns the coach's full name."""
        return f"{self.first_name} {self.last_name}".strip()


class Client(DomainEntity):
    """Represents a coaching client assigned to a specific coach."""
    coach_id: UUID = Field(..., description="ID of the coach this client belongs to")
    first_name: str = Field(..., min_length=1, max_length=100, description="Client first name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Client last name")
    email: str = Field(
        ...,
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        description="Unique client email address",
    )
    phone_number: Optional[str] = Field(default=None, max_length=20, description="Contact phone number")
    status: ClientStatus = Field(default=ClientStatus.ACTIVE, description="Current status of the client")
    notes: Optional[str] = Field(default=None, max_length=2000, description="General coaching notes about client")

    @property
    def full_name(self) -> str:
        """Returns the client's full name."""
        return f"{self.first_name} {self.last_name}".strip()


class Session(DomainEntity):
    """Represents an individual coaching session between a coach and a client."""
    client_id: UUID = Field(..., description="ID of the client participating in the session")
    coach_id: UUID = Field(..., description="ID of the coach conducting the session")
    title: str = Field(..., min_length=1, max_length=200, description="Session topic or summary")
    description: Optional[str] = Field(default=None, max_length=1000, description="Session agenda details")
    scheduled_at: datetime = Field(..., description="Session start date and time")
    duration_minutes: int = Field(default=60, ge=15, le=480, description="Duration in minutes")
    status: SessionStatus = Field(default=SessionStatus.SCHEDULED, description="Session status")
    notes: Optional[str] = Field(default=None, max_length=5000, description="Post-session review and action items")


class Goal(DomainEntity):
    """Represents a development goal set by or for a client."""
    client_id: UUID = Field(..., description="ID of the client this goal belongs to")
    title: str = Field(..., min_length=1, max_length=200, description="Target goal title")
    description: Optional[str] = Field(default=None, max_length=1000, description="Detailed goal breakdown")
    target_date: Optional[datetime] = Field(default=None, description="Deadline to achieve this goal")
    status: GoalStatus = Field(default=GoalStatus.NOT_STARTED, description="Current goal state")
    progress_percentage: int = Field(default=0, ge=0, le=100, description="Completion percentage (0-100)")
