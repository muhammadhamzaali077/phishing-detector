# Data Model: Phishing Detector Portal

## Entities

### EmailMessage
Represents a Gmail message that has been inspected by the agent.

- `message_id`: string, Gmail message identifier
- `thread_id`: string, Gmail thread identifier
- `sender`: string, sender email address or display name
- `subject`: string, email subject line
- `snippet`: string, short preview or email body snippet
- `received_at`: string, timestamp when the email was received
- `classification`: string, one of `safe` or `phishing`
- `classification_reason`: string, optional explanation of why the message was flagged
- `raw_headers`: object, optional parsed headers needed for auditing
- `raw_body`: string, optional raw message body for classification only

### PhishingAlertRecord
Represents a detected phishing alert that is stored and displayed by the portal.

- `alert_id`: string, unique identifier for the alert event
- `message_id`: string, Gmail message identifier
- `sender`: string, sender email address or display name
- `subject`: string, email subject line
- `detected_at`: string, timestamp when phishing was detected
- `received_at`: string, original email received timestamp
- `reason`: string, short reason why the email was classified as phishing
- `status`: string, e.g. `new`, `viewed`

## Data Storage

### JSON Store
The portal persists phishing alert data in a simple JSON file:

- File: `data/phishing_records.json`
- Format: array of `PhishingAlertRecord`

Example:

```json
[
  {
    "alert_id": "alert_001",
    "message_id": "178f4c...",
    "sender": "badguy@example.com",
    "subject": "Urgent account verification required",
    "received_at": "2026-06-07T14:20:00Z",
    "detected_at": "2026-06-07T14:20:18Z",
    "reason": "Suspicious login request and mismatched sender domain",
    "status": "new"
  }
]
```

## Relationships

- A `PhishingAlertRecord` is derived from an `EmailMessage` classified as `phishing`.
- The portal reads `PhishingAlertRecord` entries from the JSON store to present the running threat list.

## Validation Rules

- `message_id` and `alert_id` must be unique.
- `sender`, `subject`, and `detected_at` are required for portal display.
- `classification` for stored phishing records must equal `phishing`.
- The JSON store must be appended or replaced atomically to avoid corruption during writes.
