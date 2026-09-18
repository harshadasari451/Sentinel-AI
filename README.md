# SentinelAI

> **Project status: Active development - Phase 1 backend scaffold is available.**

SentinelAI is an AI-powered, multimodal incident-investigation platform being developed to help engineering teams analyze operational failures using evidence from logs, metrics, traces, deployment changes, runbooks, screenshots, historical incidents, and optional incident-call audio.

The repository currently contains a working, typed FastAPI foundation with health, readiness, version, incident-creation, and incident-retrieval endpoints; an in-memory incident repository; automated API tests; Docker packaging; and continuous-integration checks. Retrieval, agent orchestration, multimodal ingestion, persistent storage, and the investigation dashboard remain under development.

## Current implementation

- Five typed FastAPI endpoints with stable response contracts
- Pydantic incident models and validation
- Thread-safe in-memory incident repository
- Consistent JSON error responses and request IDs
- Automated tests for service health, validation, creation, retrieval, and missing incidents
- Docker image and local Compose configuration
- GitHub Actions checks for linting and tests

The current milestone intentionally establishes reliable backend contracts before introducing LLM or agent behavior.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
uvicorn sentinel_ai.api:app --reload
```

Open the interactive API documentation at `http://127.0.0.1:8000/docs`.

Run the quality checks:

```bash
ruff check .
pytest -q
```

Create and retrieve an incident:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/incidents \
  -H 'Content-Type: application/json' \
  -d '{"title":"Checkout latency spike","severity":"SEV2","affected_services":["checkout-service"]}'
```

## Planned capabilities

- Normalize logs, metrics, traces, deployment events, documents, images, and audio into typed evidence.
- Combine dense and lexical retrieval with metadata filtering and reranking.
- Orchestrate bounded investigation workflows with explicit state, tool contracts, retries, and stop conditions.
- Generate and verify competing hypotheses before selecting a root cause or abstaining when evidence is insufficient.
- Provide evidence-linked incident summaries and safe remediation recommendations.
- Track retrieval quality, diagnosis accuracy, grounding, latency, reliability, and cost through repeatable evaluations.
- Support observability, security controls, containerized deployment, and human-in-the-loop approval.

## Target architecture

The implementation is evolving toward:

- **Backend:** Python, FastAPI, Pydantic, PostgreSQL, pgvector, and Redis
- **AI orchestration:** LangGraph and structured LLM workflows
- **Retrieval:** hybrid search, reranking, evidence provenance, and citations
- **Multimodal AI:** text, dashboard screenshots, documents, and optional audio transcription
- **Observability:** OpenTelemetry, Prometheus, Grafana, and structured logging
- **Infrastructure:** Docker, Kubernetes, CI/CD, and cloud deployment
- **Quality:** Pytest, contract tests, evaluation datasets, and regression gates

## Target investigation workflow

1. Receive an incident and establish its operational context.
2. Collect approved evidence from metrics, logs, deployments, runtime systems, and internal documentation.
3. Retrieve and rerank relevant runbooks and historical incidents.
4. Generate several possible root causes.
5. Test each hypothesis against supporting and contradicting evidence.
6. Select the best-supported cause or report that the evidence is insufficient.
7. Produce a cited incident report and request human approval before any remediation action.

## Safety principles

- Important claims must be linked to evidence.
- Observations, hypotheses, and recommended actions remain clearly separated.
- The workflow actively searches for contradicting evidence.
- Investigation steps and model or tool calls remain traceable.
- Destructive remediation is never executed automatically.

## Roadmap

- [x] Typed API and domain-model foundation
- [x] In-memory repository and API tests
- [x] Docker and CI foundation
- [ ] PostgreSQL persistence and migrations
- [ ] Evidence ingestion and provenance model
- [ ] Hybrid retrieval and reranking
- [ ] Bounded LangGraph investigation workflow
- [ ] Evaluation harness and regression gates
- [ ] Observability, dashboard, and deployment

See [docs/architecture.md](docs/architecture.md) for the current design and boundaries.

## Author

**Harsha Vardhan Dasari**<br>
[GitHub](https://github.com/harshadasari451) · [LinkedIn](https://www.linkedin.com/in/harshadasari451/)
