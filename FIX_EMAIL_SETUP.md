# Fix Email Setup for Password Reset

## Current Status
✅ **Password reset is now working** - emails are being printed to the console/terminal

## To Enable Real Email Sending

### Step 1: Get Gmail App Password

1. Go to: https://myaccount.google.com/security
2. Enable **2-Step Verification** (if not already enabled)
3. Go to: https://myaccount.google.com/apppasswords
4. Select:
   - App: **Mail**
   - Device: **Other (Custom name)** → Enter "STOPPS Django App"
5. Click **Generate**
6. Copy the **16-character password** (it will look like: `abcd efgh ijkl mnop`)

### Step 2: Update settings.py

Open `ecomproject/settings.py` and change:

```python
# Change from console backend to SMTP
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Comment this out

# Update with your App Password
EMAIL_HOST_PASSWORD = 'your-16-character-app-password-here'  # Replace with the App Password from Step 1
```

### Step 3: Test Email

Run the test script:
```bash
python3 manage.py shell < test_email_send.py
```

Or test manually:
```bash
python3 manage.py shell
```

Then:
```python
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Test',
    'Test message',
    settings.EMAIL_HOST_USER,
    ['your-email@gmail.com'],
    fail_silently=False,
)
```

## Current Setup (Console Mode)

Right now, password reset emails are being **printed to the console/terminal** where you run `python manage.py runserver`. 

When a user requests a password reset:
1. Check your terminal/console
2. You'll see the email content printed there
3. Copy the reset link from the console
4. Share it with the user manually (or use it yourself to test)

## Troubleshooting

### If you get "Authentication failed" error:
- Make sure you're using an **App Password**, not your regular Gmail password
- App Passwords are 16 characters (may have spaces - remove them)

### If you get "Connection timeout":
- Check your internet connection
- Verify EMAIL_HOST is `smtp.gmail.com`
- Check if port 587 is blocked by firewall

### Alternative: Use Other Email Services

For production, consider:
- **SendGrid** (free tier: 100 emails/day)
- **Mailgun** (free tier: 5,000 emails/month)
- **AWS SES** (very cheap, pay per email)

These are more reliable than SMTP for production use.
