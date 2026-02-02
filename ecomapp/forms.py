from .models import Cargo, Order, Customer, Product, ProductOwner, Category, LinfoxUser
from django.contrib.auth.models import User
from django import forms


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["ordered_by", "shipping_address",
                  "mobile", "email", "payment_method"]


class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        model = Customer
        fields = ["username", "password","full_name", "county", "town", "email",  "address", "image"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make image field optional
        self.fields['image'].required = False

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "Customer with this username already exists.")

        return uname
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            email = email.strip().lower()  # Normalize email
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(
                    "A user with this email address already exists. Please use a different email."
                )
        return email


class productOwnerRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your username"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password"
        })
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email"
        })
    )

    class Meta:
        model = ProductOwner
        fields = ["username", "password", "email", "full_name", "mobile", "image"]
        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your full name"
            }),
            "mobile": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your mobile number"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make image field optional
        self.fields['image'].required = False

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "ProductOwner with this username already exists.")
        return uname
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            email = email.strip().lower()  # Normalize email
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(
                    "A user with this email address already exists. Please use a different email."
                )
        return email        


class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            return username.strip()
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            return password.strip()
        return password


class CustomerProfileEditForm(forms.ModelForm):
    """Form for customers to edit their profile"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Customer
        fields = ["full_name", "image", "address", "town", "county", "email"]
        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your full name",
                "style": "width: 100%; padding: 0.5rem 0.75rem; border: 2px solid #e5e7eb; border-radius: 6px;"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "style": "width: 100%; padding: 0.5rem; border: 2px solid #e5e7eb; border-radius: 6px;"
            }),
            "address": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your address",
                "style": "width: 100%; padding: 0.5rem 0.75rem; border: 2px solid #e5e7eb; border-radius: 6px;"
            }),
            "town": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your town/city",
                "style": "width: 100%; padding: 0.5rem 0.75rem; border: 2px solid #e5e7eb; border-radius: 6px;"
            }),
            "county": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your county",
                "style": "width: 100%; padding: 0.5rem 0.75rem; border: 2px solid #e5e7eb; border-radius: 6px;"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
                "style": "width: 100%; padding: 0.5rem 0.75rem; border: 2px solid #e5e7eb; border-radius: 6px;"
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip().lower()  # Normalize email
            # Check if email is already used by another user
            from django.contrib.auth.models import User
            existing_user = User.objects.filter(email=email).first()
            if existing_user and existing_user != self.instance.user:
                raise forms.ValidationError(
                    'A user with this email address already exists. Please use a different email.'
                )
        return email
    
    def save(self, commit=True):
        customer = super().save(commit=False)
        if commit:
            customer.save()
            # Update user email if changed
            if 'email' in self.cleaned_data:
                email = self.cleaned_data['email'].strip().lower()
                customer.user.email = email
                customer.user.save()
        return customer

class ProductOwnerProfileEditForm(forms.ModelForm):
    """Form for product owners to edit their profile"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = ProductOwner
        fields = ["full_name", "image", "mobile", "email"]
        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your full name",
                "style": "width: 100%; padding: 0.5rem 0.75rem; border: 2px solid #e5e7eb; border-radius: 6px;"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "style": "width: 100%; padding: 0.5rem; border: 2px solid #e5e7eb; border-radius: 6px;"
            }),
            "mobile": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your mobile number",
                "style": "width: 100%; padding: 0.5rem 0.75rem; border: 2px solid #e5e7eb; border-radius: 6px;"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
                "style": "width: 100%; padding: 0.5rem 0.75rem; border: 2px solid #e5e7eb; border-radius: 6px;"
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip().lower()  # Normalize email
            # Check if email is already used by another user
            from django.contrib.auth.models import User
            existing_user = User.objects.filter(email=email).first()
            if existing_user and existing_user != self.instance.user:
                raise forms.ValidationError(
                    'A user with this email address already exists. Please use a different email.'
                )
        return email
    
    def save(self, commit=True):
        product_owner = super().save(commit=False)
        if commit:
            product_owner.save()
            # Update user email if changed
            if 'email' in self.cleaned_data:
                email = self.cleaned_data['email'].strip().lower()
                product_owner.user.email = email
                product_owner.user.save()
        return product_owner


