# Implementation Plan: Phishing Detector Portal

**Branch**: `[001-phishing-detection-portal]` | **Date**: 2026-06-07 | **Spec**: `specs/001-phishing-detection-portal/spec.md`

**Input**: Feature specification from `specs/001-phishing-detection-portal/spec.md`

**Note**: This plan is the output of the `/speckit.plan` workflow.

## Summary

Build a Python-based phishing detection agent and lightweight web portal that monitors a Gmail inbox using strict read-only Gmail API permissions, classifies new incoming email as safe or phishing via the OpenAI Agents SDK, logs phishing detections to a JSON-backed portal store, and displays immediate browser alerts for newly flagged threats.

## Technical Context

**Language/Version**: Python 3.11+ with the OpenAI Agents SDK.

**Primary Dependencies**: `openai`, `google-auth`, `google-auth-oauthlib`, `google-api-python-client`, `Flask` (or `FastAPI`), `uvicorn` (if FastAPI), `requests`, `pytest`.

**Storage**: Local JSON file store (`phishing_records.json`) for detected phishing alerts.

**Testing**: `pytest` for unit/integration tests; manual browser validation for portal alert behavior.

**Target Platform**: Local server / development environment on Windows or Linux with browser access.

**Project Type**: Web service + agent runner.

**Performance Goals**: Detect and log phishing emails within 30 seconds of arrival; keep UI latency under 1 second for portal refresh or alert display.

**Constraints**: Gmail access must remain read-only; no message sending/deletion/modification; secrets must come from environment variables and no credentials may be committed to version control.

**Scale/Scope**: Single-user Gmail inbox monitoring and a lightweight browser portal for ongoing phishing alert review.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Python + OpenAI Agents SDK only: PASS
- Gmail API read-only only: PASS
- Secrets via environment variables only: PASS
- No committed secret files in repo: PASS

## Project Structure

### Documentation (this feature)

```text
specs/001-phishing-detection-portal/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── portal-api.md
├── spec.md
└── tasks.md             # generated in Phase 2 by /speckit.tasks
```

### Source Code (repository root)

```text
src/
├── agent/
│   ├── gmail_monitor.py
│   ├── classifier.py
│   └── run_agent.py
├── portal/
│   ├── app.py
│   ├── static/
│   │   ├── index.html
│   │   └── app.js
│   └── templates/
│       └── portal.html
└── storage/
    └── json_store.py

tests/
├── integration/
└── unit/
```

**Structure Decision**: Single Python project with the agent and portal co-located under `src/`, using a JSON-backed store for phishing alerts and a lightweight browser UI.

## Complexity Tracking

No constitution violations detected; the chosen design is consistent with the security-first, simple architecture required by the project.
