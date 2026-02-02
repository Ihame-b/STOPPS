#!/usr/bin/env python
"""
Quick email test script
Run: python3 manage.py shell < test_email_send.py
Or: python3 test_email_send.py (if Django is set up)
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomproject.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 70)
print("EMAIL CONFIGURATION TEST")
print("=" * 70)
print(f"Backend: {settings.EMAIL_BACKEND}")
print(f"Host: {settings.EMAIL_HOST}")
print(f"Port: {settings.EMAIL_PORT}")
print(f"Use TLS: {settings.EMAIL_USE_TLS}")
print(f"From: {settings.EMAIL_HOST_USER}")
print(f"Password Set: {'Yes' if settings.EMAIL_HOST_PASSWORD else 'No'}")
print(f"Password Length: {len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 0}")
print("=" * 70)

test_email = input("Enter test email address (or press Enter to use ihamegrbt1@gmail.com): ").strip()
if not test_email:
    test_email = "ihamegrbt1@gmail.com"

print(f"\nSending test email to: {test_email}")
print("Please wait...\n")

try:
    result = send_mail(
        subject='STOPPS - Test Email',
        message='This is a test email from STOPPS. If you receive this, your email configuration is working correctly!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[test_email],
        fail_silently=False,
    )
    print("=" * 70)
    print("SUCCESS!")
    print("=" * 70)
    print(f"Email sent successfully! Result: {result}")
    print(f"Check {test_email} inbox (and spam folder)")
    print("=" * 70)
except Exception as e:
    print("=" * 70)
    print("ERROR!")
    print("=" * 70)
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")
    print("\nFull Error:")
    import traceback
    traceback.print_exc()
    print("=" * 70)
    
    # Provide specific solutions
    error_str = str(e).lower()
    if '535' in error_str or 'authentication' in error_str:
        print("\n🔧 SOLUTION: Gmail Authentication Failed")
        print("1. Go to: https://myaccount.google.com/apppasswords")
        print("2. Generate a new App Password for 'Mail'")
        print("3. Update EMAIL_HOST_PASSWORD in settings.py")
    elif 'connection' in error_str or 'timeout' in error_str:
        print("\n🔧 SOLUTION: Connection Issue")
        print("1. Check internet connection")
        print("2. Verify EMAIL_HOST and EMAIL_PORT")
        print("3. Check firewall settings")
    else:
        print("\n🔧 Check the error details above and verify email settings")
