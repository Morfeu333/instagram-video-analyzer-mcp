# 🌐 Online MCP Server Deployment Guide

Complete guide to deploy the Instagram Video Analyzer MCP Server online with HTTP/SSE transport, making it accessible from anywhere on the internet.

## 📋 Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [What is MCP SSE?](#what-is-mcp-sse)
3. [Setup Instructions](#setup-instructions)
4. [Configuration](#configuration)
5. [Deployment](#deployment)
6. [Client Configuration](#client-configuration)
7. [Security](#security)
8. [Testing](#testing)
9. [Troubleshooting](#troubleshooting)

---

## 🏗️ Architecture Overview

### Traditional MCP (stdio)
```
Claude Code ←→ MCP Server (local) ←→ Backend API (VPS)
```

### Online MCP (SSE)
```
Claude Code ←→ MCP SSE Server (VPS) ←→ Backend API (VPS)
     |                  ↑
     └─── HTTPS/SSE ────┘
```

**Benefits:**
- ✅ Access MCP server from anywhere
- ✅ No local setup required on client machine
- ✅ Centralized deployment and updates
- ✅ Multiple clients can connect simultaneously
- ✅ Better for team collaboration

---

## 📡 What is MCP SSE?

**Server-Sent Events (SSE)** is a standard for real-time server-to-client communication over HTTP.

### How it Works

1. **Client initiates connection** via HTTP GET to `/sse` endpoint
2. **Server keeps connection open** and streams events
3. **Bidirectional communication** via SSE (server→client) and POST requests (client→server)
4. **Authentication** via Bearer tokens in headers

### MCP Protocol

The Model Context Protocol (MCP) defines:
- **Tools**: Functions that AI can call
- **Resources**: Data sources that AI can access
- **Transport**: How messages are sent (stdio, SSE, WebSocket)

Our implementation uses **SSE transport** for online access.

---

## 🚀 Setup Instructions

### 1. Initial VPS Setup

If you haven't deployed the backend yet, follow `VPS_DEPLOYMENT_GUIDE.md` first.

### 2. Deploy MCP SSE Server

```bash
# SSH into your VPS
ssh iganalyzer@your-vps-ip

# Navigate to repository
cd /home/iganalyzer/instagram-video-analyzer-mcp/deploy

# Make scripts executable
chmod +x deploy-mcp-sse.sh deploy-mcp-systemd.sh

# Deploy MCP SSE server
./deploy-mcp-sse.sh
```

### 3. Generate API Keys

```bash
# Generate secure API keys
python3 -c "import secrets; print('API Key 1:', secrets.token_urlsafe(32))"
python3 -c "import secrets; print('API Key 2:', secrets.token_urlsafe(32))"
```

### 4. Configure Environment

Edit `/home/iganalyzer/instagram-video-analyzer-mcp/mcp-server/.env.sse`:

```bash
nano /home/iganalyzer/instagram-video-analyzer-mcp/mcp-server/.env.sse
```

```env
# MCP SSE Server Configuration
API_BASE_URL=http://localhost:8000
MCP_SERVER_PORT=8100

# Authentication - Add your generated API keys
MCP_API_KEYS=your-key-1-here,your-key-2-here,your-key-3-here

# Logging
LOG_LEVEL=INFO
```

### 5. Setup Systemd Service

```bash
# Exit to root
exit

# Setup systemd service (as root)
cd /home/iganalyzer/instagram-video-analyzer-mcp/deploy
sudo ./deploy-mcp-systemd.sh
```

### 6. Configure Nginx

#### Option A: Path-based routing (same domain)

```bash
# Edit your existing nginx config
sudo nano /etc/nginx/sites-available/iganalyzer
```

Add this location block inside your `server {}` block:

```nginx
location /mcp/ {
    rewrite ^/mcp/(.*) /$1 break;
    proxy_pass http://127.0.0.1:8100;
    proxy_http_version 1.1;

    # SSE specific
    proxy_set_header Connection '';
    proxy_set_header Cache-Control 'no-cache';
    proxy_set_header X-Accel-Buffering 'no';
    chunked_transfer_encoding on;

    # Standard headers
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    # Timeouts
    proxy_read_timeout 300s;
    proxy_buffering off;
}
```

#### Option B: Subdomain routing (recommended)

```bash
# Copy MCP SSE nginx config
sudo cp /home/iganalyzer/instagram-video-analyzer-mcp/deploy/nginx-mcp-sse.conf \
       /etc/nginx/sites-available/mcp-sse

# Edit and configure
sudo nano /etc/nginx/sites-available/mcp-sse

# Enable site
sudo ln -s /etc/nginx/sites-available/mcp-sse /etc/nginx/sites-enabled/

# Setup SSL for subdomain
sudo certbot --nginx -d mcp.yourdomain.com
```

### 7. Test and Restart

```bash
# Test nginx configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx

# Check MCP SSE service
sudo systemctl status iganalyzer-mcp-sse

# Test endpoint
curl -H "Authorization: Bearer your-api-key-here" https://yourdomain.com/mcp/health
```

---

## ⚙️ Configuration

### MCP SSE Server Configuration

**File:** `/home/iganalyzer/instagram-video-analyzer-mcp/mcp-server/.env.sse`

| Variable | Description | Example |
|----------|-------------|---------|
| `API_BASE_URL` | Backend API URL | `http://localhost:8000` |
| `MCP_SERVER_PORT` | MCP SSE server port | `8100` |
| `MCP_API_KEYS` | Comma-separated API keys | `key1,key2,key3` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Server info |
| `/health` | GET | Health check |
| `/sse` | GET | SSE connection (MCP protocol) |
| `/messages` | POST | Send messages to MCP |
| `/sessions` | GET | List active sessions (admin) |
| `/generate-key` | POST | Generate new API key (admin) |

---

## 🔧 Deployment

### Quick Deployment

```bash
# All-in-one deployment script
cd /home/iganalyzer/instagram-video-analyzer-mcp/deploy
chmod +x *.sh

# Deploy everything
./deploy-mcp-sse.sh
sudo ./deploy-mcp-systemd.sh
```

### Manual Deployment

```bash
# 1. Create virtual environment
cd /home/iganalyzer/instagram-video-analyzer-mcp/mcp-server
python3.11 -m venv venv-sse
source venv-sse/bin/activate

# 2. Install dependencies
pip install -r requirements-sse.txt

# 3. Configure environment
cp .env.sse.example .env.sse
nano .env.sse

# 4. Test locally
python mcp_sse_server.py

# 5. Setup systemd (as root)
sudo systemctl enable iganalyzer-mcp-sse
sudo systemctl start iganalyzer-mcp-sse
```

### Verify Deployment

```bash
# Check service status
sudo systemctl status iganalyzer-mcp-sse

# Check logs
sudo journalctl -u iganalyzer-mcp-sse -f

# Test health endpoint
curl -H "Authorization: Bearer YOUR_API_KEY" http://localhost:8100/health

# Test via nginx
curl -H "Authorization: Bearer YOUR_API_KEY" https://yourdomain.com/mcp/health
```

---

## 💻 Client Configuration

### Option 1: Claude Desktop (with SSE support)

**File:** `claude_desktop_config.json`

```json
{
  "mcpServers": {
    "instagram-video-analyzer": {
      "transport": "sse",
      "url": "https://yourdomain.com/mcp/sse",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY_HERE"
      }
    }
  }
}
```

### Option 2: Custom MCP Client

```python
import httpx
from mcp.client import ClientSession
from mcp.client.sse import sse_client

async def connect_to_mcp():
    headers = {
        "Authorization": "Bearer YOUR_API_KEY_HERE"
    }

    async with httpx.AsyncClient() as client:
        async with sse_client(
            "https://yourdomain.com/mcp/sse",
            headers=headers
        ) as streams:
            async with ClientSession(*streams) as session:
                # Initialize connection
                await session.initialize()

                # List available tools
                tools = await session.list_tools()
                print("Available tools:", tools)

                # Call a tool
                result = await session.call_tool(
                    "get_system_stats",
                    arguments={}
                )
                print("Result:", result)
```

### Option 3: HTTP API (Direct)

```bash
# Health check
curl -H "Authorization: Bearer YOUR_KEY" \
     https://yourdomain.com/mcp/health

# Connect to SSE stream
curl -H "Authorization: Bearer YOUR_KEY" \
     -H "Accept: text/event-stream" \
     -N https://yourdomain.com/mcp/sse
```

---

## 🔒 Security

### 1. API Key Management

```bash
# Generate new API key
curl -X POST \
     -H "Authorization: Bearer ADMIN_KEY" \
     https://yourdomain.com/mcp/generate-key

# Rotate keys regularly
# Update .env.sse with new keys
# Restart service
sudo systemctl restart iganalyzer-mcp-sse
```

### 2. Rate Limiting (Nginx)

Add to nginx config:

```nginx
limit_req_zone $binary_remote_addr zone=mcp_limit:10m rate=10r/s;

location /mcp/ {
    limit_req zone=mcp_limit burst=20 nodelay;
    # ... rest of config
}
```

### 3. IP Whitelisting (Optional)

```nginx
location /mcp/ {
    allow 1.2.3.4;      # Your IP
    allow 5.6.7.8/24;   # Your network
    deny all;
    # ... rest of config
}
```

### 4. SSL/TLS

Always use HTTPS in production:

```bash
# Setup SSL for main domain
sudo certbot --nginx -d yourdomain.com

# Setup SSL for MCP subdomain
sudo certbot --nginx -d mcp.yourdomain.com
```

### 5. Firewall

```bash
# Only expose necessary ports
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw deny 8100/tcp  # Don't expose MCP port directly
```

---

## 🧪 Testing

### 1. Health Check

```bash
curl -H "Authorization: Bearer YOUR_KEY" \
     https://yourdomain.com/mcp/health
```

Expected response:
```json
{
  "status": "healthy",
  "backend": "connected",
  "timestamp": "2025-01-27T12:00:00.000Z"
}
```

### 2. SSE Connection

```bash
# Test SSE stream
curl -H "Authorization: Bearer YOUR_KEY" \
     -H "Accept: text/event-stream" \
     -N https://yourdomain.com/mcp/sse
```

### 3. Tool Execution

Using Python MCP client:

```python
import asyncio
from test_mcp_client import test_connection

async def main():
    await test_connection(
        "https://yourdomain.com/mcp/sse",
        "YOUR_API_KEY"
    )

asyncio.run(main())
```

### 4. Load Testing

```bash
# Install apache bench
sudo apt install apache2-utils

# Test concurrent connections
ab -n 100 -c 10 \
   -H "Authorization: Bearer YOUR_KEY" \
   https://yourdomain.com/mcp/health
```

---

## 🐛 Troubleshooting

### MCP SSE Server Won't Start

```bash
# Check logs
sudo journalctl -u iganalyzer-mcp-sse -n 50

# Check if port is in use
sudo netstat -tulpn | grep 8100

# Test manually
cd /home/iganalyzer/instagram-video-analyzer-mcp/mcp-server
source venv-sse/bin/activate
python mcp_sse_server.py
```

### Authentication Fails

```bash
# Verify API key in .env.sse
cat /home/iganalyzer/instagram-video-analyzer-mcp/mcp-server/.env.sse

# Check headers
curl -v -H "Authorization: Bearer YOUR_KEY" \
     https://yourdomain.com/mcp/health
```

### SSE Connection Drops

```nginx
# Increase nginx timeouts
proxy_read_timeout 600s;
proxy_connect_timeout 600s;
keepalive_timeout 600s;
```

### Backend Connection Issues

```bash
# Check backend is running
curl http://localhost:8000/health

# Check MCP can reach backend
sudo journalctl -u iganalyzer-mcp-sse -f

# Verify API_BASE_URL in .env.sse
```

### CORS Errors

```python
# Update CORS settings in mcp_sse_server.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 Monitoring

### View Active Sessions

```bash
curl -H "Authorization: Bearer YOUR_KEY" \
     https://yourdomain.com/mcp/sessions
```

### Monitor Logs

```bash
# MCP SSE logs
sudo journalctl -u iganalyzer-mcp-sse -f

# Nginx access logs
tail -f /var/log/nginx/access.log | grep /mcp/

# Nginx error logs
tail -f /var/log/nginx/error.log
```

### System Resources

```bash
# CPU and memory usage
top -u iganalyzer

# Connection count
ss -tan | grep :8100 | wc -l
```

---

## 🔄 Updates and Maintenance

### Update MCP SSE Server

```bash
cd /home/iganalyzer/instagram-video-analyzer-mcp
git pull origin main

cd mcp-server
source venv-sse/bin/activate
pip install -r requirements-sse.txt

# Restart service
sudo systemctl restart iganalyzer-mcp-sse
```

### Backup Configuration

```bash
# Backup .env.sse
cp /home/iganalyzer/instagram-video-analyzer-mcp/mcp-server/.env.sse \
   /home/iganalyzer/backups/mcp-sse-env-$(date +%Y%m%d).bak
```

### Rotate API Keys

```bash
# Generate new keys
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Update .env.sse
nano /home/iganalyzer/instagram-video-analyzer-mcp/mcp-server/.env.sse

# Restart service
sudo systemctl restart iganalyzer-mcp-sse

# Update all clients with new keys
```

---

## 📚 Additional Resources

- [MCP Protocol Specification](https://github.com/anthropics/mcp-specification)
- [SSE Transport Documentation](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Nginx SSE Configuration](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)

---

## ✅ Deployment Checklist

- [ ] Backend API deployed and running
- [ ] MCP SSE server dependencies installed
- [ ] API keys generated and configured
- [ ] `.env.sse` file created and populated
- [ ] Systemd service created and enabled
- [ ] Nginx reverse proxy configured
- [ ] SSL certificate installed
- [ ] Firewall rules configured
- [ ] Health check endpoint working
- [ ] SSE connection tested
- [ ] Client configuration updated
- [ ] Monitoring setup
- [ ] Backup procedures in place

---

**🎉 Your MCP Server is now accessible online via HTTP/SSE!**

Connect from anywhere using:
```
https://yourdomain.com/mcp/sse
```

or subdomain:
```
https://mcp.yourdomain.com/sse
```
