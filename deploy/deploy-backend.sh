#!/bin/bash
# Instagram Video Analyzer - Backend Deployment Script
# Run this as the iganalyzer user

set -e

echo "🔨 Deploying Backend..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check if running as iganalyzer
if [ "$USER" != "iganalyzer" ]; then
    echo "Please run as iganalyzer user"
    exit 1
fi

cd /home/iganalyzer

# Clone or update repository
if [ -d "instagram-video-analyzer-mcp" ]; then
    print_warning "Repository exists, pulling latest changes..."
    cd instagram-video-analyzer-mcp
    git pull origin main
else
    print_status "Cloning repository..."
    read -p "Enter repository URL: " REPO_URL
    git clone "$REPO_URL" instagram-video-analyzer-mcp
    cd instagram-video-analyzer-mcp
fi

# Setup backend
cd backend
print_status "Setting up backend environment..."

# Create virtual environment
if [ ! -d "venv" ]; then
    python3.11 -m venv venv
    print_status "Virtual environment created"
fi

# Activate and install dependencies
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
print_status "Dependencies installed"

# Setup .env file
if [ ! -f ".env" ]; then
    print_warning "Creating .env file from template..."
    cp .env.example .env
    print_warning "⚠️  IMPORTANT: Edit .env file with your actual configuration!"
    print_warning "Run: nano /home/iganalyzer/instagram-video-analyzer-mcp/backend/.env"
else
    print_status ".env file already exists"
fi

# Set permissions
chmod 600 .env

# Test backend
print_status "Testing backend..."
timeout 5s python -m app.main &
sleep 3
if curl -s http://localhost:8000/health > /dev/null; then
    print_status "Backend test successful!"
else
    print_warning "Backend test failed - check configuration"
fi

# Kill test process
pkill -f "python -m app.main" || true

print_status "✅ Backend deployment completed!"
echo ""
echo "Next steps:"
echo "1. Edit .env file: nano /home/iganalyzer/instagram-video-analyzer-mcp/backend/.env"
echo "2. Add your GEMINI_API_KEY and other credentials"
echo "3. Setup systemd service (run as sudo): sudo ./deploy-systemd.sh"
