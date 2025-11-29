#!/usr/bin/env python3
"""
pywarpcli.client
----------------

This module contains the main WarpClient class, which is the primary
interface for interacting with the `warp-cli` command-line tool.
"""

from __future__ import annotations
import subprocess
import json
from typing import final, cast, TYPE_CHECKING, Any

from .exceptions import WarpCLIError, CommandFailedError
from .models import WarpStatus, WarpStats
from .types import DualOutput

if TYPE_CHECKING:
    from .controllers.dns import DnsController
    from .controllers.registration import RegistrationController
    from .controllers.mode import ModeController
    from .controllers.settings import SettingsController


# Using @final ensures no other class can inherit from WarpClient.
# This is a good practice for a client class that manages its own state and methods.
@final
class WarpClient:
    """
    A Python client for interacting with the Cloudflare `warp-cli` utility.

    This class provides methods to execute `warp-cli` commands and returns
    the output in both raw and structured (parsed) formats.
    """

    dns: DnsController
    registration: RegistrationController
    mode: ModeController
    settings: SettingsController

    def __init__(self, warp_cli_path: str = "warp-cli"):
        """
        Initializes the WarpClient.

        Args:
            warp_cli_path: The path to the `warp-cli` executable.
                           Defaults to "warp-cli", assuming it's in the system's PATH.
        """
        self.warp_cli_path = warp_cli_path
        # Defer controller import to avoid circular dependencies
        from .controllers.dns import DnsController
        from .controllers.registration import RegistrationController
        from .controllers.mode import ModeController
        from .controllers.settings import SettingsController

        self.dns = DnsController(self)
        self.registration = RegistrationController(self)
        self.mode = ModeController(self)
        self.settings = SettingsController(self)

    def _run_command(self, command_parts: list[str], expect_json: bool = True) -> str:
        """
        The core engine for executing `warp-cli` commands.

        Args:
            command_parts: A list of command arguments (e.g., ["status"]).
            expect_json: If True, automatically adds '--json' to the command.

        Returns:
            The raw stdout from the command as a string.

        Raises:
            WarpCLIError: If the executable is not found.
            CommandFailedError: If the command returns a non-zero exit code.
        """
        base_command = [self.warp_cli_path, "--no-paginate", "--no-ansi"]
        if expect_json:
            base_command.append("--json")

        final_command = base_command + command_parts

        try:
            process = subprocess.run(
                final_command,
                capture_output=True,
                text=True,
                check=False,  # We check the return code manually to raise our custom error
            )
        except FileNotFoundError:
            raise WarpCLIError(
                f"Executable not found at '{self.warp_cli_path}'. Is Cloudflare WARP installed and in your PATH?"
            )

        if process.returncode != 0:
            raise CommandFailedError(
                command=final_command,
                return_code=process.returncode,
                stdout=process.stdout,
                stderr=process.stderr,
            )

        return process.stdout.strip()

    # --- Standalone Commands ---
    # According to our blueprint, simple commands are implemented as direct methods.

    def get_status(self) -> DualOutput[WarpStatus]:
        """
        Retrieves the current connection status.

        Corresponds to `warp-cli status`.

        Returns:
            A DualOutput object containing the parsed WarpStatus model and raw output.

        Raises:
            WarpCLIError: If the command output cannot be parsed as JSON.
        """
        raw_output = self._run_command(["status"])
        try:
            # Tell the linter to treat the output of json.loads as a dictionary
            json_data = cast(dict[str, Any], json.loads(raw_output))

            model = WarpStatus(
                status=json_data.get("status", "Unknown"),
                reason=json_data.get("reason"),  # .get() returns None if key is missing
                raw_data=json_data,
            )
            return DualOutput(model=model, raw_output=raw_output)
        except json.JSONDecodeError:
            raise WarpCLIError(
                f"Failed to parse JSON from 'status' command. Raw output: {raw_output}"
            )

    def get_stats(self) -> DualOutput[WarpStats]:
        """
        Retrieves connection statistics.

        Corresponds to `warp-cli stats`.

        Returns:
            A DualOutput object containing the parsed WarpStats model and raw output.

        Raises:
            WarpCLIError: If the command output cannot be parsed as JSON.
        """
        raw_output = self._run_command(["stats"])
        try:
            json_data = json.loads(raw_output)
            model = WarpStats(data=json_data)
            return DualOutput(model=model, raw_output=raw_output)
        except json.JSONDecodeError:
            raise WarpCLIError(
                f"Failed to parse JSON from 'stats' command. Raw output: {raw_output}"
            )

    def connect(self) -> DualOutput[str]:
        """
        Connects the client.

        Corresponds to `warp-cli connect`.
        """
        raw_output = self._run_command(["connect"])
        try:
            json_data = cast(dict[str, Any], json.loads(raw_output))
            status = json_data.get("status", "Unknown")
            return DualOutput(model=status, raw_output=raw_output)
        except json.JSONDecodeError:
            raise WarpCLIError(f"Failed to parse JSON from 'connect'. Raw: {raw_output}")

    def disconnect(self) -> DualOutput[str]:
        """
        Disconnects the client.

        Corresponds to `warp-cli disconnect`.
        """
        raw_output = self._run_command(["disconnect"])
        try:
            json_data = cast(dict[str, Any], json.loads(raw_output))
            status = json_data.get("status", "Unknown")
            return DualOutput(model=status, raw_output=raw_output)
        except json.JSONDecodeError:
            raise WarpCLIError(f"Failed to parse JSON from 'disconnect'. Raw: {raw_output}")
