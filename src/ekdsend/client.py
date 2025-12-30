"""
EKDSend Client
Main entry point for the SDK
"""

from __future__ import annotations

import time
from typing import Any, Dict, Optional, Type, TypeVar

import httpx

from ekdsend.exceptions import (
    EKDSendError,
    ValidationError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
)


T = TypeVar("T")

DEFAULT_BASE_URL = "https://es.ekddigital.com/v1"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 3


class EKDSend:
    """
    Synchronous EKDSend client.

    Example:
        >>> client = EKDSend("ek_live_xxxxxxxxxxxxx")
        >>> email = client.emails.send(
        ...     from_email="hello@yourdomain.com",
        ...     to="user@example.com",
        ...     subject="Hello!",
        ...     html="<h1>World</h1>"
        ... )
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        debug: bool = False,
    ):
        if not api_key:
            raise ValueError("API key is required")

        if not api_key.startswith("ek_live_") and not api_key.startswith("ek_test_"):
            raise ValueError(
                "Invalid API key format. Must start with 'ek_live_' or 'ek_test_'"
            )

        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._debug = debug

        self._client = httpx.Client(
            base_url=self._base_url,
            timeout=self._timeout,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
                "User-Agent": "ekdsend-python/1.1.0",
            },
        )

        # Initialize API resources
        from ekdsend.resources.emails import EmailsAPI
        from ekdsend.resources.sms import SMSAPI
        from ekdsend.resources.voice import VoiceAPI

        self.emails = EmailsAPI(self)
        self.sms = SMSAPI(self)
        self.calls = VoiceAPI(self)

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an HTTP request to the API"""
        if self._debug:
            print(f"[EKDSend] {method} {path}")
            if json:
                print(f"[EKDSend] Request body: {json}")

        last_error: Optional[Exception] = None

        for attempt in range(self._max_retries + 1):
            try:
                response = self._client.request(
                    method=method,
                    url=path,
                    json=json,
                    params=params,
                )

                request_id = response.headers.get("x-request-id")

                if not response.is_success:
                    error_data = response.json() if response.content else {}
                    self._handle_error(response.status_code,
                                       error_data, request_id)

                data = response.json()

                if self._debug:
                    print(f"[EKDSend] Response: {data}")

                return data

            except (ValidationError, AuthenticationError):
                raise

            except RateLimitError as e:
                last_error = e
                if attempt < self._max_retries:
                    if self._debug:
                        print(
                            f"[EKDSend] Rate limited. Waiting {e.retry_after}s...")
                    time.sleep(e.retry_after)
                    continue
                raise

            except Exception as e:
                last_error = e
                if attempt < self._max_retries:
                    wait_time = 2**attempt
                    if self._debug:
                        print(
                            f"[EKDSend] Request failed. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                raise

        raise last_error or EKDSendError(
            "Request failed", 500, "UNKNOWN_ERROR")

    def _handle_error(
        self,
        status_code: int,
        error_data: Dict[str, Any],
        request_id: Optional[str],
    ) -> None:
        """Handle error responses"""
        error = error_data.get("error", {})
        message = error.get("message", "API request failed")
        code = error.get("code", "UNKNOWN_ERROR")

        if status_code == 400:
            raise ValidationError(
                message=message,
                errors=error.get("details", {}),
                request_id=request_id,
            )
        elif status_code == 401:
            raise AuthenticationError(message=message, request_id=request_id)
        elif status_code == 404:
            raise NotFoundError(message=message, code=code,
                                request_id=request_id)
        elif status_code == 429:
            raise RateLimitError(
                message=message,
                retry_after=int(error.get("retry_after", 60)),
                request_id=request_id,
            )
        else:
            raise EKDSendError(
                message=message,
                status_code=status_code,
                code=code,
                request_id=request_id,
            )

    def close(self) -> None:
        """Close the HTTP client"""
        self._client.close()

    def __enter__(self) -> "EKDSend":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncEKDSend:
    """
    Asynchronous EKDSend client.

    Example:
        >>> async with AsyncEKDSend("ek_live_xxxxxxxxxxxxx") as client:
        ...     email = await client.emails.send(
        ...         from_email="hello@yourdomain.com",
        ...         to="user@example.com",
        ...         subject="Hello!",
        ...         html="<h1>World</h1>"
        ...     )
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        debug: bool = False,
    ):
        if not api_key:
            raise ValueError("API key is required")

        if not api_key.startswith("ek_live_") and not api_key.startswith("ek_test_"):
            raise ValueError(
                "Invalid API key format. Must start with 'ek_live_' or 'ek_test_'"
            )

        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._debug = debug

        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=self._timeout,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
                "User-Agent": "ekdsend-python/1.1.0",
            },
        )

        # Initialize API resources
        from ekdsend.resources.emails import AsyncEmailsAPI
        from ekdsend.resources.sms import AsyncSMSAPI
        from ekdsend.resources.voice import AsyncVoiceAPI

        self.emails = AsyncEmailsAPI(self)
        self.sms = AsyncSMSAPI(self)
        self.calls = AsyncVoiceAPI(self)

    async def request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an async HTTP request to the API"""
        import asyncio

        if self._debug:
            print(f"[EKDSend] {method} {path}")
            if json:
                print(f"[EKDSend] Request body: {json}")

        last_error: Optional[Exception] = None

        for attempt in range(self._max_retries + 1):
            try:
                response = await self._client.request(
                    method=method,
                    url=path,
                    json=json,
                    params=params,
                )

                request_id = response.headers.get("x-request-id")

                if not response.is_success:
                    error_data = response.json() if response.content else {}
                    self._handle_error(response.status_code,
                                       error_data, request_id)

                data = response.json()

                if self._debug:
                    print(f"[EKDSend] Response: {data}")

                return data

            except (ValidationError, AuthenticationError):
                raise

            except RateLimitError as e:
                last_error = e
                if attempt < self._max_retries:
                    if self._debug:
                        print(
                            f"[EKDSend] Rate limited. Waiting {e.retry_after}s...")
                    await asyncio.sleep(e.retry_after)
                    continue
                raise

            except Exception as e:
                last_error = e
                if attempt < self._max_retries:
                    wait_time = 2**attempt
                    if self._debug:
                        print(
                            f"[EKDSend] Request failed. Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    continue
                raise

        raise last_error or EKDSendError(
            "Request failed", 500, "UNKNOWN_ERROR")

    def _handle_error(
        self,
        status_code: int,
        error_data: Dict[str, Any],
        request_id: Optional[str],
    ) -> None:
        """Handle error responses"""
        error = error_data.get("error", {})
        message = error.get("message", "API request failed")
        code = error.get("code", "UNKNOWN_ERROR")

        if status_code == 400:
            raise ValidationError(
                message=message,
                errors=error.get("details", {}),
                request_id=request_id,
            )
        elif status_code == 401:
            raise AuthenticationError(message=message, request_id=request_id)
        elif status_code == 404:
            raise NotFoundError(message=message, code=code,
                                request_id=request_id)
        elif status_code == 429:
            raise RateLimitError(
                message=message,
                retry_after=int(error.get("retry_after", 60)),
                request_id=request_id,
            )
        else:
            raise EKDSendError(
                message=message,
                status_code=status_code,
                code=code,
                request_id=request_id,
            )

    async def close(self) -> None:
        """Close the HTTP client"""
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncEKDSend":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
