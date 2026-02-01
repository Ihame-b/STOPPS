# Render.com Deployment Checklist

## ✅ Project Structure Verification

Your project structure is correct for Render deployment:

```
stoppsDjangoApp-main/
├── manage.py                    ✅ Must be at root
├── requirements.txt             ✅ All dependencies listed
├── Procfile                     ✅ Gunicorn start command
├── runtime.txt                  ✅ Python version specified
├── render.yaml                  ✅ Optional: Auto-configuration
├── ecomproject/                 ✅ Django project folder
│   ├── __init__.py
│   ├── settings.py
│   ├── wsgi.py                  ✅ WSGI application
│   └── urls.py
├── ecomapp/                     ✅ Django app
│   ├── __init__.py
│   └── ...
├── static/                      ✅ Static files
├── templates/                   ✅ Templates
└── media/                       ✅ Media files (user uploads)
```

## 🔧 Render Configuration Settings

### In Render Dashboard → Your Web Service → Settings:

1. **Name**: `stopps-ecommerce` (or your choice)
2. **Region**: Choose closest to you
3. **Branch**: `main` (or your active branch)
4. **Root Directory**: ⚠️ **LEAVE EMPTY** (or blank)
5. **Runtime**: `Python 3`
6. **Build Command**: 
   ```
   pip install -r requirements.txt && python manage.py collectstatic --noinput
   ```
7. **Start Command**: 
   ```
   gunicorn ecomproject.wsgi:application
   ```

## 🔑 Environment Variables (Required)

Go to **Environment** tab and add:

1. **SECRET_KEY**: 
   - Generate: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - Or use: `)!7)jy&mv@^4&tlh6n6ccy-2nlyzd2uo+5c4dgmppsmm@b_=7&`

2. **DEBUG**: `False`

3. **ALLOWED_HOSTS**: 
   - Your Render URL: `your-app-name.onrender.com`
   - Or: `*.onrender.com` (allows any Render subdomain)

4. **DATABASE_URL**: 
   - Get from PostgreSQL database dashboard
   - Use "Internal Database URL" if same region

## 🗄️ PostgreSQL Database Setup

1. **Create Database**:
   - Render Dashboard → "New +" → "PostgreSQL"
   - Name: `stopps-db`
   - Region: Same as web service
   - Plan: Free (for testing)

2. **Get Connection String**:
   - Database Dashboard → "Connections"
   - Copy "Internal Database URL"

3. **Add to Environment Variables**:
   - Key: `DATABASE_URL`
   - Value: Paste the Internal Database URL

## 📦 Required Packages (Already in requirements.txt)

✅ `Django>=4.2,<5.0`
✅ `gunicorn` - Production server
✅ `whitenoise` - Static files serving
✅ `psycopg2-binary` - PostgreSQL adapter
✅ `dj-database-url>=2.0.0` - Database URL parsing
✅ `Pillow>=10.0` - Image processing
✅ `python-dotenv>=1.0` - Environment variables

## 🚀 Deployment Steps

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### Step 2: Create Web Service on Render
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure using settings above

### Step 3: Create PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Configure and create
3. Copy Internal Database URL

### Step 4: Add Environment Variables
Add all required environment variables listed above

### Step 5: Deploy
Click "Create Web Service" and wait for deployment

### Step 6: Run Migrations
1. Go to your service → "Shell" tab
2. Run:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'app'"
**Solution**: 
- Check Start Command is: `gunicorn ecomproject.wsgi:application`
- Verify Root Directory is **EMPTY**
- Ensure `ecomproject/wsgi.py` exists

### Error: "No module named 'dj_database_url'"
**Solution**: 
- Verify `dj-database-url>=2.0.0` is in requirements.txt
- Rebuild the service

### Error: "Database connection failed"
**Solution**:
- Verify `DATABASE_URL` environment variable is set
- Check database is not paused (free tier)
- Use Internal Database URL (not External)

### Error: "Static files not found"
**Solution**:
- Verify Build Command includes: `python manage.py collectstatic --noinput`
- Check `STATIC_ROOT` is set in settings.py
- Ensure `whitenoise` is in requirements.txt

### Error: "500 Internal Server Error"
**Solution**:
- Check logs in Render dashboard
- Verify all environment variables are set
- Check database migrations are run
- Verify `DEBUG=False` and `ALLOWED_HOSTS` is correct

## ✅ Verification Checklist

Before deploying, verify:

- [ ] `manage.py` is at project root
- [ ] `ecomproject/wsgi.py` exists
- [ ] `requirements.txt` has all packages
- [ ] `Procfile` has correct start command
- [ ] `runtime.txt` specifies Python version
- [ ] `SECRET_KEY` environment variable is set
- [ ] `DEBUG=False` in production
- [ ] `ALLOWED_HOSTS` includes your Render URL
- [ ] `DATABASE_URL` is set (if using PostgreSQL)
- [ ] Static files configuration is correct
- [ ] All migrations are ready

## 📝 Quick Reference

**Start Command**: `gunicorn ecomproject.wsgi:application`
**Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
**Root Directory**: (leave empty)
**Python Version**: 3.10.12 (in runtime.txt)

---

**Your project is properly structured for Render deployment!** 🎉
