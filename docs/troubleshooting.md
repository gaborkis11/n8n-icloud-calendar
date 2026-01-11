# Troubleshooting Guide

This guide covers common issues you might encounter when setting up iCloud Calendar integration with n8n.

## Authentication Errors

### 401 Unauthorized

**Symptoms:**
- Python scripts return 401 status
- n8n HTTP Request fails with 401

**Causes:**
1. Wrong email address
2. Using Apple ID password instead of app-specific password
3. Typo in app-specific password
4. App-specific password was revoked

**Solutions:**
1. Double-check your email address (the one you use for Apple ID)
2. Make sure you're using an **app-specific password**, not your Apple ID password
3. Verify the password format: `xxxx-xxxx-xxxx-xxxx` (16 characters with hyphens)
4. Generate a new app-specific password at [appleid.apple.com](https://appleid.apple.com)

### 403 Forbidden

**Symptoms:**
- Scripts connect but certain operations fail with 403
- Can read but not write to calendar

**Causes:**
1. App-specific password expired
2. Too many failed authentication attempts
3. Trying to write to a shared/read-only calendar
4. Account security settings changed

**Solutions:**
1. Generate a new app-specific password
2. Wait 15-30 minutes if rate-limited, then try again
3. Use a calendar you own (not shared with you)
4. Check your Apple ID security settings

## Calendar Access Errors

### 404 Not Found

**Symptoms:**
- Scripts fail with 404 when accessing calendar
- "Calendar not found" errors

**Causes:**
1. Wrong USER_ID
2. Wrong CALENDAR_ID
3. Calendar was deleted
4. Typo in the ID values

**Solutions:**
1. Re-run `1_get_user_id.py` to get the correct USER_ID
2. Re-run `2_get_calendar_id.py` to get correct CALENDAR_IDs
3. Verify the calendar still exists in your Calendar app
4. Copy-paste IDs carefully to avoid typos

### Empty Response / No Events

**Symptoms:**
- Query succeeds (207 status) but returns no events
- Events exist but aren't being returned

**Causes:**
1. No events in the specified date range
2. Wrong date format
3. Wrong CALENDAR_ID
4. Time zone issues

**Solutions:**
1. Verify events exist in that date range in your Calendar app
2. Use correct date format: `YYYYMMDD` (e.g., `20240115`)
3. Try a different calendar
4. Expand the date range to test

### Can't Write to Calendar

**Symptoms:**
- Read works but write fails
- 403 error when creating events

**Causes:**
1. Calendar is shared (you don't own it)
2. Calendar is read-only
3. Subscription calendar (can't be modified)

**Solutions:**
1. Use `test_all_calendars.py` to find writable calendars
2. Choose a calendar you created yourself
3. iCloud default calendars and Family calendars are usually writable

## n8n-Specific Issues

### Sub-Workflow Not Executing

**Symptoms:**
- Main workflow runs but Sub-Workflow doesn't execute
- toolWorkflow calls fail silently

**Causes:**
1. Sub-Workflow is not active
2. Wrong workflow reference
3. Permission issues

**Solutions:**
1. Make sure Sub-Workflow is toggled **ON** (active)
2. Verify the workflow name/ID in toolWorkflow configuration
3. Check n8n user permissions

### Credential Issues in n8n

**Symptoms:**
- Python scripts work but n8n fails
- Authentication works locally but not in n8n

**Causes:**
1. Credential not properly configured
2. Wrong credential type selected
3. Base64 encoding issues (for Header Auth)

**Solutions:**
1. Recreate the credential in n8n
2. Try Basic Auth credential instead of Header Auth
3. Verify base64 encoding is correct (no extra spaces or newlines)

### Date/Time Format Errors

**Symptoms:**
- Events created at wrong time
- Date parsing errors in workflows

**Causes:**
1. Wrong datetime format
2. Time zone issues
3. Using local time instead of UTC

**Solutions:**
1. Use ISO 8601 format: `2024-01-15T10:00:00Z`
2. Or use CalDAV format: `20240115T100000Z`
3. The 'Z' suffix indicates UTC time

## CalDAV Protocol Issues

### PROPFIND Fails

**Symptoms:**
- `1_get_user_id.py` fails
- Can't discover calendars

**Causes:**
1. Network/firewall blocking PROPFIND requests
2. iCloud service temporarily unavailable
3. Invalid credentials

**Solutions:**
1. Test from a different network
2. Try again later
3. Verify credentials

### REPORT Fails

**Symptoms:**
- Can list calendars but can't query events
- `3_test_read_events.py` fails

**Causes:**
1. Malformed XML request
2. Invalid date range
3. Calendar doesn't support REPORT

**Solutions:**
1. Use the provided scripts without modification
2. Check date format (YYYYMMDD)
3. Try a different calendar

### PUT Fails

**Symptoms:**
- Can read but can't create events
- `4_test_write_event.py` fails

**Causes:**
1. Calendar is read-only
2. Invalid ICS format
3. Event UID conflict

**Solutions:**
1. Use a writable calendar (your own, not shared)
2. Use the provided scripts without modification
3. Ensure unique event UIDs (scripts handle this automatically)

## Network Issues

### Connection Timeout

**Symptoms:**
- Scripts hang or timeout
- "Connection error" messages

**Causes:**
1. Network connectivity issues
2. Firewall blocking connections
3. iCloud service down

**Solutions:**
1. Check internet connection
2. Try from a different network
3. Check [Apple System Status](https://www.apple.com/support/systemstatus/)

### SSL/TLS Errors

**Symptoms:**
- Certificate verification errors
- SSL handshake failures

**Causes:**
1. Outdated Python/requests library
2. Corporate proxy/firewall
3. System certificate issues

**Solutions:**
1. Update Python and requests: `pip install --upgrade requests`
2. Configure proxy settings if needed
3. Update system certificates

## Getting Help

If you're still stuck:

1. **Check the error message carefully** - It often contains the solution
2. **Search existing issues** - Someone may have solved it already
3. **Open an issue** - Include:
   - Which script/workflow failed
   - Full error message
   - Steps you've already tried
   - Your setup (n8n version, self-hosted vs cloud)

**Never share:**
- Your app-specific password
- Your USER_ID or CALENDAR_ID (these are semi-private)
- Base64-encoded credentials
