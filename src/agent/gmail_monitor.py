import base64
import os
import re
from email import message_from_bytes
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_credentials(client_secrets_path: str, token_path: str) -> Credentials:
    creds = None
    token_file = Path(token_path)
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_path, SCOPES)
            creds = flow.run_local_server(port=0)
        token_file.parent.mkdir(parents=True, exist_ok=True)
        with token_file.open("w", encoding="utf-8") as token_handle:
            token_handle.write(creds.to_json())
    return creds


def build_gmail_service(credentials: Credentials):
    return build("gmail", "v1", credentials=credentials)


def list_unread_messages(service: Any, max_results: int = 20) -> list[dict]:
    response = service.users().messages().list(
        userId="me",
        q="is:unread in:inbox",
        maxResults=max_results,
    ).execute()
    return response.get("messages", [])


def get_message(service: Any, message_id: str) -> dict:
    return service.users().messages().get(
        userId="me", id=message_id, format="full"
    ).execute()


def _get_text_body(payload: dict) -> str:
    if payload.get("body") and payload["body"].get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"].encode("ASCII")).decode(
            "utf-8", errors="ignore"
        )
    if payload.get("parts"):
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                return _get_text_body(part)
            if part.get("mimeType") == "text/html":
                body = _get_text_body(part)
                return re.sub(r"<[^>]+>", " ", body)
    return ""


def parse_email_message(message: dict) -> dict:
    payload = message.get("payload", {})
    headers = {h["name"]: h["value"] for h in payload.get("headers", [])}
    sender = headers.get("From", "Unknown sender")
    subject = headers.get("Subject", "(no subject)")
    received_at = headers.get("Date", "")
    snippet = message.get("snippet", "")
    body = _get_text_body(payload)
    if not snippet and body:
        snippet = body[:250]
    return {
        "message_id": message.get("id", ""),
        "thread_id": message.get("threadId", ""),
        "sender": sender,
        "subject": subject,
        "snippet": snippet,
        "received_at": received_at,
        "body": body,
        "classification": "unknown",
        "classification_reason": "",
    }
