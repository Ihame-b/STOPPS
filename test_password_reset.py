#!/usr/bin/env python
"""
Test script to verify password reset is working
Run: python3 manage.py shell < test_password_reset.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomproject.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

print("=" * 70)
print("PASSWORD RESET TEST")
print("=" * 70)

# Get user email
email = input("Enter user email to test (or press Enter for ihamegrbt1@gmail.com): ").strip()
if not email:
    email = "ihamegrbt1@gmail.com"

try:
    user = User.objects.get(email=email)
    print(f"\n✅ User found:")
    print(f"   Username: {user.username}")
    print(f"   Email: {user.email}")
    print(f"   Is Active: {user.is_active}")
    print(f"   Has Usable Password: {user.has_usable_password()}")
    print(f"   Password Hash Length: {len(user.password) if user.password else 0}")
    
    # Test password
    print(f"\n🔐 Testing password authentication...")
    test_password = input("Enter the NEW password to test: ").strip()
    
    if test_password:
        auth_result = authenticate(username=user.username, password=test_password)
        if auth_result:
            print(f"✅ SUCCESS! Authentication works with the new password!")
            print(f"   You can login with:")
            print(f"   - Username: {user.username}")
            print(f"   - Password: {test_password}")
        else:
            print(f"❌ FAILED! Authentication does NOT work with this password.")
            print(f"\nPossible issues:")
            print(f"1. Password might not have been saved correctly")
            print(f"2. You might be using the wrong username")
            print(f"3. There might be a caching issue - try waiting a few seconds")
            print(f"\nTry logging in with:")
            print(f"   Username: {user.username}")
            print(f"   Email: {user.email}")
    else:
        print("No password provided for testing")
        
except User.DoesNotExist:
    print(f"❌ User with email {email} not found")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("=" * 70)
