#!/usr/bin/env python3
"""
pywarpcli.controllers.registration
----------------------------------

This module contains the RegistrationController for managing `warp-cli registration` subcommands.
"""

import json
from typing import Any, cast, final, Optional 

from .base import BaseController
from ..exceptions import WarpCLIError
from ..types import DualOutput
from ..models import RegistrationInfo, Device


@final
class RegistrationController(BaseController):
    """
    Manages the 'registration' subcommand group of `warp-cli`.
    """

    def show(self) -> DualOutput[RegistrationInfo]:
        """
        Retrieves current registration information.

        Corresponds to `warp-cli registration show`.
        """
        raw_output = self._client._run_command(["registration", "show"])
        try:
            json_data = cast(dict[str, Any], json.loads(raw_output))
            
            # Safely get the nested account type
            account_info = json_data.get("account", {})
            account_type = account_info.get("type", "Unknown")

            model = RegistrationInfo(
                id=json_data.get("id", "Unknown"),
                account_type=account_type,
                raw_data=json_data
            )
            return DualOutput(model=model, raw_output=raw_output)
        except json.JSONDecodeError:
            raise WarpCLIError(f"Failed to parse JSON from 'registration show'. Raw: {raw_output}")

    def get_organization(self) -> DualOutput[str]:
        """
        Gets the name of the current Teams organization.

        Corresponds to `warp-cli registration organization`.
        This command does not return JSON.
        """
        raw_output = self._client._run_command(["registration", "organization"], expect_json=False)
        return DualOutput(model=raw_output, raw_output=raw_output)

    def get_devices(self) -> DualOutput[list[Device]]:
        """
        Retrieves the list of devices associated with the current registration.

        Corresponds to `warp-cli registration devices`.
        """
        raw_output = self._client._run_command(["registration", "devices"])
        try:
            json_list = cast(list[dict[str, Any]], json.loads(raw_output))
            
            model = [
                Device(
                    # Map the 'device_id' JSON key to our model's 'id' field
                    id=item.get("device_id", "Unknown"),
                    model=item.get("model", "Unknown"),
                    name=item.get("name", "Unknown"),
                    active=item.get("active", False),
                    # Safely get 'is_this_device', which might be missing
                    is_this_device=item.get("is_this_device", False),
                    raw_data=item
                )
                for item in json_list
            ]
            return DualOutput(model=model, raw_output=raw_output)
        except json.JSONDecodeError:
            raise WarpCLIError(f"Failed to parse JSON from 'registration devices'. Raw: {raw_output}")