# Creating Django Superuser

## Quick Method

Run this command in your terminal:

```bash
python3 manage.py createsuperuser
```

You will be prompted to enter:
- **Username**: (choose a username, e.g., `admin`)
- **Email address**: (enter your email, e.g., `admin@stopps.com`)
- **Password**: (enter a secure password - it won't be visible as you type)
- **Password (again)**: (confirm your password)

## Example Session

```
$ python3 manage.py createsuperuser
Username: admin
Email address: admin@stopps.com
Password: 
Password (again): 
Superuser created successfully.
```

## After Creating Superuser

1. **Access Admin Panel**: http://127.0.0.1:8000/admin/
2. **Login** with your superuser credentials
3. You'll have full access to manage:
   - Users
   - Products
   - Orders
   - Product Owners
   - Customers
   - Cargo/Transport
   - All other models

## Alternative: Create via Python Shell

If you prefer to create via code:

```python
python3 manage.py shell
```

Then in the shell:
```python
from django.contrib.auth.models import User
User.objects.create_superuser('admin', 'admin@stopps.com', 'your_password')
```

## Important Notes

- **Superuser has full access** to the Django admin panel
- **Keep credentials secure** - don't share your superuser password
- **Use strong passwords** for production
- You can create multiple superusers if needed

## Troubleshooting

### "Username already exists"
- Choose a different username
- Or use an existing superuser account

### "Email already exists"
- Use a different email address
- Or login with existing account

### Can't access admin panel
- Make sure server is running: `python3 manage.py runserver`
- Check URL: http://127.0.0.1:8000/admin/
- Verify you're using correct credentials

---

**Ready to create your superuser? Run the command above!**
