# n8n Workflow Files

These are ready-to-import n8n Sub-Workflows for iCloud Calendar integration.

## Files

| File | Purpose |
|------|---------|
| `calendar-read.json` | Read events from iCloud Calendar |
| `calendar-write.json` | Create events in iCloud Calendar |

## How to Import

### Step 1: Import into n8n

1. In n8n, go to **Workflows**
2. Click **Add workflow** → **Import from file**
3. Select the JSON file
4. The workflow will be created in **inactive** state

### Step 2: Configure Credentials

Both workflows have a Code node with configuration at the top. You need to edit:

```javascript
// ============================================
// CONFIGURATION - REPLACE WITH YOUR VALUES!
// ============================================
const USER_ID = 'YOUR_USER_ID';  // From 1_get_user_id.py
const CALENDARS = {
  'personal': 'YOUR_CALENDAR_ID',  // From 2_get_calendar_id.py
};
const EMAIL = 'YOUR_APPLE_ID@email.com';
const PASSWORD = 'xxxx-xxxx-xxxx-xxxx';  // App-specific password
// ============================================
```

### Step 3: Activate

After configuration, toggle the workflow to **Active**.

## Workflow Details

### Calendar Read Sub-Workflow

**Input:**
```json
{
  "date": "2024-01-15",
  "calendar": "personal"
}
```

**Output:**
```json
{
  "result": "Events for 2024-01-15 (personal):\n- 09:00: Meeting\n- 14:00: Call",
  "events": [
    {"time": "09:00", "title": "Meeting"},
    {"time": "14:00", "title": "Call"}
  ],
  "calendar": "personal",
  "date": "2024-01-15"
}
```

### Calendar Write Sub-Workflow

**Input:**
```json
{
  "title": "New Meeting",
  "date": "2024-01-15",
  "startTime": "10:00",
  "endTime": "11:00",
  "calendar": "personal"
}
```

**Output:**
```json
{
  "result": "Event created successfully in personal calendar:\n- Title: New Meeting\n- Date: 2024-01-15\n- Time: 10:00 - 11:00",
  "success": true,
  "calendar": "personal",
  "eventUid": "n8n-1705312800000-abc123xyz"
}
```

## Multiple Calendars

To support multiple calendars, add them to the `CALENDARS` object:

```javascript
const CALENDARS = {
  'personal': 'your-personal-calendar-id',
  'work': 'your-work-calendar-id',
  'family': 'your-family-calendar-id',
};
```

Then specify which calendar to use in the input:
```json
{
  "date": "2024-01-15",
  "calendar": "work"
}
```

## Using with AI Agent

To use these as AI Agent tools:

1. In your AI Agent workflow, add a **Tool** node
2. Select **Call n8n Workflow Tool**
3. Configure the tool name and description
4. Select the Sub-Workflow
5. Define the input schema

Example for calendar read:
```json
{
  "type": "object",
  "properties": {
    "date": {
      "type": "string",
      "description": "Date in YYYY-MM-DD format"
    },
    "calendar": {
      "type": "string",
      "description": "Calendar name (personal, work, etc.)"
    }
  },
  "required": ["date"]
}
```

## Troubleshooting

### Workflow Not Found

Make sure the Sub-Workflow is **active** (toggle on in the top right).

### Authentication Errors

- Verify EMAIL and PASSWORD in the Code node
- Make sure you're using an app-specific password
- Test with Python scripts first

### Wrong Calendar

Check that CALENDAR_ID matches the calendar you want.
Run `2_get_calendar_id.py` to list all calendars.

## Security Note

These workflow files contain placeholder values. After importing:
1. Replace placeholders with your actual credentials
2. **Do not export and share** the configured workflows (they contain secrets)
