import os
import re

import openai


def classify_email_message(email_message: dict) -> tuple[str, str]:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise EnvironmentError("OPENAI_API_KEY is required for classification")
    openai.api_key = openai_api_key

    prompt = (
        "You are an email security assistant. Classify the following message as either 'safe' or 'phishing'. "
        "Answer with a single word: safe or phishing. Then provide a short reason if the message is phishing. "
        "Do not make any changes to the email."
        "\n\n"
        f"From: {email_message.get('sender')}\n"
        f"Subject: {email_message.get('subject')}\n"
        f"Received: {email_message.get('received_at')}\n"
        f"Snippet:\n{email_message.get('snippet')}\n"
        f"Body:\n{email_message.get('body')}\n"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Classify emails strictly as safe or phishing."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        max_tokens=256,
    )
    content = response.choices[0].message.content.strip()
    classification = "safe"
    reason = ""
    lower = content.lower()
    if "phishing" in lower:
        classification = "phishing"
        reason_match = re.search(r"phishing[:\-]?\s*(.*)", lower)
        if reason_match:
            reason = reason_match.group(1).strip()
        else:
            reason = content
    elif "safe" in lower:
        classification = "safe"
    else:
        classification = "safe"
        reason = "Classification defaulted to safe because no phishing signal was returned."

    return classification, reason
