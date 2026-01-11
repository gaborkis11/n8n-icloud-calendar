#!/usr/bin/env python3
"""
iCloud CalDAV CALENDAR_ID Discovery Script
Step 2: List all your calendars and their IDs

Usage: python3 2_get_calendar_id.py
"""

import requests
from requests.auth import HTTPBasicAuth
import re

# ============================================
# CONFIGURATION - REPLACE WITH YOUR VALUES!
# ============================================
EMAIL = "YOUR_APPLE_ID@email.com"           # Your Apple ID email
PASSWORD = "xxxx-xxxx-xxxx-xxxx"            # App-specific password
USER_ID = "YOUR_USER_ID"                    # From step 1 (1_get_user_id.py)
# ============================================


def get_calendars():
    print("iCloud CalDAV - Calendar Discovery")
    print("=" * 60)
    print(f"USER_ID: {USER_ID}")
    print("-" * 60)

    if "YOUR_" in EMAIL or "xxxx" in PASSWORD or "YOUR_" in USER_ID:
        print("\n" + "=" * 60)
        print("ERROR: Please configure your credentials first!")
        print("=" * 60)
        print("\nEdit this file and replace:")
        print("  - EMAIL: Your Apple ID email address")
        print("  - PASSWORD: Your app-specific password")
        print("  - USER_ID: The value from step 1")
        return

    try:
        response = requests.request(
            "PROPFIND",
            f"https://caldav.icloud.com/{USER_ID}/calendars/",
            auth=HTTPBasicAuth(EMAIL, PASSWORD),
            headers={"Depth": "1"}
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 207:
            print("\n" + "=" * 60)
            print("SUCCESS! Retrieved calendar list")
            print("=" * 60)

            # Parse calendars from response
            calendars = []
            responses = re.findall(r'<response[^>]*>(.*?)</response>', response.text, re.DOTALL)

            for resp in responses:
                href_match = re.search(r'<href>([^<]+)</href>', resp)
                name_match = re.search(r'<displayname>([^<]*)</displayname>', resp, re.IGNORECASE)
                color_match = re.search(r'<calendar-color[^>]*>([^<]*)</calendar-color>', resp, re.IGNORECASE)

                if href_match:
                    href = href_match.group(1)
                    # Only actual calendars (with UUID)
                    if '/calendars/' in href and href.count('/') >= 4:
                        calendar_id = href.split('/calendars/')[-1].rstrip('/')
                        # Skip system folders
                        if calendar_id and calendar_id not in ['inbox', 'outbox', 'notification', 'tasks']:
                            name = name_match.group(1) if name_match else "Unnamed"
                            color = color_match.group(1) if color_match else ""
                            calendars.append({
                                'name': name,
                                'id': calendar_id,
                                'color': color
                            })

            if calendars:
                print(f"\nFound {len(calendars)} calendar(s):\n")
                print("=" * 60)
                for i, cal in enumerate(calendars, 1):
                    print(f"\n{i}. {cal['name']}")
                    print(f"   CALENDAR_ID: {cal['id']}")
                    if cal['color']:
                        print(f"   Color: {cal['color']}")
                print("\n" + "=" * 60)
                print("\nCopy the CALENDAR_ID of the calendar you want to use.")
                print("You'll need it for the n8n workflow configuration.")
                print("\nTIP: Test with 3_test_read_events.py first!")
            else:
                print("\nNo calendars found automatically.")
                print("\n--- RAW RESPONSE (for manual parsing) ---")
                print(response.text)

        elif response.status_code == 401:
            print("\nERROR: Authentication failed (401)")
            print("Check your EMAIL and PASSWORD.")

        elif response.status_code == 403:
            print("\nERROR: Access denied (403)")
            print("Your app-specific password may have expired.")

        elif response.status_code == 404:
            print("\nERROR: Not found (404)")
            print("The USER_ID is probably incorrect.")
            print(f"Current USER_ID: {USER_ID}")
            print("\nRe-run 1_get_user_id.py to get the correct value.")

        else:
            print(f"\nUnexpected error: {response.status_code}")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("\nConnection error! Check your internet connection.")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    get_calendars()
