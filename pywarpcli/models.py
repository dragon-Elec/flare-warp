#!/usr/bin/env python3
"""
pywarpcli.models
----------------

This module defines the data structures used to represent the output of
warp-cli commands in a structured, predictable way.
"""

from dataclasses import dataclass, field
from typing import Any, Optional

# A 'dataclass' is a class designed to be a clean container for data.
# It automatically handles basic methods for you, making the code concise.


@dataclass
class WarpStatus:
    """
    Represents the structured data from a `warp-cli status` command.
    """

    status: str
    reason: Optional[str] = None
    # We also store the full, raw JSON response. This is useful for debugging
    # and for accessing new fields if warp-cli adds them in the future,
    # without needing to update our model immediately.
    raw_data: dict[str, Any] = field(repr=False, default_factory=dict)


@dataclass
class WarpStats:
    """
    Represents the structured data from a `warp-cli stats` command.
    """

    # For stats, the most flexible approach is to store the entire
    # data dictionary. This allows the application to access any
    # statistic provided by warp-cli without us needing to pre-define
    # every single field (e.g., 'bytes_sent', 'bytes_received', etc.).
    data: dict[str, Any]


# As we add more features, we will add more models here. For example:
#
# @dataclass
# class RegistrationInfo:
#     device_id: str
#     account_type: str
#     ...
