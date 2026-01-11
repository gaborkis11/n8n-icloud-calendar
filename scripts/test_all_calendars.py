#!/usr/bin/env python3
"""
iCloud CalDAV - Test All Calendars
Optional: Find which calendars you can write to

Usage: python3 test_all_calendars.py

This script tests write access to multiple calendars.
Useful when you have several calendars and want to find writable ones.
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

# Add your CALENDAR_IDs here (from step 2)
CALENDARS = [
    "CALENDAR_ID_1",
    "CALENDAR_ID_2",
    # Add more as needed...
]
# ============================================


def test_calendar(calendar_id, index):
    """Test write access to a single calendar"""
    print(f"\n--- Calendar #{index + 1}: {calendar_id[:20]}... ---")

    event_uid = f"test-{index}-{int(datetime.datetime.now().timestamp())}"
    now = datetime.datetime.utcnow()
    start = (now + datetime.timedelta(hours=1)).strftime("%Y%m%dT%H%M%SZ")
    end = (now + datetime.timedelta(hours=2)).strftime("%Y%m%dT%H%M%SZ")
    dtstamp = now.strftime("%Y%m%dT%H%M%SZ")

    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//n8n Test//EN
CALSCALE:GREGORIAN
BEGIN:VEVENT
UID:{event_uid}
DTSTAMP:{dtstamp}
DTSTART:{start}
DTEND:{end}
SUMMARY:Write Test #{index + 1} - DELETE ME
END:VEVENT
END:VCALENDAR"""

    url = f"https://caldav.icloud.com/{USER_ID}/calendars/{calendar_id}/{event_uid}.ics"

    try:
        response = requests.put(
            url,
            data=ics_content,
            auth=HTTPBasicAuth(EMAIL, PASSWORD),
            headers={"Content-Type": "text/calendar; charset=utf-8"}
        )

        if response.status_code in [201, 204]:
            print(f"WRITABLE! Status: {response.status_code}")
            return True
        else:
            print(f"Not writable. Status: {response.status_code}")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    print("=" * 60)
    print("iCloud CalDAV - Test All Calendars for Write Access")
    print("=" * 60)

    if "YOUR_" in EMAIL or "xxxx" in PASSWORD or "YOUR_" in USER_ID:
        print("\n" + "=" * 60)
        print("ERROR: Please configure your credentials first!")
        print("=" * 60)
        return

    if not CALENDARS or CALENDARS[0] == "CALENDAR_ID_1":
        print("\n" + "=" * 60)
        print("ERROR: Please add your CALENDAR_IDs to the CALENDARS list!")
        print("=" * 60)
        print("\nRun 2_get_calendar_id.py to get your calendar IDs,")
        print("then add them to the CALENDARS list in this file.")
        return

    results = []
    for i, cal_id in enumerate(CALENDARS):
        success = test_calendar(cal_id, i)
        results.append((i + 1, cal_id, success))

    print("\n" + "=" * 60)
    print("RESULTS:")
    print("=" * 60)

    writable = []
    for num, cal_id, success in results:
        status = "WRITABLE" if success else "Read-only/Shared"
        print(f"\n#{num}: {status}")
        print(f"    ID: {cal_id}")
        if success:
            writable.append(cal_id)

    print("\n" + "=" * 60)
    if writable:
        print(f"Found {len(writable)} writable calendar(s)!")
        print("=" * 60)
        print("\nUse one of these CALENDAR_IDs for your n8n workflow.")
        print("\nNote: Test events were created - delete them from your calendar.")
    else:
        print("No writable calendars found!")
        print("=" * 60)
        print("\nAll calendars are either shared (read-only) or inaccessible.")
        print("Make sure you have at least one calendar that YOU own.")


if __name__ == "__main__":
    main()
