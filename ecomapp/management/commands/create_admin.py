"""
Django management command to create a superuser from environment variables.
This is useful for automated deployments where shell access is not available.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Creates a superuser from environment variables (ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD)'

    def handle(self, *args, **options):
        # Get credentials from environment variables, with secure defaults for testing
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@stopps.com')
        password = os.environ.get('ADMIN_PASSWORD', 'Admin@123')
        
        # Create superuser (or update if exists)
        try:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            
            if created:
                # New user - set password
                user.set_password(password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created superuser "{username}" with email "{email}"'
                    )
                )
            else:
                # User exists - update password and ensure superuser status
                user.email = email
                user.is_staff = True
                user.is_superuser = True
                user.set_password(password)  # Reset password to ensure it's correct
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Updated existing user "{username}" - password reset to default'
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating/updating superuser: {str(e)}')
            )
