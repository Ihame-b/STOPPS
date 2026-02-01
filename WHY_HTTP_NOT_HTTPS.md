# Why Django Development Server Uses HTTP (Not HTTPS)

## The Short Answer

Django's built-in `runserver` command **does not support HTTPS** by default. It's designed for local development only and doesn't handle SSL/TLS certificates.

## Why HTTP in Development?

1. **Simplicity**: HTTP is simpler for local development - no certificates needed
2. **Performance**: No SSL overhead during development
3. **Standard Practice**: Most developers use HTTP locally, HTTPS in production
4. **Django Design**: The `runserver` command is intentionally lightweight for development

## Your Current Settings

Looking at your `settings.py`, you have:
```python
# Production security settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True  # Forces HTTPS in production
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # ... other HTTPS settings
```

This means:
- **Development (DEBUG=True)**: HTTP is allowed ✅
- **Production (DEBUG=False)**: HTTPS is enforced ✅

## Options to Enable HTTPS in Development

If you **really need HTTPS** for development, you have these options:

### Option 1: Use django-extensions (Recommended)
```bash
pip install django-extensions
python manage.py runserver_plus --cert-file cert.pem
```

### Option 2: Use a Reverse Proxy (nginx)
Set up nginx to handle SSL and proxy to Django

### Option 3: Use a Production Server (Gunicorn + SSL)
Configure Gunicorn with SSL certificates

### Option 4: Use ngrok or similar
Tunnel your local server with HTTPS support

## Recommendation

**For development**: Use HTTP (current setup) ✅
- Faster
- Simpler
- Standard practice
- No certificate management

**For production**: Use HTTPS (already configured) ✅
- Your settings already enforce HTTPS in production
- When you deploy, HTTPS will be enabled automatically

## Do You Need HTTPS in Development?

Most developers don't need HTTPS locally because:
- You're testing on your own machine
- No sensitive data transmission
- Faster development workflow

**However**, if you need HTTPS for:
- Testing payment integrations
- Testing OAuth/SSO flows
- Testing specific HTTPS-only features

Then I can help you set it up!
