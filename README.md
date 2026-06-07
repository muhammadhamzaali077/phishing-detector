# phishing-detector

Phishing Detector Agent with Web Portal

A Python-based phishing detection system that monitors a Gmail inbox using strict read-only access, classifies incoming emails with OpenAI, logs phishing detections to a web portal, and triggers immediate browser alerts for flagged threats.

## Features

- Gmail OAuth read-only monitoring
- OpenAI-powered email classification
- Real-time phishing alert portal
- Browser pop-up notifications
- JSON-backed persistence
- Continuous polling agent

## Quick Start

See `specs/001-phishing-detection-portal/quickstart.md` for setup instructions.

## Project Structure

```
src/
├── agent/
│   ├── gmail_monitor.py
│   ├── classifier.py
│   └── run_agent.py
├── portal/
│   ├── app.py
│   ├── static/
│   │   ├── app.js
│   │   └── index.html
│   └── templates/
│       └── portal.html
└── storage/
    └── json_store.py
```

## License

Private project
