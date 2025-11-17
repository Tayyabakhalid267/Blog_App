# Deployment Guide

## Important Note About Netlify

**Netlify is designed for static sites and JAMstack applications.** Django is a full Python web framework that requires a server environment to run Python code, which Netlify does not natively support.

### Why Django Won't Work Directly on Netlify

1. **Netlify serves static files only** - It's optimized for HTML/CSS/JS files, not dynamic Python applications
2. **No Python runtime** - Netlify doesn't execute Python server-side code
3. **Database requirements** - Django needs a persistent database connection

### Recommended Deployment Options for Django

#### Option 1: PythonAnywhere (Easiest for beginners)
- **Best for**: Learning, small projects, free tier available
- **Steps**:
  1. Sign up at https://www.pythonanywhere.com
  2. Upload your code via Git or file manager
  3. Configure web app with Django settings
  4. Set up virtual environment
  5. Configure static files
- **Pros**: Free tier, easy setup, great for learning
- **Cons**: Limited resources on free tier

#### Option 2: Heroku (Recommended)
- **Best for**: Production apps, scalability
- **Steps**:
  1. Install Heroku CLI
  2. Create `Procfile` (already included in this project)
  3. Add `requirements.txt` (already included)
  4. Configure environment variables
  5. Deploy: `git push heroku main`
- **Pros**: Easy deployment, add-ons available, scalable
- **Cons**: No free tier anymore (starts at $5/month)

#### Option 3: Railway.app
- **Best for**: Modern deployment, generous free tier
- **Steps**:
  1. Sign up at https://railway.app
  2. Connect your GitHub repository
  3. Railway auto-detects Django
  4. Set environment variables
  5. Deploy automatically
- **Pros**: Free tier with $5 credit/month, modern UI
- **Cons**: Credit-based system

#### Option 4: DigitalOcean App Platform
- **Best for**: Professional deployments
- **Cost**: Starts at $5/month
- **Steps**:
  1. Sign up at DigitalOcean
  2. Create new app from GitHub
  3. Configure build settings
  4. Set environment variables
  5. Deploy
- **Pros**: Professional, scalable, good documentation
- **Cons**: Paid only

#### Option 5: Render
- **Best for**: Free tier with automatic deployments
- **Steps**:
  1. Sign up at https://render.com
  2. Create new Web Service
  3. Connect GitHub repository
  4. Configure: `gunicorn mb_project.wsgi:application`
  5. Set environment variables
  6. Deploy
- **Pros**: Free tier available, automatic SSL
- **Cons**: Free tier may spin down with inactivity

### Converting to JAMstack (If You Must Use Netlify)

If you specifically want to use Netlify, you would need to:

1. **Convert backend to serverless functions** (Netlify Functions)
   - Rewrite Django views as serverless functions
   - Use serverless-friendly database (e.g., FaunaDB, Supabase)
   
2. **Create a static frontend**
   - Use React/Vue/Next.js for the UI
   - Call serverless functions for data
   
3. **This is a complete rewrite** and defeats the purpose of using Django

### Quick Deployment to Heroku (Recommended)

This project is already configured for Heroku with:
- `Procfile` ✓
- `requirements.txt` ✓
- `gunicorn` included ✓

**Steps:**

```bash
# Install Heroku CLI
# Windows: Download from https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create your-message-board

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set DEBUG=False
heroku config:set DISABLE_COLLECTSTATIC=1

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Open app
heroku open
```

### Production Checklist

Before deploying to ANY platform:

- [ ] Change `SECRET_KEY` in settings.py to environment variable
- [ ] Set `DEBUG = False` in production
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Set up proper database (PostgreSQL recommended)
- [ ] Configure static file serving (WhiteNoise)
- [ ] Set up HTTPS/SSL
- [ ] Configure email backend
- [ ] Set up logging
- [ ] Configure CORS if needed
- [ ] Set up monitoring

### Environment Variables Needed

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=your-database-url (for PostgreSQL)
```

### For Local Testing with Production Settings

```bash
# Set environment variables
$env:SECRET_KEY="test-secret-key"
$env:DEBUG="False"

# Run with gunicorn
gunicorn mb_project.wsgi:application
```

## Conclusion

While Netlify is excellent for static sites, Django requires a platform that supports Python execution. Use Heroku, Railway, Render, or PythonAnywhere for deploying this Django application.
