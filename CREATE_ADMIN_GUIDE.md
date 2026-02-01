# How to Create Admin User on Render

This guide explains how to create a superuser/admin account for your Render-hosted Django app.

## ✅ Two Methods Available

### Method 1: Automatic Creation (Recommended)

The admin user will be created automatically when your service starts.

#### Step 1: Set Environment Variables in Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click your Web Service
3. Go to **Environment** tab
4. Click **"Add Environment Variable"**
5. Add these three variables:

   - **Key**: `ADMIN_USERNAME`
     **Value**: `admin` (or your preferred username)

   - **Key**: `ADMIN_EMAIL`
     **Value**: `admin@example.com` (or your email)

   - **Key**: `ADMIN_PASSWORD`
     **Value**: `your_secure_password` (choose a strong password)

#### Step 2: Update Start Command

1. Go to **Settings** tab
2. Find **"Start Command"**
3. Change it to:
   ```
   python manage.py migrate && python manage.py create_admin && gunicorn ecomproject.wsgi:application
   ```
4. Click **"Save Changes"**

#### Step 3: Wait for Deployment

- Render will automatically restart your service
- Migrations will run
- Admin user will be created automatically
- Service will start normally

#### Step 4: Login

Visit:
- **Django Admin**: `https://your-app.onrender.com/admin/`
- **Custom Admin**: `https://your-app.onrender.com/admin-login/`

Use the credentials you set in environment variables.

---

### Method 2: Manual Creation via URL (Backup)

If Method 1 doesn't work, use this one-time setup endpoint.

#### Step 1: Set Environment Variables

Same as Method 1 - set `ADMIN_USERNAME`, `ADMIN_EMAIL`, and `ADMIN_PASSWORD` in Render.

#### Step 2: Access Setup Endpoint

Send a POST request to:
```
https://your-app.onrender.com/setup/create-admin/
```

**Using curl:**
```bash
curl -X POST https://your-app.onrender.com/setup/create-admin/
```

**Using Python:**
```python
import requests
response = requests.post('https://your-app.onrender.com/setup/create-admin/')
print(response.json())
```

**Using Browser Extension:**
- Install a REST client extension (like "REST Client" for Chrome)
- Create a POST request to the URL above

#### Step 3: Check Response

You should see:
```json
{
  "success": true,
  "message": "Admin user \"admin\" created successfully",
  "username": "admin",
  "email": "admin@example.com",
  "note": "You can now login at /admin/ or /admin-login/"
}
```

#### Step 4: Login

Use the credentials from your environment variables to login.

---

## 🔒 Security Notes

1. **Change Default Password**: If you use the default password (`admin123`), change it immediately after first login.

2. **Strong Password**: Use a strong password for `ADMIN_PASSWORD` environment variable.

3. **One-Time Use**: The setup endpoint will only work once. After a superuser exists, it will return an error.

4. **Environment Variables**: Never commit passwords to Git. Always use environment variables.

---

## 🐛 Troubleshooting

### "Admin user already exists" Error

**Solution**: A superuser already exists. You can:
- Use existing credentials to login
- Or delete the existing user and recreate (not recommended in production)

### "Failed to create admin user" Error

**Possible causes:**
- Database connection issue
- Invalid environment variables
- Database migrations not run

**Solution**: 
1. Check that `DATABASE_URL` is set correctly
2. Verify migrations ran successfully
3. Check Render logs for detailed error messages

### Can't Login After Creation

**Check:**
1. Verify you're using the correct username and password
2. Check that environment variables are set correctly
3. Try resetting the password via Django admin if accessible

---

## 📝 Default Credentials (if no env vars set)

If you don't set environment variables, the system will use:
- **Username**: `admin`
- **Email**: `admin@stopps.com`
- **Password**: `Admin@123`

⚠️ **Important**: These are for testing only. Change the password immediately after first login in production!

---

## ✅ Verification

After setup, verify the admin user was created:

1. Try logging in at `/admin/` or `/admin-login/`
2. If successful, you should see the admin dashboard
3. You can manage users, products, orders, etc.

---

**Your admin user is now ready!** 🎉
