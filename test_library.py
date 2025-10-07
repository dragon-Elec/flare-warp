#!/usr/bin/env python3
"""
A simple command-line script to test the functionality of the pywarpcli library.
This script is for development and verification purposes only.
"""

import sys
import time
from pywarpcli.client import WarpClient
from pywarpcli.exceptions import WarpCLIError

def run_test(name, func):
    """Helper function to run a test and print the outcome."""
    print("\n" + "="*30)
    print(f"   Running: {name}")
    print("="*30)
    try:
        result = func()
        print("✅ SUCCESS!")
        print(f"   Model      : {result.model}")
        print(f"   Raw Output : {result.raw_output}")
    except WarpCLIError as e:
        print(f"❌ FAILED: A library error occurred.")
        print(e)
    except Exception as e:
        print(f"❌ FAILED: An unexpected error occurred: {e}")

def main():
    """Main function to run the library tests."""
    print("🚀 Starting pywarpcli library test...")
    
    try:
        client = WarpClient()
    except Exception as e:
        print(f"❌ CRITICAL: Failed to initialize WarpClient: {e}")
        sys.exit(1)

    # --- Run Standard Tests ---
    run_test("client.get_status()", client.get_status)
    run_test("client.get_stats()", client.get_stats)

    # --- Interactive Connect/Disconnect Test ---
    print("\n" + "#"*40)
    print("   INTERACTIVE TEST: Connect/Disconnect")
    print("#"*40)
    
    # Step 1: Disconnect
    input("Press Enter to attempt to DISCONNECT warp...")
    run_test("client.disconnect()", client.disconnect)
    
    # Step 2: Check status after disconnect
    print("\nChecking status after 2 seconds...")
    time.sleep(2)
    run_test("client.get_status()", client.get_status)
    
    # Step 3: Connect
    input("\nPress Enter to attempt to CONNECT warp...")
    run_test("client.connect()", client.connect)

    # Step 4: Check status after connect
    print("\nChecking status after 2 seconds...")
    time.sleep(2)
    run_test("client.get_status()", client.get_status)

    print("\n🏁 Test script finished.")


if __name__ == "__main__":
    main()