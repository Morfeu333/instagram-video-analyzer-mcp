#!/bin/bash
# Instagram Video Analyzer - Quick Deployment Script
# Complete deployment automation
# Run as root initially, switches to iganalyzer user as needed

set -e

echo "🚀 Instagram Video Analyzer - Quick Deploy"
echo "=========================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root or with sudo"
    exit 1
fi

echo ""
read -p "Enter your domain name (e.g., example.com): " DOMAIN
read -p "Enter your email for SSL certificate: " EMAIL
read -p "Enter your GitHub repository URL: " REPO_URL

echo ""
print_warning "This script will:"
echo "  1. Setup VPS with all dependencies"
echo "  2. Deploy backend and frontend"
echo "  3. Configure Nginx"
echo "  4. Setup SSL certificate"
echo "  5. Create systemd services"
echo ""
read -p "Continue? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Step 1: VPS Setup
print_status "Step 1/5: Setting up VPS..."
bash setup-vps.sh

# Step 2: Deploy as iganalyzer user
print_status "Step 2/5: Deploying backend..."
su - iganalyzer << 'EOSU'
cd /home/iganalyzer
git clone "$REPO_URL" instagram-video-analyzer-mcp || (cd instagram-video-analyzer-mcp && git pull)
cd instagram-video-analyzer-mcp/backend
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
EOSU

print_warning "⚠️  Configure your .env file now!"
read -p "Press Enter after you've edited /home/iganalyzer/instagram-video-analyzer-mcp/backend/.env"

# Step 3: Deploy frontend
print_status "Step 3/5: Deploying frontend..."
su - iganalyzer << 'EOSU'
cd /home/iganalyzer/instagram-video-analyzer-mcp/frontend
mkdir -p src/lib
cat > src/lib/utils.ts << 'EOF'
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
EOF
npm install
npm run build
EOSU

# Step 4: Configure Nginx
print_status "Step 4/5: Configuring Nginx..."
sed "s/yourdomain.com/$DOMAIN/g" nginx-config-template.conf > /etc/nginx/sites-available/iganalyzer
ln -sf /etc/nginx/sites-available/iganalyzer /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

# Step 5: Setup Systemd and SSL
print_status "Step 5/5: Setting up services and SSL..."
bash deploy-systemd.sh

print_status "Setting up SSL certificate..."
certbot --nginx -d "$DOMAIN" -d "www.$DOMAIN" --non-interactive --agree-tos -m "$EMAIL"

print_status "✅ Deployment completed successfully!"
echo ""
echo "🎉 Your Instagram Video Analyzer is now live at: https://$DOMAIN"
echo ""
echo "Next steps:"
echo "  1. Test frontend: https://$DOMAIN"
echo "  2. Test API: https://$DOMAIN/health"
echo "  3. Configure MCP locally to point to: https://$DOMAIN"
echo ""
echo "Useful commands:"
echo "  Backend logs:  sudo journalctl -u iganalyzer-backend -f"
echo "  Nginx logs:    tail -f /var/log/nginx/error.log"
echo "  Service status: sudo systemctl status iganalyzer-backend"
