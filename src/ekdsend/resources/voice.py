"""
EKDSend Voice API Resource
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from ekdsend.types import VoiceCall, PaginatedResponse


if TYPE_CHECKING:
    from ekdsend.client import EKDSend, AsyncEKDSend


class VoiceAPI:
    """Synchronous Voice API"""

    def __init__(self, client: "EKDSend"):
        self._client = client

    def create(
        self,
        *,
        to: str,
        from_number: str,
        tts_message: Optional[str] = None,
        audio_url: Optional[str] = None,
        voice: str = "alloy",
        language: str = "en-US",
        record: bool = False,
        machine_detection: bool = False,
        webhook_url: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> VoiceCall:
        """
        Create a voice call.

        Args:
            to: Recipient phone number (E.164 format: +1234567890)
            from_number: Caller ID phone number (must be verified)
            tts_message: Text-to-speech message content
            audio_url: URL to audio file for playback (alternative to TTS)
            voice: TTS voice (alloy, echo, fable, onyx, nova, shimmer)
            language: TTS language code (default: en-US)
            record: Enable call recording
            machine_detection: Enable answering machine detection
            webhook_url: URL for call status callbacks
            metadata: Custom key-value metadata

        Returns:
            VoiceCall object with id and status
        """
        if not tts_message and not audio_url:
            raise ValueError("Either tts_message or audio_url is required")

        payload: Dict[str, Any] = {
            "to": to,
            "from": from_number,
            "voice": voice,
            "language": language,
            "record": record,
            "machine_detection": machine_detection,
        }

        if tts_message:
            payload["tts_message"] = tts_message
        if audio_url:
            payload["audio_url"] = audio_url
        if webhook_url:
            payload["webhook_url"] = webhook_url
        if metadata:
            payload["metadata"] = metadata

        response = self._client.request("POST", "/calls", json=payload)
        return VoiceCall(**response["data"])

    def get(self, call_id: str) -> VoiceCall:
        """
        Get a call by ID.

        Args:
            call_id: The call ID to retrieve

        Returns:
            VoiceCall object
        """
        response = self._client.request("GET", f"/calls/{call_id}")
        return VoiceCall(**response["data"])

    def list(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> PaginatedResponse[VoiceCall]:
        """
        List calls with pagination and filtering.

        Args:
            limit: Number of calls to return (max 100)
            offset: Pagination offset
            status: Filter by status (queued, ringing, in-progress, completed, failed)
            from_date: Filter from date (ISO8601)
            to_date: Filter to date (ISO8601)

        Returns:
            Paginated list of calls
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

        response = self._client.request("GET", "/calls", params=params)
        return PaginatedResponse(
            data=[VoiceCall(**item) for item in response["data"]],
            total=response["total"],
            limit=response["limit"],
            offset=response["offset"],
        )

    def hangup(self, call_id: str) -> VoiceCall:
        """
        Hang up an active call.

        Args:
            call_id: The call ID to hang up

        Returns:
            Updated VoiceCall object
        """
        response = self._client.request("DELETE", f"/calls/{call_id}")
        return VoiceCall(**response["data"])

    def get_recording(self, call_id: str) -> Dict[str, Any]:
        """
        Get recording for a call.

        Args:
            call_id: The call ID

        Returns:
            Recording object with URL and metadata
        """
        response = self._client.request("GET", f"/calls/{call_id}/recording")
        return response["data"]


class AsyncVoiceAPI:
    """Asynchronous Voice API"""

    def __init__(self, client: "AsyncEKDSend"):
        self._client = client

    async def create(
        self,
        *,
        to: str,
        from_number: str,
        tts_message: Optional[str] = None,
        audio_url: Optional[str] = None,
        voice: str = "alloy",
        language: str = "en-US",
        record: bool = False,
        machine_detection: bool = False,
        webhook_url: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> VoiceCall:
        """
        Create a voice call asynchronously.

        Args:
            to: Recipient phone number (E.164 format)
            from_number: Caller ID phone number
            tts_message: Text-to-speech message
            audio_url: URL to audio file
            voice: TTS voice
            language: TTS language code
            record: Enable call recording
            machine_detection: Enable machine detection
            webhook_url: URL for callbacks
            metadata: Custom metadata

        Returns:
            VoiceCall object with id and status
        """
        if not tts_message and not audio_url:
            raise ValueError("Either tts_message or audio_url is required")

        payload: Dict[str, Any] = {
            "to": to,
            "from": from_number,
            "voice": voice,
            "language": language,
            "record": record,
            "machine_detection": machine_detection,
        }

        if tts_message:
            payload["tts_message"] = tts_message
        if audio_url:
            payload["audio_url"] = audio_url
        if webhook_url:
            payload["webhook_url"] = webhook_url
        if metadata:
            payload["metadata"] = metadata

        response = await self._client.request("POST", "/calls", json=payload)
        return VoiceCall(**response["data"])

    async def get(self, call_id: str) -> VoiceCall:
        """Get a call by ID asynchronously."""
        response = await self._client.request("GET", f"/calls/{call_id}")
        return VoiceCall(**response["data"])

    async def list(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> PaginatedResponse[VoiceCall]:
        """List calls asynchronously."""
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

        response = await self._client.request("GET", "/calls", params=params)
        return PaginatedResponse(
            data=[VoiceCall(**item) for item in response["data"]],
            total=response["total"],
            limit=response["limit"],
            offset=response["offset"],
        )

    async def hangup(self, call_id: str) -> VoiceCall:
        """Hang up an active call asynchronously."""
        response = await self._client.request("DELETE", f"/calls/{call_id}")
        return VoiceCall(**response["data"])

    async def get_recording(self, call_id: str) -> Dict[str, Any]:
        """Get recording for a call asynchronously."""
        response = await self._client.request("GET", f"/calls/{call_id}/recording")
        return response["data"]
