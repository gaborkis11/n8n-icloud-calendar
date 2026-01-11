#!/usr/bin/env python3
"""
iCloud CalDAV USER_ID Discovery Script
Step 1: Get your USER_ID from iCloud CalDAV

Usage: python3 1_get_user_id.py
"""

import requests
from requests.auth import HTTPBasicAuth

# ============================================
# CONFIGURATION - REPLACE WITH YOUR VALUES!
# ============================================
EMAIL = "YOUR_APPLE_ID@email.com"           # Your Apple ID email
PASSWORD = "xxxx-xxxx-xxxx-xxxx"            # App-specific password (NOT your Apple ID password!)
# ============================================


def get_user_id():
    print("iCloud CalDAV - USER_ID Discovery")
    print("=" * 50)
    print(f"Email: {EMAIL}")
    print("-" * 50)

    if "YOUR_APPLE_ID" in EMAIL or "xxxx" in PASSWORD:
        print("\n" + "=" * 50)
        print("ERROR: Please configure your credentials first!")
        print("=" * 50)
        print("\nEdit this file and replace:")
        print("  - EMAIL: Your Apple ID email address")
        print("  - PASSWORD: Your app-specific password")
        print("\nSee docs/setup-app-password.md for instructions.")
        return

    try:
        response = requests.request(
            "PROPFIND",
            "https://caldav.icloud.com/.well-known/caldav",
            auth=HTTPBasicAuth(EMAIL, PASSWORD),
            headers={"Depth": "0"}
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 207:
            print("\n" + "=" * 50)
            print("SUCCESS! Connected to iCloud CalDAV")
            print("=" * 50)

            # Extract USER_ID from response
            import re
            match = re.search(r'/(\d+)/principal/', response.text)
            if match:
                user_id = match.group(1)
                print(f"\n{'='*50}")
                print(f"YOUR USER_ID: {user_id}")
                print(f"{'='*50}")
                print(f"\nCopy this value for the next step!")
                print(f"Use it in: 2_get_calendar_id.py")
            else:
                print("\nUSER_ID not found automatically.")
                print("Look for: <href>/XXXXXXXXXX/principal/</href>")
                print("\n--- RAW RESPONSE ---")
                print(response.text)

        elif response.status_code == 401:
            print("\n" + "=" * 50)
            print("ERROR: Authentication failed (401 Unauthorized)")
            print("=" * 50)
            print("\nPossible causes:")
            print("  - Wrong email address")
            print("  - Wrong app-specific password")
            print("  - Using Apple ID password instead of app-specific password")
            print("\nSolution:")
            print("  Create a new app-specific password at appleid.apple.com")

        elif response.status_code == 403:
            print("\n" + "=" * 50)
            print("ERROR: Access denied (403 Forbidden)")
            print("=" * 50)
            print("\nPossible causes:")
            print("  - App-specific password expired or revoked")
            print("  - Too many failed attempts (rate limited)")
            print("\nSolution:")
            print("  Create a new app-specific password at appleid.apple.com")

        else:
            print(f"\nUnexpected error: {response.status_code}")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("\nConnection error! Check your internet connection.")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    get_user_id()
