#!/bin/bash

# IHC Requests System - Installation Script
# This script will set up the Django project and get it running

set -e  # Exit on any error

echo "=========================================="
echo "IHC Requests System - Installation Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3 is installed
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION found"

# Check if pip is installed
print_status "Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3."
    exit 1
fi

print_success "pip3 found"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install requirements
print_status "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Dependencies installed from requirements.txt"
else
    print_warning "requirements.txt not found, installing basic Django dependencies..."
    pip install django psycopg2-binary
    print_success "Basic dependencies installed"
fi

# Check if PostgreSQL is running (for production setup)
print_status "Checking database setup..."
if command -v psql &> /dev/null; then
    print_success "PostgreSQL found"
    print_warning "Make sure PostgreSQL is running and the database 'antibody_requests_db' exists"
    print_warning "You may need to create the database manually:"
    echo "  sudo -u postgres createdb antibody_requests_db"
    echo "  sudo -u postgres createuser myuser"
    echo "  sudo -u postgres psql -c \"ALTER USER myuser WITH PASSWORD 'mypassword';\""
    echo "  sudo -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE antibody_requests_db TO myuser;\""
else
    print_warning "PostgreSQL not found. For production, install PostgreSQL:"
    echo "  Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib"
    echo "  CentOS/RHEL: sudo yum install postgresql postgresql-server"
    echo "  macOS: brew install postgresql"
fi

# Run Django migrations
print_status "Running Django migrations..."
python manage.py makemigrations
python manage.py migrate
print_success "Database migrations completed"

# Create superuser (optional)
echo ""
print_status "Would you like to create a superuser account? (y/n)"
read -r create_superuser
if [[ $create_superuser =~ ^[Yy]$ ]]; then
    print_status "Creating superuser..."
    python manage.py createsuperuser
    print_success "Superuser created"
else
    print_warning "You can create a superuser later with: python manage.py createsuperuser"
fi

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput
print_success "Static files collected"

# Set up environment variables
print_status "Setting up environment variables..."
if [ ! -f ".env" ]; then
    cat > .env << EOF
# Django Settings
DEBUG=True
SECRET_KEY=django-insecure-%_ekxhi34pfn5u1m%jyw=b3dli5khv%ulzy#hhn#q@v+cgu82#
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_NAME=antibody_requests_db
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=localhost
DB_PORT=5432
EOF
    print_success "Environment file (.env) created"
else
    print_status "Environment file (.env) already exists"
fi

# Create a run script
print_status "Creating run script..."
cat > run.sh << 'EOF'
#!/bin/bash

# IHC Requests System - Run Script
echo "Starting IHC Requests System..."

# Activate virtual environment
source venv/bin/activate

# Run Django development server
python manage.py runserver 0.0.0.0:8000
EOF

chmod +x run.sh
print_success "Run script (run.sh) created"

# Create a production setup script
print_status "Creating production setup script..."
cat > setup_production.sh << 'EOF'
#!/bin/bash

# Production Setup Script for IHC Requests System

echo "Setting up production environment..."

# Update settings for production
sed -i 's/DEBUG = True/DEBUG = False/' antibody_requests/settings.py

# Set allowed hosts for production
echo "Please update ALLOWED_HOSTS in antibody_requests/settings.py with your domain"

# Install production dependencies
pip install gunicorn

echo "Production setup complete!"
echo "To run in production: gunicorn antibody_requests.wsgi:application"
EOF

chmod +x setup_production.sh
print_success "Production setup script (setup_production.sh) created"

# Final instructions
echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
print_success "Your IHC Requests System is ready to run!"
echo ""
echo "To start the development server:"
echo "  ./run.sh"
echo ""
echo "Or manually:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "The application will be available at:"
echo "  http://localhost:8000"
echo ""
echo "Admin interface:"
echo "  http://localhost:8000/admin"
echo ""
print_warning "For production deployment, run: ./setup_production.sh"
echo ""
echo "==========================================" 