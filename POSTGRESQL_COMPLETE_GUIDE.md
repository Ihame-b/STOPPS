# PostgreSQL Complete Guide for STOPPS Project

## 📋 Table of Contents
1. [Overview](#overview)
2. [Current Configuration](#current-configuration)
3. [Local Development Setup](#local-development-setup)
4. [Production Setup (Render.com)](#production-setup-rendercom)
5. [Database Configuration Details](#database-configuration-details)
6. [Migrations](#migrations)
7. [Troubleshooting](#troubleshooting)
8. [Connection Details](#connection-details)

---

## Overview

This project uses **PostgreSQL** as the database backend. The configuration automatically switches between:
- **Local Development**: Uses local PostgreSQL database
- **Production**: Uses `DATABASE_URL` environment variable from hosting platform

---

## Current Configuration

### Database Settings Location
- **File**: `ecomproject/settings.py` (lines 97-136)
- **Engine**: `django.db.backends.postgresql`
- **Adapter**: `psycopg2-binary` (PostgreSQL adapter for Python)

### Required Packages
- ✅ `psycopg2-binary` - PostgreSQL adapter (already in requirements.txt)
- ⚠️ `dj-database-url` - For parsing DATABASE_URL (needs to be added)

---

## Local Development Setup

### Database Connection Details (Local)
- **Database Name**: `STOPPS`
- **User**: `postgres`
- **Password**: `ihame12`
- **Host**: `localhost`
- **Port**: `5432`

### Steps to Set Up Local PostgreSQL

1. **Install PostgreSQL** (if not installed):
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib
   
   # Check if running
   sudo service postgresql status
   ```

2. **Create Database**:
   ```bash
   sudo -u postgres psql
   ```
   Then in PostgreSQL prompt:
   ```sql
   CREATE DATABASE STOPPS;
   \q
   ```

3. **Set Password** (if needed):
   ```bash
   sudo -u postgres psql
   ```
   ```sql
   ALTER USER postgres WITH PASSWORD 'ihame12';
   \q
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

---

## Production Setup (Render.com)

### Step 1: Create PostgreSQL Database on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** button (top right)
3. Select **"PostgreSQL"** from dropdown
4. Configure:
   - **Name**: `stopps-db` (or your preferred name)
   - **Database**: (auto-generated or custom)
   - **User**: (auto-generated)
   - **Region**: Choose same region as your web service
   - **PostgreSQL Version**: Latest stable (recommended)
   - **Plan**: Select plan (Free tier available for testing)
5. Click **"Create Database"**

### Step 2: Get Database URL

After database is created:

1. Go to your database dashboard
2. Find **"Connections"** section
3. Copy **"Internal Database URL"** (for services in same region)
   - OR **"External Database URL"** (for external connections)
4. Format will be:
   ```
   postgresql://username:password@hostname:5432/database_name
   ```

### Step 3: Add DATABASE_URL Environment Variable

1. Go to your **Web Service** in Render dashboard
2. Click **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Add:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the Internal Database URL from Step 2
5. Click **"Save Changes"**

### Step 4: Add Required Package

Make sure `dj-database-url` is in `requirements.txt`:

```txt
dj-database-url>=2.0.0
```

If not present, add it:
```bash
echo "dj-database-url>=2.0.0" >> requirements.txt
```

### Step 5: Run Migrations on Production

After deployment:

1. Go to your service in Render dashboard
2. Click **"Shell"** tab
3. Run:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

---

## Database Configuration Details

### How It Works

The `settings.py` file automatically detects the environment:

```python
# Check if DATABASE_URL exists (production)
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Production: Use DATABASE_URL from environment
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600
        )
    }
else:
    # Development: Use local PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'STOPPS',
            'USER': 'postgres',
            'PASSWORD': 'ihame12',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
```

### Environment Variables

**Production (Render.com):**
- `DATABASE_URL` - Full PostgreSQL connection string

**Development (Optional - can override defaults):**
- `DB_USER` - Database user (default: `postgres`)
- `DB_PASSWORD` - Database password (default: `ihame12`)
- `DB_HOST` - Database host (default: `localhost`)
- `DB_PORT` - Database port (default: `5432`)
- `DB_NAME` - Database name (default: `STOPPS`)

---

## Migrations

### Run Migrations Locally
```bash
python manage.py migrate
```

### Run Migrations on Production (Render)
1. Go to Render dashboard → Your service
2. Click **"Shell"** tab
3. Run:
   ```bash
   python manage.py migrate
   ```

### Create New Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Check Migration Status
```bash
python manage.py showmigrations
```

---

## Troubleshooting

### ❌ "relation does not exist" Error
**Solution**: Run migrations
```bash
python manage.py migrate
```

### ❌ "password authentication failed"
**Solutions**:
1. Verify PostgreSQL password is `ihame12` (for local)
2. Check PostgreSQL is running:
   ```bash
   sudo service postgresql status
   ```
3. For production: Verify `DATABASE_URL` is correct

### ❌ "database does not exist"
**Solutions**:
1. **Local**: Create database:
   ```bash
   sudo -u postgres psql
   CREATE DATABASE STOPPS;
   ```
2. **Production**: Verify database was created on Render

### ❌ "could not connect to server"
**Solutions**:
1. Check PostgreSQL service is running:
   ```bash
   sudo service postgresql start
   sudo service postgresql status
   ```
2. Verify host/port settings
3. Check firewall settings

### ❌ "ModuleNotFoundError: No module named 'dj_database_url'"
**Solution**: Add to requirements.txt and install:
```bash
echo "dj-database-url>=2.0.0" >> requirements.txt
pip install dj-database-url
```

### ❌ "psycopg2" Import Error
**Solution**: Install psycopg2-binary:
```bash
pip install psycopg2-binary
```

### ❌ Database Connection Timeout (Production)
**Solutions**:
1. Use **Internal Database URL** (not External) if services are in same region
2. Check database is not paused (free tier databases pause after inactivity)
3. Verify `DATABASE_URL` environment variable is set correctly

---

## Connection Details

### Local Development
```
Engine: django.db.backends.postgresql
Name: STOPPS
User: postgres
Password: ihame12
Host: localhost
Port: 5432
```

### Production (Render.com)
```
Format: postgresql://username:password@hostname:5432/database_name
Source: DATABASE_URL environment variable
Auto-configured: Yes (via dj-database-url)
```

---

## Important Notes

1. ✅ **Never commit sensitive data** - Use environment variables
2. ✅ **Use PostgreSQL in production** - SQLite is for development only
3. ✅ **Run migrations after deployment** - Always migrate on production
4. ✅ **Backup database regularly** - Especially before major changes
5. ✅ **Use Internal Database URL** - For services in same region (faster, more secure)

---

## Quick Reference Commands

```bash
# Check database connection
python manage.py check --database default

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Show migrations
python manage.py showmigrations

# Check PostgreSQL status (local)
sudo service postgresql status

# Start PostgreSQL (local)
sudo service postgresql start

# Access PostgreSQL shell (local)
sudo -u postgres psql

# List databases (in psql)
\l

# Connect to database (in psql)
\c STOPPS

# Exit psql
\q
```

---

**Your PostgreSQL database is configured and ready!** 🎉
