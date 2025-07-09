# Antibody Requests Management System

A Django-based web application for managing antibody requests, studies, and related data in a research laboratory setting.

## Features

- **Request Management**: Create, view, edit, and search antibody requests
- **Data Management**: Manage requestors, antibodies, tissues, statuses, and studies
- **Search Functionality**: Advanced search with multiple filters
- **Responsive Design**: Bootstrap-based UI that works on desktop and mobile
- **Field Truncation**: All display fields are truncated to 40 characters for clean table views

## Models

- **Request**: Main request entity with relationships to other models
- **Requestor**: People who submit requests
- **Antibody**: Antibody information including vendor, species, etc.
- **Study**: Research studies associated with requests
- **Tissue**: Tissue types for requests
- **Status**: Request status tracking

## Technology Stack

- **Backend**: Django 5.2.3
- **Database**: PostgreSQL
- **Frontend**: Bootstrap 5, Font Awesome
- **Python**: 3.10+

## Installation

### 1. **Install Dependencies**

```bash
sudo apt upgrade
sudo apt install python3.12 postgresql postgresql-contrib python3.12-venv pip3
```

### 2. **Set Up PostgreSQL Database**

```bash

sudo -u postgres psql
------------------------------------------------------------------------------
CREATE DATABASE antibody_requests_db;

CREATE USER myuser WITH PASSWORD 'mypassword';

\c antibody_requests_db

GRANT ALL PRIVILEGES ON DATABASE antibody_requests_db TO myuser;

GRANT ALL PRIVILEGES ON SCHEMA public TO myuser;
```

### 3. **Clone the Repository**

```bash
git clone https://github.com/nick0h/dbmanage.git
cd dbmanage
```

### 4. **Run the Installation Script**

```bash
chmod +x install.sh
./install.sh
```

The installation script will automatically:
- Create a Python virtual environment
- Install required dependencies
- Run database migrations
- Optionally create a superuser account
- Collect static files
- Set up environment variables

### 5. **Start the Development Server**

```bash
./run.sh
```

Or manually:
```bash
source venv/bin/activate
python manage.py runserver
```

The application will be available at: **http://localhost:8000**

## Usage

### Main Pages

- **Home** (`/`): Main dashboard with navigation options
- **New Request** (`/requests/create/`): Create a new antibody request
- **Search Requests** (`/requests/search/`): Search and filter existing requests
- **All Requests** (`/requests/`): View all requests with pagination
- **Data Management** (`/data/`): Manage system data (requestors, antibodies, etc.)

### Data Management

The system includes management pages for:
- **Requestors**: People who submit requests
- **Antibodies**: Antibody catalog with detailed information
- **Tissues**: Tissue types for requests
- **Statuses**: Request status tracking
- **Studies**: Research studies

Each section provides:
- List view with truncated fields (40 characters max)
- Add new items
- Edit existing items
- Navigation back to home and data management

## Database Configuration

The application is configured to use PostgreSQL. Update the database settings in `antibody_requests/settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "antibody_requests_db",
        "USER": "myuser",
        "PASSWORD": "mypassword",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

## Project Structure

```
dbProj/
├── antibody_requests/          # Main Django project
│   ├── settings.py            # Project settings
│   ├── urls.py                # Main URL configuration
│   └── wsgi.py                # WSGI configuration
├── requests_app/              # Main application
│   ├── models.py              # Database models
│   ├── views.py               # View logic
│   ├── forms.py               # Form definitions
│   ├── urls.py                # App URL configuration
│   └── templates/             # HTML templates
│       └── requests_app/      # App-specific templates
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore file
└── README.md                  # This file
```

## Features in Detail

### Request Management
- Create requests with description, special requests, and tissue selection
- Edit request status and add notes
- Search by request ID, date range, requestor, tissue, and study
- Pagination for large datasets

### Data Management
- CRUD operations for all data entities
- Form validation and sanitization
- Consistent UI with Bootstrap styling
- Navigation breadcrumbs

### Search and Filtering
- Multiple search criteria
- Date range filtering
- Dropdown selections for related data
- Real-time search results

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the repository or contact the development team. 