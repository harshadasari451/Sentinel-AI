from threading import RLock
from uuid import UUID

from sentinel_ai.domain.incidents import Incident, IncidentCreate


class IncidentRepository:
    """Small in-memory repository used by the first API milestone."""

    def __init__(self) -> None:
        self._incidents: dict[UUID, Incident] = {}
        self._lock = RLock()

    def create(self, payload: IncidentCreate) -> Incident:
        incident = Incident.from_create(payload)
        with self._lock:
            self._incidents[incident.id] = incident
        return incident

    def get(self, incident_id: UUID) -> Incident | None:
        with self._lock:
            return self._incidents.get(incident_id)

    def is_ready(self) -> bool:
        return True
