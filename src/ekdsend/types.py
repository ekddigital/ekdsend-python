"""
Type definitions for EKDSend SDK
"""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class Attachment(BaseModel):
    """Email attachment"""
    filename: str
    content: str  # Base64-encoded content
    type: str  # MIME type


class SendEmailParams(BaseModel):
    """Parameters for sending an email"""
    from_email: str = Field(..., alias="from")
    to: str | List[str]
    subject: str
    html: Optional[str] = None
    text: Optional[str] = None
    template_id: Optional[str] = None
    template_data: Optional[Dict[str, Any]] = None
    cc: Optional[str | List[str]] = None
    bcc: Optional[str | List[str]] = None
    reply_to: Optional[str] = None
    attachments: Optional[List[Attachment]] = None
    headers: Optional[Dict[str, str]] = None
    scheduled_at: Optional[datetime | str] = None
    tags: Optional[List[str]] = None

    class Config:
        populate_by_name = True


class SendEmailResponse(BaseModel):
    """Response from sending an email"""
    id: str
    status: Literal["queued", "sending", "sent", "delivered", "failed"]
    created_at: datetime


class Email(BaseModel):
    """Email object"""
    id: str
    from_email: str = Field(..., alias="from")
    to: List[str]
    subject: str
    status: Literal["queued", "sending", "sent",
                    "delivered", "failed", "bounced"]
    created_at: datetime
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    opened_at: Optional[datetime] = None
    clicked_at: Optional[datetime] = None
    bounced_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        populate_by_name = True


class EmailList(BaseModel):
    """Paginated list of emails"""
    data: List[Email]
    total: int
    limit: int
    offset: int
    has_more: bool


class SendSMSParams(BaseModel):
    """Parameters for sending an SMS"""
    from_number: str = Field(..., alias="from")
    to: str
    body: str
    scheduled_at: Optional[datetime | str] = None
    webhook_url: Optional[str] = None

    class Config:
        populate_by_name = True


class SendSMSResponse(BaseModel):
    """Response from sending an SMS"""
    id: str
    status: Literal["queued", "sending", "sent", "delivered", "failed"]
    segments: int
    created_at: datetime


class SMS(BaseModel):
    """SMS object"""
    id: str
    from_number: str = Field(..., alias="from")
    to: str
    body: str
    status: Literal["queued", "sending", "sent", "delivered", "failed"]
    segments: int
    created_at: datetime
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None

    class Config:
        populate_by_name = True


class SMSList(BaseModel):
    """Paginated list of SMS messages"""
    data: List[SMS]
    total: int
    limit: int
    offset: int
    has_more: bool


class TTSParams(BaseModel):
    """Text-to-speech parameters"""
    text: str
    voice: Optional[str] = None
    speed: Optional[float] = 1.0


class CreateCallParams(BaseModel):
    """Parameters for creating a voice call"""
    from_number: str = Field(..., alias="from")
    to: str
    tts: Optional[TTSParams] = None
    audio_url: Optional[str] = None
    record: Optional[bool] = False
    max_duration: Optional[int] = None
    webhook_url: Optional[str] = None

    class Config:
        populate_by_name = True


class CreateCallResponse(BaseModel):
    """Response from creating a call"""
    id: str
    status: Literal["queued", "ringing", "in-progress", "completed", "failed"]
    created_at: datetime


class Call(BaseModel):
    """Call object"""
    id: str
    from_number: str = Field(..., alias="from")
    to: str
    status: Literal["queued", "ringing", "in-progress",
                    "completed", "failed", "no-answer", "busy"]
    duration: Optional[int] = None
    recording_url: Optional[str] = None
    created_at: datetime
    answered_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

    class Config:
        populate_by_name = True


class CallList(BaseModel):
    """Paginated list of calls"""
    data: List[Call]
    total: int
    limit: int
    offset: int
    has_more: bool
