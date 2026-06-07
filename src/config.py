import os
from pathlib import Path


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GMAIL_CREDENTIALS_PATH = os.getenv("GMAIL_CREDENTIALS_PATH", "credentials.json")
    GMAIL_TOKEN_PATH = os.getenv("GMAIL_TOKEN_PATH", "token.json")
    PHISHING_RECORDS_PATH = os.getenv("PHISHING_RECORDS_PATH", "data/phishing_records.json")
    POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "30"))

    @classmethod
    def validate(cls) -> None:
        missing = []
        if not cls.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        if not Path(cls.GMAIL_CREDENTIALS_PATH).exists():
            missing.append(f"GMAIL_CREDENTIALS_PATH ({cls.GMAIL_CREDENTIALS_PATH})")
        if missing:
            raise EnvironmentError(
                "Missing required configuration: " + ", ".join(missing)
            )

    @classmethod
    def validate_portal(cls) -> None:
        store_path = Path(cls.PHISHING_RECORDS_PATH)
        store_path.parent.mkdir(parents=True, exist_ok=True)
        if not store_path.exists():
            store_path.write_text("[]", encoding="utf-8")
