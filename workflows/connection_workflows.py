#!/usr/bin/env python3
"""
pywarpcli.workflows.connection_workflows
----------------------------------------

This module contains high-level, multi-step workflows related to connection management.
"""

import time
from typing import Optional

from pywarpcli.client import WarpClient
from pywarpcli.exceptions import WarpCLIError


def connect_until_status(
    client: WarpClient, target_status: str = "Connected", timeout: float = 10.0, interval: float = 0.5
) -> bool:
    """
    Attempts to connect and waits until the status reaches the target status.

    Args:
        client: The WarpClient instance.
        target_status: The status string to wait for (default: "Connected").
        timeout: Maximum time to wait in seconds.
        interval: Time to wait between status checks in seconds.

    Returns:
        True if the target status was reached, False if the timeout was exceeded.
    """
    try:
        # Initiate connection
        client.connect()
    except WarpCLIError:
        # If connect fails (e.g. already connected), we still proceed to check status
        pass

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            status = client.get_status().model.status
            if status == target_status:
                return True
        except WarpCLIError:
            pass
        
        time.sleep(interval)

    return False


def disconnect_until_status(
    client: WarpClient, target_status: str = "Disconnected", timeout: float = 10.0, interval: float = 0.5
) -> bool:
    """
    Attempts to disconnect and waits until the status reaches the target status.

    Args:
        client: The WarpClient instance.
        target_status: The status string to wait for (default: "Disconnected").
        timeout: Maximum time to wait in seconds.
        interval: Time to wait between status checks in seconds.

    Returns:
        True if the target status was reached, False if the timeout was exceeded.
    """
    try:
        # Initiate disconnection
        client.disconnect()
    except WarpCLIError:
        pass

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            status = client.get_status().model.status
            if status == target_status:
                return True
        except WarpCLIError:
            pass
        
        time.sleep(interval)

    return False
