#!/bin/bash

# Database Setup Script for Antibody Requests Django Project
# This script sets up the PostgreSQL database, user, and permissions

set -e  # Exit on any error

echo "=========================================="
echo "Antibody Requests - Database Setup Script"
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
    print_error "Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib"
    print_error "CentOS/RHEL: sudo yum install postgresql postgresql-server"
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

# Check if we can connect as postgres user
print_status "Testing connection as postgres user..."
if ! psql -h $DB_HOST -p $DB_PORT -U postgres -c "SELECT 1;" > /dev/null 2>&1; then
    print_error "Cannot connect as postgres user. This script requires postgres user access."
    print_error "You may need to:"
    print_error "1. Set up PostgreSQL authentication in pg_hba.conf"
    print_error "2. Use sudo to run as postgres user"
    print_error "3. Set PGPASSWORD environment variable"
    
    read -p "Would you like to try with sudo? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Attempting to run commands with sudo..."
        SUDO_PREFIX="sudo -u postgres"
    else
        print_error "Please set up PostgreSQL authentication or run this script with appropriate permissions."
        exit 1
    fi
else
    SUDO_PREFIX=""
    print_success "Can connect as postgres user"
fi

# Check if database exists
print_status "Checking if database '$DB_NAME' exists..."
if check_database_exists; then
    print_success "Database '$DB_NAME' already exists"
    read -p "Would you like to drop and recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Dropping existing database '$DB_NAME'..."
        $SUDO_PREFIX dropdb -h $DB_HOST -p $DB_PORT "$DB_NAME" 2>/dev/null || print_warning "Could not drop database (may not exist)"
        print_success "Database dropped"
    else
        print_status "Keeping existing database"
    fi
fi

# Create database if it doesn't exist
if ! check_database_exists; then
    print_status "Creating database '$DB_NAME'..."
    $SUDO_PREFIX createdb -h $DB_HOST -p $DB_PORT "$DB_NAME"
    print_success "Database '$DB_NAME' created"
fi

# Check if user exists
print_status "Checking if user '$DB_USER' exists..."
if check_user_exists; then
    print_success "User '$DB_USER' already exists"
    read -p "Would you like to update the user password? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Updating password for user '$DB_USER'..."
        $SUDO_PREFIX psql -h $DB_HOST -p $DB_PORT -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
        print_success "Password updated"
    fi
else
    print_status "Creating user '$DB_USER'..."
    $SUDO_PREFIX psql -h $DB_HOST -p $DB_PORT -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
    print_success "User '$DB_USER' created"
fi

# Grant privileges
print_status "Granting privileges to user '$DB_USER' on database '$DB_NAME'..."
$SUDO_PREFIX psql -h $DB_HOST -p $DB_PORT -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
$SUDO_PREFIX psql -h $DB_HOST -p $DB_PORT -c "ALTER USER $DB_USER CREATEDB;"
print_success "Privileges granted"

# Test connection with the new user
print_status "Testing connection with user '$DB_USER'..."
if psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT 1;" > /dev/null 2>&1; then
    print_success "Connection test successful"
else
    print_warning "Connection test failed. You may need to:"
    print_warning "1. Update pg_hba.conf to allow password authentication"
    print_warning "2. Restart PostgreSQL service"
    print_warning "3. Check if the password was set correctly"
fi

# Show database information
print_status "Database setup complete!"
echo ""
echo "Database Information:"
echo "  Name: $DB_NAME"
echo "  User: $DB_USER"
echo "  Host: $DB_HOST"
echo "  Port: $DB_PORT"
echo ""
echo "You can now run the Django migrations:"
echo "  python manage.py migrate"
echo ""
echo "Or run the full update script:"
echo "  ./update.sh"
echo "" 