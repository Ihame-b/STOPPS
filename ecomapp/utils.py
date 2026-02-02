from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import six
import logging

# Set up logger for email debugging
logger = logging.getLogger(__name__)


class MyPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp)
        )


password_reset_token = MyPasswordResetTokenGenerator()


def generate_verification_token():
    """Generate a unique verification token"""
    return get_random_string(length=64)


def send_verification_email(user, request, user_type='customer', is_already_verified=False):
    """Send welcome email with email verification link to user"""
    from .models import EmailVerificationToken
    
    # Create or get existing token
    token_obj, created = EmailVerificationToken.objects.get_or_create(
        user=user,
        defaults={'token': generate_verification_token()}
    )
    
    if not created:
        # Regenerate token if already exists and not verified
        if not token_obj.is_verified:
            token_obj.token = generate_verification_token()
            token_obj.is_verified = False
            token_obj.save()
    
    # Build verification URL
    verification_url = request.build_absolute_uri(
        reverse('ecomapp:verify_email', kwargs={'token': token_obj.token})
    )
    
    # Email subject based on user type
    user_type_names = {
        'customer': 'Customer',
        'productowner': 'Product Owner',
        'admin': 'Admin',
        'linfox': 'Linfox User'
    }
    user_type_name = user_type_names.get(user_type, 'User')
    
    # Email subject - welcome message
    if is_already_verified:
        subject = f'Welcome to STOPPS - Your {user_type_name} Account is Ready!'
    else:
        subject = f'Welcome to STOPPS - Verify Your {user_type_name} Account'
    
    # Create email template context
    context = {
        'user': user,
        'verification_url': verification_url,
        'user_type': user_type_name,
        'site_name': 'STOPPS',
        'is_already_verified': is_already_verified,
        'login_url': request.build_absolute_uri(reverse('ecomapp:customerlogin'))
    }
    
    # Determine login URL based on user type
    if user_type == 'customer':
        context['login_url'] = request.build_absolute_uri(reverse('ecomapp:customerlogin'))
    elif user_type == 'productowner':
        context['login_url'] = request.build_absolute_uri(reverse('ecomapp:productOwnerlogin'))
    elif user_type == 'admin':
        context['login_url'] = request.build_absolute_uri(reverse('ecomapp:adminlogin'))
    elif user_type == 'linfox':
        context['login_url'] = request.build_absolute_uri(reverse('ecomapp:linfoxlogin'))
    
    # Render email template
    html_message = render_to_string('emails/verification_email.html', context)
    plain_message = strip_tags(html_message)
    
    # Send email
    try:
        logger.info(f"Attempting to send welcome/verification email to {user.email}")
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Welcome/verification email sent successfully to {user.email}")
        print(f"✅ Welcome email sent successfully to {user.email}")
        return True
    except Exception as e:
        logger.error(f"Error sending welcome/verification email to {user.email}: {str(e)}")
        print(f"Error sending welcome/verification email: {e}")
        return False


