"""
EKDSend Python SDK
Official SDK for EKDSend API - Email, SMS, and Voice communications
"""

from ekdsend.client import EKDSend, AsyncEKDSend
from ekdsend.resources.emails import EmailsAPI, AsyncEmailsAPI
from ekdsend.resources.sms import SMSAPI, AsyncSMSAPI
from ekdsend.resources.voice import VoiceAPI, AsyncVoiceAPI
from ekdsend.exceptions import (
    EKDSendError,
    ValidationError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
)
from ekdsend.types import (
    SendEmailParams,
    SendEmailResponse,
    Email,
    EmailList,
    SendSMSParams,
    SendSMSResponse,
    SMS,
    SMSList,
    CreateCallParams,
    CreateCallResponse,
    Call,
    CallList,
    TTSParams,
    Attachment,
)

__version__ = "1.1.0"
__all__ = [
    # Clients
    "EKDSend",
    "AsyncEKDSend",
    # Resources
    "EmailsAPI",
    "AsyncEmailsAPI",
    "SMSAPI",
    "AsyncSMSAPI",
    "VoiceAPI",
    "AsyncVoiceAPI",
    # Exceptions
    "EKDSendError",
    "ValidationError",
    "AuthenticationError",
    "RateLimitError",
    "NotFoundError",
    # Types
    "SendEmailParams",
    "SendEmailResponse",
    "Email",
    "EmailList",
    "SendSMSParams",
    "SendSMSResponse",
    "SMS",
    "SMSList",
    "CreateCallParams",
    "CreateCallResponse",
    "Call",
    "CallList",
    "TTSParams",
    "Attachment",
]
