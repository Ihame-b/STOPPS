#!/usr/bin/env python3
"""
Helper script to update Gmail App Password in settings.py
Run: python3 update_email_password.py
"""

import re
import os

def update_email_password():
    settings_file = 'ecomproject/settings.py'
    
    if not os.path.exists(settings_file):
        print(f"❌ Error: {settings_file} not found!")
        return
    
    print("=" * 70)
    print("Gmail App Password Updater")
    print("=" * 70)
    print("\nTo get your Gmail App Password:")
    print("1. Go to: https://myaccount.google.com/apppasswords")
    print("2. Generate a new App Password for 'Mail'")
    print("3. Copy the 16-character password\n")
    
    new_password = input("Enter your Gmail App Password (16 characters): ").strip()
    
    # Remove spaces if user pasted with spaces
    new_password = new_password.replace(' ', '')
    
    if len(new_password) != 16:
        print(f"\n⚠️  Warning: Password is {len(new_password)} characters, expected 16")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Cancelled.")
            return
    
    # Read the file
    try:
        with open(settings_file, 'r') as f:
            content = f.read()
        
        # Find and replace EMAIL_HOST_PASSWORD
        pattern = r"EMAIL_HOST_PASSWORD\s*=\s*os\.environ\.get\(['\"]EMAIL_HOST_PASSWORD['\"],\s*['\"][^'\"]*['\"]\)|EMAIL_HOST_PASSWORD\s*=\s*['\"][^'\"]*['\"]"
        
        replacement = f"EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '{new_password}')"
        
        new_content = re.sub(pattern, replacement, content)
        
        if new_content == content:
            # Try simpler pattern
            pattern2 = r"(EMAIL_HOST_PASSWORD\s*=\s*os\.environ\.get\(['\"]EMAIL_HOST_PASSWORD['\"],\s*)['\"][^'\"]*['\"]"
            new_content = re.sub(pattern2, r"\1'" + new_password + "')", content)
        
        # Write back
        with open(settings_file, 'w') as f:
            f.write(new_content)
        
        print("\n✅ Password updated successfully!")
        print(f"\nUpdated {settings_file}")
        print("\nNext steps:")
        print("1. Test email sending: python3 manage.py shell < test_email_send.py")
        print("2. Or restart your Django server and try password reset again")
        
    except Exception as e:
        print(f"\n❌ Error updating file: {e}")
        print("\nPlease manually update EMAIL_HOST_PASSWORD in ecomproject/settings.py")

if __name__ == '__main__':
    update_email_password()
