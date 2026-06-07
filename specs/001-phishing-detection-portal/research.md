# Research: Phishing Detector Portal

## Decision: Gmail integration strategy

- Chosen approach: Poll the Gmail inbox at short intervals using the Gmail API with read-only OAuth credentials.
- Rationale: Polling keeps the architecture simple and avoids extra complexity from push notifications or Pub/Sub integration. It is sufficient for a single-user firewall-style portal and matches the requirement for active monitoring without modifying messages.
- Alternatives considered: Gmail watch notifications via Pub/Sub, which would be more scalable but require additional cloud infrastructure and significantly more setup complexity.

## Decision: Classification engine

- Chosen approach: Use the OpenAI Agents SDK with a Python wrapper around the OpenAI LLM to classify email content as safe or phishing.
- Rationale: The OpenAI Agents SDK provides a simple API for prompt-driven classification and aligns with the projects requirement to use Python plus the OpenAI Agents SDK.
- Alternatives considered: Rule-based keyword detection or local ML models. These were rejected because the user explicitly requested the OpenAI-based classification path and because an LLM-based classifier can better handle real-world phishing language.

## Decision: Front-end portal stack

- Chosen approach: Build a lightweight portal using Flask with simple HTML/JavaScript, or optionally FastAPI with a minimal static frontend.
- Rationale: Flask provides an easy-to-understand way to serve a web UI and JSON endpoints without adding unnecessary frontend complexity. A plain JS poller can detect new phishing records and trigger pop-up alerts in the browser.
- Alternatives considered: React or a heavier frontend framework, which would increase implementation complexity unnecessarily for a simple alert list.

## Decision: Storage format

- Chosen approach: Persist detected phishing alerts in a simple JSON file (`phishing_records.json`).
- Rationale: JSON storage is easy to implement, easy to inspect, and entirely consistent with the requirement for a straightforward file-based store. It also avoids database setup and keeps the prototype simple.
- Alternatives considered: SQLite or full database storage. These were rejected in favor of minimal local storage for a single-user portal MVP.

## Decision: Credentials handling

- Chosen approach: Load `OPENAI_API_KEY` from environment variables and read Gmail OAuth credentials from `credentials.json` and `token.json` kept out of version control.
- Rationale: This strictly enforces the security constitution and prevents secret leakage in the repository.
- Alternatives considered: Storing credentials in a `.env` file. This was rejected because the constitution mandates environment-based secret loading and committed secret exclusion.
