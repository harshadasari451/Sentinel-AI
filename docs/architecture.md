# SentinelAI architecture

## Current milestone

The checked-in implementation is the first backend milestone. It establishes typed API contracts, request validation, incident lifecycle primitives, a replaceable repository boundary, tests, and delivery automation. It does not yet contain an LLM-driven investigation workflow.

```text
client
  |
  v
FastAPI application
  |-- system endpoints: health, readiness, version
  |-- incident endpoints: create, retrieve
  |
  v
IncidentRepository
  |
  v
in-memory storage (Phase 1)
```

## Boundary decisions

- The API depends on an incident repository rather than a database implementation.
- Pydantic models reject unknown input fields and preserve stable output contracts.
- Incidents use UUID identifiers and timezone-aware creation timestamps.
- Every response carries a request ID for later log and trace correlation.
- Health, readiness, and version checks are independent of future AI providers.

## Next milestones

1. Replace in-memory storage with PostgreSQL and versioned migrations.
2. Add typed evidence records with immutable provenance and checksums.
3. Introduce connector interfaces for operational systems and fixture replay.
4. Add hybrid retrieval and reranking with an evaluation dataset.
5. Implement bounded investigation nodes, persistence, and a human approval gate.
6. Instrument requests, tools, and workflow nodes with traces, metrics, and logs.

## Non-goals for Phase 1

- No autonomous remediation
- No unsupported root-cause claims
- No production credentials or external system access
- No benchmark claims before the evaluation harness exists
