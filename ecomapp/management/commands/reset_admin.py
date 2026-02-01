"""
Django management command to reset admin user password.
This is useful when you forget the password or need to reset it.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Resets admin user password (creates if doesn\'t exist)'

    def handle(self, *args, **options):
        # Get credentials from environment variables, with secure defaults
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@stopps.com')
        password = os.environ.get('ADMIN_PASSWORD', 'Admin@123')
        
        # Get or create user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_staff': True, 'is_superuser': True}
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created new superuser "{username}"')
            )
        else:
            # Update existing user
            user.email = email
            user.is_staff = True
            user.is_superuser = True
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists. Resetting password...')
            )
        
        # Set password (this will hash it properly)
        user.set_password(password)
        user.save()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Admin user ready!\n'
                f'   Username: {username}\n'
                f'   Email: {email}\n'
                f'   Password: {password}\n'
                f'\nYou can now login at /admin/ or /admin-login/'
            )
        )
