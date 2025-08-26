# 🚀 Instagram Video Analyzer MCP - Installation Guide

## 📋 Prerequisites

### System Requirements
- **Python**: 3.11 or higher
- **Node.js**: 18+ (for frontend, optional)
- **Git**: Latest version
- **FFmpeg**: For video processing
- **Google AI API Key**: For Gemini integration

### Platform Support
- ✅ Windows 10/11
- ✅ macOS 12+
- ✅ Linux (Ubuntu 20.04+)

## 🔧 Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Morfeu333/instagram-video-analyzer-mcp.git
cd instagram-video-analyzer-mcp
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Configure Environment Variables
Create `.env` file in `backend/` directory:

```bash
# backend/.env
DATABASE_URL=sqlite:///./video_analyzer.db
GOOGLE_API_KEY=your_gemini_api_key_here
UPLOAD_DIR=../data/videos
RESULTS_DIR=../data/results
TEMP_DIR=../data/temp
MAX_FILE_SIZE=104857600
LOG_LEVEL=INFO
```

#### Initialize Database
```bash
python -c "
from app.database import init_db
init_db()
print('Database initialized successfully!')
"
```

#### Test Backend
```bash
python -m app.main
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 3. MCP Server Setup

#### Install UV (Python Package Manager)
```bash
# Windows
curl -LsSf https://astral.sh/uv/install.ps1 | powershell

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Install MCP Dependencies
```bash
cd mcp-server
uv sync
```

#### Test MCP Server
```bash
uv run instagram-video-analyzer-mcp
```

### 4. Claude Code Integration

#### Locate Configuration File

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/claude/claude_desktop_config.json`

#### Add MCP Configuration

```json
{
  "mcpServers": {
    "instagram-video-analyzer": {
      "command": "uv",
      "args": [
        "--directory", 
        "/full/path/to/instagram-video-analyzer-mcp/mcp-server", 
        "run", 
        "instagram-video-analyzer-mcp"
      ],
      "env": {
        "API_BASE_URL": "http://localhost:8000",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Important**: Replace `/full/path/to/` with your actual installation path.

#### Restart Claude Code
Close and reopen Claude Code to load the new MCP server.

### 5. Verify Installation

#### Test Backend API
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "timestamp": "2025-08-26T05:00:00Z"}
```

#### Test MCP Integration
In Claude Code, try:
```
Get system statistics for the Instagram video analyzer
```

You should see system metrics and confirmation that the MCP is working.

#### Test Video Analysis
```
Analyze this Instagram video: https://www.instagram.com/reel/DMiEEmlMI7J/
```

## 🔑 API Key Setup

### Google AI (Gemini) API Key

1. **Visit Google AI Studio**: https://aistudio.google.com/
2. **Create API Key**: Click "Get API Key" → "Create API Key"
3. **Copy Key**: Save the generated key securely
4. **Add to Environment**: Update your `.env` file

```bash
GOOGLE_API_KEY=AIzaSyC_your_actual_api_key_here
```

### Verify API Key
```bash
python -c "
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content('Hello, world!')
    print('✅ Google AI API key is working!')
    print(f'Response: {response.text[:50]}...')
except Exception as e:
    print(f'❌ API key error: {e}')
"
```

## 📁 Directory Structure After Installation

```
instagram-video-analyzer-mcp/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application
│   │   ├── database.py             # Database configuration
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── models.py           # SQLAlchemy models
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── ai_analyzer.py      # AI analysis service
│   │       └── instagram_downloader.py
│   ├── requirements.txt
│   ├── .env                        # Environment variables
│   └── video_analyzer.db           # SQLite database
├── mcp-server/
│   ├── instagram_video_analyzer_mcp.py
│   ├── pyproject.toml
│   ├── uv.lock
│   └── tests/
├── data/
│   ├── videos/                     # Downloaded videos
│   ├── results/                    # Analysis results
│   └── temp/                       # Temporary files
├── docs/
├── frontend/ (optional)
├── README.md
├── TECHNICAL_DOCUMENTATION.md
├── INSTALLATION_GUIDE.md
└── LICENSE
```

## 🧪 Testing Your Installation

### 1. Backend Health Check
```bash
curl -X GET http://localhost:8000/health
```

### 2. System Statistics
```bash
curl -X GET http://localhost:8000/stats
```

### 3. Video Information
```bash
curl -X GET "http://localhost:8000/video-info?url=https://www.instagram.com/reel/DMiEEmlMI7J/"
```

### 4. Full Analysis Test
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.instagram.com/reel/DMiEEmlMI7J/", "analysis_type": "transcription"}'
```

### 5. MCP Tools Test
In Claude Code:
```
List recent video analyses and show system statistics
```

## 🔧 Troubleshooting

### Common Installation Issues

#### Python Version Error
```bash
python --version  # Should be 3.11+
```

If older version:
```bash
# Install Python 3.11+ from python.org
# Or use pyenv:
pyenv install 3.11.0
pyenv global 3.11.0
```

#### UV Installation Failed
```bash
# Alternative installation
pip install uv
```

#### FFmpeg Missing
```bash
# Windows (using chocolatey)
choco install ffmpeg

# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg
```

#### Database Permission Error
```bash
# Ensure data directory exists and is writable
mkdir -p data/videos data/results data/temp
chmod 755 data/
```

#### Claude Code Not Detecting MCP
1. **Check configuration file path**
2. **Verify JSON syntax** (use JSON validator)
3. **Restart Claude Code completely**
4. **Check MCP server logs**

### Debug Commands

#### View Backend Logs
```bash
tail -f backend/app.log
```

#### Test MCP Server Directly
```bash
cd mcp-server
uv run python -c "
import asyncio
from instagram_video_analyzer_mcp import get_system_stats
print(asyncio.run(get_system_stats()))
"
```

#### Check Database
```bash
sqlite3 backend/video_analyzer.db ".tables"
sqlite3 backend/video_analyzer.db "SELECT COUNT(*) FROM video_jobs;"
```

## 🚀 Next Steps

After successful installation:

1. **Read the [Technical Documentation](TECHNICAL_DOCUMENTATION.md)**
2. **Explore the [API Reference](README.md#api-reference)**
3. **Try the [Usage Examples](README.md#usage-examples)**
4. **Set up monitoring and logging**
5. **Consider production deployment**

## 🆘 Getting Help

If you encounter issues:

1. **Check the logs** for detailed error messages
2. **Review this guide** for missed steps
3. **Search existing issues** on GitHub
4. **Create a new issue** with:
   - Your operating system
   - Python version
   - Complete error message
   - Steps to reproduce

---

**Installation Support**: [GitHub Issues](https://github.com/Morfeu333/instagram-video-analyzer-mcp/issues)
**Documentation**: [README.md](README.md)
**Technical Details**: [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)
