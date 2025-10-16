#!/usr/bin/env python3
"""
pywarpcli.types
---------------

This module defines common, reusable type definitions for the library's API.
"""

from dataclasses import dataclass
from typing import TypeVar, Generic

# A TypeVar allows us to create a generic container. This means DualOutput
# can hold a WarpStatus, a WarpStats, or any other model we create in the future.
ModelType = TypeVar("ModelType")


@dataclass
class DualOutput(Generic[ModelType]):
    """
    A generic container holding both a structured data model and the raw
    string output from a command.

    Attributes:
        model: The parsed, structured data object (e.g., WarpStatus).
        raw_output: The original, unmodified stdout string from the command.
    """

    model: ModelType
    raw_output: str
