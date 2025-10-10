#!/bin/bash
# Instagram Video Analyzer - Frontend Deployment Script
# Run this as the iganalyzer user

set -e

echo "🎨 Deploying Frontend..."

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

cd /home/iganalyzer/instagram-video-analyzer-mcp/frontend

print_status "Installing frontend dependencies..."
npm install

# Check if lib/utils.ts exists, create if not
if [ ! -f "src/lib/utils.ts" ]; then
    print_warning "Creating missing lib/utils.ts..."
    mkdir -p src/lib
    cat > src/lib/utils.ts << 'EOF'
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

/**
 * Utility function to merge Tailwind CSS classes
 * Combines clsx for conditional classes and tailwind-merge to handle conflicts
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
EOF
fi

print_status "Building frontend for production..."
npm run build

# Create nginx-ready dist directory
print_status "Frontend built successfully!"
print_status "Build location: /home/iganalyzer/instagram-video-analyzer-mcp/frontend/dist"

print_status "✅ Frontend deployment completed!"
echo ""
echo "Next steps:"
echo "1. Configure Nginx to serve from: /home/iganalyzer/instagram-video-analyzer-mcp/frontend/dist"
echo "2. Setup SSL certificate with: sudo certbot --nginx -d yourdomain.com"
echo "3. Reload Nginx: sudo systemctl reload nginx"
