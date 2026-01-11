# n8n-icloud-calendar

**Connect n8n to iCloud Calendar using CalDAV**

A complete solution for integrating iCloud Calendar with n8n workflows. This project provides Python scripts to discover your CalDAV credentials and ready-to-import n8n Sub-Workflows for reading and creating calendar events.

## The Problem

Integrating iCloud Calendar with n8n is challenging because:

1. **The CalDAV community node doesn't work with iCloud** - It fails with authentication errors
2. **AI Agent's Code Tool runs in a sandbox** - It cannot make HTTP requests to external services
3. **iCloud requires app-specific passwords** - Regular Apple ID passwords don't work
4. **Finding your USER_ID and CALENDAR_ID is not obvious** - These are required for API calls

## The Solution

This project provides:

- **Python scripts** to discover your iCloud CalDAV credentials (USER_ID, CALENDAR_ID)
- **n8n Sub-Workflows** that handle CalDAV communication
- **Architecture** that bypasses sandbox limitations using the toolWorkflow approach

### Architecture

```
Your Workflow (or AI Agent)
         │
         ▼
    toolWorkflow
         │
         ▼
    Sub-Workflow ──────► iCloud CalDAV API
    (HTTP Request)            │
         │                    ▼
         ◄──────────── iCloud Calendar
```

## Quick Start

### Prerequisites

- Apple ID with iCloud Calendar enabled
- n8n instance (self-hosted or cloud)
- Python 3.x with `requests` library (`pip install requests`)

### Step 1: Create an App-Specific Password

1. Go to [appleid.apple.com](https://appleid.apple.com)
2. Sign in with your Apple ID
3. Navigate to **Sign-In and Security** → **App-Specific Passwords**
4. Click **Generate an app-specific password**
5. Name it something like "n8n calendar"
6. **Copy and save the password** (format: `xxxx-xxxx-xxxx-xxxx`)

> **Important:** This is NOT your Apple ID password. You must generate a new app-specific password.

See [docs/setup-app-password.md](docs/setup-app-password.md) for detailed instructions.

### Step 2: Get Your USER_ID

```bash
cd scripts
python3 1_get_user_id.py
```

Edit the script first and add your:
- `EMAIL`: Your Apple ID email
- `PASSWORD`: The app-specific password from Step 1

The script will output your USER_ID (a number like `272090464`).

### Step 3: Get Your CALENDAR_ID

```bash
python3 2_get_calendar_id.py
```

This lists all your calendars and their IDs. Pick the calendar you want to use.

### Step 4: Test the Connection

```bash
# Test reading events
python3 3_test_read_events.py

# Test creating events
python3 4_test_write_event.py
```

If both tests pass, you're ready for n8n!

### Step 5: Import n8n Workflows

1. In n8n, go to **Workflows** → **Import from File**
2. Import `workflows/calendar-read.json`
3. Import `workflows/calendar-write.json`
4. Configure the HTTP Request nodes with your credentials

See [docs/n8n-workflow-setup.md](docs/n8n-workflow-setup.md) for detailed n8n configuration.

## Project Structure

```
n8n-icloud-calendar/
├── README.md                    # This file
├── LICENSE                      # MIT License
├── docs/
│   ├── setup-app-password.md    # App-specific password guide
│   ├── n8n-workflow-setup.md    # n8n configuration guide
│   └── troubleshooting.md       # Common issues and solutions
├── scripts/
│   ├── README.md                # Scripts documentation
│   ├── 1_get_user_id.py         # Step 1: Get USER_ID
│   ├── 2_get_calendar_id.py     # Step 2: Get CALENDAR_ID
│   ├── 3_test_read_events.py    # Step 3: Test reading
│   ├── 4_test_write_event.py    # Step 4: Test writing
│   └── test_all_calendars.py    # Optional: Test multiple calendars
└── workflows/
    ├── README.md                # Workflow import guide
    ├── calendar-read.json       # Sub-Workflow for reading events
    └── calendar-write.json      # Sub-Workflow for creating events
```

## Features

### Calendar Read Sub-Workflow

- Query events by date range
- Returns parsed event data (title, start time, end time, description)
- Supports all-day events

### Calendar Write Sub-Workflow

- Create new calendar events
- Set title, start/end time, description
- Returns confirmation of created event

## Use Cases

- **Voice assistants**: "What's on my calendar tomorrow?"
- **Automation**: Create calendar events from form submissions
- **AI Agents**: Let your AI assistant manage your calendar
- **Integrations**: Sync events between systems

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Wrong credentials | Check email and app-specific password |
| 403 Forbidden | Password expired or wrong calendar | Create new app-specific password, or use a different calendar |
| 404 Not Found | Wrong USER_ID or CALENDAR_ID | Re-run discovery scripts |
| Empty response | No events in date range | This is normal for empty calendars |

See [docs/troubleshooting.md](docs/troubleshooting.md) for more details.

## Why Sub-Workflows?

n8n's AI Agent Code Tool runs in a VM2 sandbox that blocks HTTP requests. Using Sub-Workflows with the `toolWorkflow` approach:

1. Keeps calendar logic in dedicated workflows
2. Allows the AI Agent to call them as tools
3. Bypasses sandbox restrictions
4. Makes the solution reusable and maintainable

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

MIT License - see [LICENSE](LICENSE) file.

## Acknowledgments

- Thanks to Apple for CalDAV support (even if the documentation could be better)
- Thanks to the n8n community for inspiration

---


