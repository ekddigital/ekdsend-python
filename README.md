# EKDSend Python SDK

The official Python SDK for the EKDSend API. Send emails, SMS, and voice calls with ease.

[![PyPI version](https://badge.fury.io/py/ekdsend.svg)](https://badge.fury.io/py/ekdsend)
[![Python Versions](https://img.shields.io/pypi/pyversions/ekdsend.svg)](https://pypi.org/project/ekdsend/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

```bash
pip install ekdsend
```

## Quick Start

```python
from ekdsend import EKDSend

client = EKDSend("ek_live_xxxxxxxxxxxxx")

# Send an email
email = client.emails.send(
    from_email="hello@yourdomain.com",
    to="user@example.com",
    subject="Hello from EKDSend!",
    html="<h1>Welcome!</h1><p>Thanks for joining us.</p>"
)

print(f"Email sent: {email.id}")
```

## Async Support

```python
import asyncio
from ekdsend import AsyncEKDSend

async def main():
    async with AsyncEKDSend("ek_live_xxxxxxxxxxxxx") as client:
        email = await client.emails.send(
            from_email="hello@yourdomain.com",
            to="user@example.com",
            subject="Hello!",
            html="<h1>World</h1>"
        )
        print(f"Email sent: {email.id}")

asyncio.run(main())
```

## Configuration

```python
from ekdsend import EKDSend

client = EKDSend(
    api_key="ek_live_xxxxxxxxxxxxx",
    base_url="https://es.ekddigital.com/v1",  # Optional
    timeout=30.0,                            # Request timeout in seconds
    max_retries=3,                           # Auto-retry on failures
    debug=True                               # Enable debug logging
)
```

## Email API

### Send Email

```python
email = client.emails.send(
    from_email="hello@yourdomain.com",
    to=["user1@example.com", "user2@example.com"],
    subject="Weekly Newsletter",
    html="<h1>Newsletter</h1><p>Your weekly update.</p>",
    text="Newsletter\n\nYour weekly update.",  # Optional plain text
    cc="cc@example.com",
    bcc=["bcc1@example.com", "bcc2@example.com"],
    reply_to="support@yourdomain.com",
    tags=["newsletter", "weekly"],
    metadata={"campaign_id": "spring-2024"}
)
```

### With Attachments

```python
import base64

with open("report.pdf", "rb") as f:
    pdf_content = base64.b64encode(f.read()).decode()

email = client.emails.send(
    from_email="reports@yourdomain.com",
    to="manager@company.com",
    subject="Monthly Report",
    html="<p>Please find the report attached.</p>",
    attachments=[
        {
            "filename": "report.pdf",
            "content": pdf_content,
            "content_type": "application/pdf"
        }
    ]
)
```

### Schedule Email

```python
from datetime import datetime, timedelta

send_time = datetime.utcnow() + timedelta(hours=24)

email = client.emails.send(
    from_email="hello@yourdomain.com",
    to="user@example.com",
    subject="Reminder",
    html="<p>Don't forget your meeting tomorrow!</p>",
    scheduled_at=send_time.isoformat() + "Z"
)

# Cancel scheduled email
cancelled = client.emails.cancel(email.id)
```

### Retrieve & List Emails

```python
# Get specific email
email = client.emails.get("em_xxxxxxxxxxxxx")
print(f"Status: {email.status}")

# List emails with filters
emails = client.emails.list(
    limit=50,
    status="delivered",
    from_date="2024-01-01T00:00:00Z",
    tags=["transactional"]
)

for email in emails.data:
    print(f"{email.id}: {email.subject} - {email.status}")
```

## SMS API

### Send SMS

```python
sms = client.sms.send(
    to="+14155551234",
    message="Your verification code is: 123456",
    from_number="+14155559999",  # Optional
    metadata={"type": "verification"}
)

print(f"SMS sent: {sms.id}")
```

### Schedule SMS

```python
from datetime import datetime, timedelta

send_time = datetime.utcnow() + timedelta(hours=2)

sms = client.sms.send(
    to="+14155551234",
    message="Your appointment is in 1 hour!",
    scheduled_at=send_time.isoformat() + "Z"
)
```

### Retrieve & List SMS

```python
# Get specific SMS
sms = client.sms.get("sms_xxxxxxxxxxxxx")

# List SMS messages
messages = client.sms.list(limit=25, status="delivered")

for msg in messages.data:
    print(f"{msg.id}: {msg.to} - {msg.status}")
```

## Voice API

### Make a Call with Text-to-Speech

```python
call = client.calls.create(
    to="+14155551234",
    from_number="+14155559999",
    tts_message="Hello! This is an important message from EKDSend.",
    voice="alloy",        # alloy, echo, fable, onyx, nova, shimmer
    language="en-US",
    record=True,
    machine_detection=True
)

print(f"Call initiated: {call.id}")
```

### Make a Call with Audio File

```python
call = client.calls.create(
    to="+14155551234",
    from_number="+14155559999",
    audio_url="https://example.com/message.mp3"
)
```

### Call Management

```python
# Get call status
call = client.calls.get("call_xxxxxxxxxxxxx")
print(f"Call status: {call.status}, Duration: {call.duration}s")

# List calls
calls = client.calls.list(limit=20, status="completed")

# Hang up active call
hung_up = client.calls.hangup("call_xxxxxxxxxxxxx")

# Get call recording
recording = client.calls.get_recording("call_xxxxxxxxxxxxx")
print(f"Recording URL: {recording['url']}")
```

## Error Handling

```python
from ekdsend import EKDSend
from ekdsend.exceptions import (
    EKDSendError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    NotFoundError
)

client = EKDSend("ek_live_xxxxxxxxxxxxx")

try:
    email = client.emails.send(
        from_email="hello@yourdomain.com",
        to="invalid-email",
        subject="Test",
        html="<p>Hello</p>"
    )
except AuthenticationError as e:
    print(f"Invalid API key: {e.message}")
except ValidationError as e:
    print(f"Validation failed: {e.message}")
    print(f"Errors: {e.errors}")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except NotFoundError as e:
    print(f"Resource not found: {e.message}")
except EKDSendError as e:
    print(f"API error: {e.message} (Code: {e.code})")
    print(f"Request ID: {e.request_id}")
```

## Type Hints

The SDK includes full type annotations for better IDE support:

```python
from ekdsend import EKDSend
from ekdsend.types import Email, SMS, VoiceCall

client = EKDSend("ek_live_xxxxxxxxxxxxx")

# Type-safe response objects
email: Email = client.emails.send(
    from_email="hello@yourdomain.com",
    to="user@example.com",
    subject="Hello",
    html="<p>World</p>"
)

# Access typed properties
print(email.id)           # str
print(email.status)       # str
print(email.created_at)   # str (ISO8601)
```

## Framework Integration

### FastAPI

```python
from fastapi import FastAPI, HTTPException
from ekdsend import AsyncEKDSend
from ekdsend.exceptions import EKDSendError

app = FastAPI()
client = AsyncEKDSend("ek_live_xxxxxxxxxxxxx")

@app.post("/send-welcome")
async def send_welcome(user_email: str, name: str):
    try:
        email = await client.emails.send(
            from_email="welcome@yourdomain.com",
            to=user_email,
            subject=f"Welcome, {name}!",
            html=f"<h1>Welcome {name}!</h1>"
        )
        return {"email_id": email.id}
    except EKDSendError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
async def shutdown():
    await client.close()
```

### Django

```python
# settings.py
EKDSEND_API_KEY = "ek_live_xxxxxxxxxxxxx"

# utils/email.py
from django.conf import settings
from ekdsend import EKDSend

def get_email_client():
    return EKDSend(settings.EKDSEND_API_KEY)

# views.py
from .utils.email import get_email_client

def send_notification(request):
    client = get_email_client()
    try:
        email = client.emails.send(
            from_email="noreply@yourdomain.com",
            to=request.user.email,
            subject="Notification",
            html="<p>You have a new notification!</p>"
        )
        return JsonResponse({"success": True, "email_id": email.id})
    finally:
        client.close()
```

### Flask

```python
from flask import Flask, jsonify
from ekdsend import EKDSend

app = Flask(__name__)
app.config["EKDSEND_API_KEY"] = "ek_live_xxxxxxxxxxxxx"

def get_client():
    return EKDSend(app.config["EKDSEND_API_KEY"])

@app.route("/send", methods=["POST"])
def send_email():
    client = get_client()
    try:
        email = client.emails.send(
            from_email="hello@yourdomain.com",
            to=request.json["to"],
            subject=request.json["subject"],
            html=request.json["html"]
        )
        return jsonify({"email_id": email.id})
    finally:
        client.close()
```

## Requirements

- Python 3.8+
- httpx
- pydantic

## Development

```bash
# Clone the repository
git clone https://github.com/ekddigital/ekdsend-python.git
cd ekdsend-python

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run type checking
mypy src/ekdsend

# Format code
black src/ekdsend tests
isort src/ekdsend tests
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [Documentation](https://es.ekddigital.com/docs)
- [API Reference](https://es.ekddigital.com/docs/api-reference)
- [GitHub](https://github.com/ekddigital/ekdsend-python)
- [PyPI](https://pypi.org/project/ekdsend/)
