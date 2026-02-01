# Default Admin Credentials for Testing

## 🔑 Default Login Credentials

These credentials are automatically created when you deploy to Render (if no environment variables are set):

- **Username**: `admin`
- **Email**: `admin@stopps.com`
- **Password**: `Admin@123`

## 📍 Login URLs

- **Django Admin Panel**: `https://your-app.onrender.com/admin/`
- **Custom Admin Login**: `https://your-app.onrender.com/admin-login/`

## ⚠️ Important Security Notes

1. **Change Password Immediately**: These are default credentials for testing. Change the password after first login in production.

2. **Set Environment Variables**: For production, set these environment variables in Render:
   - `ADMIN_USERNAME` - Your custom username
   - `ADMIN_EMAIL` - Your email address
   - `ADMIN_PASSWORD` - A strong, secure password

3. **Default Behavior**: If environment variables are NOT set, the system will use the defaults above.

## 🚀 Quick Start

1. Deploy your app to Render
2. Update Start Command to: `python manage.py migrate && python manage.py create_admin && gunicorn ecomproject.wsgi:application`
3. Wait for deployment
4. Login with the default credentials above
5. **Change the password immediately!**

---

**For Testing Only** - Use strong credentials in production! 🔒
