import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile


def ensure_store_exists(store_path: str) -> Path:
    store_file = Path(store_path)
    if not store_file.exists():
        store_file.parent.mkdir(parents=True, exist_ok=True)
        store_file.write_text("[]", encoding="utf-8")
    return store_file


def read_phishing_records(store_path: str) -> list[dict]:
    store_file = ensure_store_exists(store_path)
    with store_file.open("r", encoding="utf-8") as handle:
        try:
            return json.load(handle)
        except json.JSONDecodeError:
            return []


def append_phishing_alert(store_path: str, alert: dict) -> bool:
    store_file = ensure_store_exists(store_path)
    records = read_phishing_records(store_path)
    existing_ids = {record.get("message_id") for record in records}
    if alert.get("message_id") in existing_ids:
        return False
    records.append(alert)
    with NamedTemporaryFile("w", delete=False, dir=store_file.parent, encoding="utf-8") as temp_file:
        json.dump(records, temp_file, indent=2)
        temp_name = temp_file.name
    os.replace(temp_name, store_file)
    return True
