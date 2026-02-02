# Fix Gmail Authentication Error (535)

## Problem
The error `535 Username and Password not accepted` means your Gmail password is incorrect or expired.

## Solution: Generate Gmail App Password

### Step 1: Enable 2-Step Verification
1. Go to: https://myaccount.google.com/security
2. Under "Signing in to Google", find **2-Step Verification**
3. If not enabled, click it and follow the setup process
4. You'll need your phone to verify

### Step 2: Generate App Password
1. Go to: https://myaccount.google.com/apppasswords
   - Or: Google Account → Security → 2-Step Verification → App passwords
2. Select:
   - **App**: Choose "Mail"
   - **Device**: Choose "Other (Custom name)"
   - Enter: "STOPPS Django App"
3. Click **Generate**
4. You'll see a 16-character password like: `abcd efgh ijkl mnop`
5. **Copy this password** (remove spaces if any)

### Step 3: Update settings.py

Open `ecomproject/settings.py` and update line 207:

```python
EMAIL_HOST_PASSWORD = 'your-16-character-app-password-here'  # Paste the App Password here
```

**Important**: 
- Use the App Password, NOT your regular Gmail password
- Remove any spaces from the password
- It should be exactly 16 characters

### Step 4: Test

Run this command to test:
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
    ['ihamegrbt1@gmail.com'],
    fail_silently=False,
)
```

## Alternative: Use Environment Variables (More Secure)

Instead of hardcoding the password, use environment variables:

1. Create a `.env` file in the project root:
```bash
EMAIL_HOST_PASSWORD=your-app-password-here
```

2. Update `settings.py`:
```python
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
```

3. Load environment variables (install python-dotenv if needed):
```bash
pip install python-dotenv
```

Then in `settings.py` at the top:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Quick Fix Command

After generating the App Password, you can quickly update it:

```bash
# Edit settings.py and replace the password on line 207
nano ecomproject/settings.py
# Or use your preferred editor
```

## Still Having Issues?

1. **Make sure 2-Step Verification is enabled** - App Passwords only work with 2-Step Verification
2. **Check the password** - It should be exactly 16 characters, no spaces
3. **Wait a few minutes** - Sometimes it takes a few minutes for the App Password to activate
4. **Try generating a new one** - If it still doesn't work, generate a new App Password

## Security Note

Never commit your App Password to Git! Use environment variables or keep it in a `.env` file that's in `.gitignore`.
