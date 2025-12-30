"""
Custom exceptions for EKDSend SDK
"""

from typing import Dict, List, Optional


class EKDSendError(Exception):
    """Base error class for all EKDSend errors"""

    def __init__(
        self,
        message: str,
        status_code: int,
        code: str,
        request_id: Optional[str] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.request_id = request_id

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


class ValidationError(EKDSendError):
    """Thrown when request validation fails (400)"""

    def __init__(
        self,
        message: str = "Validation failed",
        errors: Optional[Dict[str, List[str]]] = None,
        request_id: Optional[str] = None,
    ):
        super().__init__(message, 400, "VALIDATION_ERROR", request_id)
        self.errors = errors or {}


class AuthenticationError(EKDSendError):
    """Thrown when authentication fails (401)"""

    def __init__(
        self,
        message: str = "Invalid API key",
        request_id: Optional[str] = None,
    ):
        super().__init__(message, 401, "AUTHENTICATION_ERROR", request_id)


class RateLimitError(EKDSendError):
    """Thrown when rate limit is exceeded (429)"""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: int = 60,
        request_id: Optional[str] = None,
    ):
        super().__init__(message, 429, "RATE_LIMIT_EXCEEDED", request_id)
        self.retry_after = retry_after


class NotFoundError(EKDSendError):
    """Thrown when resource is not found (404)"""

    def __init__(
        self,
        message: str = "Resource not found",
        code: str = "NOT_FOUND",
        request_id: Optional[str] = None,
    ):
        super().__init__(message, 404, code, request_id)
