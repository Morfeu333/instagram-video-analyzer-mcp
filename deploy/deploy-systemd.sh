#!/bin/bash
# Instagram Video Analyzer - Systemd Service Setup
# Run this as root or with sudo

set -e

echo "🔄 Setting up Systemd Services..."

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root or with sudo"
    exit 1
fi

# Create backend systemd service
print_status "Creating backend systemd service..."
cat > /etc/systemd/system/iganalyzer-backend.service << 'EOF'
[Unit]
Description=Instagram Video Analyzer Backend API
After=network.target

[Service]
Type=simple
User=iganalyzer
Group=iganalyzer
WorkingDirectory=/home/iganalyzer/instagram-video-analyzer-mcp/backend
Environment="PATH=/home/iganalyzer/instagram-video-analyzer-mcp/backend/venv/bin"
ExecStart=/home/iganalyzer/instagram-video-analyzer-mcp/backend/venv/bin/python -m app.main
Restart=always
RestartSec=10

# Resource limits
LimitNOFILE=65536

# Logging
StandardOutput=append:/home/iganalyzer/logs/backend-stdout.log
StandardError=append:/home/iganalyzer/logs/backend-stderr.log

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
print_status "Reloading systemd daemon..."
systemctl daemon-reload

# Enable service
print_status "Enabling backend service..."
systemctl enable iganalyzer-backend

# Start service
print_status "Starting backend service..."
systemctl start iganalyzer-backend

# Check status
sleep 2
if systemctl is-active --quiet iganalyzer-backend; then
    print_status "✅ Backend service is running!"
    systemctl status iganalyzer-backend --no-pager -l
else
    print_error "Backend service failed to start"
    print_error "Check logs: sudo journalctl -u iganalyzer-backend -n 50"
    exit 1
fi

print_status "✅ Systemd services setup completed!"
echo ""
echo "Useful commands:"
echo "  View status:  sudo systemctl status iganalyzer-backend"
echo "  View logs:    sudo journalctl -u iganalyzer-backend -f"
echo "  Restart:      sudo systemctl restart iganalyzer-backend"
echo "  Stop:         sudo systemctl stop iganalyzer-backend"
