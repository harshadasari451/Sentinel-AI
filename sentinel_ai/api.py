import os
from collections.abc import Awaitable, Callable
from uuid import UUID, uuid4

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from sentinel_ai import __version__
from sentinel_ai.domain.incidents import Incident, IncidentCreate
from sentinel_ai.services.incidents import IncidentRepository


def create_app(repository: IncidentRepository | None = None) -> FastAPI:
    app = FastAPI(
        title="SentinelAI API",
        version=__version__,
        description="Phase 1 API foundation for evidence-grounded incident investigation.",
    )
    app.state.incidents = repository or IncidentRepository()

    @app.middleware("http")
    async def request_context(
        request: Request,
        call_next: Callable[[Request], Awaitable[JSONResponse]],
    ):
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

    @app.get("/healthz", tags=["system"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/readyz", tags=["system"])
    async def readiness(request: Request) -> dict[str, str]:
        if not request.app.state.incidents.is_ready():
            return JSONResponse(status_code=503, content={"status": "not_ready"})
        return {"status": "ready"}

    @app.get("/version", tags=["system"])
    async def version() -> dict[str, str]:
        return {
            "version": os.getenv("APP_VERSION", __version__),
            "git_sha": os.getenv("GIT_SHA", "development"),
        }

    @app.post(
        "/api/v1/incidents",
        response_model=Incident,
        status_code=status.HTTP_201_CREATED,
        tags=["incidents"],
    )
    async def create_incident(payload: IncidentCreate, request: Request) -> Incident:
        return request.app.state.incidents.create(payload)

    @app.get(
        "/api/v1/incidents/{incident_id}",
        response_model=Incident,
        tags=["incidents"],
    )
    async def get_incident(incident_id: UUID, request: Request) -> Incident | JSONResponse:
        incident = request.app.state.incidents.get(incident_id)
        if incident is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": "incident_not_found", "incident_id": str(incident_id)},
            )
        return incident

    return app


app = create_app()
