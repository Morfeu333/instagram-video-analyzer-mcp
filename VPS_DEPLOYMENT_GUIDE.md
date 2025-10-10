# 🚀 VPS Deployment Guide - Instagram Video Analyzer MCP

Complete step-by-step guide to deploy the Instagram Video Analyzer with MCP functionality on an Ubuntu VPS.

## 📋 Table of Contents
1. [VPS Requirements](#vps-requirements)
2. [Initial Server Setup](#initial-server-setup)
3. [Install Dependencies](#install-dependencies)
4. [Deploy Backend API](#deploy-backend-api)
5. [Deploy Frontend](#deploy-frontend)
6. [Configure Nginx](#configure-nginx)
7. [Setup SSL/HTTPS](#setup-ssl-https)
8. [Deploy MCP Server](#deploy-mcp-server)
9. [Setup Systemd Services](#setup-systemd-services)
10. [Monitoring & Maintenance](#monitoring--maintenance)

---

## 🖥️ VPS Requirements

### Minimum Specifications
- **OS**: Ubuntu 22.04 LTS or 24.04 LTS
- **RAM**: 2GB minimum (4GB recommended)
- **CPU**: 2 cores minimum
- **Storage**: 20GB minimum (50GB+ recommended for video storage)
- **Network**: Public IP address, ports 80, 443 open

### Required Software
- Python 3.11+
- Node.js 18+
- Nginx
- FFmpeg
- uv (Python package manager)
- PM2 or systemd (for process management)

---

## 🔧 Initial Server Setup

### 1. Connect to VPS
```bash
ssh root@your-vps-ip
```

### 2. Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 3. Create Application User
```bash
sudo adduser iganalyzer
sudo usermod -aG sudo iganalyzer
su - iganalyzer
```

### 4. Setup Firewall
```bash
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 📦 Install Dependencies

### 1. Install Python 3.11
```bash
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev
```

### 2. Install Node.js 18
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### 3. Install System Tools
```bash
sudo apt install -y \
    git \
    nginx \
    ffmpeg \
    curl \
    build-essential \
    certbot \
    python3-certbot-nginx
```

### 4. Install uv (Python Package Manager)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
```

### 5. Install PM2 (Process Manager)
```bash
sudo npm install -g pm2
```

---

## 🔨 Deploy Backend API

### 1. Clone Repository
```bash
cd /home/iganalyzer
git clone https://github.com/your-username/instagram-video-analyzer-mcp.git
cd instagram-video-analyzer-mcp
```

### 2. Setup Backend Environment
```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
```bash
cp .env.example .env
nano .env
```

**Edit `.env` with your settings:**
```env
# API Configuration
GEMINI_API_KEY=your_actual_gemini_api_key
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Database
DATABASE_URL=sqlite:///./video_analyzer.db

# File Storage
UPLOAD_DIR=/home/iganalyzer/data/videos
RESULTS_DIR=/home/iganalyzer/data/results
TEMP_DIR=/home/iganalyzer/data/temp
MAX_FILE_SIZE=100000000

# Instagram Configuration
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password

# Security
SECRET_KEY=your-secure-random-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Logging
LOG_LEVEL=INFO
LOG_FILE=/home/iganalyzer/logs/backend.log

# CORS - Add your domain
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 4. Create Data Directories
```bash
mkdir -p /home/iganalyzer/data/{videos,results,temp}
mkdir -p /home/iganalyzer/logs
```

### 5. Test Backend
```bash
python -m app.main
# Test at http://your-vps-ip:8000/health
# Press Ctrl+C to stop
```

---

## 🎨 Deploy Frontend

### 1. Build Frontend
```bash
cd /home/iganalyzer/instagram-video-analyzer-mcp/frontend

# Install dependencies
npm install

# Build for production
npm run build
```

### 2. Configure Frontend API URL
Before building, ensure the API URL is correct:

**Edit `frontend/src/services/api.ts` if needed:**
```typescript
const api = axios.create({
  baseURL: '/api',  // Will be proxied by Nginx
  timeout: 30000,
});
```

---

## ⚙️ Configure Nginx

### 1. Create Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/iganalyzer
```

**Add this configuration:**
```nginx
# Backend API upstream
upstream backend_api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Max upload size (for video files)
    client_max_body_size 100M;

    # Frontend (React app)
    root /home/iganalyzer/instagram-video-analyzer-mcp/frontend/dist;
    index index.html;

    # Compression
    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/json;

    # Frontend routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy
    location /api/ {
        proxy_pass http://backend_api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;

        # Timeout settings for long-running analyses
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://backend_api/health;
    }

    # Static files caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 2. Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/iganalyzer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔒 Setup SSL/HTTPS

### 1. Install SSL Certificate with Certbot
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 2. Auto-renewal Setup
```bash
sudo systemctl status certbot.timer
```

### 3. Test Auto-renewal
```bash
sudo certbot renew --dry-run
```

---

## 🤖 Deploy MCP Server

**Important Note:** The MCP server is designed to run on your **local machine** (where Claude Code is installed), not on the VPS. It acts as a bridge between Claude Code and your VPS backend API.

### Local Machine Setup (Not on VPS)

### 1. Install MCP Server Locally
```bash
# On your local machine (Windows/Mac/Linux)
cd /path/to/instagram-video-analyzer-mcp/mcp-server
uv sync
```

### 2. Configure MCP to Point to VPS
Edit your local Claude Code configuration:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux:** `~/.config/claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "instagram-video-analyzer": {
      "command": "uv",
      "args": [
        "--directory",
        "/full/path/to/mcp-server",
        "run",
        "instagram-video-analyzer-mcp"
      ],
      "env": {
        "API_BASE_URL": "https://yourdomain.com",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### 3. Test MCP Connection
Restart Claude Code and test with:
```
Get system statistics from the Instagram Video Analyzer
```

---

## 🔄 Setup Systemd Services

### 1. Create Backend Service
```bash
sudo nano /etc/systemd/system/iganalyzer-backend.service
```

**Add this configuration:**
```ini
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
```

### 2. Enable and Start Backend Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable iganalyzer-backend
sudo systemctl start iganalyzer-backend
sudo systemctl status iganalyzer-backend
```

### 3. View Backend Logs
```bash
sudo journalctl -u iganalyzer-backend -f
# or
tail -f /home/iganalyzer/logs/backend-stdout.log
```

---

## 📊 Monitoring & Maintenance

### 1. Check Service Status
```bash
# Backend
sudo systemctl status iganalyzer-backend

# Nginx
sudo systemctl status nginx
```

### 2. View Logs
```bash
# Backend logs
tail -f /home/iganalyzer/logs/backend.log

# Nginx access logs
tail -f /var/log/nginx/access.log

# Nginx error logs
tail -f /var/log/nginx/error.log
```

### 3. Database Backup
```bash
# Create backup script
nano /home/iganalyzer/scripts/backup-db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/home/iganalyzer/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup SQLite database
cp /home/iganalyzer/instagram-video-analyzer-mcp/backend/video_analyzer.db \
   $BACKUP_DIR/video_analyzer_$DATE.db

# Backup data directories
tar -czf $BACKUP_DIR/data_$DATE.tar.gz /home/iganalyzer/data/

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

```bash
chmod +x /home/iganalyzer/scripts/backup-db.sh

# Add to crontab (daily at 2 AM)
crontab -e
# Add: 0 2 * * * /home/iganalyzer/scripts/backup-db.sh
```

### 4. Update Application
```bash
cd /home/iganalyzer/instagram-video-analyzer-mcp

# Pull latest changes
git pull origin main

# Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart iganalyzer-backend

# Update frontend
cd ../frontend
npm install
npm run build
sudo systemctl reload nginx
```

### 5. Monitor Disk Space
```bash
# Check disk usage
df -h

# Check data directory size
du -sh /home/iganalyzer/data/*

# Clean old videos (older than 30 days)
find /home/iganalyzer/data/videos -name "*.mp4" -mtime +30 -delete
find /home/iganalyzer/data/temp -name "*" -mtime +7 -delete
```

---

## 🧪 Testing Deployment

### 1. Test Backend API
```bash
curl https://yourdomain.com/health
```

Expected response:
```json
{"status":"healthy","timestamp":"2025-01-27T23:54:00Z"}
```

### 2. Test Frontend
Open browser: `https://yourdomain.com`

### 3. Test Full Analysis Flow
1. Open frontend in browser
2. Submit an Instagram video URL
3. Monitor job status
4. Verify results display correctly

### 4. Test MCP Connection (from local machine)
In Claude Code:
```
Analyze this Instagram video: https://www.instagram.com/reel/example/
```

---

## 🚨 Troubleshooting

### Backend Not Starting
```bash
# Check logs
sudo journalctl -u iganalyzer-backend -n 50

# Check if port 8000 is in use
sudo netstat -tulpn | grep 8000

# Test backend manually
cd /home/iganalyzer/instagram-video-analyzer-mcp/backend
source venv/bin/activate
python -m app.main
```

### Frontend Not Loading
```bash
# Check Nginx syntax
sudo nginx -t

# Rebuild frontend
cd /home/iganalyzer/instagram-video-analyzer-mcp/frontend
npm run build
sudo systemctl reload nginx
```

### SSL Certificate Issues
```bash
# Renew certificate manually
sudo certbot renew --force-renewal

# Check certificate status
sudo certbot certificates
```

### MCP Connection Fails
1. Verify `API_BASE_URL` in Claude Code config
2. Test VPS API directly: `curl https://yourdomain.com/health`
3. Check MCP server logs
4. Restart Claude Code

### Database Locked
```bash
# Check for processes using database
sudo lsof | grep video_analyzer.db

# Restart backend
sudo systemctl restart iganalyzer-backend
```

---

## 🎯 Security Best Practices

### 1. Firewall Configuration
```bash
# Only allow necessary ports
sudo ufw status
sudo ufw allow from trusted-ip to any port 22  # Restrict SSH
```

### 2. Keep System Updated
```bash
# Create update script
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y
```

### 3. Secure Environment Variables
```bash
# Restrict .env file permissions
chmod 600 /home/iganalyzer/instagram-video-analyzer-mcp/backend/.env
```

### 4. Rate Limiting (Optional)
Add to Nginx config:
```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

location /api/ {
    limit_req zone=api_limit burst=20 nodelay;
    # ... rest of proxy config
}
```

---

## 📞 Support

If you encounter issues:
1. Check logs: `/home/iganalyzer/logs/`
2. Review systemd status: `sudo systemctl status iganalyzer-backend`
3. Test components individually
4. Check GitHub Issues: [Project Issues](https://github.com/your-repo/issues)

---

## ✅ Deployment Checklist

- [ ] VPS provisioned with Ubuntu 22.04+
- [ ] All dependencies installed
- [ ] Backend configured and running
- [ ] Frontend built and served
- [ ] Nginx configured correctly
- [ ] SSL certificate installed
- [ ] Systemd services enabled
- [ ] Firewall configured
- [ ] Backup system setup
- [ ] MCP server configured locally
- [ ] Full system test completed

---

**Deployment completed! Your Instagram Video Analyzer with MCP functionality is now live!** 🎉
