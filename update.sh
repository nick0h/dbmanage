#!/bin/bash

# Update script for Antibody Requests Django Project
# This script handles database migrations, static files, and other updates

set -e  # Exit on any error

echo "=========================================="
echo "Antibody Requests - Database Update Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Database configuration (should match settings.py)
DB_NAME="antibody_requests_db"
DB_USER="myuser"
DB_PASSWORD="mypassword"
DB_HOST="localhost"
DB_PORT="5432"

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

# Check if we're in the correct directory
if [ ! -f "manage.py" ]; then
    print_error "manage.py not found. Please run this script from the project root directory."
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    print_warning "Virtual environment not detected. Please activate your virtual environment first."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if PostgreSQL is installed
print_status "Checking PostgreSQL installation..."
if ! command -v psql &> /dev/null; then
    print_error "PostgreSQL client (psql) is not installed. Please install PostgreSQL first."
    print_error "Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib"
    print_error "CentOS/RHEL: sudo yum install postgresql postgresql-server"
    print_error "macOS: brew install postgresql"
    exit 1
fi

if ! command -v createdb &> /dev/null; then
    print_error "PostgreSQL utilities (createdb) are not installed. Please install PostgreSQL development tools."
    exit 1
fi

print_success "PostgreSQL client tools found"

# Check if PostgreSQL service is running
print_status "Checking PostgreSQL service status..."
if ! pg_isready -h $DB_HOST -p $DB_PORT > /dev/null 2>&1; then
    print_error "PostgreSQL is not running or not accessible on $DB_HOST:$DB_PORT"
    print_error "Please start PostgreSQL service first:"
    print_error "  Ubuntu/Debian: sudo systemctl start postgresql"
    print_error "  CentOS/RHEL: sudo systemctl start postgresql"
    print_error "  macOS: brew services start postgresql"
    exit 1
fi
print_success "PostgreSQL service is running"

# Function to check if database exists
check_database_exists() {
    psql -h $DB_HOST -p $DB_PORT -U postgres -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"
}

# Function to check if user exists
check_user_exists() {
    psql -h $DB_HOST -p $DB_PORT -U postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1
}

# Check if database exists
print_status "Checking if database '$DB_NAME' exists..."
if check_database_exists; then
    print_success "Database '$DB_NAME' exists"
else
    print_warning "Database '$DB_NAME' does not exist"
    
    # Check if we can connect as postgres user
    print_status "Attempting to create database as postgres user..."
    if psql -h $DB_HOST -p $DB_PORT -U postgres -c "SELECT 1;" > /dev/null 2>&1; then
        print_success "Can connect as postgres user"
        
        # Create database
        print_status "Creating database '$DB_NAME'..."
        createdb -h $DB_HOST -p $DB_PORT -U postgres "$DB_NAME"
        print_success "Database '$DB_NAME' created"
        
        # Check if user exists, create if not
        if check_user_exists; then
            print_success "User '$DB_USER' exists"
        else
            print_status "Creating user '$DB_USER'..."
            psql -h $DB_HOST -p $DB_PORT -U postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
            print_success "User '$DB_USER' created"
        fi
        
        # Grant privileges
        print_status "Granting privileges to user '$DB_USER' on database '$DB_NAME'..."
        psql -h $DB_HOST -p $DB_PORT -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
        psql -h $DB_HOST -p $DB_PORT -U postgres -c "ALTER USER $DB_USER CREATEDB;"
        print_success "Privileges granted"
        
    else
        print_error "Cannot connect as postgres user. You may need to:"
        print_error "1. Set up PostgreSQL authentication in pg_hba.conf"
        print_error "2. Create the database manually:"
        print_error "   sudo -u postgres createdb $DB_NAME"
        print_error "   sudo -u postgres createuser $DB_USER"
        print_error "   sudo -u postgres psql -c \"ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';\""
        print_error "   sudo -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;\""
        
        read -p "Would you like to try creating the database manually? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_status "Attempting manual database creation..."
            sudo -u postgres createdb "$DB_NAME" 2>/dev/null || print_warning "Database creation failed"
            sudo -u postgres createuser "$DB_USER" 2>/dev/null || print_warning "User creation failed"
            sudo -u postgres psql -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null || print_warning "Password setting failed"
            sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" 2>/dev/null || print_warning "Privilege granting failed"
        else
            exit 1
        fi
    fi
fi

# Test database connection with Django settings
print_status "Testing database connection with Django settings..."
if python manage.py dbshell -c "SELECT 1;" > /dev/null 2>&1; then
    print_success "Database connection successful"
else
    print_error "Cannot connect to database with Django settings"
    print_error "Please check your database configuration in settings.py"
    print_error "Make sure the database credentials match:"
    print_error "  NAME: $DB_NAME"
    print_error "  USER: $DB_USER"
    print_error "  PASSWORD: $DB_PASSWORD"
    print_error "  HOST: $DB_HOST"
    print_error "  PORT: $DB_PORT"
    exit 1
fi

# Install/upgrade dependencies
print_status "Installing/upgrading Python dependencies..."
pip install -r requirements.txt
print_success "Dependencies updated"

# Check for pending migrations
print_status "Checking for pending migrations..."
PENDING_MIGRATIONS=$(python manage.py showmigrations --list | grep -c "\[ \]" || true)

if [ "$PENDING_MIGRATIONS" -gt 0 ]; then
    print_status "Found $PENDING_MIGRATIONS pending migration(s)"
    
    # Show what migrations will be applied
    print_status "Pending migrations:"
    python manage.py showmigrations --list | grep "\[ \]"
    
    # Apply migrations
    print_status "Applying migrations..."
    python manage.py migrate
    print_success "Migrations applied successfully"
else
    print_success "No pending migrations found"
fi

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput
print_success "Static files collected"

# Check for any data migrations or fixtures that need to be loaded
print_status "Checking for data migrations..."

# Check if there are any fixtures to load
if [ -d "requests_app/fixtures" ]; then
    print_status "Found fixtures directory, checking for unloaded fixtures..."
    for fixture in requests_app/fixtures/*.json; do
        if [ -f "$fixture" ]; then
            fixture_name=$(basename "$fixture" .json)
            print_status "Loading fixture: $fixture_name"
            python manage.py loaddata "$fixture_name" || print_warning "Failed to load fixture $fixture_name"
        fi
    done
fi

# Run any custom management commands if they exist
print_status "Running custom management commands..."

# Check if there are any custom management commands that need to be run
if python manage.py help | grep -q "populate_priorities"; then
    print_status "Running populate_priorities command..."
    python manage.py populate_priorities || print_warning "populate_priorities command failed or not needed"
fi

# Validate the project
print_status "Validating Django project..."
python manage.py check
print_success "Project validation passed"

# Show current migration status
print_status "Current migration status:"
python manage.py showmigrations --list

# Show database tables
print_status "Database tables:"
python manage.py dbshell -c "\dt" 2>/dev/null || print_warning "Could not list database tables"

# Show database size and info
print_status "Database information:"
python manage.py dbshell -c "SELECT pg_size_pretty(pg_database_size('$DB_NAME'));" 2>/dev/null || print_warning "Could not get database size"

echo ""
echo "=========================================="
print_success "Update completed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Start the development server: python manage.py runserver"
echo "2. Create a superuser if needed: python manage.py createsuperuser"
echo "3. Access the admin interface at: http://localhost:8000/admin/"
echo "" 