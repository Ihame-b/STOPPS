# Email Troubleshooting Guide

## Common Issues and Solutions

### Issue: "Failed to send password reset email"

### Solution 1: Check Email Configuration

Verify these settings in `ecomproject/settings.py`:

```python
EMAIL_HOST = 'smtp.gmail.com'  # For Gmail
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # NOT your regular password!
```

### Solution 2: Gmail App Password

If using Gmail, you **MUST** use an App Password, not your regular password:

1. Go to your Google Account settings
2. Enable 2-Step Verification
3. Go to App Passwords
4. Generate a new app password for "Mail"
5. Use that 16-character password in `EMAIL_HOST_PASSWORD`

### Solution 3: Test Email Configuration

Run this in Django shell to test:

```bash
python3 manage.py shell
```

Then run:
```python
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Test Email',
    'This is a test',
    settings.EMAIL_HOST_USER,
    ['your-test-email@example.com'],
    fail_silently=False,
)
```

### Solution 4: Use Console Backend for Testing

Temporarily enable console email backend in `settings.py`:

```python
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

This will print emails to the console instead of sending them.

### Solution 5: Check Console Output

When requesting a password reset, check the console/terminal for detailed error messages. The system now prints:
- Email configuration details
- Specific error messages
- Connection issues
- Authentication problems

### Common Error Messages:

1. **"Authentication failed"** or **"535"**
   - Solution: Use Gmail App Password instead of regular password

2. **"Connection timeout"**
   - Solution: Check EMAIL_HOST and EMAIL_PORT settings
   - Check firewall/network settings

3. **"EMAIL_HOST_USER not set"**
   - Solution: Set EMAIL_HOST_USER in settings.py

4. **"EMAIL_HOST_PASSWORD not set"**
   - Solution: Set EMAIL_HOST_PASSWORD in settings.py

### For Production:

Consider using:
- SendGrid
- Mailgun
- AWS SES
- Or other professional email services

These services provide better reliability and deliverability than SMTP.
