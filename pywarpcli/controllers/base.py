#!/usr/bin/env python3
"""
pywarpcli.controllers.base
--------------------------

This module contains the BaseController class that all other controllers inherit from.
"""

# By importing 'WarpClient' this way, we avoid circular import errors
# and allow our type checker to understand the code.
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pywarpcli.client import WarpClient


class BaseController:
    """
    A base class for all command group controllers.

    It holds a reference to the main client instance to access its core
    functionality, like the _run_command method.
    """

    def __init__(self, client: WarpClient):
        self._client = client
