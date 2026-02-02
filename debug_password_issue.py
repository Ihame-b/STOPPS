#!/usr/bin/env python
"""
Debug script to identify password reset/login issues
Run: python3 manage.py shell < debug_password_issue.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomproject.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from ecomapp.models import Customer

print("=" * 70)
print("PASSWORD RESET/LOGIN DEBUG TOOL")
print("=" * 70)

email = input("\nEnter user email (or press Enter for ihamegrbt1@gmail.com): ").strip()
if not email:
    email = "ihamegrbt1@gmail.com"

try:
    user = User.objects.get(email=email)
    print(f"\n✅ User Found:")
    print(f"   ID: {user.pk}")
    print(f"   Username: '{user.username}'")
    print(f"   Email: '{user.email}'")
    print(f"   Is Active: {user.is_active}")
    print(f"   Has Usable Password: {user.has_usable_password()}")
    print(f"   Password Hash Length: {len(user.password) if user.password else 0}")
    print(f"   Password Hash (first 30 chars): {user.password[:30] if user.password else 'None'}...")
    
    # Check if customer exists
    try:
        customer = Customer.objects.get(user=user)
        print(f"   Customer Profile: ✅ Exists")
    except Customer.DoesNotExist:
        print(f"   Customer Profile: ❌ Not Found")
    
    # Test password
    print(f"\n🔐 Password Testing:")
    test_password = input("Enter the password to test: ").strip()
    
    if test_password:
        # Test with exact password
        print(f"\n1. Testing with exact password (no trimming)...")
        auth1 = authenticate(username=user.username, password=test_password)
        print(f"   Result: {'✅ SUCCESS' if auth1 else '❌ FAILED'}")
        
        # Test with trimmed password
        print(f"\n2. Testing with trimmed password...")
        auth2 = authenticate(username=user.username, password=test_password.strip())
        print(f"   Result: {'✅ SUCCESS' if auth2 else '❌ FAILED'}")
        
        # Test with username trimmed
        print(f"\n3. Testing with trimmed username...")
        auth3 = authenticate(username=user.username.strip(), password=test_password.strip())
        print(f"   Result: {'✅ SUCCESS' if auth3 else '❌ FAILED'}")
        
        # Show what to use for login
        print(f"\n📋 Login Instructions:")
        print(f"   Use Username: '{user.username}'")
        print(f"   Use Password: (the password you just tested)")
        print(f"   ⚠️  Make sure there are no extra spaces!")
        
        if not auth1 and not auth2 and not auth3:
            print(f"\n❌ All authentication tests FAILED!")
            print(f"\nPossible issues:")
            print(f"1. Password might not have been saved correctly during reset")
            print(f"2. Password might be different from what you think")
            print(f"3. There might be a database sync issue")
            print(f"\n💡 Try resetting the password again and make sure to:")
            print(f"   - Use a strong password (at least 8 characters)")
            print(f"   - Copy/paste carefully (no extra spaces)")
            print(f"   - Wait a few seconds after reset before trying to login")
        else:
            print(f"\n✅ At least one authentication method worked!")
            print(f"   The password is correct, make sure you're using the exact username shown above")
    else:
        print("No password provided for testing")
        
except User.DoesNotExist:
    print(f"❌ User with email {email} not found")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
