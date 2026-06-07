import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

from google.auth.transport.requests import Request

# Ensure src is importable when executed from the repository root
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import Config
from agent.classifier import classify_email_message
from agent.gmail_monitor import (
    build_gmail_service,
    get_credentials,
    get_message,
    list_unread_messages,
    parse_email_message,
)
from storage.json_store import append_phishing_alert, read_phishing_records


def process_unread_messages() -> None:
    Config.validate()
    creds = get_credentials(Config.GMAIL_CREDENTIALS_PATH, Config.GMAIL_TOKEN_PATH)
    service = build_gmail_service(creds)
    messages = list_unread_messages(service)
    if not messages:
        print("No new unread Gmail messages found.")
        return

    known_records = read_phishing_records(Config.PHISHING_RECORDS_PATH)
    known_message_ids = {record.get("message_id") for record in known_records}

    for entry in messages:
        message_id = entry.get("id")
        if not message_id or message_id in known_message_ids:
            continue

        raw_message = get_message(service, message_id)
        email_message = parse_email_message(raw_message)
        classification, reason = classify_email_message(email_message)
        email_message["classification"] = classification
        email_message["classification_reason"] = reason

        if classification == "phishing":
            alert = {
                "alert_id": f"alert_{message_id}_{int(time.time())}",
                "message_id": message_id,
                "sender": email_message["sender"],
                "subject": email_message["subject"],
                "received_at": email_message["received_at"],
                "detected_at": datetime.utcnow().isoformat() + "Z",
                "reason": reason or "Detected as phishing by the classifier.",
                "status": "new",
            }
            if append_phishing_alert(Config.PHISHING_RECORDS_PATH, alert):
                print(f"Phishing alert recorded for message {message_id}")
            else:
                print(f"Skipped duplicate phishing alert for message {message_id}")
        else:
            print(f"Message {message_id} classified as safe.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Gmail phishing detector agent.")
    parser.add_argument(
        "--poll",
        action="store_true",
        help="Continuously poll Gmail for new unread messages.",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=Config.POLL_INTERVAL_SECONDS,
        help="Polling interval in seconds when --poll is enabled.",
    )
    args = parser.parse_args()

    if args.poll:
        print(f"Starting Gmail phishing agent in polling mode every {args.interval} seconds...")
        while True:
            try:
                process_unread_messages()
            except Exception as exc:
                print(f"Agent error: {exc}")
            time.sleep(args.interval)
    else:
        process_unread_messages()


if __name__ == "__main__":
    main()
