# n8n Workflow Setup Guide

This guide explains how to set up the iCloud Calendar Sub-Workflows in n8n and connect them to your main workflow or AI Agent.

## Prerequisites

Before starting, make sure you have:

- [ ] Your Apple ID email address
- [ ] Your app-specific password (see [setup-app-password.md](setup-app-password.md))
- [ ] Your USER_ID (from `1_get_user_id.py`)
- [ ] Your CALENDAR_ID (from `2_get_calendar_id.py`)
- [ ] Successfully tested read/write with Python scripts

## Part 1: Import Sub-Workflows

### Step 1: Import Calendar Read Sub-Workflow

1. In n8n, go to **Workflows** in the left sidebar
2. Click **Add workflow** → **Import from file**
3. Select `workflows/calendar-read.json`
4. The workflow will be created in inactive state

### Step 2: Import Calendar Write Sub-Workflow

1. Repeat the import process for `workflows/calendar-write.json`
2. You should now have two new workflows:
   - Calendar Read Sub-Workflow
   - Calendar Write Sub-Workflow

## Part 2: Configure Credentials

Both Sub-Workflows use HTTP Request nodes that need authentication configured.

### Create Header Auth Credential

1. Go to **Credentials** in n8n settings
2. Click **Add Credential**
3. Search for **Header Auth**
4. Configure:
   - **Name**: `iCloud CalDAV Auth`
   - **Header Name**: `Authorization`
   - **Header Value**: `Basic <base64-encoded-credentials>`

#### How to Create the Base64 Value

Your credentials need to be base64-encoded in the format `email:password`.

**Option 1: Using Terminal (Mac/Linux)**
```bash
echo -n "your-email@icloud.com:xxxx-xxxx-xxxx-xxxx" | base64
```

**Option 2: Using Python**
```python
import base64
credentials = "your-email@icloud.com:xxxx-xxxx-xxxx-xxxx"
print(base64.b64encode(credentials.encode()).decode())
```

**Option 3: Using an Online Tool**
1. Go to https://www.base64encode.org/
2. Enter: `your-email@icloud.com:xxxx-xxxx-xxxx-xxxx`
3. Click Encode
4. Copy the result

The final Header Value should look like:
```
Basic eW91ci1lbWFpbEBpY2xvdWQuY29tOnh4eHgteHh4eC14eHh4LXh4eHg=
```

### Alternative: Use Basic Auth Credential

Instead of Header Auth, you can use Basic Auth credential:

1. Go to **Credentials** → **Add Credential**
2. Search for **HTTP Basic Auth**
3. Configure:
   - **Name**: `iCloud CalDAV`
   - **User**: Your Apple ID email
   - **Password**: Your app-specific password

Then in the HTTP Request nodes, select:
- Authentication: **Predefined Credential Type**
- Credential Type: **HTTP Basic Auth**
- HTTP Basic Auth: Select your credential

## Part 3: Configure Sub-Workflows

### Calendar Read Sub-Workflow

1. Open the imported Calendar Read workflow
2. Find the **HTTP Request** node
3. Update these values:
   - URL: Replace `YOUR_USER_ID` with your actual USER_ID
   - URL: Replace `YOUR_CALENDAR_ID` with your actual CALENDAR_ID
   - Select your authentication credential
4. Save the workflow
5. **Activate** the workflow (toggle in top-right)

The URL format should be:
```
https://caldav.icloud.com/YOUR_USER_ID/calendars/YOUR_CALENDAR_ID/
```

### Calendar Write Sub-Workflow

1. Open the imported Calendar Write workflow
2. Find the **HTTP Request** node
3. Update the same values (USER_ID, CALENDAR_ID, credential)
4. Save and **Activate** the workflow

## Part 4: Connect to Your Main Workflow

### Option A: Using toolWorkflow (for AI Agents)

If you're using an AI Agent that needs calendar access:

1. In your AI Agent workflow, add a **Tool** node
2. Select **Call n8n Workflow Tool** (toolWorkflow)
3. Configure:
   - **Name**: `calendar_get_events`
   - **Description**: "Get calendar events for a date range"
   - **Workflow**: Select "Calendar Read Sub-Workflow"
4. Define input schema:
   ```json
   {
     "type": "object",
     "properties": {
       "start_date": {
         "type": "string",
         "description": "Start date in YYYYMMDD format"
       },
       "end_date": {
         "type": "string",
         "description": "End date in YYYYMMDD format"
       }
     },
     "required": ["start_date", "end_date"]
   }
   ```

5. Repeat for calendar_create_event with the Write Sub-Workflow

### Option B: Using Execute Workflow Node

For regular workflows (not AI Agent):

1. Add an **Execute Workflow** node
2. Select the Calendar Read or Write Sub-Workflow
3. Pass required parameters:
   - For read: `start_date`, `end_date`
   - For write: `title`, `start_datetime`, `end_datetime`, `description`

### Option C: Direct HTTP Request

You can also make direct CalDAV calls without Sub-Workflows. See the Sub-Workflow JSON files for the exact HTTP request configuration.

## Part 5: Testing

### Test Calendar Read

1. Create a simple workflow with:
   - Manual Trigger
   - Execute Workflow node (pointing to Calendar Read)
   - Set input: `start_date: "20240115"`, `end_date: "20240116"`
2. Execute manually
3. Check output for events

### Test Calendar Write

1. Create a test workflow with:
   - Manual Trigger
   - Execute Workflow node (pointing to Calendar Write)
   - Set input:
     ```json
     {
       "title": "Test from n8n",
       "start_datetime": "2024-01-15T10:00:00",
       "end_datetime": "2024-01-15T11:00:00",
       "description": "Test event"
     }
     ```
2. Execute manually
3. Check your calendar app for the new event

## Workflow Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Main Workflow                         │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Trigger  │───►│  AI Agent    │───►│   Response   │  │
│  └──────────┘    └──────┬───────┘    └──────────────┘  │
│                         │                               │
│              toolWorkflow calls                         │
│                         │                               │
└─────────────────────────┼───────────────────────────────┘
                          │
           ┌──────────────┼──────────────┐
           ▼                             ▼
┌─────────────────────┐    ┌─────────────────────┐
│  Calendar Read      │    │  Calendar Write     │
│  Sub-Workflow       │    │  Sub-Workflow       │
│  ┌───────────────┐  │    │  ┌───────────────┐  │
│  │ Webhook       │  │    │  │ Webhook       │  │
│  │ HTTP Request  │  │    │  │ HTTP Request  │  │
│  │ Parse Events  │  │    │  │ Response      │  │
│  │ Response      │  │    │  └───────────────┘  │
│  └───────────────┘  │    └─────────────────────┘
└──────────┬──────────┘              │
           │                         │
           ▼                         ▼
      iCloud CalDAV API ◄────────────┘
```

## Troubleshooting

### Sub-Workflow Not Found

- Make sure the Sub-Workflow is **active** (toggle on)
- Check the workflow name matches exactly

### 401 Unauthorized in n8n

- Verify your credential is correctly configured
- Test with the Python scripts first to confirm credentials work
- Regenerate app-specific password if needed

### No Events Returned

- Check the date format (YYYYMMDD)
- Verify CALENDAR_ID is correct
- Ensure there are actually events in that date range

### Event Not Created

- Check CALENDAR_ID is for YOUR calendar (not a shared one)
- Verify the datetime format
- Check n8n execution logs for detailed error

## Next Steps

- Set up error handling in your main workflow
- Add logging for debugging
- Consider caching for frequently accessed data
- Set up webhook triggers for real-time calendar updates
