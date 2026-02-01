# 🚀 Quick Deployment Instructions

Your Django project is now ready for deployment! Follow these steps:

## Step 1: Push to GitHub

1. **Create a new repository on GitHub:**
   - Go to https://github.com/new
   - Name it (e.g., `stopps-ecommerce`)
   - Don't initialize with README
   - Click "Create repository"
2. **Push your code:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Deploy on Render.com (FREE)

1. **Sign up at [render.com](https://render.com)** using your GitHub account

2. **Create a Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure the service:**
   - **Name**: `stopps-ecommerce` (or your choice)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python manage.py collectstatic --noinput
     ```
   - **Start Command**: 
     ```
     gunicorn ecomproject.wsgi:application
     ```

4. **Add PostgreSQL Database:**
   - In Render dashboard, click "New +" → "PostgreSQL"
   - Name it (e.g., `stopps-db`)
   - Copy the `Internal Database URL` (you'll need it)

5. **Add Environment Variables:**
   Click "Environment" tab and add:
   
   - `SECRET_KEY`: Generate one using:
     ```bash
     python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   
   - `DEBUG`: `False`
   
   - `ALLOWED_HOSTS`: `your-app-name.onrender.com` (replace with your actual Render URL)
   
   - `DATABASE_URL`: Paste the Internal Database URL from step 4

6. **Click "Create Web Service"**

## Step 3: Run Migrations

After deployment:

1. Go to your service in Render dashboard
2. Click "Shell" tab
3. Run:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

## Step 4: Access Your Site

Your site will be live at: `https://your-app-name.onrender.com`

## Important Notes

✅ **Static files** are handled automatically by WhiteNoise  
⚠️ **Media files** (uploaded images) need external storage:
   - Use Cloudinary (free tier available)
   - Or AWS S3 (free tier for 12 months)

✅ **Database** will be PostgreSQL (automatically configured)  
✅ **HTTPS** is enabled automatically  
✅ **Auto-deploy** from GitHub on every push

## Troubleshooting

- **Build fails**: Check build logs in Render dashboard
- **500 errors**: Check logs for database connection issues
- **Static files not loading**: Ensure `collectstatic` is in build command
- **Database errors**: Verify DATABASE_URL is set correctly

## Next Steps

1. Set up media file storage (Cloudinary recommended)
2. Configure custom domain (optional)
3. Set up email service for production
4. Monitor your app in Render dashboard

---

**Your project is ready! Just push to GitHub and deploy on Render! 🎉**
