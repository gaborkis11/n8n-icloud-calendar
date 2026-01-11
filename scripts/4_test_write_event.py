#!/usr/bin/env python3
"""
iCloud CalDAV Write Test
Step 4: Test creating events in your calendar

Usage: python3 4_test_write_event.py
"""

import requests
from requests.auth import HTTPBasicAuth
import datetime

# ============================================
# CONFIGURATION - REPLACE WITH YOUR VALUES!
# ============================================
EMAIL = "YOUR_APPLE_ID@email.com"           # Your Apple ID email
PASSWORD = "xxxx-xxxx-xxxx-xxxx"            # App-specific password
USER_ID = "YOUR_USER_ID"                    # From step 1
CALENDAR_ID = "YOUR_CALENDAR_ID"            # From step 2 (must be YOUR calendar, not shared!)
# ============================================


def create_test_event():
    print("iCloud CalDAV - Write Test")
    print("=" * 50)

    if "YOUR_" in EMAIL or "xxxx" in PASSWORD or "YOUR_" in USER_ID or "YOUR_" in CALENDAR_ID:
        print("\n" + "=" * 50)
        print("ERROR: Please configure your credentials first!")
        print("=" * 50)
        print("\nEdit this file and replace:")
        print("  - EMAIL: Your Apple ID email address")
        print("  - PASSWORD: Your app-specific password")
        print("  - USER_ID: From step 1")
        print("  - CALENDAR_ID: From step 2")
        return False

    # Generate unique event ID
    event_uid = f"n8n-test-{int(datetime.datetime.now().timestamp())}"

    # Event times (1 hour from now, 1 hour duration)
    now = datetime.datetime.utcnow()
    start = (now + datetime.timedelta(hours=1)).strftime("%Y%m%dT%H%M%SZ")
    end = (now + datetime.timedelta(hours=2)).strftime("%Y%m%dT%H%M%SZ")
    dtstamp = now.strftime("%Y%m%dT%H%M%SZ")

    # ICS content (iCalendar format)
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//n8n iCloud Calendar//EN
CALSCALE:GREGORIAN
BEGIN:VEVENT
UID:{event_uid}
DTSTAMP:{dtstamp}
DTSTART:{start}
DTEND:{end}
SUMMARY:n8n Test Event - DELETE ME
DESCRIPTION:This is a test event created by n8n-icloud-calendar setup script. You can delete it.
END:VEVENT
END:VCALENDAR"""

    url = f"https://caldav.icloud.com/{USER_ID}/calendars/{CALENDAR_ID}/{event_uid}.ics"

    print(f"\nCreating test event...")
    print(f"Event: 'n8n Test Event - DELETE ME'")
    print(f"Start: ~1 hour from now")
    print(f"Calendar: {CALENDAR_ID[:8]}...")
    print("-" * 50)

    try:
        response = requests.put(
            url,
            data=ics_content,
            auth=HTTPBasicAuth(EMAIL, PASSWORD),
            headers={"Content-Type": "text/calendar; charset=utf-8"}
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 201:
            print("\n" + "=" * 50)
            print("SUCCESS! Event created (201 Created)")
            print("=" * 50)
            print("\nCheck your Calendar app - you should see:")
            print("  'n8n Test Event - DELETE ME'")
            print("  Starting in about 1 hour")
            print("\nYou can delete the test event manually.")
            return True

        elif response.status_code == 204:
            print("\n" + "=" * 50)
            print("SUCCESS! Event updated (204 No Content)")
            print("=" * 50)
            print("\nThe event already existed and was updated.")
            return True

        elif response.status_code == 403:
            print("\n" + "=" * 50)
            print("ERROR: Write access denied (403 Forbidden)")
            print("=" * 50)
            print("\nPossible causes:")
            print("  - This is a SHARED calendar (you can't write to shared calendars)")
            print("  - App-specific password expired")
            print("  - Wrong CALENDAR_ID")
            print("\nSolution:")
            print("  Use a calendar that YOU own (not shared with you).")
            print("  Run 2_get_calendar_id.py again and pick a different calendar.")
            print(f"\nResponse: {response.text}")
            return False

        elif response.status_code == 404:
            print("\n" + "=" * 50)
            print("ERROR: Calendar not found (404)")
            print("=" * 50)
            print("\nThe USER_ID or CALENDAR_ID is incorrect.")
            print("Run steps 1 and 2 again to get correct values.")
            return False

        elif response.status_code == 401:
            print("\n" + "=" * 50)
            print("ERROR: Authentication failed (401)")
            print("=" * 50)
            print("Check your EMAIL and PASSWORD.")
            return False

        else:
            print(f"\n" + "=" * 50)
            print(f"ERROR: Unexpected status {response.status_code}")
            print("=" * 50)
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("\nConnection error! Check your internet connection.")
        return False
    except Exception as e:
        print(f"\nError: {e}")
        return False


if __name__ == "__main__":
    success = create_test_event()

    print("\n" + "=" * 50)
    if success:
        print("WRITE TEST PASSED!")
        print("=" * 50)
        print("\nBoth READ and WRITE work!")
        print("You can now proceed with the n8n workflow setup.")
        print("\nSee: docs/n8n-workflow-setup.md")
    else:
        print("WRITE TEST FAILED!")
        print("=" * 50)
        print("\nTry a different calendar, or check the error above.")