class LinfoxProfileEditForm(forms.ModelForm):
    """Form for Linfox users to edit their profile"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = LinfoxUser
        fields = ["full_name", "image", "mobile", "email"]
        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your full name",
                "style": "width: 100%; padding: 0.5rem 0.75rem; border: 2px solid #e5e7eb; border-radius: 6px;"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "style": "width: 100%; padding: 0.5rem; border: 2px solid #e5e7eb; border-radius: 6px;"
            }),
            "mobile": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your mobile number",
                "style": "width: 100%; padding: 0.5rem 0.75rem; border: 2px solid #e5e7eb; border-radius: 6px;"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
                "style": "width: 100%; padding: 0.5rem 0.75rem; border: 2px solid #e5e7eb; border-radius: 6px;"
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip().lower()  # Normalize email
            # Check if email is already used by another user
            from django.contrib.auth.models import User
            existing_user = User.objects.filter(email=email).first()
            if existing_user and existing_user != self.instance.user:
                raise forms.ValidationError(
                    'A user with this email address already exists. Please use a different email.'
                )
        return email
    
    def save(self, commit=True):
        linfox_user = super().save(commit=False)
        if commit:
            linfox_user.save()
            # Update user email if changed
            if 'email' in self.cleaned_data:
                email = self.cleaned_data['email'].strip().lower()
                linfox_user.user.email = email
                linfox_user.user.save()
        return linfox_user


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class ProductForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=MultiFileInput(attrs={"class": "form-control"}))
    class Meta:
        model = Product
        fields = ["title", "slug", "category", "image", "county", "town", "marked_price",
                  "selling_price", "description", "warranty", "return_policy"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product title here..."
            }),
            "slug": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the unique slug here..."
            }),
            "category": forms.Select(attrs={
                "class": "form-control"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
             "county": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter product country here..."
            }),
             "town": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter product city here..."
            }),
            "marked_price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Marked price of the product..."
            }),
            "selling_price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Selling price of the product..."
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Description of the product...",
                "rows": 5
            }),
            "warranty": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product warranty here..."
            }),
            "return_policy": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product return policy here..."
            }),

        }



class CargoForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=MultiFileInput(attrs={"class": "form-control"}))
    class Meta:
        model = Cargo
        fields = ["CampanyName", "driverName", "address", "image", "price", "cargo_status"]
        widgets = {
            "CampanyName": forms.Select(attrs={
                "class": "form-control"
            }),
            "driverName": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the Driver name here..."
            }),
            "address": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the address eg: kk 310st..."
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the price..."
            }),
            "cargo_status": forms.Select(attrs={
                "class": "form-control"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make image field optional
        self.fields['image'].required = False



class PasswordForgotForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Enter the email used in your account..."
    }))

    def clean_email(self):
        e = self.cleaned_data.get("email")
        # Check if user exists (for any user type: Customer, ProductOwner, Admin, LinfoxUser)
        from django.contrib.auth.models import User
        if not User.objects.filter(email=e).exists():
            raise forms.ValidationError(
                "No account found with this email address.")
        return e


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password',
            'placeholder': 'Enter New Password',
        }),
        label="New Password",
        min_length=8,
        help_text="Password must be at least 8 characters long."
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password',
            'placeholder': 'Confirm New Password',
        }),
        label="Confirm New Password"
    )

    def clean_new_password(self):
        password = self.cleaned_data.get("new_password")
        if password:
            password = password.strip()
            if len(password) < 8:
                raise forms.ValidationError(
                    "Password must be at least 8 characters long."
                )
        return password

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_new_password = self.cleaned_data.get("confirm_new_password")
        
        if confirm_new_password:
            confirm_new_password = confirm_new_password.strip()
        
        if new_password and confirm_new_password:
            if new_password != confirm_new_password:
                raise forms.ValidationError(
                    "New Passwords did not match! Make sure both passwords are exactly the same."
                )
        return confirm_new_password


#map
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Admin


class MultiFileInput(forms.ClearableFileInput):
    """Widget to allow selecting multiple files in Django forms."""
    allow_multiple_selected = True




class UserForm(UserCreationForm):
	'''
	Form that uses built-in UserCreationForm to handel user creation
	'''
	first_name = forms.CharField(max_length=30, required=True,
		widget=forms.TextInput(attrs={'placeholder': '*Your first name..'}))
	last_name = forms.CharField(max_length=30, required=True,
		widget=forms.TextInput(attrs={'placeholder': '*Your last name..'}))
	username = forms.EmailField(max_length=254, required=True,
		widget=forms.TextInput(attrs={'placeholder': '*Email..'}))
	password1 = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder': '*Password..','class':'password'}))
	password2 = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder': '*Confirm Password..','class':'password'}))

	#reCAPTCHA token
	token = forms.CharField(
		widget=forms.HiddenInput())

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )





class AuthForm(AuthenticationForm):
	'''
	Form that uses built-in AuthenticationForm to handel user auth
	'''
	username = forms.EmailField(max_length=254, required=True,
		widget=forms.TextInput(attrs={'placeholder': '*Email..'}))
	password = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder': '*Password..','class':'password'}))

	class Meta:
		model = User
		fields = ('username','password', )




class UserProfileForm(forms.ModelForm):
	'''
	Basic model-form for our user profile that extends Django user model.
	
	'''
	address = forms.CharField(max_length=100, required=True, widget = forms.HiddenInput())
	town = forms.CharField(max_length=100, required=True, widget = forms.HiddenInput())
	county = forms.CharField(max_length=100, required=True, widget = forms.HiddenInput())
	post_code = forms.CharField(max_length=8, required=True, widget = forms.HiddenInput())
	country = forms.CharField(max_length=40, required=True, widget = forms.HiddenInput())
	longitude = forms.CharField(max_length=50, required=True, widget = forms.HiddenInput())
	latitude = forms.CharField(max_length=50, required=True, widget = forms.HiddenInput())


	class Meta:
		model = Admin
		fields = ('address', 'town', 'county', 'post_code',
		 'country', 'longitude', 'latitude')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["title", "slug"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter category title (e.g., Electronics, Clothing)"
            }),
            "slug": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter unique slug (e.g., electronics, clothing)"
            })
        }        