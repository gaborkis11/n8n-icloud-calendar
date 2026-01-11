# Setting Up an App-Specific Password for iCloud

Apple requires app-specific passwords for third-party applications to access iCloud services. This guide walks you through creating one for n8n calendar integration.

## Prerequisites

- An Apple ID with two-factor authentication enabled
- iCloud Calendar enabled on your account

## Step-by-Step Guide

### 1. Go to Apple ID Settings

Open your browser and navigate to:

**[https://appleid.apple.com](https://appleid.apple.com)**

### 2. Sign In

Sign in with your Apple ID and password. Complete two-factor authentication if prompted.

### 3. Navigate to App-Specific Passwords

1. Click on **Sign-In and Security** in the left sidebar
2. Look for **App-Specific Passwords**
3. Click on it to expand the section

### 4. Generate a New Password

1. Click the **"+"** button or **"Generate an app-specific password"**
2. Enter a label for this password (e.g., "n8n calendar" or "calendar automation")
3. Click **Create**

### 5. Copy Your Password

Apple will display a password in this format:

```
xxxx-xxxx-xxxx-xxxx
```

**Important:**
- Copy this password immediately
- Store it securely (password manager recommended)
- You won't be able to see it again after closing the dialog
- If you lose it, you'll need to generate a new one

### 6. Use the Password

Use this app-specific password (NOT your Apple ID password) in:
- The Python scripts (`EMAIL` and `PASSWORD` fields)
- n8n HTTP Request node credentials

## Security Notes

### What App-Specific Passwords Can Do

- Access iCloud services (Calendar, Contacts, etc.)
- Cannot change your Apple ID password
- Cannot access Apple ID account settings
- Cannot make purchases

### Managing App-Specific Passwords

- You can have up to 25 app-specific passwords
- Revoke any password anytime at appleid.apple.com
- If you change your Apple ID password, all app-specific passwords are revoked
- Generate separate passwords for different apps/services

### Recommendations

1. **Use a unique password for n8n** - Don't reuse passwords across services
2. **Label clearly** - So you know which password is for what
3. **Revoke if compromised** - If you suspect a password is compromised, revoke it immediately
4. **Store securely** - Use a password manager

## Troubleshooting

### "App-Specific Passwords" Not Visible

- Two-factor authentication must be enabled
- Go to Security → Two-Factor Authentication and enable it first

### Password Not Working (401 Error)

- Make sure you're using the app-specific password, not your Apple ID password
- Check for typos (the format is `xxxx-xxxx-xxxx-xxxx`)
- Try generating a new password

### Password Revoked Unexpectedly

This happens when:
- You changed your Apple ID password
- You manually revoked it
- Your account security settings changed

Solution: Generate a new app-specific password.

### Too Many Passwords (25 Limit)

Review your existing passwords and revoke ones you no longer need:
1. Go to appleid.apple.com
2. Sign-In and Security → App-Specific Passwords
3. Click on a password to see details
4. Click "Revoke" to remove unused passwords

## Next Steps

Once you have your app-specific password:

1. Go to the `scripts/` directory
2. Run `python3 1_get_user_id.py` to find your USER_ID
3. Follow the main README for complete setup instructions
