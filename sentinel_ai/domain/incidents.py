from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class Severity(StrEnum):
    SEV1 = "SEV1"
    SEV2 = "SEV2"
    SEV3 = "SEV3"
    SEV4 = "SEV4"


class IncidentStatus(StrEnum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"


class IncidentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str = Field(min_length=5, max_length=160)
    severity: Severity
    affected_services: list[str] = Field(min_length=1, max_length=25)
    description: str | None = Field(default=None, max_length=2_000)


class Incident(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UUID
    title: str
    severity: Severity
    status: IncidentStatus
    affected_services: list[str]
    description: str | None
    created_at: datetime

    @classmethod
    def from_create(cls, payload: IncidentCreate) -> "Incident":
        return cls(
            id=uuid4(),
            title=payload.title,
            severity=payload.severity,
            status=IncidentStatus.OPEN,
            affected_services=payload.affected_services,
            description=payload.description,
            created_at=datetime.now(UTC),
        )
