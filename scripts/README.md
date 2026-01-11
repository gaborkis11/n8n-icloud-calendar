# iCloud CalDAV Discovery Scripts

These Python scripts help you discover your iCloud CalDAV credentials (USER_ID and CALENDAR_ID) which are required for n8n integration.

## Prerequisites

- Python 3.x
- `requests` library

```bash
pip install requests
```

## Usage Order

Run the scripts in order. Each script builds on information from the previous one.

### Step 1: Get Your USER_ID

```bash
python3 1_get_user_id.py
```

**Before running:**
1. Open `1_get_user_id.py` in a text editor
2. Replace `YOUR_APPLE_ID@email.com` with your Apple ID email
3. Replace `xxxx-xxxx-xxxx-xxxx` with your app-specific password
4. Save the file

**Output:** Your USER_ID (a number like `272090464`)

### Step 2: Get Your CALENDAR_ID(s)

```bash
python3 2_get_calendar_id.py
```

**Before running:**
1. Open `2_get_calendar_id.py`
2. Add your EMAIL, PASSWORD, and USER_ID (from step 1)
3. Save the file

**Output:** List of all your calendars with their CALENDAR_IDs

### Step 3: Test Reading Events

```bash
python3 3_test_read_events.py
```

**Before running:**
1. Open `3_test_read_events.py`
2. Add your EMAIL, PASSWORD, USER_ID, and CALENDAR_ID
3. Save the file

**Output:** Events from today/tomorrow (or confirmation that read works)

### Step 4: Test Writing Events

```bash
python3 4_test_write_event.py
```

**Before running:**
1. Open `4_test_write_event.py`
2. Add your credentials (same as step 3)
3. Make sure CALENDAR_ID is for a calendar YOU own (not shared)
4. Save the file

**Output:** Confirmation that a test event was created

**Important:** Check your Calendar app after running - you'll see a test event. Delete it manually.

### Optional: Test All Calendars

```bash
python3 test_all_calendars.py
```

This script tests write access to multiple calendars at once. Useful if you have many calendars and want to find which ones are writable.

## Configuration Template

Each script has a configuration section at the top:

```python
# ============================================
# CONFIGURATION - REPLACE WITH YOUR VALUES!
# ============================================
EMAIL = "YOUR_APPLE_ID@email.com"           # Your Apple ID email
PASSWORD = "xxxx-xxxx-xxxx-xxxx"            # App-specific password
USER_ID = "YOUR_USER_ID"                    # From step 1
CALENDAR_ID = "YOUR_CALENDAR_ID"            # From step 2
# ============================================
```

## Common Issues

### "Please configure your credentials first!"

You haven't replaced the placeholder values. Edit the script and add your actual credentials.

### 401 Unauthorized

- Check your email address
- Make sure you're using an **app-specific password**, not your Apple ID password
- See [../docs/setup-app-password.md](../docs/setup-app-password.md)

### 403 Forbidden

- Your app-specific password may have expired
- You might be trying to write to a shared calendar
- Generate a new password at appleid.apple.com

### 404 Not Found

- USER_ID or CALENDAR_ID is wrong
- Re-run the earlier scripts to get correct values

### Connection Error

- Check your internet connection
- iCloud services might be temporarily unavailable

## Security Notes

**Do NOT commit these scripts with your real credentials!**

If you accidentally commit credentials:
1. Immediately revoke the app-specific password at appleid.apple.com
2. Generate a new one
3. Remove the commit from git history (or just generate new credentials)

Consider using environment variables for sensitive data:

```python
import os
EMAIL = os.environ.get('ICLOUD_EMAIL', 'YOUR_APPLE_ID@email.com')
PASSWORD = os.environ.get('ICLOUD_PASSWORD', 'xxxx-xxxx-xxxx-xxxx')
```

Then run with:
```bash
ICLOUD_EMAIL="your@email.com" ICLOUD_PASSWORD="xxxx-xxxx-xxxx-xxxx" python3 1_get_user_id.py
```

## Next Steps

Once all tests pass:
1. Note down your USER_ID and CALENDAR_ID
2. Go to the `workflows/` directory
3. Import the Sub-Workflows into n8n
4. Configure them with your credentials

See [../docs/n8n-workflow-setup.md](../docs/n8n-workflow-setup.md) for n8n configuration.
