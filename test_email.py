"""
Quick test script to verify email configuration
Run this from Django shell: python manage.py shell < test_email.py
Or run: python manage.py shell, then copy-paste the code below
"""

from django.core.mail import send_mail
from django.conf import settings

# Test email sending
try:
    result = send_mail(
        subject='Test Email from STOPPS',
        message='This is a test email to verify email configuration.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['your-email@example.com'],  # Replace with your email
        fail_silently=False,
    )
    print(f"Email sent successfully! Result: {result}")
    print(f"Email settings:")
    print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"  EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'Not set'}")
except Exception as e:
    print(f"Error sending email: {e}")
    import traceback
    traceback.print_exc()
