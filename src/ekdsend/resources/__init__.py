"""
EKDSend API Resources
"""

from ekdsend.resources.emails import EmailsAPI, AsyncEmailsAPI
from ekdsend.resources.sms import SMSAPI, AsyncSMSAPI
from ekdsend.resources.voice import VoiceAPI, AsyncVoiceAPI

__all__ = [
    "EmailsAPI",
    "AsyncEmailsAPI",
    "SMSAPI",
    "AsyncSMSAPI",
    "VoiceAPI",
    "AsyncVoiceAPI",
]
