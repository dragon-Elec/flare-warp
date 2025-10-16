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
from ..models import DnsStats


class DnsController(BaseController):
    """
    Manages the 'dns' subcommand group of `warp-cli`.
    """

    def get_stats(self) -> DualOutput[DnsStats]: # <-- UPDATE THE RETURN TYPE
        """
        Retrieves DNS stats for the current connection.
        ...
        """
        raw_output = self._client._run_command(["dns", "stats"])
        try:
            json_data = cast(dict[str, Any], json.loads(raw_output))
            # Create an instance of our specific DnsStats model
            model = DnsStats(
                dns_proxy_enabled=json_data.get("dns_proxy_enabled", False),
                avg_duration_millis=json_data.get("avg_duration_millis", 0.0),
                timed_out=json_data.get("timed_out", 0),
                no_records_found=json_data.get("no_records_found", 0),
                other_error=json_data.get("other_error", 0),
                success=json_data.get("success", 0),
                total=json_data.get("total", 0),
                raw_data=json_data
            )
            return DualOutput(model=model, raw_output=raw_output)
        except json.JSONDecodeError:
            raise WarpCLIError(
                f"Failed to parse JSON from 'dns stats' command. Raw output: {raw_output}"
            )