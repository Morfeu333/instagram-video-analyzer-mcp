# 🌐 MCP SSE Server - Quick Start

HTTP/SSE transport for online MCP access.

## 🚀 Quick Start

### Local Testing

1. **Install dependencies:**
```bash
pip install -r requirements-sse.txt
```

2. **Create .env.sse file:**
```bash
cp .env.sse.example .env.sse
nano .env.sse
```

3. **Run server:**
```bash
python mcp_sse_server.py
```

4. **Test:**
```bash
# Generate test API key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Test health check
curl -H "Authorization: Bearer YOUR_KEY" http://localhost:8100/health
```

### VPS Deployment

See [MCP_ONLINE_DEPLOYMENT_GUIDE.md](../MCP_ONLINE_DEPLOYMENT_GUIDE.md) for complete deployment instructions.

**Quick deploy:**
```bash
cd /home/iganalyzer/instagram-video-analyzer-mcp/deploy
./deploy-mcp-sse.sh
sudo ./deploy-mcp-systemd.sh
```

## 📡 Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/` | GET | No | Server info |
| `/health` | GET | Yes | Health check |
| `/sse` | GET | Yes | SSE connection (MCP protocol) |
| `/messages` | POST | Yes | Send messages |
| `/sessions` | GET | Yes | List active sessions |
| `/generate-key` | POST | Yes | Generate new API key |

## 🔑 Authentication

All endpoints (except `/`) require Bearer token authentication:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://yourdomain.com/mcp/health
```

## 🧪 Testing

```bash
# Set environment variables
export MCP_SSE_URL="https://yourdomain.com/mcp"
export MCP_API_KEY="your-api-key-here"

# Run test client
python test_mcp_sse_client.py
```

## 🔧 Configuration

**Environment variables in `.env.sse`:**

```env
API_BASE_URL=http://localhost:8000
MCP_SERVER_PORT=8100
MCP_API_KEYS=key1,key2,key3
LOG_LEVEL=INFO
```

## 💻 Client Configuration

### Claude Desktop

```json
{
  "mcpServers": {
    "instagram-video-analyzer": {
      "transport": "sse",
      "url": "https://yourdomain.com/mcp/sse",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

### Custom Python Client

```python
import httpx

async with httpx.AsyncClient() as client:
    async with client.stream(
        "GET",
        "https://yourdomain.com/mcp/sse",
        headers={"Authorization": "Bearer YOUR_KEY"}
    ) as response:
        async for line in response.aiter_lines():
            if line.startswith("data: "):
                print(line[6:])
```

## 🐛 Troubleshooting

**Server won't start:**
```bash
# Check port availability
sudo netstat -tulpn | grep 8100

# Check logs
python mcp_sse_server.py
```

**Authentication fails:**
```bash
# Verify API key in .env.sse
cat .env.sse | grep MCP_API_KEYS
```

**Can't connect from client:**
```bash
# Test locally first
curl -H "Authorization: Bearer YOUR_KEY" http://localhost:8100/health

# Then test through nginx
curl -H "Authorization: Bearer YOUR_KEY" https://yourdomain.com/mcp/health
```

## 📚 Documentation

- [Complete Deployment Guide](../MCP_ONLINE_DEPLOYMENT_GUIDE.md)
- [VPS Setup Guide](../VPS_DEPLOYMENT_GUIDE.md)
- [MCP Protocol Docs](https://github.com/anthropics/mcp-specification)

## 🔒 Security

- Always use HTTPS in production
- Rotate API keys regularly
- Use strong API keys (32+ characters)
- Enable rate limiting in nginx
- Monitor access logs

## 📊 Monitoring

```bash
# Active connections
curl -H "Authorization: Bearer YOUR_KEY" \
     https://yourdomain.com/mcp/sessions

# View logs
sudo journalctl -u iganalyzer-mcp-sse -f
```

---

**Happy MCP-ing! 🚀**
