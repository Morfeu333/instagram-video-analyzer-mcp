#!/bin/bash
# Setup systemd service for MCP SSE Server
# Run this as root or with sudo

set -e

echo "🔄 Setting up MCP SSE Systemd Service..."

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

# Create MCP SSE systemd service
print_status "Creating MCP SSE systemd service..."
cat > /etc/systemd/system/iganalyzer-mcp-sse.service << 'EOF'
[Unit]
Description=Instagram Video Analyzer MCP SSE Server
After=network.target iganalyzer-backend.service
Requires=iganalyzer-backend.service

[Service]
Type=simple
User=iganalyzer
Group=iganalyzer
WorkingDirectory=/home/iganalyzer/instagram-video-analyzer-mcp/mcp-server
Environment="PATH=/home/iganalyzer/instagram-video-analyzer-mcp/mcp-server/venv-sse/bin"
EnvironmentFile=/home/iganalyzer/instagram-video-analyzer-mcp/mcp-server/.env.sse
ExecStart=/home/iganalyzer/instagram-video-analyzer-mcp/mcp-server/venv-sse/bin/python mcp_sse_server.py
Restart=always
RestartSec=10

# Resource limits
LimitNOFILE=65536

# Logging
StandardOutput=append:/home/iganalyzer/logs/mcp-sse-stdout.log
StandardError=append:/home/iganalyzer/logs/mcp-sse-stderr.log

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
print_status "Reloading systemd daemon..."
systemctl daemon-reload

# Enable service
print_status "Enabling MCP SSE service..."
systemctl enable iganalyzer-mcp-sse

# Start service
print_status "Starting MCP SSE service..."
systemctl start iganalyzer-mcp-sse

# Check status
sleep 2
if systemctl is-active --quiet iganalyzer-mcp-sse; then
    print_status "✅ MCP SSE service is running!"
    systemctl status iganalyzer-mcp-sse --no-pager -l
else
    print_error "MCP SSE service failed to start"
    print_error "Check logs: sudo journalctl -u iganalyzer-mcp-sse -n 50"
    exit 1
fi

print_status "✅ MCP SSE systemd service setup completed!"
echo ""
echo "Useful commands:"
echo "  View status:  sudo systemctl status iganalyzer-mcp-sse"
echo "  View logs:    sudo journalctl -u iganalyzer-mcp-sse -f"
echo "  Restart:      sudo systemctl restart iganalyzer-mcp-sse"
echo "  Stop:         sudo systemctl stop iganalyzer-mcp-sse"
