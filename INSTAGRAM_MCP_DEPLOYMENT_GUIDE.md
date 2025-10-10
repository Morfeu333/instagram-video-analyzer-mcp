# 🚀 Instagram Video Analyzer MCP - Complete Deployment Guide

## 📋 **TABLE OF CONTENTS**
1. [Current Status & Problem Analysis](#current-status--problem-analysis)
2. [Local PC Always-On Solutions](#local-pc-always-on-solutions)
3. [External Server Deployment](#external-server-deployment)
4. [Cloud Platform Deployment](#cloud-platform-deployment)
5. [N8N Integration Setup](#n8n-integration-setup)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Cost Analysis & Recommendations](#cost-analysis--recommendations)

---

## 🔍 **CURRENT STATUS & PROBLEM ANALYSIS**

### **✅ Current Working State:**
- **MCP Server:** ✅ Configured correctly in Claude Desktop
- **Backend API:** ✅ Running on localhost:8000
- **Database:** ✅ SQLite with 39 jobs processed (97.4% success rate)
- **Storage:** ✅ 511MB videos, 117 files processed

### **❌ Identified Problems:**
1. **Manual Restart Required:** Backend stops when computer restarts
2. **Local Dependency:** Only works when local PC is on
3. **Single Point of Failure:** No redundancy or backup
4. **Limited Accessibility:** Cannot be used from other devices/locations

### **🎯 Solution Requirements:**
- **Reliability:** 99.9% uptime
- **Accessibility:** Available from anywhere
- **Scalability:** Handle multiple concurrent requests
- **Integration:** Compatible with N8N and other automation tools
- **Cost-Effective:** Reasonable operational costs

---

## 💻 **LOCAL PC ALWAYS-ON SOLUTIONS**

### **🔧 SOLUTION 1: Windows Service (RECOMMENDED)**

#### **Step 1: Install NSSM (Non-Sucking Service Manager)**
```bash
# Download NSSM from: https://nssm.cc/download
# Extract to: C:\nssm\
```

#### **Step 2: Create Service Script**
Create `C:\InfluenciadorDigital\instagram-video-analyzer-mcp\service_wrapper.bat`:
```batch
@echo off
cd /d "C:\InfluenciadorDigital\instagram-video-analyzer-mcp\backend"
python -m app.main
```

#### **Step 3: Install as Windows Service**
```bash
# Open Command Prompt as Administrator
cd C:\nssm\win64
nssm install "Instagram-MCP-Backend" "C:\InfluenciadorDigital\instagram-video-analyzer-mcp\service_wrapper.bat"
nssm set "Instagram-MCP-Backend" DisplayName "Instagram Video Analyzer MCP Backend"
nssm set "Instagram-MCP-Backend" Description "Backend service for Instagram Video Analyzer MCP"
nssm set "Instagram-MCP-Backend" Start SERVICE_AUTO_START
nssm start "Instagram-MCP-Backend"
```

#### **Step 4: Verify Service**
```bash
# Check service status
sc query "Instagram-MCP-Backend"

# Test MCP connection
# Use Claude to run: get_system_stats_instagram-video-analyzer()
```

### **🔧 SOLUTION 2: Task Scheduler (ALTERNATIVE)**

#### **Create Scheduled Task:**
1. **Open:** Task Scheduler (taskschd.msc)
2. **Create Basic Task:** "Instagram MCP Backend"
3. **Trigger:** "When the computer starts"
4. **Action:** "Start a program"
   - **Program:** `python`
   - **Arguments:** `-m app.main`
   - **Start in:** `C:\InfluenciadorDigital\instagram-video-analyzer-mcp\backend`
5. **Settings:** 
   - ✅ Run whether user is logged on or not
   - ✅ Run with highest privileges
   - ✅ If task fails, restart every 1 minute

### **🔧 SOLUTION 3: Startup Script (SIMPLE)**

#### **Create Startup Script:**
```batch
# File: C:\InfluenciadorDigital\instagram-video-analyzer-mcp\auto_start.bat
@echo off
echo Starting Instagram MCP Backend...
cd /d "C:\InfluenciadorDigital\instagram-video-analyzer-mcp\backend"
start /min python -m app.main
echo Backend started in minimized window
```

#### **Add to Startup:**
1. **Press:** Win + R
2. **Type:** `shell:startup`
3. **Copy:** `auto_start.bat` to startup folder
4. **Restart:** Computer to test

---

## ☁️ **EXTERNAL SERVER DEPLOYMENT**

### **🖥️ VPS DEPLOYMENT (DigitalOcean/Linode/AWS EC2)**

#### **Server Requirements:**
- **OS:** Ubuntu 22.04 LTS
- **RAM:** 2GB minimum (4GB recommended)
- **Storage:** 20GB SSD
- **CPU:** 2 vCPUs
- **Network:** 1TB transfer

#### **Step 1: Server Setup**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv git nginx -y

# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
```

#### **Step 2: Deploy Application**
```bash
# Clone repository
git clone <your-repo-url> /opt/instagram-mcp
cd /opt/instagram-mcp

# Setup Python environment
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup MCP server
cd ../mcp-server
uv sync
```

#### **Step 3: Create Systemd Service**
Create `/etc/systemd/system/instagram-mcp.service`:
```ini
[Unit]
Description=Instagram Video Analyzer MCP Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/instagram-mcp/backend
Environment=PATH=/opt/instagram-mcp/backend/venv/bin
ExecStart=/opt/instagram-mcp/backend/venv/bin/python -m app.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### **Step 4: Configure Nginx Reverse Proxy**
Create `/etc/nginx/sites-available/instagram-mcp`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### **Step 5: Enable and Start Services**
```bash
# Enable nginx site
sudo ln -s /etc/nginx/sites-available/instagram-mcp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Enable and start MCP service
sudo systemctl enable instagram-mcp
sudo systemctl start instagram-mcp
sudo systemctl status instagram-mcp
```

#### **Step 6: SSL Certificate (Let's Encrypt)**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

## 🌐 **CLOUD PLATFORM DEPLOYMENT**

### **🚀 VERCEL DEPLOYMENT**

#### **Limitations:**
- ❌ **Serverless Functions:** 10-second timeout limit
- ❌ **No Persistent Storage:** SQLite won't work
- ❌ **No Background Processes:** Cannot run continuous backend

#### **Alternative: Vercel + External Database**
```javascript
// api/analyze.js
import { createClient } from '@supabase/supabase-js'

export default async function handler(req, res) {
  // Use Supabase for database
  // Use external video processing service
  // Return analysis results
}
```

### **🐳 DOCKER + RAILWAY/RENDER DEPLOYMENT**

#### **Step 1: Create Dockerfile**
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY mcp-server/ ./mcp-server/

# Expose port
EXPOSE 8000

# Start command
CMD ["python", "-m", "backend.app.main"]
```

#### **Step 2: Create docker-compose.yml**
```yaml
version: '3.8'
services:
  instagram-mcp:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/instagram_mcp
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: instagram_mcp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

#### **Step 3: Deploy to Railway**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### **☁️ AWS LAMBDA + API GATEWAY**

#### **Serverless Framework Configuration**
```yaml
# serverless.yml
service: instagram-mcp

provider:
  name: aws
  runtime: python3.11
  region: us-east-1
  timeout: 900  # 15 minutes max

functions:
  analyze:
    handler: handler.analyze_video
    events:
      - http:
          path: analyze
          method: post
    environment:
      GEMINI_API_KEY: ${env:GEMINI_API_KEY}

plugins:
  - serverless-python-requirements
```

---

## 🔗 **N8N INTEGRATION SETUP**

### **🔧 HTTP Request Node Configuration**

#### **For Local Deployment:**
```json
{
  "method": "POST",
  "url": "http://localhost:8000/analyze",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "url": "{{$json.instagram_url}}",
    "analysis_type": "comprehensive"
  }
}
```

#### **For External Server:**
```json
{
  "method": "POST",
  "url": "https://your-domain.com/analyze",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer {{$json.api_key}}"
  },
  "body": {
    "url": "{{$json.instagram_url}}",
    "analysis_type": "comprehensive"
  }
}
```

### **🔄 N8N Workflow Example**
```json
{
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "instagram-analyze"
      }
    },
    {
      "name": "Instagram MCP",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://your-domain.com/analyze",
        "method": "POST"
      }
    },
    {
      "name": "Process Results",
      "type": "n8n-nodes-base.function",
      "parameters": {
        "functionCode": "// Process analysis results"
      }
    }
  ]
}
```

---

## 📊 **MONITORING & MAINTENANCE**

### **🔍 Health Check Endpoints**
```python
# Add to FastAPI app
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "1.0.0"
    }

@app.get("/metrics")
async def get_metrics():
    return {
        "total_jobs": get_job_count(),
        "success_rate": calculate_success_rate(),
        "avg_processing_time": get_avg_processing_time()
    }
```

### **📈 Monitoring Tools**
- **Uptime Monitoring:** UptimeRobot, Pingdom
- **Application Monitoring:** New Relic, DataDog
- **Log Management:** LogTail, Papertrail
- **Error Tracking:** Sentry

### **🔄 Backup Strategy**
```bash
# Daily database backup
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp /opt/instagram-mcp/backend/video_analyzer.db /backups/db_backup_$DATE.db
find /backups -name "db_backup_*.db" -mtime +7 -delete
```

---

## 💰 **COST ANALYSIS & RECOMMENDATIONS**

### **💻 Local PC (Always-On)**
- **Electricity:** ~$10-20/month
- **Internet:** Existing connection
- **Maintenance:** Time investment
- **Total:** $10-20/month

### **☁️ VPS Hosting**
- **DigitalOcean Droplet:** $12-24/month
- **Domain:** $10-15/year
- **SSL Certificate:** Free (Let's Encrypt)
- **Total:** $12-24/month

### **🚀 Cloud Platforms**
- **Railway:** $5-20/month
- **Render:** $7-25/month
- **AWS Lambda:** $0-10/month (pay per use)
- **Total:** $5-25/month

### **🎯 RECOMMENDATIONS**

#### **For Development/Personal Use:**
✅ **Local PC with Windows Service** (Most cost-effective)

#### **For Production/Business Use:**
✅ **VPS with Docker** (Best balance of cost/performance/control)

#### **For High Scalability:**
✅ **AWS Lambda + RDS** (Pay per use, infinite scale)

#### **For Simplicity:**
✅ **Railway/Render** (Easy deployment, managed infrastructure)

---

## 🚀 **NEXT STEPS**

### **Immediate Actions:**
1. ✅ **Choose deployment strategy** based on requirements
2. ✅ **Implement local Windows Service** for immediate reliability
3. ✅ **Set up external deployment** for redundancy
4. ✅ **Configure N8N integration** for automation
5. ✅ **Implement monitoring** for proactive maintenance

### **Long-term Improvements:**
- **Database Migration:** SQLite → PostgreSQL
- **Caching Layer:** Redis for performance
- **Load Balancing:** Multiple instances
- **API Authentication:** Secure access control
- **Rate Limiting:** Prevent abuse

---

## 📁 **IMPLEMENTATION SCRIPTS**

### **🔧 Windows Service Setup Script**
Create `setup_windows_service.bat`:
```batch
@echo off
echo Setting up Instagram MCP as Windows Service...

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script must be run as Administrator!
    pause
    exit /b 1
)

REM Download and setup NSSM
if not exist "C:\nssm" (
    echo Downloading NSSM...
    mkdir C:\nssm
    REM Manual download required from https://nssm.cc/download
    echo Please download NSSM and extract to C:\nssm\
    pause
)

REM Create service wrapper
echo Creating service wrapper...
echo @echo off > service_wrapper.bat
echo cd /d "C:\InfluenciadorDigital\instagram-video-analyzer-mcp\backend" >> service_wrapper.bat
echo python -m app.main >> service_wrapper.bat

REM Install service
echo Installing Windows Service...
C:\nssm\win64\nssm install "Instagram-MCP-Backend" "%CD%\service_wrapper.bat"
C:\nssm\win64\nssm set "Instagram-MCP-Backend" DisplayName "Instagram Video Analyzer MCP Backend"
C:\nssm\win64\nssm set "Instagram-MCP-Backend" Description "Backend service for Instagram Video Analyzer MCP"
C:\nssm\win64\nssm set "Instagram-MCP-Backend" Start SERVICE_AUTO_START

REM Start service
echo Starting service...
C:\nssm\win64\nssm start "Instagram-MCP-Backend"

echo Service installed and started successfully!
echo You can manage it through Windows Services (services.msc)
pause
```

### **🐳 Docker Production Setup**
Create `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  instagram-mcp:
    build:
      context: .
      dockerfile: Dockerfile.prod
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@db:5432/instagram_mcp
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    restart: unless-stopped
    volumes:
      - ./data:/app/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: instagram_mcp
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs
    depends_on:
      - instagram-mcp
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### **🔄 Automated Deployment Script**
Create `deploy.sh`:
```bash
#!/bin/bash

# Instagram MCP Deployment Script
set -e

echo "🚀 Starting Instagram MCP Deployment..."

# Configuration
DOMAIN=${1:-"your-domain.com"}
EMAIL=${2:-"your-email@domain.com"}
ENVIRONMENT=${3:-"production"}

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install dependencies
echo "🔧 Installing dependencies..."
sudo apt install -y docker.io docker-compose nginx certbot python3-certbot-nginx git curl

# Clone or update repository
if [ -d "/opt/instagram-mcp" ]; then
    echo "📥 Updating existing repository..."
    cd /opt/instagram-mcp
    git pull origin main
else
    echo "📥 Cloning repository..."
    sudo git clone <your-repo-url> /opt/instagram-mcp
    cd /opt/instagram-mcp
fi

# Setup environment variables
echo "⚙️ Setting up environment..."
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
POSTGRES_PASSWORD=$(openssl rand -base64 32)
GEMINI_API_KEY=your-gemini-api-key-here
DOMAIN=$DOMAIN
EMAIL=$EMAIL
ENVIRONMENT=$ENVIRONMENT
EOF
    echo "Please edit .env file with your actual API keys!"
fi

# Build and start services
echo "🐳 Building and starting Docker services..."
sudo docker-compose -f docker-compose.prod.yml up -d --build

# Setup SSL certificate
echo "🔒 Setting up SSL certificate..."
sudo certbot --nginx -d $DOMAIN --email $EMAIL --agree-tos --non-interactive

# Setup monitoring
echo "📊 Setting up monitoring..."
cat > /opt/instagram-mcp/monitor.sh << 'EOF'
#!/bin/bash
# Health check script
HEALTH_URL="http://localhost:8000/health"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)

if [ $RESPONSE -ne 200 ]; then
    echo "$(date): Health check failed with status $RESPONSE" >> /var/log/instagram-mcp-monitor.log
    # Restart service
    cd /opt/instagram-mcp
    sudo docker-compose -f docker-compose.prod.yml restart instagram-mcp
fi
EOF

chmod +x /opt/instagram-mcp/monitor.sh

# Setup cron job for monitoring
echo "⏰ Setting up monitoring cron job..."
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/instagram-mcp/monitor.sh") | crontab -

echo "✅ Deployment completed successfully!"
echo "🌐 Your Instagram MCP is available at: https://$DOMAIN"
echo "📊 Health check: https://$DOMAIN/health"
echo "📚 API docs: https://$DOMAIN/docs"
```

### **🔍 N8N Custom Node**
Create `InstagramMCPNode.js`:
```javascript
const { INodeType, INodeTypeDescription } = require('n8n-workflow');

class InstagramMCP implements INodeType {
    description: INodeTypeDescription = {
        displayName: 'Instagram MCP',
        name: 'instagramMcp',
        group: ['transform'],
        version: 1,
        description: 'Analyze Instagram videos using MCP',
        defaults: {
            name: 'Instagram MCP',
        },
        inputs: ['main'],
        outputs: ['main'],
        properties: [
            {
                displayName: 'MCP Server URL',
                name: 'serverUrl',
                type: 'string',
                default: 'http://localhost:8000',
                required: true,
            },
            {
                displayName: 'Instagram URL',
                name: 'instagramUrl',
                type: 'string',
                default: '',
                required: true,
            },
            {
                displayName: 'Analysis Type',
                name: 'analysisType',
                type: 'options',
                options: [
                    { name: 'Comprehensive', value: 'comprehensive' },
                    { name: 'Transcription', value: 'transcription' },
                    { name: 'Visual Description', value: 'visual_description' },
                    { name: 'Summary', value: 'summary' },
                ],
                default: 'comprehensive',
            },
        ],
    };

    async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
        const items = this.getInputData();
        const returnData: INodeExecutionData[] = [];

        for (let i = 0; i < items.length; i++) {
            const serverUrl = this.getNodeParameter('serverUrl', i) as string;
            const instagramUrl = this.getNodeParameter('instagramUrl', i) as string;
            const analysisType = this.getNodeParameter('analysisType', i) as string;

            const response = await this.helpers.request({
                method: 'POST',
                url: `${serverUrl}/analyze`,
                body: {
                    url: instagramUrl,
                    analysis_type: analysisType,
                },
                json: true,
            });

            returnData.push({
                json: response,
            });
        }

        return [returnData];
    }
}

module.exports = { InstagramMCP };
```

---

## 🎯 **QUICK START CHECKLIST**

### **✅ Local Setup (5 minutes):**
1. [ ] Download and extract NSSM to `C:\nssm\`
2. [ ] Run `setup_windows_service.bat` as Administrator
3. [ ] Test with `get_system_stats_instagram-video-analyzer()`
4. [ ] Verify service in Windows Services (services.msc)

### **✅ VPS Setup (30 minutes):**
1. [ ] Create VPS instance (Ubuntu 22.04)
2. [ ] Point domain to VPS IP
3. [ ] Run deployment script: `./deploy.sh your-domain.com your-email@domain.com`
4. [ ] Update `.env` with actual API keys
5. [ ] Test external access

### **✅ N8N Integration (10 minutes):**
1. [ ] Install N8N: `npm install n8n -g`
2. [ ] Create HTTP Request node pointing to MCP
3. [ ] Test workflow with sample Instagram URL
4. [ ] Set up automation triggers

---

## 🆘 **TROUBLESHOOTING GUIDE**

### **❌ Common Issues:**

#### **"All connection attempts failed"**
```bash
# Check if backend is running
curl http://localhost:8000/health

# If not running, restart service
sudo systemctl restart instagram-mcp
# OR for Windows:
net stop "Instagram-MCP-Backend" && net start "Instagram-MCP-Backend"
```

#### **"Port 8000 already in use"**
```bash
# Find process using port 8000
sudo lsof -i :8000
# OR for Windows:
netstat -ano | findstr :8000

# Kill process and restart
sudo kill -9 <PID>
```

#### **"Database connection failed"**
```bash
# Check database status
sudo docker-compose logs db

# Reset database
sudo docker-compose down -v
sudo docker-compose up -d
```

### **📞 Support Resources:**
- **Documentation:** `/docs` endpoint on your deployment
- **Health Check:** `/health` endpoint
- **Metrics:** `/metrics` endpoint
- **Logs:** Check service logs for detailed error information

**🎉 This comprehensive guide covers all deployment scenarios for your Instagram MCP!**
