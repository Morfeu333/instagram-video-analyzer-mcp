#!/bin/bash
# Instagram Video Analyzer - VPS Initial Setup Script
# Run this on your Ubuntu VPS as root or with sudo

set -e  # Exit on error

echo "🚀 Instagram Video Analyzer - VPS Setup"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root or with sudo"
    exit 1
fi

print_status "Starting VPS setup..."

# Update system
print_status "Updating system packages..."
apt update && apt upgrade -y

# Install basic tools
print_status "Installing basic tools..."
apt install -y curl wget git build-essential software-properties-common

# Install Python 3.11
print_status "Installing Python 3.11..."
add-apt-repository -y ppa:deadsnakes/ppa
apt update
apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Install Node.js 18
print_status "Installing Node.js 18..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# Install system dependencies
print_status "Installing system dependencies..."
apt install -y \
    nginx \
    ffmpeg \
    certbot \
    python3-certbot-nginx \
    sqlite3

# Install uv for Python package management
print_status "Installing uv (Python package manager)..."
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    print_status "uv installed successfully"
else
    print_status "uv already installed"
fi

# Install PM2
print_status "Installing PM2 process manager..."
npm install -g pm2

# Create application user
print_status "Creating application user 'iganalyzer'..."
if id "iganalyzer" &>/dev/null; then
    print_warning "User 'iganalyzer' already exists"
else
    adduser --disabled-password --gecos "" iganalyzer
    usermod -aG sudo iganalyzer
    print_status "User 'iganalyzer' created"
fi

# Setup firewall
print_status "Configuring firewall..."
ufw --force enable
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
print_status "Firewall configured"

# Create directory structure
print_status "Creating directory structure..."
mkdir -p /home/iganalyzer/{data/{videos,results,temp},logs,backups,scripts}
chown -R iganalyzer:iganalyzer /home/iganalyzer

print_status "✅ VPS setup completed!"
echo ""
echo "Next steps:"
echo "1. Switch to iganalyzer user: su - iganalyzer"
echo "2. Clone the repository"
echo "3. Run deploy-backend.sh and deploy-frontend.sh"
echo "4. Configure Nginx with your domain"
echo "5. Setup SSL with certbot"
echo ""
print_warning "Don't forget to configure your .env file with API keys!"
