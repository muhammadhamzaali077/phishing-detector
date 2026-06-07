---
description: "Task list for Phishing Detector Portal implementation"
---

# Tasks: Phishing Detector Portal

**Input**: Design documents from `/specs/001-phishing-detection-portal/`

**Prerequisites**: `plan.md`, `spec.md`, `data-model.md`, `contracts/`, `quickstart.md`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize the repository environment, install dependencies, and create the shared JSON persistence layer.

- [X] T001 Create `requirements.txt` in the repository root with the Python dependencies: `openai`, `google-auth`, `google-auth-oauthlib`, `google-api-python-client`, `Flask`, `requests`, `pytest`
- [X] T002 Create `src/config.py` to load `OPENAI_API_KEY`, `GMAIL_CREDENTIALS_PATH`, `GMAIL_TOKEN_PATH`, and `PHISHING_RECORDS_PATH` from environment variables
- [X] T003 Create `data/phishing_records.json` with an initial empty array `[]`
- [X] T004 Create `src/storage/json_store.py` with functions to read phishing records and append confirmed phishing alerts atomically
- [X] T005 Install Python dependencies from `requirements.txt` into the local environment

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build the core Gmail auth, classification, and portal routing foundation before story-specific behavior.

- [X] T006 Create `src/agent/gmail_monitor.py` and implement Gmail OAuth read-only flow using `google-auth-oauthlib` and the Gmail `readonly` scope
- [X] T007 Create `src/agent/classifier.py` and implement OpenAI classification logic that returns `safe` or `phishing` for an email payload
- [X] T008 Create `src/agent/run_agent.py` to orchestrate configuration loading, Gmail polling, classification calls, and phishing alert dispatching
- [X] T009 Create `src/portal/app.py` as a Flask backend exposing `/alerts` and `/health` endpoints and serving portal static files
- [X] T010 Create `src/portal/static/index.html` and `src/portal/static/app.js` for the web portal UI

---

## Phase 3: User Story 1 - Monitor Gmail and classify new email traffic (Priority: P1)

**Goal**: Continuously fetch new unread Gmail messages and classify each message without modifying Gmail content.

**Independent Test**: Verify that the agent reads unread inbox messages and returns a classification of `safe` or `phishing` for each message.

- [X] T011 [US1] Implement mailbox polling in `src/agent/gmail_monitor.py` to fetch only new unread messages from the Gmail inbox
- [X] T012 [US1] Implement `parse_email_message` in `src/agent/gmail_monitor.py` to extract sender, subject, snippet, and received timestamp
- [X] T013 [US1] Implement OpenAI request construction in `src/agent/classifier.py` to evaluate the email content and return a definitive verdict
- [X] T014 [US1] Implement the classification workflow in `src/agent/run_agent.py` so that safe messages are skipped and phishing candidates are forwarded to storage

---

## Phase 4: User Story 2 - Log detected phishing emails to the portal (Priority: P1)

**Goal**: Persist confirmed phishing detections with sender and subject details, and make the alert records accessible to the portal.

**Independent Test**: Validate that a phishing detection produces a new JSON alert entry with sender and subject and that `/alerts` returns it.

- [X] T015 [US2] Implement `append_phishing_alert` in `src/storage/json_store.py` to record `alert_id`, `message_id`, `sender`, `subject`, `received_at`, `detected_at`, and `reason`
- [X] T016 [US2] Persist confirmed phishing detections in `src/agent/run_agent.py` by sending them to `src/storage/json_store.py`
- [X] T017 [US2] Implement the `/alerts` endpoint in `src/portal/app.py` to read stored phishing records from `data/phishing_records.json`
- [X] T018 [US2] Ensure portal static assets in `src/portal/static/app.js` can fetch `/alerts` from the same Flask server

---

## Phase 5: User Story 3 - Show immediate alert for phishing detections (Priority: P2)

**Goal**: Display a running list of detected phishing threats and trigger a browser pop-up immediately when a new threat appears.

**Independent Test**: Confirm that a newly stored phishing alert causes the portal to show a pop-up with sender and subject details.

- [X] T019 [US3] Implement portal alert rendering in `src/portal/static/app.js` to display the running phishing alert list with sender and subject fields
- [X] T020 [US3] Implement a browser pop-up in `src/portal/static/app.js` that triggers when a newly detected phishing record appears with `status: new`
- [X] T021 [US3] Implement periodic polling in `src/portal/static/app.js` to refresh the alert list from `/alerts` every 10 seconds
- [X] T022 [US3] Update `src/portal/static/index.html` to include the portal layout, threat list, and alert messaging area

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, security checks, and documentation to complete the implementation.

- [X] T023 Update `specs/001-phishing-detection-portal/quickstart.md` with exact setup and run instructions for the Gmail OAuth flow and portal launch
- [X] T024 [P] Validate that `src/config.py` loads all required secrets from environment variables only and that `credentials.json` is referenced securely
- [X] T025 [P] Validate that `src/agent/gmail_monitor.py` only uses Gmail read-only scopes and does not modify any message content
- [X] T026 [P] Perform an end-to-end local validation by running `src/agent/run_agent.py`, opening the portal, and confirming the alert list and popup behavior

---

## Dependencies & Execution Order

- Phase 1 tasks must complete first to establish the environment and JSON store.
- Phase 2 tasks depend on Phase 1 and provide the shared Gmail auth, classification, and portal foundation.
- User Story phases depend on Phase 2 and can be implemented independently once the foundation is ready.
- Polish tasks depend on the completion of the user story phases.

## Parallel Opportunities

- `T002`, `T003`, and `T004` are parallelizable because they are independent setup actions.
- `T006`, `T007`, `T009`, and `T010` can be developed in parallel once the environment is ready.
- `T015`, `T017`, and `T019` are parallelizable after core storage and portal scaffolding exist.
- User stories `US1`, `US2`, and `US3` can be developed concurrently after Phase 2 is finished.