def send_password_reset_email(user, request, user_type='customer'):
    """Send password reset link to user"""
    from django.utils.encoding import force_bytes
    from django.utils.http import urlsafe_base64_encode
    import six
    
    try:
        token = password_reset_token.make_token(user)
        
        # Encode user ID for URL
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Build reset URL - try reverse first
        try:
            reset_url = request.build_absolute_uri(
                reverse('ecomapp:password_reset_confirm', kwargs={
                    'uidb64': uidb64,
                    'token': token
                })
            )
        except Exception as url_error:
            logger.error(f"Error building reset URL: {url_error}")
            # Fallback: build URL manually
            base_url = request.build_absolute_uri('/')
            reset_url = f"{base_url}password-reset-confirm/{uidb64}/{token}/"
            logger.info(f"Using fallback URL: {reset_url}")
    except Exception as token_error:
        logger.error(f"Error generating reset token: {token_error}")
        print(f"Error generating reset token: {token_error}")
        return False
    
    # Email subject based on user type
    user_type_names = {
        'customer': 'Customer',
        'productowner': 'Product Owner',
        'admin': 'Admin',
        'linfox': 'Linfox User'
    }
    user_type_name = user_type_names.get(user_type, 'User')
    
    # Email content
    subject = f'Reset Your {user_type_name} Password - STOPPS'
    
    # Create email template context
    context = {
        'user': user,
        'reset_url': reset_url,
        'user_type': user_type_name,
        'site_name': 'STOPPS'
    }
    
    # Render email template
    try:
        html_message = render_to_string('emails/password_reset_email.html', context)
        plain_message = strip_tags(html_message)
    except Exception as template_error:
        logger.error(f"Error rendering email template: {template_error}")
        # Fallback to simple text email
        html_message = None
        plain_message = f"""
Hello {user.get_full_name() or user.username},

We received a request to reset your password for your {user_type_name} account on {context['site_name']}.

Click the link below to reset your password:
{reset_url}

If you did not request a password reset, please ignore this email.

This link will expire in 24 hours.

© {context['site_name']} Team
"""
    
    # Send email
    try:
        logger.info(f"Attempting to send password reset email to {user.email}")
        logger.info(f"Reset URL: {reset_url}")
        logger.info(f"Email settings - Host: {settings.EMAIL_HOST}, Port: {settings.EMAIL_PORT}, User: {settings.EMAIL_HOST_USER}")
        
        # Check if using console backend (for testing)
        if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
            logger.info("Using console email backend - email will be printed to console")
        
        # Validate email settings
        if not settings.EMAIL_HOST_USER:
            error_msg = "EMAIL_HOST_USER is not configured in settings.py"
            logger.error(error_msg)
            print(f"ERROR: {error_msg}")
            return False
        
        if not settings.EMAIL_HOST_PASSWORD:
            error_msg = "EMAIL_HOST_PASSWORD is not configured in settings.py"
            logger.error(error_msg)
            print(f"ERROR: {error_msg}")
            return False
        
        # Send email with or without HTML
        email_kwargs = {
            'subject': subject,
            'message': plain_message,
            'from_email': settings.EMAIL_HOST_USER,
            'recipient_list': [user.email],
            'fail_silently': False,
        }
        if html_message:
            email_kwargs['html_message'] = html_message
        
        result = send_mail(**email_kwargs)
        
        if result:
            logger.info(f"Password reset email sent successfully to {user.email}. Result: {result}")
            print(f"✅ Password reset email sent successfully to {user.email}")
            return True
        else:
            logger.warning(f"Email send returned False for {user.email}")
            print(f"⚠️ Email send returned False - email may not have been sent")
            return False
    except Exception as e:
        import traceback
        error_msg = f"Error sending password reset email to {user.email}: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        
        # Detailed error output
        print("\n" + "=" * 70)
        print("PASSWORD RESET EMAIL ERROR - DETAILED DIAGNOSTICS")
        print("=" * 70)
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        print(f"\nRecipient: {user.email}")
        print(f"Reset URL: {reset_url}")
        print(f"\nEmail Configuration:")
        print(f"  Backend: {settings.EMAIL_BACKEND}")
        print(f"  Host: {settings.EMAIL_HOST}")
        print(f"  Port: {settings.EMAIL_PORT}")
        print(f"  Use TLS: {settings.EMAIL_USE_TLS}")
        print(f"  From Email: {settings.EMAIL_HOST_USER}")
        print(f"  Password Set: {'Yes' if settings.EMAIL_HOST_PASSWORD else 'No'}")
        print(f"  Password Length: {len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 0} characters")
        print("\nFull Traceback:")
        print(traceback.format_exc())
        print("=" * 70 + "\n")
        
        # Check for specific error types and provide solutions
        error_str = str(e).lower()
        error_detail = ""
        solution = ""
        
        if '535' in error_str or 'authentication failed' in error_str or 'invalid credentials' in error_str:
            error_detail = "Gmail Authentication Failed"
            solution = """
SOLUTION:
1. Go to https://myaccount.google.com/apppasswords
2. Generate a new App Password for 'Mail'
3. Copy the 16-character password
4. Update EMAIL_HOST_PASSWORD in settings.py with the new App Password
5. Make sure 2-Step Verification is enabled on your Google account
            """
        elif '534' in error_str or 'application-specific password' in error_str:
            error_detail = "Gmail Requires App Password"
            solution = """
SOLUTION:
Your Gmail account requires an App Password (not your regular password).
1. Enable 2-Step Verification: https://myaccount.google.com/security
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Select 'Mail' and your device
4. Use the 16-character password in EMAIL_HOST_PASSWORD
            """
        elif 'connection' in error_str or 'timeout' in error_str or 'network' in error_str:
            error_detail = "Cannot Connect to Email Server"
            solution = """
SOLUTION:
1. Check your internet connection
2. Verify EMAIL_HOST is correct (smtp.gmail.com for Gmail)
3. Check if port 587 is blocked by firewall
4. Try using port 465 with EMAIL_USE_SSL = True instead of EMAIL_USE_TLS
            """
        elif 'smtplib' in str(type(e)).lower() or 'smtp' in error_str:
            error_detail = "SMTP Server Error"
            solution = f"""
SOLUTION:
SMTP error occurred: {str(e)}
1. Verify EMAIL_HOST and EMAIL_PORT are correct
2. Check if your email provider requires different settings
3. For Gmail, ensure 'Less secure app access' is enabled OR use App Password
            """
        else:
            error_detail = f"Unknown Error: {str(e)}"
            solution = f"""
SOLUTION:
Unexpected error occurred. Please check:
1. Email configuration in settings.py
2. Network connectivity
3. Email provider requirements
4. Check the full traceback above for details
            """
        
        logger.error(f"{error_detail}\n{solution}")
        print(f"\nERROR TYPE: {error_detail}")
        print(solution)
        print("=" * 70 + "\n")
        
        return False
