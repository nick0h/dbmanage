# Deployment Guide

Installation, configuration, and maintenance for the Histopathology Requests Management System.

## System Requirements

| Component | Minimum |
|-----------|---------|
| OS | Linux (Ubuntu 20.04+), macOS, or WSL |
| Python | 3.10+ |
| PostgreSQL | 12+ |
| RAM | 512 MB (development), 2 GB+ (production) |
| Disk | 1 GB |

## Fresh Installation

### Step 1: System Dependencies

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip postgresql postgresql-contrib
```

### Step 2: Database Setup

Run the database setup script (requires postgres user access):

```bash
chmod +x setup_database.sh
./setup_database.sh
```

This creates:

| Setting | Default Value |
|---------|--------------|
| Database | `antibody_requests_db` |
| User | `myuser` |
| Password | `mypassword` |
| Host | `localhost` |
| Port | `5432` |

To customize, edit `setup_database.sh` and the `DATABASES` block in `antibody_requests/settings.py` to match.

Manual setup alternative:

```sql
CREATE DATABASE antibody_requests_db;
CREATE USER myuser WITH PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE antibody_requests_db TO myuser;
\c antibody_requests_db
GRANT ALL PRIVILEGES ON SCHEMA public TO myuser;
```

### Step 3: Application Setup

```bash
chmod +x install.sh
./install.sh
```

The install script:

1. Creates a Python virtual environment (`venv/`)
2. Installs dependencies from `requirements.txt`
3. Runs database migrations
4. Optionally creates a Django superuser
5. Collects static files
6. Creates a `.env` file (if missing)
7. Creates `run.sh` for starting the dev server

### Step 4: Email Configuration

Copy the example environment file and set your credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```env
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
ADMIN_EMAIL=admin@yourdomain.com
```

For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) rather than your account password.

### Step 5: Start the Server

```bash
./run.sh
```

Or manually:

```bash
source venv/bin/activate
python manage.py runserver
```

Visit **http://localhost:8000**.

## Updating an Existing Installation

```bash
chmod +x update.sh
./update.sh
```

This script activates the virtual environment, pulls any git changes, installs updated dependencies, runs migrations, and collects static files.

## Production Deployment

### Settings Checklist

Before deploying to production, update `antibody_requests/settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
SECRET_KEY = os.getenv('SECRET_KEY')  # Generate a new key; never commit it
```

Generate a secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Move all sensitive values to environment variables or `.env`:

- `SECRET_KEY`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- Database credentials

### Static Files

```bash
python manage.py collectstatic --noinput
```

Static files are collected to `staticfiles/` (configured via `STATIC_ROOT`).

### WSGI Server (Gunicorn)

Gunicorn is included in `requirements.txt`:

```bash
source venv/bin/activate
gunicorn antibody_requests.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

For production, place Nginx or Apache in front of Gunicorn for SSL termination and static file serving.

Example Nginx location block:

```nginx
location /static/ {
    alias /path/to/dbProj/staticfiles/;
}

location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

### Database Backups

```bash
pg_dump -U myuser -h localhost antibody_requests_db > backup_$(date +%Y%m%d).sql
```

Restore:

```bash
psql -U myuser -h localhost antibody_requests_db < backup_20250623.sql
```

## Maintenance Commands

| Task | Command |
|------|---------|
| Create superuser | `python manage.py createsuperuser` |
| Run migrations | `python manage.py migrate` |
| Make migrations | `python manage.py makemigrations` |
| Collect static | `python manage.py collectstatic` |
| Django shell | `python manage.py shell` |
| Test email | Visit `/email-test/` as a staff user |

## Troubleshooting

### Database connection refused

- Verify PostgreSQL is running: `pg_isready -h localhost -p 5432`
- Check credentials in `settings.py` match your database setup
- Ensure `pg_hba.conf` allows password authentication for local connections

### Migration errors

```bash
python manage.py showmigrations
python manage.py migrate --plan
```

If migrations are out of sync, check for unapplied migrations and run `./update.sh`.

### Static files not loading

```bash
python manage.py collectstatic --noinput
```

In development, Django serves static files automatically when `DEBUG = True`. In production, configure your web server to serve the `staticfiles/` directory.

### Email not sending

1. Verify `.env` credentials are set correctly
2. Visit `/email-test/` (staff login required) to send a test email
3. Check Django logs for SMTP errors
4. For Gmail, ensure "Less secure app access" is off and an App Password is used

### NotificationSettings reload warning

If you see `Model 'requests_app.notificationsettings' was already registered`, the `NotificationSettings` model is defined twice in `models.py`. Remove the duplicate definition to fix this.

## File Reference

| File | Purpose |
|------|---------|
| `install.sh` | First-time project setup |
| `setup_database.sh` | PostgreSQL database and user creation |
| `update.sh` | Apply updates on existing installations |
| `run.sh` | Start development server (created by install.sh) |
| `.env.example` | Template for environment variables |
| `requirements.txt` | Python package dependencies |
