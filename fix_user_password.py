#!/usr/bin/env python
"""
Manual password fix script - Use this if password reset isn't working
Run: python3 manage.py shell < fix_user_password.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomproject.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import connection

print("=" * 70)
print("MANUAL PASSWORD FIX TOOL")
print("=" * 70)

email = input("\nEnter user email: ").strip()
if not email:
    print("Email is required!")
    exit(1)

try:
    user = User.objects.get(email=email)
    print(f"\n✅ User found:")
    print(f"   Username: {user.username}")
    print(f"   Email: {user.email}")
    print(f"   Current password hash (first 30): {user.password[:30] if user.password else 'None'}...")
    
    # Get new password
    new_password = input("\nEnter NEW password (at least 8 characters): ").strip()
    if len(new_password) < 8:
        print("❌ Password must be at least 8 characters!")
        exit(1)
    
    # Confirm password
    confirm = input("Confirm password: ").strip()
    if new_password != confirm:
        print("❌ Passwords don't match!")
        exit(1)
    
    # Store old hash
    old_hash = user.password
    
    # Set new password
    print("\n🔄 Setting new password...")
    user.set_password(new_password)
    
    # Save with explicit update
    user.save(update_fields=['password'])
    
    # Force database commit
    connection.commit()
    
    # Get fresh user from database
    user = User.objects.get(pk=user.pk)
    
    # Verify password changed
    if user.password == old_hash:
        print("❌ ERROR: Password hash did not change!")
        print("   The password was not saved to the database.")
        exit(1)
    
    print(f"✅ Password hash changed!")
    print(f"   New hash (first 30): {user.password[:30]}...")
    
    # Test authentication
    print("\n🔐 Testing authentication...")
    auth_result = authenticate(username=user.username, password=new_password)
    
    if auth_result:
        print("✅ SUCCESS! Password is working correctly!")
        print(f"\nYou can now login with:")
        print(f"   Username: {user.username}")
        print(f"   Password: {new_password}")
    else:
        print("❌ WARNING: Password was saved but authentication test failed.")
        print("   This might be a caching issue. Try logging in anyway.")
        print(f"\nTry logging in with:")
        print(f"   Username: {user.username}")
        print(f"   Password: {new_password}")
    
except User.DoesNotExist:
    print(f"❌ User with email {email} not found")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
