# Fix Admin Login Issues

## Problem: Username/Password Not Working

If you can't login with the default credentials, here are solutions:

## ✅ Solution 1: Use Reset Endpoint (Easiest)

The setup endpoint now **resets the password** even if the user exists.

### Step 1: Send POST Request

Visit or POST to:
```
https://stop-v8rq.onrender.com/setup/create-admin/
```

**Using curl:**
```bash
curl -X POST https://stop-v8rq.onrender.com/setup/create-admin/
```

**Using Python:**
```python
import requests
response = requests.post('https://stop-v8rq.onrender.com/setup/create-admin/')
print(response.json())
```

### Step 2: Check Response

You should see:
```json
{
  "success": true,
  "message": "Admin user \"admin\" updated successfully",
  "username": "admin",
  "email": "admin@stopps.com",
  "password": "Admin@123",
  "note": "You can now login at /admin/ or /admin-login/"
}
```

### Step 3: Login

Use these credentials:
- **Username**: `admin`
- **Password**: `Admin@123`

---

## ✅ Solution 2: Update Start Command (Automatic Reset)

The `create_admin` command now **resets the password** on every run.

### Step 1: Update Start Command in Render

Change your Start Command to:
```
python manage.py migrate && python manage.py create_admin && gunicorn ecomproject.wsgi:application
```

### Step 2: Save and Wait

Render will restart and reset the password automatically.

### Step 3: Login

Use:
- **Username**: `admin`
- **Password**: `Admin@123`

---

## ✅ Solution 3: Use Reset Command (Alternative)

If you have shell access, you can use:

```bash
python manage.py reset_admin
```

This will reset the password to the default.

---

## 🔍 Troubleshooting

### Still Can't Login?

1. **Check Render Logs**: Look for messages about user creation
2. **Verify Environment Variables**: Make sure you're not overriding defaults
3. **Try the Setup Endpoint**: Use Solution 1 above
4. **Check Username**: Make sure you're using exactly `admin` (case-sensitive)

### Wrong Credentials?

The default credentials are:
- **Username**: `admin` (lowercase, no spaces)
- **Password**: `Admin@123` (case-sensitive: capital A, @ symbol, numbers)

### User Already Exists Error?

The updated code now **resets the password** even if the user exists, so this shouldn't be an issue anymore.

---

## 📝 What Changed

The code has been updated to:
- ✅ Reset password even if user exists
- ✅ Use proper password hashing (`set_password()`)
- ✅ Ensure user has superuser and staff permissions
- ✅ Update email if changed

---

**After using any solution above, you should be able to login!** 🎉
