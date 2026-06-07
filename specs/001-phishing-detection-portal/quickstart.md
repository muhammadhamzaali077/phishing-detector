# Quickstart: Phishing Detector Portal

## Prerequisites

- Python 3.11 or newer installed.
- A Gmail account with OAuth client credentials downloaded as `credentials.json`.
- A browser for the portal UI.
- Environment variable `OPENAI_API_KEY` configured.
- `credentials.json` and `token.json` must be stored locally and excluded from version control.

## Setup

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the environment:

Windows:
```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:
```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install openai google-auth google-auth-oauthlib google-api-python-client Flask pytest
```

4. Set environment variables:

```bash
set OPENAI_API_KEY=your_openai_api_key
```

For PowerShell:

```powershell
$env:OPENAI_API_KEY = "your_openai_api_key"
```

Optional environment variable overrides:

```powershell
$env:GMAIL_CREDENTIALS_PATH = "credentials.json"
$env:GMAIL_TOKEN_PATH = "token.json"
$env:PHISHING_RECORDS_PATH = "data\phishing_records.json"
```

## First Run

1. Place `credentials.json` in the project root.
2. Run the Gmail OAuth flow to create `token.json` if needed.
3. Launch the portal and agent.

## Run commands

Assuming the implementation follows the planned structure:

```bash
python src/agent/run_agent.py
```

In a second terminal:

```bash
python src/portal/app.py
```

If you wish to run the agent continuously, use:

```bash
python src/agent/run_agent.py --poll --interval 30
```

## Validation

1. Open the portal at `http://localhost:8000` (or the configured port).
2. Send a test phishing-like message to the monitored Gmail inbox.
3. Confirm that the portal list updates with the new phishing alert.
4. Confirm that a browser pop-up alert appears showing the sender and subject for the newly flagged phishing email.
5. Confirm safe emails do not appear in the portal list.

## Expected Outcomes

- The portal serves a running list of detected phishing emails.
- New flagged emails automatically populate the portal.
- Each phishing detection triggers an immediate browser pop-up with sender and subject details.
- The JSON store `data/phishing_records.json` is populated with alert records.
