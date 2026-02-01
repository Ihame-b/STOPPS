# User Roles and Permissions Documentation

## 👥 User Types Overview

This system has **two types of admin users** who can access admin/Linfox functionality:

### 1. Super Admin (Admin)
- **Model**: `Admin` (in `ecomapp.models.Admin`)
- **Purpose**: Main administrative users with full system access
- **Profile**: Linked to Django User via ForeignKey
- **Access**: Can access all Admin pages and Linfox pages
- **Login**: Can login at `/admin-login/` or `/linfox-login/`
- **Redirect**: After login → `/admin-home/`

### 2. Linfox User (Admin)
- **Model**: `LinfoxUser` (in `ecomapp.models.LinfoxUser`)
- **Purpose**: Linfox-specific administrative users
- **Profile**: Linked to Django User via OneToOneField
- **Access**: Can access all Admin pages and Linfox pages
- **Login**: Can login at `/admin-login/` or `/linfox-login/`
- **Redirect**: After login → `/linfox-home/`

### 3. Regular Customer
- **Model**: `Customer` (in `ecomapp.models.Customer`)
- **Purpose**: Regular e-commerce customers
- **Access**: Customer-facing pages only (products, cart, checkout)
- **Login**: `/login/` (customer login)
- **Cannot access**: Admin or Linfox pages

### 4. Product Owner
- **Model**: `ProductOwner` (in `ecomapp.models.ProductOwner`)
- **Purpose**: Users who own/manage products
- **Access**: Product owner dashboard and product management
- **Login**: `/product-login/`
- **Cannot access**: Admin or Linfox pages (unless also has Admin/LinfoxUser profile)

## 🔐 Unified Login System

### Key Feature
**Both Super Admin and Linfox User can login from the same pages:**
- `/admin-login/` - Accepts both Admin and LinfoxUser
- `/linfox-login/` - Accepts both Admin and LinfoxUser

### Login Logic
1. User enters credentials
2. System checks if user has:
   - `Admin` profile, OR
   - `LinfoxUser` profile
3. If either exists, user is logged in
4. Redirect based on priority:
   - If LinfoxUser exists → `/linfox-home/`
   - Else if Admin exists → `/admin-home/`

## 🛡️ Access Control

### Mixins

#### `AdminRequiredMixin`
- **Allows**: Admin users AND LinfoxUser users
- **Used in**: Admin pages (AdminHomeView, AdminOrderListView, etc.)
- **Redirects to**: `/admin-login/` if not authorized

#### `LinfoxRequiredMixin`
- **Allows**: Admin users AND LinfoxUser users
- **Used in**: Linfox pages (LinfoxHomeView, LinfoxCargoListView, etc.)
- **Redirects to**: `/admin-login/` if not authorized

### Important Notes
- Both mixins now allow **both** Admin and LinfoxUser
- This means Super Admin can access Linfox pages
- Linfox User can access Admin pages
- They share the same access level for admin functionality

## 📋 User Profile Structure

### Super Admin (Admin)
```python
class Admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="admins")
    mobile = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    post_code = models.CharField(max_length=8)
    has_profile = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
```

### Linfox User (Admin)
```python
class LinfoxUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="linfox")
    mobile = models.CharField(max_length=20)
```

## 🔄 Dual Role Users

A single Django User can have **both** Admin and LinfoxUser profiles:
- User can be Super Admin AND Linfox User simultaneously
- When logging in, system checks for both
- Redirect priority: LinfoxUser takes precedence (goes to `/linfox-home/`)

## 📍 Login URLs

| User Type | Login URL | Redirects To |
|-----------|-----------|--------------|
| Super Admin | `/admin-login/` or `/linfox-login/` | `/admin-home/` |
| Linfox User | `/admin-login/` or `/linfox-login/` | `/linfox-home/` |
| Customer | `/login/` | Customer profile |
| Product Owner | `/product-login/` | Product owner home |

## 🎯 Creating Users

### Create Super Admin
1. Go to Django Admin: `/admin/`
2. Create a Django User
3. Create an `Admin` profile linked to that User
4. User can now login at `/admin-login/` or `/linfox-login/`

### Create Linfox User
1. Go to Django Admin: `/admin/`
2. Create a Django User
3. Create a `LinfoxUser` profile linked to that User
4. User can now login at `/admin-login/` or `/linfox-login/`

### Create Dual Role User
1. Create a Django User
2. Create both `Admin` and `LinfoxUser` profiles for the same User
3. User has access to both admin and Linfox features
4. Login redirects to `/linfox-home/` (LinfoxUser takes priority)

## ⚠️ Important Distinctions

### Super Admin vs Linfox User

| Feature | Super Admin | Linfox User |
|---------|-------------|-------------|
| Model | `Admin` | `LinfoxUser` |
| Relationship | ForeignKey to User | OneToOneField to User |
| Primary Purpose | General system administration | Linfox-specific operations |
| Default Redirect | `/admin-home/` | `/linfox-home/` |
| Can Access Admin Pages | ✅ Yes | ✅ Yes |
| Can Access Linfox Pages | ✅ Yes | ✅ Yes |

### Key Points
- **Both are admin users** - they have the same access level
- **Different models** - but unified login system
- **Different redirects** - but can access all pages
- **Can coexist** - a user can be both

## 🔍 Code References

### Login Views
- `AdminLoginView` - Accepts both Admin and LinfoxUser
- `LinfoxLoginView` - Accepts both Admin and LinfoxUser

### Access Control
- `AdminRequiredMixin` - Allows both Admin and LinfoxUser
- `LinfoxRequiredMixin` - Allows both Admin and LinfoxUser

### Models
- `ecomapp.models.Admin` - Super Admin model
- `ecomapp.models.LinfoxUser` - Linfox User (Admin) model

---

**Summary**: There are two types of admin users (Super Admin and Linfox User), but they share the same login system and access permissions. Both can login from either login page and access all admin/Linfox functionality.
