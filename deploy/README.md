# 📦 Deployment Scripts

Automated deployment scripts for Instagram Video Analyzer on Ubuntu VPS.

## 📁 Files

- **`VPS_DEPLOYMENT_GUIDE.md`** - Complete step-by-step deployment guide
- **`setup-vps.sh`** - Initial VPS setup (run as root)
- **`deploy-backend.sh`** - Backend deployment (run as iganalyzer user)
- **`deploy-frontend.sh`** - Frontend deployment (run as iganalyzer user)
- **`deploy-systemd.sh`** - Systemd service setup (run as root)
- **`nginx-config-template.conf`** - Nginx configuration template
- **`quick-deploy.sh`** - Complete automated deployment (run as root)

## 🚀 Quick Start

### Option 1: Automated Deployment (Recommended)

```bash
# On your VPS as root
cd /root
wget https://your-repo/deploy/quick-deploy.sh
chmod +x quick-deploy.sh
./quick-deploy.sh
```

### Option 2: Manual Step-by-Step

```bash
# 1. Initial VPS setup (as root)
wget https://your-repo/deploy/setup-vps.sh
chmod +x setup-vps.sh
./setup-vps.sh

# 2. Switch to iganalyzer user
su - iganalyzer

# 3. Deploy backend
cd /tmp
wget https://your-repo/deploy/deploy-backend.sh
chmod +x deploy-backend.sh
./deploy-backend.sh

# 4. Edit .env file
nano /home/iganalyzer/instagram-video-analyzer-mcp/backend/.env

# 5. Deploy frontend
wget https://your-repo/deploy/deploy-frontend.sh
chmod +x deploy-frontend.sh
./deploy-frontend.sh

# 6. Exit to root
exit

# 7. Setup systemd (as root)
wget https://your-repo/deploy/deploy-systemd.sh
chmod +x deploy-systemd.sh
./deploy-systemd.sh

# 8. Configure Nginx
wget https://your-repo/deploy/nginx-config-template.conf -O /etc/nginx/sites-available/iganalyzer
# Edit with your domain
nano /etc/nginx/sites-available/iganalyzer
ln -s /etc/nginx/sites-available/iganalyzer /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx

# 9. Setup SSL
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## 📋 Prerequisites

- Ubuntu 22.04 LTS or 24.04 LTS VPS
- Root access
- Domain name pointed to VPS IP
- Gemini API key

## ⚙️ Configuration

### Backend Environment Variables

Edit `/home/iganalyzer/instagram-video-analyzer-mcp/backend/.env`:

```env
GEMINI_API_KEY=your_actual_key_here
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Nginx Domain

Edit `/etc/nginx/sites-available/iganalyzer`:

Replace `yourdomain.com` with your actual domain.

## 🔍 Verification

```bash
# Check backend
sudo systemctl status iganalyzer-backend
curl https://yourdomain.com/health

# Check frontend
curl https://yourdomain.com

# View logs
sudo journalctl -u iganalyzer-backend -f
```

## 🐛 Troubleshooting

### Backend won't start
```bash
sudo journalctl -u iganalyzer-backend -n 50
cd /home/iganalyzer/instagram-video-analyzer-mcp/backend
source venv/bin/activate
python -m app.main  # Test manually
```

### Frontend 404 errors
```bash
cd /home/iganalyzer/instagram-video-analyzer-mcp/frontend
npm run build
sudo systemctl reload nginx
```

### SSL certificate issues
```bash
sudo certbot renew --force-renewal
sudo systemctl reload nginx
```

## 📚 Full Documentation

See **VPS_DEPLOYMENT_GUIDE.md** for complete documentation including:
- Detailed setup instructions
- MCP server configuration
- Security best practices
- Monitoring and maintenance
- Backup procedures

## 🔐 Security Notes

1. Always use strong passwords
2. Keep `.env` file permissions strict: `chmod 600 .env`
3. Enable firewall: `ufw enable`
4. Keep system updated: `apt update && apt upgrade`
5. Use SSL/HTTPS in production

## 📞 Support

For issues and questions:
- Check logs: `/home/iganalyzer/logs/`
- Review full guide: `VPS_DEPLOYMENT_GUIDE.md`
- GitHub Issues: [Your repo issues page]

---

**Happy Deploying! 🚀**
