import sys
from pathlib import Path

from flask import Flask, jsonify, render_template

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import Config
from storage.json_store import ensure_store_exists, read_phishing_records

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates",
)

Config.validate_portal()
ensure_store_exists(Config.PHISHING_RECORDS_PATH)


@app.route("/")
def index():
    return render_template("portal.html")


@app.route("/alerts")
def alerts():
    records = read_phishing_records(Config.PHISHING_RECORDS_PATH)
    return jsonify(records)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
