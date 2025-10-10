#!/bin/bash
# Deploy MCP SSE Server to VPS
# Run this as the iganalyzer user

set -e

echo "🌐 Deploying MCP SSE Server..."

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

cd /home/iganalyzer/instagram-video-analyzer-mcp/mcp-server

print_status "Installing MCP SSE Server dependencies..."

# Create virtual environment if not exists
if [ ! -d "venv-sse" ]; then
    python3.11 -m venv venv-sse
    print_status "Virtual environment created"
fi

# Activate and install dependencies
source venv-sse/bin/activate
pip install --upgrade pip
pip install -r requirements-sse.txt
print_status "Dependencies installed"

# Create .env file for MCP SSE server
if [ ! -f ".env.sse" ]; then
    print_warning "Creating .env.sse file..."
    cat > .env.sse << 'EOF'
# MCP SSE Server Configuration
API_BASE_URL=http://localhost:8000
MCP_SERVER_PORT=8100

# Authentication - Generate secure API keys
# Use: python -c "import secrets; print(secrets.token_urlsafe(32))"
MCP_API_KEYS=your-api-key-here,another-key-here

# Logging
LOG_LEVEL=INFO
EOF
    print_warning "⚠️  IMPORTANT: Edit .env.sse and set your API keys!"
    print_warning "Generate keys with: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
    echo ""
    read -p "Press Enter after you've edited .env.sse"
else
    print_status ".env.sse file already exists"
fi

# Test MCP SSE server
print_status "Testing MCP SSE server..."
timeout 5s python mcp_sse_server.py &
sleep 3
if curl -s http://localhost:8100/health > /dev/null; then
    print_status "MCP SSE server test successful!"
else
    print_warning "MCP SSE server test failed - check configuration"
fi

# Kill test process
pkill -f "python mcp_sse_server.py" || true

print_status "✅ MCP SSE server deployment completed!"
echo ""
echo "Next steps:"
echo "1. Review .env.sse file: nano /home/iganalyzer/instagram-video-analyzer-mcp/mcp-server/.env.sse"
echo "2. Setup systemd service (run as sudo): sudo ./deploy-mcp-systemd.sh"
echo "3. Configure Nginx reverse proxy for port 8100"
echo "4. Test: curl http://localhost:8100/health"
