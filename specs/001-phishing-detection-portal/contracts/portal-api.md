# Portal API Contract

## Purpose
Defines the API contract for the web portal that displays detected phishing threats and allows the frontend to receive new alert notifications.

## API Endpoints

### GET /api/alerts

Returns the current list of detected phishing alerts.

#### Response
- `200 OK`
- Content-Type: `application/json`

```json
[
  {
    "alert_id": "string",
    "message_id": "string",
    "sender": "string",
    "subject": "string",
    "received_at": "string",
    "detected_at": "string",
    "reason": "string",
    "status": "string"
  }
]
```

### GET /api/alerts/latest

Optional helper endpoint that returns only the most recent phishing alert.

#### Response
- `200 OK`
- Content-Type: `application/json`

```json
{
  "alert_id": "string",
  "message_id": "string",
  "sender": "string",
  "subject": "string",
  "received_at": "string",
  "detected_at": "string",
  "reason": "string",
  "status": "string"
}
```

## Portal Event Flow

1. The agent monitors Gmail and detects a phishing email.
2. The agent stores a `PhishingAlertRecord` in `data/phishing_records.json`.
3. The portal backend exposes `/api/alerts` for the frontend to poll periodically.
4. The frontend compares newly fetched alerts with the current list and triggers a browser pop-up when a new alert appears.

## Data Schema: PhishingAlertRecord

- `alert_id`: unique identifier for the alert event
- `message_id`: Gmail message identifier
- `sender`: sender email address or display name
- `subject`: email subject line
- `received_at`: original email arrival timestamp
- `detected_at`: phishing detection timestamp
- `reason`: brief explanation of classification outcome
- `status`: `new` or `viewed`

## Security Contract

- The portal API must not expose Gmail credentials or internal secrets.
- The API must only present phishing alert metadata and may not expose full message bodies or raw Gmail tokens.
- The backend must use read-only Gmail API scopes and must not allow the portal to modify Gmail state.
