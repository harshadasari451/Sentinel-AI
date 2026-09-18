from uuid import uuid4

from fastapi.testclient import TestClient

from sentinel_ai.api import create_app
from sentinel_ai.services.incidents import IncidentRepository


def make_client() -> TestClient:
    return TestClient(create_app(IncidentRepository()))


def test_health() -> None:
    response = make_client().get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness() -> None:
    response = make_client().get("/readyz")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_version_has_build_fields() -> None:
    response = make_client().get("/version")
    assert response.status_code == 200
    assert set(response.json()) == {"version", "git_sha"}


def test_request_id_is_returned() -> None:
    response = make_client().get("/healthz", headers={"X-Request-ID": "req-test"})
    assert response.headers["X-Request-ID"] == "req-test"


def test_create_and_retrieve_incident() -> None:
    client = make_client()
    payload = {
        "title": "Checkout latency spike",
        "severity": "SEV2",
        "affected_services": ["checkout-service", "postgres"],
        "description": "Latency increased immediately after a configuration change.",
    }

    created = client.post("/api/v1/incidents", json=payload)
    assert created.status_code == 201
    body = created.json()
    assert body["title"] == payload["title"]
    assert body["status"] == "open"

    retrieved = client.get(f"/api/v1/incidents/{body['id']}")
    assert retrieved.status_code == 200
    assert retrieved.json() == body


def test_rejects_unknown_fields() -> None:
    response = make_client().post(
        "/api/v1/incidents",
        json={
            "title": "Checkout latency spike",
            "severity": "SEV2",
            "affected_services": ["checkout-service"],
            "unsupported": True,
        },
    )
    assert response.status_code == 422


def test_requires_an_affected_service() -> None:
    response = make_client().post(
        "/api/v1/incidents",
        json={
            "title": "Checkout latency spike",
            "severity": "SEV2",
            "affected_services": [],
        },
    )
    assert response.status_code == 422


def test_missing_incident_returns_structured_404() -> None:
    incident_id = uuid4()
    response = make_client().get(f"/api/v1/incidents/{incident_id}")
    assert response.status_code == 404
    assert response.json() == {
        "error": "incident_not_found",
        "incident_id": str(incident_id),
    }
