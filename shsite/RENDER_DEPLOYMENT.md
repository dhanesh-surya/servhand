# Deployment Guide: Render.com

## Step 1: Prepare Your Repository

1. **Push your code to GitHub** if you haven't already:
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

## Step 2: Create a Render Account

1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account (recommended for easier deployment)
3. Authorize Render to access your GitHub repositories

## Step 3: Deploy Your Service

### Option A: Using render.yaml (Recommended)

1. Go to Render Dashboard
2. Click **"New +"** → **"Web Service"**
3. Select **"Connect a Repository"** and choose `servicehands.git`
4. Render will auto-detect `render.yaml` and use the configuration
5. Click **"Create Web Service"**

### Option B: Manual Configuration

1. Go to Render Dashboard
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Set the following:
   - **Name:** servicehands
   - **Environment:** Python 3
   - **Build Command:** 
     ```
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - **Start Command:** 
     ```
     gunicorn shsite.wsgi:application
     ```
   - **Plan:** Free (or Pro for better performance)

## Step 4: Configure Environment Variables

1. In Render Dashboard, go to your service
2. Click **"Environment"**
3. Add the following variables:
   - `DEBUG` = `False`
   - `SECRET_KEY` = Generate a new secret key (use Django shell or [djecrety.ir](https://djecrety.ir))
   - `ALLOWED_HOSTS` = `servicehands.onrender.com,yourdomain.com`
   - `DATABASE_URL` = (will be auto-set if using PostgreSQL)
   - `EMAIL_HOST_USER` = Your email
   - `EMAIL_HOST_PASSWORD` = Your app-specific password
   - Other email settings as needed

## Step 5: Create a PostgreSQL Database (Optional but Recommended)

1. In Render Dashboard, click **"New +"** → **"PostgreSQL"**
2. Name it: `servicehands-postgres`
3. Select **"Free"** plan
4. Click **"Create Database"**
5. Copy the connection string and set it as `DATABASE_URL` in your service's environment

## Step 6: Update Django Settings for Production

The included `shsite/settings.py` should be updated with environment variable support. Replace your current settings.py with the production version provided in the configuration files.

## Step 7: Deploy & Monitor

1. Render will automatically deploy your service
2. Check the **"Logs"** tab to monitor deployment
3. Once deployment is complete, visit your service URL (e.g., `servicehands.onrender.com`)

## Important Notes

### Security
- ✅ Never commit `.env` file to GitHub
- ✅ Use environment variables for sensitive data
- ✅ Update SECRET_KEY for production
- ✅ Set DEBUG to False in production

### Static Files
- The `whitenoise` package is included to serve static files in production
- Run `python manage.py collectstatic` before deployment

### Database
- **Free Plan:** SQLite will be reset when the service restarts
- **Recommended:** Use PostgreSQL for persistent data storage
- The `dj-database-url` package is included for easy database URL configuration

### Email
- For Gmail: Use an [App Password](https://myaccount.google.com/apppasswords)
- Update `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in environment variables

## Troubleshooting

### 500 Error or Import Errors
- Check the **Logs** tab in Render Dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify environment variables are set correctly

### Static Files Not Loading
- Run: `python manage.py collectstatic --noinput`
- Ensure `STATIC_ROOT` is set in settings.py
- Check that `whitenoise` middleware is enabled

### Database Connection Issues
- Verify `DATABASE_URL` is correctly set
- Ensure PostgreSQL database is running
- Check migrations: `python manage.py migrate`

### Deployment Hangs
- Free tier may have limited resources
- Check system logs for memory/CPU issues
- Consider upgrading to Pro plan

## Additional Resources

- [Render Django Deployment Docs](https://render.com/docs/deploy-django)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [dj-database-url Documentation](https://github.com/jacobian/dj-database-url)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

## Next Steps

1. Update `shsite/settings.py` with the production configuration template
2. Generate a new SECRET_KEY and add it to environment variables
3. Push changes to GitHub
4. Deploy on Render
5. Test your application thoroughly
