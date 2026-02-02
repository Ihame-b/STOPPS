# ⚡ QUICK FIX: Email Not Sending

## The Problem
Your Gmail password is being rejected. Error: `535 Username and Password not accepted`

## The Solution (5 minutes)

### Option 1: Use Helper Script (Easiest)
```bash
python3 update_email_password.py
```
Follow the prompts to enter your new Gmail App Password.

### Option 2: Manual Fix

1. **Get Gmail App Password** (2 minutes):
   - Go to: https://myaccount.google.com/apppasswords
   - Click "Select app" → Choose "Mail"
   - Click "Select device" → Choose "Other" → Enter "STOPPS"
   - Click "Generate"
   - **Copy the 16-character password**

2. **Update settings.py** (1 minute):
   - Open `ecomproject/settings.py`
   - Find line 207: `EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'gsgxechqvudhjync')`
   - Replace `'gsgxechqvudhjync'` with your new App Password
   - Save the file

3. **Test** (1 minute):
   ```bash
   python3 manage.py shell
   ```
   Then:
   ```python
   from django.core.mail import send_mail
   from django.conf import settings
   send_mail('Test', 'Test', settings.EMAIL_HOST_USER, ['ihamegrbt1@gmail.com'], fail_silently=False)
   ```

## Why This Happens
Gmail requires an **App Password** (not your regular password) when:
- 2-Step Verification is enabled (recommended)
- Using third-party apps like Django

Your regular Gmail password won't work for SMTP.

## After Fixing
Once you update the password:
- ✅ Password reset emails will be sent to customers
- ✅ Email verification will work
- ✅ All email features will work

## Need Help?
See `SETUP_GMAIL_APP_PASSWORD.md` for detailed instructions.
