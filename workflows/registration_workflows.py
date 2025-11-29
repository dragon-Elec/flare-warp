#!/usr/bin/env python3
"""
pywarpcli.workflows.registration_workflows
------------------------------------------

This module contains high-level, multi-step workflows related to registration.
These functions orchestrate calls to the core pywarpcli library to provide
richer, more complete data objects for the application.
"""
"""
pywarpcli.workflows.registration
--------------------------------

This module contains workflows for registration-related tasks.
"""

from pywarpcli.client import WarpClient
from pywarpcli.exceptions import WarpCLIError
from pywarpcli.models import FullRegistrationInfo


def get_full_registration_details(client: WarpClient) -> FullRegistrationInfo:
    """
    Retrieves full registration details, combining information from multiple
    commands.

    This is a workflow that orchestrates calls to the pywarpcli library to
    provide a more complete data object.
    """
    # Get the basic registration info
    reg_info = client.registration.show().model

    # Get the list of devices
    device_name = "Unknown"
    try:
        devices = client.registration.get_devices().model
        for device in devices:
            if device.is_this_device:
                device_name = device.name
                break
    except WarpCLIError:
        # If we can't get the device list, we'll just use "Unknown"
        pass

    # Combine the information into a new model
    return FullRegistrationInfo(
        id=reg_info.id,
        account_type=reg_info.account_type,
        device_name=device_name,
        raw_data=reg_info.raw_data,
    )
