#!/usr/bin/env python3
"""
pywarpcli.exceptions
--------------------

This module contains the set of pywarpcli's custom exceptions.
"""


class WarpCLIError(Exception):
    """Base exception class for all pywarpcli errors."""

    pass


class CommandFailedError(WarpCLIError):
    """
    Raised when a `warp-cli` subprocess command returns a non-zero exit code,
    indicating a failure.
    """

    def __init__(self, command: list[str], return_code: int, stdout: str, stderr: str):
        """
        Initializes the exception with detailed information from the failed command.

        Args:
            command: The command that was executed as a list of strings.
            return_code: The exit code of the process.
            stdout: The standard output from the process.
            stderr: The standard error from the process.
        """
        self.command = command
        self.return_code = return_code
        self.stdout = stdout.strip()
        self.stderr = stderr.strip()

        # Create a detailed, multi-line error message
        message = (
            f"Command `{' '.join(command)}` failed with exit code {return_code}.\n"
            f"--- STDERR ---\n{self.stderr or '[No stderr output]'}\n"
            f"--- STDOUT ---\n{self.stdout or '[No stdout output]'}"
        )
        super().__init__(message)
