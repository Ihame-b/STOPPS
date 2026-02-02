#!/usr/bin/env python
"""
Fix duplicate emails before making email field unique
Run: python3 manage.py shell < fix_duplicate_emails.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomproject.settings')
django.setup()

from django.contrib.auth.models import User
from django.db.models import Count

print("=" * 70)
print("FIXING DUPLICATE EMAILS")
print("=" * 70)

# Find duplicate emails
duplicates = User.objects.values('email').annotate(count=Count('email')).filter(count__gt=1, email__isnull=False).exclude(email='')

if not duplicates:
    print("\n✅ No duplicate emails found!")
else:
    print(f"\nFound {len(duplicates)} duplicate email addresses\n")
    
    for dup in duplicates:
        email = dup['email']
        count = dup['count']
        print(f"Processing: {email} (used by {count} users)")
        
        users = User.objects.filter(email=email).order_by('id')
        # Keep the first user's email, modify others
        first_user = users.first()
        print(f"  Keeping email for: {first_user.username} (ID: {first_user.id})")
        
        for idx, user in enumerate(users[1:], start=1):
            # Make email unique by appending user ID
            new_email = f"{email.split('@')[0]}+{user.id}@{email.split('@')[1]}"
            user.email = new_email
            user.save()
            print(f"  Changed email for: {user.username} (ID: {user.id}) to: {new_email}")

print("\n" + "=" * 70)
print("✅ Duplicate emails fixed!")
print("=" * 70)

# Verify no duplicates remain
remaining = User.objects.values('email').annotate(count=Count('email')).filter(count__gt=1, email__isnull=False).exclude(email='')
if remaining:
    print(f"\n⚠️ Warning: {len(remaining)} duplicate emails still exist")
else:
    print("\n✅ All emails are now unique!")
