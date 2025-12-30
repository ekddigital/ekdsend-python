"""
EKDSend Email API Resource
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union

from ekdsend.types import Email, SendEmailRequest, PaginatedResponse


if TYPE_CHECKING:
    from ekdsend.client import EKDSend, AsyncEKDSend


class EmailsAPI:
    """Synchronous Email API"""

    def __init__(self, client: "EKDSend"):
        self._client = client

    def send(
        self,
        *,
        from_email: str,
        to: Union[str, List[str]],
        subject: str,
        html: Optional[str] = None,
        text: Optional[str] = None,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        reply_to: Optional[str] = None,
        attachments: Optional[List[Dict[str, str]]] = None,
        headers: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, str]] = None,
        scheduled_at: Optional[str] = None,
    ) -> Email:
        """
        Send an email.

        Args:
            from_email: Sender email address (must be verified)
            to: Recipient email(s)
            subject: Email subject line
            html: HTML content
            text: Plain text content (auto-generated from HTML if not provided)
            cc: CC recipient(s)
            bcc: BCC recipient(s)
            reply_to: Reply-to address
            attachments: List of attachments with 'filename' and 'content' (base64)
            headers: Custom email headers
            tags: Tags for categorization
            metadata: Custom key-value metadata
            scheduled_at: ISO8601 timestamp for scheduling

        Returns:
            Email object with id and status
        """
        # Normalize recipients to lists
        if isinstance(to, str):
            to = [to]
        if isinstance(cc, str):
            cc = [cc]
        if isinstance(bcc, str):
            bcc = [bcc]

        payload: Dict[str, Any] = {
            "from": from_email,
            "to": to,
            "subject": subject,
        }

        if html:
            payload["html"] = html
        if text:
            payload["text"] = text
        if cc:
            payload["cc"] = cc
        if bcc:
            payload["bcc"] = bcc
        if reply_to:
            payload["reply_to"] = reply_to
        if attachments:
            payload["attachments"] = attachments
        if headers:
            payload["headers"] = headers
        if tags:
            payload["tags"] = tags
        if metadata:
            payload["metadata"] = metadata
        if scheduled_at:
            payload["scheduled_at"] = scheduled_at

        response = self._client.request("POST", "/emails", json=payload)
        return Email(**response["data"])

    def get(self, email_id: str) -> Email:
        """
        Get an email by ID.

        Args:
            email_id: The email ID to retrieve

        Returns:
            Email object
        """
        response = self._client.request("GET", f"/emails/{email_id}")
        return Email(**response["data"])

    def list(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> PaginatedResponse[Email]:
        """
        List emails with pagination and filtering.

        Args:
            limit: Number of emails to return (max 100)
            offset: Pagination offset
            status: Filter by status (sent, delivered, bounced, etc.)
            from_date: Filter from date (ISO8601)
            to_date: Filter to date (ISO8601)
            tags: Filter by tags

        Returns:
            Paginated list of emails
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
        if tags:
            params["tags"] = ",".join(tags)

        response = self._client.request("GET", "/emails", params=params)
        return PaginatedResponse(
            data=[Email(**item) for item in response["data"]],
            total=response["total"],
            limit=response["limit"],
            offset=response["offset"],
        )

    def cancel(self, email_id: str) -> Email:
        """
        Cancel a scheduled email.

        Args:
            email_id: The email ID to cancel

        Returns:
            Updated email object
        """
        response = self._client.request("DELETE", f"/emails/{email_id}")
        return Email(**response["data"])


class AsyncEmailsAPI:
    """Asynchronous Email API"""

    def __init__(self, client: "AsyncEKDSend"):
        self._client = client

    async def send(
        self,
        *,
        from_email: str,
        to: Union[str, List[str]],
        subject: str,
        html: Optional[str] = None,
        text: Optional[str] = None,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        reply_to: Optional[str] = None,
        attachments: Optional[List[Dict[str, str]]] = None,
        headers: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, str]] = None,
        scheduled_at: Optional[str] = None,
    ) -> Email:
        """
        Send an email asynchronously.

        Args:
            from_email: Sender email address (must be verified)
            to: Recipient email(s)
            subject: Email subject line
            html: HTML content
            text: Plain text content
            cc: CC recipient(s)
            bcc: BCC recipient(s)
            reply_to: Reply-to address
            attachments: List of attachments
            headers: Custom email headers
            tags: Tags for categorization
            metadata: Custom metadata
            scheduled_at: ISO8601 timestamp for scheduling

        Returns:
            Email object with id and status
        """
        if isinstance(to, str):
            to = [to]
        if isinstance(cc, str):
            cc = [cc]
        if isinstance(bcc, str):
            bcc = [bcc]

        payload: Dict[str, Any] = {
            "from": from_email,
            "to": to,
            "subject": subject,
        }

        if html:
            payload["html"] = html
        if text:
            payload["text"] = text
        if cc:
            payload["cc"] = cc
        if bcc:
            payload["bcc"] = bcc
        if reply_to:
            payload["reply_to"] = reply_to
        if attachments:
            payload["attachments"] = attachments
        if headers:
            payload["headers"] = headers
        if tags:
            payload["tags"] = tags
        if metadata:
            payload["metadata"] = metadata
        if scheduled_at:
            payload["scheduled_at"] = scheduled_at

        response = await self._client.request("POST", "/emails", json=payload)
        return Email(**response["data"])

    async def get(self, email_id: str) -> Email:
        """Get an email by ID asynchronously."""
        response = await self._client.request("GET", f"/emails/{email_id}")
        return Email(**response["data"])

    async def list(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> PaginatedResponse[Email]:
        """List emails with pagination and filtering asynchronously."""
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
        if tags:
            params["tags"] = ",".join(tags)

        response = await self._client.request("GET", "/emails", params=params)
        return PaginatedResponse(
            data=[Email(**item) for item in response["data"]],
            total=response["total"],
            limit=response["limit"],
            offset=response["offset"],
        )

    async def cancel(self, email_id: str) -> Email:
        """Cancel a scheduled email asynchronously."""
        response = await self._client.request("DELETE", f"/emails/{email_id}")
        return Email(**response["data"])
