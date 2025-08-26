# 🔧 Instagram Video Analyzer MCP - Technical Documentation

## 📋 Table of Contents
- [Architecture Overview](#architecture-overview)
- [System Components](#system-components)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## 🏗️ Architecture Overview

The Instagram Video Analyzer MCP is a comprehensive system that combines:

### Core Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Claude Code   │    │   MCP Server    │    │  Backend API    │
│   (Client)      │◄──►│   (Bridge)      │◄──►│   (FastAPI)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                              ┌─────────────────┐
                                              │  Google Gemini  │
                                              │   AI Service    │
                                              └─────────────────┘
```

### Technology Stack
- **MCP Server**: Python 3.11+ with FastMCP
- **Backend API**: FastAPI with SQLAlchemy
- **AI Processing**: Google Gemini 2.5 Flash
- **Database**: SQLite (local) / PostgreSQL (production)
- **Video Processing**: Instaloader + FFmpeg
- **Frontend**: React + TypeScript + Vite (optional)

## 🧩 System Components

### 1. MCP Server (`mcp-server/`)
**File**: `instagram_video_analyzer_mcp.py`

**Purpose**: Bridge between Claude Code and the Backend API

**Key Functions**:
```python
@mcp.tool()
async def analyze_instagram_video(url: str, analysis_type: str = "comprehensive"):
    """Main analysis function"""
    
@mcp.tool()
async def get_job_status(job_id: str):
    """Check analysis progress"""
    
@mcp.tool()
async def get_system_stats():
    """System performance metrics"""
```

**Configuration**:
```python
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
```

### 2. Backend API (`backend/`)
**Main File**: `app/main.py`

**Key Endpoints**:
- `POST /analyze` - Start video analysis
- `GET /job/{job_id}` - Get job status
- `GET /jobs/recent` - List recent analyses
- `DELETE /job/{job_id}` - Cancel job
- `GET /stats` - System statistics
- `GET /video-info` - Basic video info

**Database Models** (`app/models/models.py`):
```python
class VideoJob(Base):
    id = Column(String, primary_key=True)
    url = Column(String, nullable=False)
    status = Column(String, default="pending")
    analysis_type = Column(String, default="comprehensive")
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    file_path = Column(String)
    file_size = Column(Integer)
    
class AnalysisResult(Base):
    id = Column(String, primary_key=True)
    job_id = Column(String, ForeignKey("video_jobs.id"))
    analysis_type = Column(String)
    model_used = Column(String)
    raw_response = Column(Text)
    structured_analysis = Column(JSON)
```

### 3. AI Processing Pipeline

**Video Download**:
```python
# Instagram video extraction
loader = instaloader.Instaloader()
post = instaloader.Post.from_shortcode(loader.context, shortcode)
video_url = post.video_url
```

**AI Analysis**:
```python
# Google Gemini integration
model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content([
    video_file,
    analysis_prompt
])
```

## 🔌 API Endpoints

### Analysis Endpoints

#### `POST /analyze`
Start a new video analysis job.

**Request Body**:
```json
{
  "url": "https://www.instagram.com/reel/DMiEEmlMI7J/",
  "analysis_type": "comprehensive"
}
```

**Response**:
```json
{
  "success": true,
  "job_id": "e3e209e9-6f2f-4f00-8ece-753fc7a365a2",
  "status": "pending",
  "message": "Analysis started successfully"
}
```

#### `GET /job/{job_id}`
Get the status and results of an analysis job.

**Response**:
```json
{
  "job_id": "e3e209e9-6f2f-4f00-8ece-753fc7a365a2",
  "status": "completed",
  "progress": 100,
  "created_at": "2025-08-26T04:58:17.768790",
  "completed_at": "2025-08-26T04:59:17.773436",
  "analysis_result": {
    "analysis_type": "transcription",
    "model_used": "gemini-2.5-flash",
    "file_size": 10451323,
    "raw_response": "Detailed transcription...",
    "structured_analysis": {
      "word_count": 229,
      "sections": {},
      "full_text": "Complete transcription..."
    }
  }
}
```

### System Endpoints

#### `GET /stats`
Get system performance statistics.

**Response**:
```json
{
  "total_jobs": 19,
  "pending_jobs": 0,
  "processing_jobs": 0,
  "completed_jobs": 19,
  "failed_jobs": 0,
  "disk_usage": {
    "upload": {
      "path": "data/videos",
      "total_size": 197848583,
      "total_size_mb": 188.68,
      "file_count": 57
    },
    "results": {
      "path": "data/results",
      "total_size": 143545,
      "total_size_mb": 0.14,
      "file_count": 31
    }
  }
}
```

## 🗄️ Database Schema

### Tables

#### `video_jobs`
```sql
CREATE TABLE video_jobs (
    id VARCHAR PRIMARY KEY,
    url VARCHAR NOT NULL,
    status VARCHAR DEFAULT 'pending',
    analysis_type VARCHAR DEFAULT 'comprehensive',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    file_path VARCHAR,
    file_size INTEGER,
    error_message TEXT
);
```

#### `analysis_results`
```sql
CREATE TABLE analysis_results (
    id VARCHAR PRIMARY KEY,
    job_id VARCHAR REFERENCES video_jobs(id),
    analysis_type VARCHAR,
    model_used VARCHAR,
    raw_response TEXT,
    structured_analysis JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### `user_sessions`
```sql
CREATE TABLE user_sessions (
    id VARCHAR PRIMARY KEY,
    session_id VARCHAR UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_activity DATETIME,
    total_jobs INTEGER DEFAULT 0
);
```

#### `system_metrics`
```sql
CREATE TABLE system_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_name VARCHAR,
    metric_value REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## ⚙️ Configuration

### Environment Variables

#### MCP Server
```bash
API_BASE_URL=http://localhost:8000
LOG_LEVEL=INFO
```

#### Backend API
```bash
# Database
DATABASE_URL=sqlite:///./video_analyzer.db

# Google AI
GOOGLE_API_KEY=your_gemini_api_key

# File Storage
UPLOAD_DIR=../data/videos
RESULTS_DIR=../data/results
TEMP_DIR=../data/temp

# API Settings
MAX_FILE_SIZE=100MB
ALLOWED_DOMAINS=instagram.com,www.instagram.com
```

### Claude Code Configuration
```json
{
  "mcpServers": {
    "instagram-video-analyzer": {
      "command": "uv",
      "args": [
        "--directory", 
        "C:/InfluenciadorDigital/instagram-video-analyzer-mcp/mcp-server", 
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

## 🚀 Deployment

### Local Development

1. **Start Backend**:
```bash
cd backend
python -m app.main
```

2. **Start MCP Server**:
```bash
cd mcp-server
uv run instagram-video-analyzer-mcp
```

### Production Deployment

#### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/analyzer
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    volumes:
      - ./data:/app/data
      
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=analyzer
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 📊 Monitoring

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# MCP server status
curl http://localhost:8000/stats
```

### Logging
- **Backend**: Structured JSON logs with timestamps
- **MCP Server**: Emoji-enhanced logs for better readability
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL

### Metrics Tracked
- Total jobs processed
- Success/failure rates
- Average processing time
- Disk usage statistics
- API response times

## 🔧 Troubleshooting

### Common Issues

#### MCP Server Connection Failed
```bash
# Check if backend is running
curl http://localhost:8000/health

# Verify MCP configuration
cat ~/.config/claude/claude_desktop_config.json

# Check MCP server logs
uv run instagram-video-analyzer-mcp --log-level DEBUG
```

#### Video Download Fails
```bash
# Test Instagram URL manually
python -c "
import instaloader
L = instaloader.Instaloader()
post = instaloader.Post.from_shortcode(L.context, 'DMiEEmlMI7J')
print(post.video_url)
"
```

#### AI Analysis Timeout
```bash
# Check Google API key
export GOOGLE_API_KEY=your_key
python -c "import google.generativeai as genai; genai.configure(api_key='$GOOGLE_API_KEY'); print('OK')"
```

### Debug Commands
```bash
# View recent logs
tail -f backend/app.log

# Check database
sqlite3 backend/video_analyzer.db ".tables"

# Test MCP tools
uv run python -c "
from instagram_video_analyzer_mcp import get_system_stats
import asyncio
print(asyncio.run(get_system_stats()))
"
```

---

**Last Updated**: August 26, 2025
**Version**: 2.0.0
