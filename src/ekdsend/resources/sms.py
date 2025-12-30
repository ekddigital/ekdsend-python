"""
EKDSend SMS API Resource
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from ekdsend.types import SMS, PaginatedResponse


if TYPE_CHECKING:
    from ekdsend.client import EKDSend, AsyncEKDSend


class SMSAPI:
    """Synchronous SMS API"""

    def __init__(self, client: "EKDSend"):
        self._client = client

    def send(
        self,
        *,
        to: str,
        message: str,
        from_number: Optional[str] = None,
        scheduled_at: Optional[str] = None,
        webhook_url: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> SMS:
        """
        Send an SMS message.

        Args:
            to: Recipient phone number (E.164 format: +1234567890)
            message: SMS message content (max 1600 chars for concatenated)
            from_number: Sender phone number (optional, uses default if not set)
            scheduled_at: ISO8601 timestamp for scheduling
            webhook_url: URL for delivery status callbacks
            metadata: Custom key-value metadata

        Returns:
            SMS object with id and status
        """
        payload: Dict[str, Any] = {
            "to": to,
            "message": message,
        }

        if from_number:
            payload["from"] = from_number
        if scheduled_at:
            payload["scheduled_at"] = scheduled_at
        if webhook_url:
            payload["webhook_url"] = webhook_url
        if metadata:
            payload["metadata"] = metadata

        response = self._client.request("POST", "/sms", json=payload)
        return SMS(**response["data"])

    def get(self, sms_id: str) -> SMS:
        """
        Get an SMS by ID.

        Args:
            sms_id: The SMS ID to retrieve

        Returns:
            SMS object
        """
        response = self._client.request("GET", f"/sms/{sms_id}")
        return SMS(**response["data"])

    def list(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> PaginatedResponse[SMS]:
        """
        List SMS messages with pagination and filtering.

        Args:
            limit: Number of messages to return (max 100)
            offset: Pagination offset
            status: Filter by status (sent, delivered, failed)
            from_date: Filter from date (ISO8601)
            to_date: Filter to date (ISO8601)

        Returns:
            Paginated list of SMS messages
        """
        params: Dict[str, Any] = {
            "limit": limit,
            "offset": offset,
        }

        if status:
            params["status"] = status
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date

        response = self._client.request("GET", "/sms", params=params)
        return PaginatedResponse(
            data=[SMS(**item) for item in response["data"]],
            total=response["total"],
            limit=response["limit"],
            offset=response["offset"],
        )

    def cancel(self, sms_id: str) -> SMS:
        """
        Cancel a scheduled SMS.

        Args:
            sms_id: The SMS ID to cancel

        Returns:
            Updated SMS object
        """
        response = self._client.request("DELETE", f"/sms/{sms_id}")
        return SMS(**response["data"])


class AsyncSMSAPI:
    """Asynchronous SMS API"""

    def __init__(self, client: "AsyncEKDSend"):
        self._client = client

    async def send(
        self,
        *,
        to: str,
        message: str,
        from_number: Optional[str] = None,
        scheduled_at: Optional[str] = None,
        webhook_url: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> SMS:
        """
        Send an SMS message asynchronously.

        Args:
            to: Recipient phone number (E.164 format)
            message: SMS message content
            from_number: Sender phone number
            scheduled_at: ISO8601 timestamp for scheduling
            webhook_url: URL for delivery callbacks
            metadata: Custom metadata

        Returns:
            SMS object with id and status
        """
        payload: Dict[str, Any] = {
            "to": to,
            "message": message,
        }

        if from_number:
            payload["from"] = from_number
        if scheduled_at:
            payload["scheduled_at"] = scheduled_at
        if webhook_url:
            payload["webhook_url"] = webhook_url
        if metadata:
            payload["metadata"] = metadata

        response = await self._client.request("POST", "/sms", json=payload)
        return SMS(**response["data"])

    async def get(self, sms_id: str) -> SMS:
        """Get an SMS by ID asynchronously."""
        response = await self._client.request("GET", f"/sms/{sms_id}")
        return SMS(**response["data"])

    async def list(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> PaginatedResponse[SMS]:
        """List SMS messages asynchronously."""
        params: Dict[str, Any] = {
            "limit": limit,
            "offset": offset,
        }

        if status:
            params["status"] = status
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date

        response = await self._client.request("GET", "/sms", params=params)
        return PaginatedResponse(
            data=[SMS(**item) for item in response["data"]],
            total=response["total"],
            limit=response["limit"],
            offset=response["offset"],
        )

    async def cancel(self, sms_id: str) -> SMS:
        """Cancel a scheduled SMS asynchronously."""
        response = await self._client.request("DELETE", f"/sms/{sms_id}")
        return SMS(**response["data"])
