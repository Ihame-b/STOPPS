from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from .models import *


class LinfoxUserAdmin(admin.ModelAdmin):
    """Custom admin for LinfoxUser to send welcome emails"""
    list_display = ['full_name', 'user', 'mobile']
    search_fields = ['full_name', 'user__username', 'user__email', 'mobile']
    
    def save_model(self, request, obj, form, change):
        """Override save to send welcome email for new LinfoxUsers"""
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        
        # Send welcome email for newly created LinfoxUsers
        if is_new and obj.user and obj.user.email:
            from .utils import send_verification_email
            from .models import EmailVerificationToken
            import secrets
            
            # Create email verification token and mark as verified for admin-created users
            token = secrets.token_urlsafe(32)
            EmailVerificationToken.objects.update_or_create(
                user=obj.user,
                defaults={'token': token, 'is_verified': True}
            )
            
            # Activate user if not already active
            if not obj.user.is_active:
                obj.user.is_active = True
                obj.user.save()
            
            # Send welcome email (account is already verified)
            try:
                send_verification_email(obj.user, request, user_type='linfox', is_already_verified=True)
            except Exception as e:
                # Log error but don't fail the save
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error sending welcome email to LinfoxUser {obj.user.email}: {str(e)}")


class AdminUserAdmin(admin.ModelAdmin):
    """Custom admin for Admin to send welcome emails"""
    list_display = ['full_name', 'user', 'mobile']
    search_fields = ['full_name', 'user__username', 'user__email', 'mobile']
    
    def save_model(self, request, obj, form, change):
        """Override save to send welcome email for new Admin users"""
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        
        # Send welcome email for newly created Admin users
        if is_new and obj.user and obj.user.email:
            from .utils import send_verification_email
            from .models import EmailVerificationToken
            import secrets
            
            # Create email verification token and mark as verified for admin-created users
            token = secrets.token_urlsafe(32)
            EmailVerificationToken.objects.update_or_create(
                user=obj.user,
                defaults={'token': token, 'is_verified': True}
            )
            
            # Activate user if not already active
            if not obj.user.is_active:
                obj.user.is_active = True
                obj.user.save()
            
            # Send welcome email (account is already verified)
            try:
                send_verification_email(obj.user, request, user_type='admin', is_already_verified=True)
            except Exception as e:
                # Log error but don't fail the save
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error sending welcome email to Admin {obj.user.email}: {str(e)}")


# Register models with custom admin classes
admin.site.register(LinfoxUser, LinfoxUserAdmin)
admin.site.register(Admin, AdminUserAdmin)
admin.site.register(
    [Customer, ProductOwner, Cargo, Category, Product, Cart, CartProduct, Order, ProductImage])
