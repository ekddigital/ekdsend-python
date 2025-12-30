"""
Utility functions for EKDSend SDK
Following DRY principle - centralized helper functions
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, TypeVar, Union
from datetime import datetime


T = TypeVar("T")


def to_list(value: Optional[Union[T, List[T]]]) -> Optional[List[T]]:
    """
    Convert a single value or list to a list.
    Useful for fields that accept both single values and arrays.

    Args:
        value: Single value or list of values

    Returns:
        List of values or None if input is None
    """
    if value is None:
        return None
    return value if isinstance(value, list) else [value]


def build_query_params(params: Dict[str, Any]) -> Dict[str, str]:
    """
    Build query parameters dict, filtering out None values.

    Args:
        params: Dictionary of parameters

    Returns:
        Dictionary with None values removed and all values as strings
    """
    return {
        k: str(v) if not isinstance(v, str) else v
        for k, v in params.items()
        if v is not None
    }


def serialize_datetime(value: Optional[Union[str, datetime]]) -> Optional[str]:
    """
    Convert datetime to ISO format string if needed.

    Args:
        value: String or datetime object

    Returns:
        ISO format string or original string
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def exponential_backoff(
    attempt: int,
    base_delay: float = 1.0,
    max_delay: float = 30.0
) -> float:
    """
    Calculate exponential backoff delay.

    Args:
        attempt: Current attempt number (0-based)
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds

    Returns:
        Delay in seconds with jitter
    """
    import random

    delay = min(base_delay * (2 ** attempt), max_delay)
    # Add jitter (±10%)
    jitter = delay * 0.1 * (random.random() * 2 - 1)
    return delay + jitter
