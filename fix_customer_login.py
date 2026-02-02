#!/usr/bin/env python
"""
Fix script to activate all customers and verify their emails
Run: python3 manage.py shell < fix_customer_login.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomproject.settings')
django.setup()

from django.contrib.auth.models import User
from ecomapp.models import Customer, EmailVerificationToken

print("=" * 70)
print("FIXING CUSTOMER LOGIN ISSUES")
print("=" * 70)

# Get all customers
customers = Customer.objects.all()
print(f"\nTotal customers: {customers.count()}")

fixed_count = 0
for customer in customers:
    user = customer.user
    needs_fix = False
    fixes = []
    
    # Check if user is active
    if not user.is_active:
        needs_fix = True
        fixes.append("User not active")
        user.is_active = True
    
    # Check email verification
    try:
        verification = EmailVerificationToken.objects.get(user=user)
        if not verification.is_verified:
            needs_fix = True
            fixes.append("Email not verified")
            verification.is_verified = True
            verification.save()
    except EmailVerificationToken.DoesNotExist:
        # Create verification token and mark as verified
        needs_fix = True
        fixes.append("Missing verification token")
        # Use update_or_create to avoid duplicate key errors
        import secrets
        token = secrets.token_urlsafe(32)
        EmailVerificationToken.objects.update_or_create(
            user=user,
            defaults={
                'token': token,
                'is_verified': True
            }
        )
    
    if needs_fix:
        user.save()
        fixed_count += 1
        print(f"\n✅ Fixed: {customer.full_name} ({user.username})")
        print(f"   Issues: {', '.join(fixes)}")
        print(f"   Status: Active={user.is_active}, Verified=True")

print(f"\n" + "=" * 70)
print(f"✅ Fixed {fixed_count} customers")
print(f"✅ All customers should now be able to login")
print("=" * 70)
