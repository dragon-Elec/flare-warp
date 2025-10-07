#!/usr/bin/env python3
"""
pywarpcli.controllers.dns
-------------------------

This module contains the DnsController class for managing `warp-cli dns` subcommands.
"""

import json
from typing import Any, cast

from .base import BaseController
from ..exceptions import WarpCLIError
from ..types import DualOutput


class DnsController(BaseController):
    """
    Manages the 'dns' subcommand group of `warp-cli`.
    """

    def get_stats(self) -> DualOutput[dict[str, Any]]:
        """
        Retrieves DNS stats for the current connection.

        Corresponds to `warp-cli dns stats`.

        Returns:
            A DualOutput object where the model is a dictionary containing the DNS stats.

        Raises:
            WarpCLIError: If the command output cannot be parsed as JSON.
        """
        # We use the client's internal _run_command method
        raw_output = self._client._run_command(["dns", "stats"])
        try:
            # For now, we'll use a generic dictionary as the model for DNS stats.
            # We can create a dedicated dataclass later if needed.
            model = cast(dict[str, Any], json.loads(raw_output))
            return DualOutput(model=model, raw_output=raw_output)
        except json.JSONDecodeError:
            raise WarpCLIError(
                f"Failed to parse JSON from 'dns stats' command. Raw output: {raw_output}"
            )
