# Histopathology Requests Management System

A Django web application for managing histopathology laboratory requests — staining, embedding, and sectioning — along with supporting reference data (studies, antibodies, probes, tissues, and more).

## Features

- **Three request workflows**: Staining, embedding, and sectioning, each with create, view, edit, search, and history
- **Reference data management**: Requestors, studies, antibodies, probes, tissues, statuses, assignees, and priorities
- **Bulk import**: Excel/CSV import for studies, antibodies, and probes (staff only)
- **Change history**: Audit logs for all request types
- **Email notifications**: Configurable status-based alerts (staff only)
- **Django admin**: Full admin interface for advanced data management
- **Responsive UI**: Bootstrap 5 with custom Borealis theme

## Technology Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 5.2+ |
| Database | PostgreSQL |
| Frontend | Bootstrap 5, Font Awesome |
| Email | SMTP (Gmail-compatible) |
| Python | 3.10+ |

## Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL
- pip

### Installation

```bash
# 1. Set up the database (requires postgres access)
./setup_database.sh

# 2. Install dependencies, run migrations, collect static files
./install.sh

# 3. Start the development server
./run.sh
```

Or manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The application will be available at **http://localhost:8000**.

### Environment Variables

Copy `.env.example` to `.env` and configure email settings:

```bash
cp .env.example .env
```

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for full configuration details.

## Documentation

| Document | Description |
|----------|-------------|
| [User Guide](docs/USER_GUIDE.md) | How to create, search, and manage requests |
| [Developer Guide](docs/DEVELOPER_GUIDE.md) | Architecture, models, URLs, and code structure |
| [Deployment Guide](docs/DEPLOYMENT.md) | Database setup, production deployment, and maintenance |

## Main URLs

| Page | URL |
|------|-----|
| Home | `/` |
| Staining requests (active) | `/staining/current/` |
| New staining request | `/staining/create/` |
| Embedding requests (active) | `/embedding/current/` |
| New embedding request | `/embedding/create/` |
| Sectioning requests (active) | `/sectioning/current/` |
| New sectioning request | `/sectioning/create/` |
| Data management | `/data/` |
| Request history logs | `/logs/` |
| Django admin | `/admin/` |

## Project Structure

```
dbProj/
├── antibody_requests/       # Django project settings and root URLs
├── requests_app/            # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── forms.py             # Form definitions
│   ├── urls.py              # App URL routing
│   ├── admin.py             # Django admin configuration
│   ├── email_utils.py       # Email notification helpers
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JS, and images
├── docs/                    # Project documentation
├── manage.py
├── requirements.txt
├── install.sh               # First-time setup script
├── setup_database.sh        # PostgreSQL setup script
├── update.sh                # Migration and update script
└── run.sh                   # Development server script (created by install.sh)
```

## Scripts

| Script | Purpose |
|--------|---------|
| `setup_database.sh` | Create PostgreSQL database and user |
| `install.sh` | Create venv, install deps, migrate, collect static |
| `update.sh` | Apply migrations and updates on an existing install |
| `run.sh` | Start the development server |

## License

MIT License — see the LICENSE file for details.
