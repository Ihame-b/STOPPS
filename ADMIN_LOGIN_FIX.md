# Fix Admin Login - Step by Step

## 🔑 Correct Credentials

The default credentials are:
- **Username**: `admin` (all lowercase, no spaces)
- **Password**: `Admin@123` (case-sensitive: capital A, @ symbol, numbers)

## ✅ Quick Fix Options

### Option 1: Use Reset Page (Easiest)

1. Visit: `https://stop-v8rq.onrender.com/reset-admin/`
2. Click the "Reset Admin Password" button
3. Wait for success message
4. Use the credentials shown to login

### Option 2: Use API Endpoint

**Method A: GET request (see credentials)**
Visit in browser:
```
https://stop-v8rq.onrender.com/setup/create-admin/
```

**Method B: POST request (reset password)**
Using curl:
```bash
curl -X POST https://stop-v8rq.onrender.com/setup/create-admin/
```

Or use a browser extension like "REST Client" to send POST request.

### Option 3: Update Start Command

1. Go to Render Dashboard → Your Service → Settings
2. Update Start Command to:
   ```
   python manage.py migrate && python manage.py create_admin && gunicorn ecomproject.wsgi:application
   ```
3. Save and wait for redeployment
4. Login with: `admin` / `Admin@123`

## ⚠️ Common Mistakes

1. **Username**: Must be exactly `admin` (lowercase)
   - ❌ Wrong: `Admin`, `ADMIN`, ` admin ` (with spaces)
   - ✅ Correct: `admin`

2. **Password**: Must be exactly `Admin@123` (case-sensitive)
   - ❌ Wrong: `admin@123`, `Admin123`, `admin@123`
   - ✅ Correct: `Admin@123` (capital A, @, numbers)

3. **Login URL**: Make sure you're using the right URL
   - Django Admin: `https://stop-v8rq.onrender.com/admin/`
   - Custom Admin: `https://stop-v8rq.onrender.com/admin-login/`

## 🔍 Verify User Exists

If you have access to logs, check for:
- "Successfully created superuser" message
- "Updated existing user" message
- Any error messages

## 📝 If Still Not Working

1. **Push latest code**:
   ```bash
   git push origin main
   ```

2. **Wait for deployment** (2-3 minutes)

3. **Visit reset page**: `https://stop-v8rq.onrender.com/reset-admin/`

4. **Click reset button**

5. **Try login again** with exact credentials:
   - Username: `admin`
   - Password: `Admin@123`

## 🎯 Exact Steps to Login

1. Go to: `https://stop-v8rq.onrender.com/admin/`
2. Enter:
   - Username: `admin` (type it exactly, lowercase)
   - Password: `Admin@123` (capital A, @, numbers)
3. Click "Log in"

If it still doesn't work, the user might not exist. Use the reset page to create it.

---

**Remember**: Both username and password are case-sensitive! 🔒
