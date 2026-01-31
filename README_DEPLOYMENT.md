# Deployment Guide for STOPPS E-Commerce Project

## Quick Deploy to Render.com

### Step 1: Push to GitHub

1. Initialize git (if not done):
```bash
git init
git add .
git commit -m "Initial commit - Ready for deployment"
```

2. Create a new repository on GitHub and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to [render.com](https://render.com) and sign up with GitHub
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `stopps-ecommerce` (or your choice)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn ecomproject.wsgi:application`

5. **Add Environment Variables** (in Render dashboard):
   - `SECRET_KEY`: Generate using: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `your-app-name.onrender.com` (replace with your actual Render URL)
   - `DATABASE_URL`: (Auto-created by Render when you add PostgreSQL database)

6. **Add PostgreSQL Database**:
   - In Render dashboard, click "New +" → "PostgreSQL"
   - Name it (e.g., `stopps-db`)
   - Copy the `DATABASE_URL` and add it as environment variable

7. Click "Create Web Service"

### Step 3: Run Migrations

After deployment, in Render dashboard:
1. Go to your service
2. Click "Shell"
3. Run:
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Step 4: Handle Media Files

For production, you need to handle uploaded images. Options:

**Option 1: Cloudinary (Recommended - Free tier available)**
1. Sign up at [cloudinary.com](https://cloudinary.com)
2. Add to requirements.txt: `django-cloudinary-storage`
3. Update settings.py to use Cloudinary

**Option 2: AWS S3 (Free tier for 12 months)**
1. Create AWS account
2. Set up S3 bucket
3. Configure django-storages

### Environment Variables Summary

Required for production:
- `SECRET_KEY`: Django secret key
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: Your domain (comma-separated)
- `DATABASE_URL`: PostgreSQL connection string (auto-provided by Render)

Optional (for email):
- `EMAIL_HOST_USER`: Your email
- `EMAIL_HOST_PASSWORD`: Your email password
- `EMAIL_HOST`: SMTP server
- `EMAIL_PORT`: SMTP port

### Important Notes

1. **Never commit sensitive data** - Use environment variables
2. **Static files** - Handled automatically by WhiteNoise
3. **Media files** - Need external storage (Cloudinary/S3)
4. **Database** - Use PostgreSQL in production (SQLite is for development only)

### Troubleshooting

- **Build fails**: Check requirements.txt and build logs
- **Static files not loading**: Ensure `collectstatic` runs in build command
- **Database errors**: Verify DATABASE_URL is set correctly
- **500 errors**: Check logs in Render dashboard
