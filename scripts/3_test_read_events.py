#!/usr/bin/env python3
"""
iCloud CalDAV Read Test
Step 3: Test reading events from your calendar

Usage: python3 3_test_read_events.py
"""

import requests
from requests.auth import HTTPBasicAuth
import datetime
import re

# ============================================
# CONFIGURATION - REPLACE WITH YOUR VALUES!
# ============================================
EMAIL = "YOUR_APPLE_ID@email.com"           # Your Apple ID email
PASSWORD = "xxxx-xxxx-xxxx-xxxx"            # App-specific password
USER_ID = "YOUR_USER_ID"                    # From step 1
CALENDAR_ID = "YOUR_CALENDAR_ID"            # From step 2 (the one you want to use)
# ============================================


def get_events(start_date, end_date):
    """
    Query events using CalDAV REPORT request
    """
    print(f"\nQuerying events from {start_date} to {end_date}...")

    # CalDAV REPORT XML request
    xml_body = f"""<?xml version="1.0" encoding="UTF-8"?>
<c:calendar-query xmlns:d="DAV:" xmlns:c="urn:ietf:params:xml:ns:caldav">
  <d:prop>
    <d:getetag/>
    <c:calendar-data/>
  </d:prop>
  <c:filter>
    <c:comp-filter name="VCALENDAR">
      <c:comp-filter name="VEVENT">
        <c:time-range start="{start_date}T000000Z" end="{end_date}T235959Z"/>
      </c:comp-filter>
    </c:comp-filter>
  </c:filter>
</c:calendar-query>"""

    url = f"https://caldav.icloud.com/{USER_ID}/calendars/{CALENDAR_ID}/"

    try:
        response = requests.request(
            "REPORT",
            url,
            data=xml_body,
            auth=HTTPBasicAuth(EMAIL, PASSWORD),
            headers={
                "Content-Type": "application/xml; charset=utf-8",
                "Depth": "1"
            }
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 207:  # Multi-Status (success)
            events = parse_events(response.text)
            return events
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return None

    except Exception as e:
        print(f"Connection error: {e}")
        return None


def parse_events(xml_response):
    """
    Parse ICS events from XML response
    """
    events = []

    # Find VEVENT blocks
    vevent_pattern = r'BEGIN:VEVENT(.*?)END:VEVENT'
    matches = re.findall(vevent_pattern, xml_response, re.DOTALL)

    for match in matches:
        # SUMMARY (event title)
        summary_match = re.search(r'SUMMARY[^:]*:(.+)', match)
        summary = summary_match.group(1).strip() if summary_match else "Untitled"

        # DTSTART (start time)
        dtstart_match = re.search(r'DTSTART[^:]*:(\d{8}T?\d{0,6})', match)
        if dtstart_match:
            dtstart = dtstart_match.group(1)
            if 'T' in dtstart and len(dtstart) >= 13:
                time_str = dtstart[9:11] + ":" + dtstart[11:13]
            else:
                time_str = "All day"
        else:
            time_str = "?"

        events.append({
            "title": summary,
            "time": time_str
        })

    # Sort by time
    events.sort(key=lambda x: x['time'] if x['time'] not in ["All day", "?"] else "00:00")

    return events


def main():
    print("=" * 60)
    print("iCloud CalDAV - Read Test")
    print("=" * 60)

    if "YOUR_" in EMAIL or "xxxx" in PASSWORD or "YOUR_" in USER_ID or "YOUR_" in CALENDAR_ID:
        print("\n" + "=" * 60)
        print("ERROR: Please configure your credentials first!")
        print("=" * 60)
        print("\nEdit this file and replace:")
        print("  - EMAIL: Your Apple ID email address")
        print("  - PASSWORD: Your app-specific password")
        print("  - USER_ID: From step 1")
        print("  - CALENDAR_ID: From step 2")
        return

    # Date range: today and tomorrow
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    today_str = today.strftime("%Y%m%d")
    tomorrow_str = tomorrow.strftime("%Y%m%d")

    print(f"\nToday: {today}")
    print(f"Tomorrow: {tomorrow}")
    print(f"CALENDAR_ID: {CALENDAR_ID[:8]}...")

    events = get_events(today_str, tomorrow_str)

    print("\n" + "=" * 60)
    if events is not None:
        if events:
            print(f"SUCCESS! Found {len(events)} event(s):")
            print("=" * 60)
            for event in events:
                print(f"  {event['time']} - {event['title']}")
        else:
            print("SUCCESS! No events in this time range.")
            print("=" * 60)
            print("(This is normal if your calendar is empty today/tomorrow)")

        print("\n" + "=" * 60)
        print("READ TEST PASSED!")
        print("=" * 60)
        print("\nNext step: Run 4_test_write_event.py to test writing")
    else:
        print("READ TEST FAILED!")
        print("=" * 60)
        print("\nCheck the error message above for troubleshooting.")


if __name__ == "__main__":
    main()
