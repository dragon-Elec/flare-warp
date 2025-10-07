#!/usr/bin/env python3
"""
A simple command-line script to test the functionality of the pywarpcli library.
This script is for development and verification purposes only.
"""

import sys
from pywarpcli.client import WarpClient
from pywarpcli.exceptions import WarpCLIError


def main():
    """Main function to run the library tests."""
    print("🚀 Starting pywarpcli library test...")

    try:
        # Initialize the client. This will use 'warp-cli' from your system's PATH.
        client = WarpClient()
    except Exception as e:
        print(f"❌ CRITICAL: Failed to initialize WarpClient: {e}")
        sys.exit(1)

    # --- [TEST 1] get_status() ---
    print("\n" + "=" * 30)
    print("   Running: client.get_status()")
    print("=" * 30)
    try:
        # Access attributes by name, which is clearer and more robust.
        result = client.get_status()

        print("✅ SUCCESS!")
        print(f"   Parsed Model : {result.model}")
        print(f"   Model Status : '{result.model.status}'")
        print("-" * 20)
        print("   Raw JSON Output:")
        print(result.raw_output)

    except WarpCLIError as e:
        print(f"❌ FAILED: A library error occurred.")
        print(e)
    except Exception as e:
        print(f"❌ FAILED: An unexpected error occurred: {e}")

    # --- [TEST 2] get_stats() ---
    print("\n" + "=" * 30)
    print("   Running: client.get_stats()")
    print("=" * 30)
    try:
        # Access attributes by name here as well.
        result = client.get_stats()

        print("✅ SUCCESS!")
        print(f"   Parsed Model : {result.model}")
        # Example of accessing data within the model
        bytes_sent = result.model.data.get("bytes_sent", "N/A")
        print(f"   Stat (bytes_sent): {bytes_sent}")
        print("-" * 20)
        print("   Raw JSON Output:")
        print(result.raw_output)

    except WarpCLIError as e:
        print(f"❌ FAILED: A library error occurred.")
        print(e)
    except Exception as e:
        print(f"❌ FAILED: An unexpected error occurred: {e}")

    print("\n🏁 Test script finished.")


if __name__ == "__main__":
    main()
