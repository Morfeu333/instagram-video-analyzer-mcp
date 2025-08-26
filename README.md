# 🎬 Instagram Video Analyzer MCP Server

A comprehensive Model Context Protocol (MCP) server for analyzing Instagram videos using AI. This server enables Claude and other LLMs to analyze Instagram content with advanced AI capabilities including transcription, visual analysis, and content insights.

## 🎯 **What This Does**

Transform Instagram videos into actionable insights using AI:
- **📝 Transcription**: Convert speech to text with timestamps
- **👁️ Visual Analysis**: Detailed scene-by-scene descriptions
- **🧠 Content Insights**: Extract key themes, emotions, and engagement factors
- **📊 Performance Metrics**: Track analysis jobs and system health
- **🔄 Real-time Processing**: Monitor progress with live updates

**Perfect for**: Content creators, marketers, researchers, and AI enthusiasts who need to analyze Instagram video content at scale.

## 🌟 Features

### 🛠️ **6 Powerful Tools**
- **`analyze_instagram_video`** - Complete video analysis with AI
- **`get_job_status`** - Monitor analysis progress
- **`list_recent_analyses`** - View recent analysis history
- **`cancel_job`** - Cancel running analyses
- **`get_system_stats`** - System performance metrics
- **`get_video_info`** - Basic video information

### 📚 **3 Dynamic Resources**
- **`analysis://{job_id}`** - Access specific analysis results
- **`jobs://recent`** - Recent jobs overview
- **`stats://system`** - Real-time system statistics

### 🎯 **Analysis Types**
- **Comprehensive** - Full analysis with transcription, visual description, and insights
- **Transcription** - Audio-to-text conversion only
- **Visual Description** - Detailed visual content analysis
- **Summary** - Concise content overview

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Google AI API Key (for Gemini)
- Claude Code or compatible MCP client
- FFmpeg (for video processing)

### ⚡ 5-Minute Setup

1. **Clone and setup:**
```bash
git clone https://github.com/Morfeu333/instagram-video-analyzer-mcp.git
cd instagram-video-analyzer-mcp
```

2. **Start the backend:**
```bash
cd backend
pip install -r requirements.txt
# Add your GOOGLE_API_KEY to .env file
python -m app.main
```

3. **Install and run MCP server:**
```bash
cd mcp-server
uv sync
uv run instagram-video-analyzer-mcp
```

4. **Configure Claude Code** (see [Installation Guide](INSTALLATION_GUIDE.md) for details)

### Claude Code Configuration

Add to your Claude Code configuration file:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux:** `~/.config/claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "instagram-video-analyzer": {
      "command": "uv",
      "args": ["--directory", "/path/to/mcp-server", "run", "instagram-video-analyzer-mcp"],
      "env": {
        "API_BASE_URL": "http://localhost:8000",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## 📖 Usage Examples

### 🎬 Basic Video Analysis
```
Analyze this Instagram video: https://www.instagram.com/reel/DMiEEmlMI7J/
```
**Result**: Complete transcription + visual analysis + content insights

### 📝 Transcription Only
```
Get only the transcription of this video: https://www.instagram.com/reel/DMiEEmlMI7J/
```
**Result**: Timestamped speech-to-text conversion

### 👁️ Visual Analysis
```
Describe the visual content of this video: https://www.instagram.com/reel/DMiEEmlMI7J/
```
**Result**: Scene-by-scene visual descriptions

### 📊 Batch Analysis
```
Analyze these 5 Instagram videos and compare their content themes:
- https://www.instagram.com/reel/video1/
- https://www.instagram.com/reel/video2/
- https://www.instagram.com/reel/video3/
```

### 🔍 System Monitoring
```
Show me the system statistics and recent analyses
```
**Result**: Performance metrics, job history, disk usage

## 🔧 API Reference

### Tools

#### `analyze_instagram_video`
Analyzes an Instagram video using AI.

**Parameters:**
- `url` (string, required): Instagram video URL
- `analysis_type` (string, optional): Type of analysis
  - `comprehensive` (default): Complete analysis
  - `transcription`: Audio transcription only
  - `visual_description`: Visual content analysis
  - `summary`: Concise overview

**Returns:**
```json
{
  "success": true,
  "job_id": "uuid-string",
  "status": "completed",
  "analysis": {
    "analysis_type": "comprehensive",
    "model_used": "gemini-2.5-flash",
    "raw_response": "Detailed analysis...",
    "file_size": 19058688
  }
}
```

#### `get_job_status`
Retrieves the status of an analysis job.

**Parameters:**
- `job_id` (string, required): Job identifier

**Returns:**
```json
{
  "job_id": "uuid-string",
  "status": "completed",
  "progress": 100,
  "created_at": "2024-01-15T10:30:00Z",
  "completed_at": "2024-01-15T10:32:30Z",
  "analysis_result": { ... }
}
```

#### `list_recent_analyses`
Lists recent video analyses.

**Parameters:**
- `limit` (int, optional): Maximum results (default: 10)
- `page` (int, optional): Page number (default: 1)

#### `cancel_job`
Cancels a running analysis job.

**Parameters:**
- `job_id` (string, required): Job to cancel

#### `get_system_stats`
Retrieves system performance statistics.

**Returns:**
```json
{
  "total_jobs": 150,
  "completed_jobs": 142,
  "failed_jobs": 3,
  "pending_jobs": 5,
  "success_rate": 94.67,
  "average_processing_time": 125.5
}
```

#### `get_video_info`
Gets basic information about an Instagram video.

**Parameters:**
- `url` (string, required): Instagram video URL

### Resources

#### `analysis://{job_id}`
Access detailed results of a specific analysis.

#### `jobs://recent`
Overview of recent analysis jobs.

#### `stats://system`
Real-time system performance metrics.

## 🎯 Advanced Features

### Scene-by-Scene Analysis
The MCP server can provide synchronized analysis where each spoken phrase is matched with its corresponding visual scene:

```
Frase 1 (0:00-0:03): "Check out this amazing tip!"
Scene 1: Close-up of person's face, excited expression, blurred background...

Frase 2 (0:03-0:07): "You'll only need..."
Scene 2: Hands holding objects, organized desk, natural lighting...
```

### Batch Processing
Analyze multiple videos and compare insights across content.

### Real-time Monitoring
Track analysis progress and system performance in real-time.

## 🔍 Troubleshooting

### Common Issues

**MCP Server won't start:**
- Verify Python 3.11+ is installed
- Check that the API is running: `curl http://localhost:8000/health`
- Ensure all dependencies are installed: `uv sync`

**Analysis fails:**
- Verify the Instagram URL is valid and public
- Check API connectivity
- Review logs for detailed error messages

**Claude Code integration issues:**
- Verify configuration file path and syntax
- Restart Claude Code after configuration changes
- Check MCP server logs for connection errors

### Logging
The server provides structured logging for debugging:

```
2024-01-15 10:30:00 INFO 🚀 Starting Instagram Video Analyzer MCP Server...
2024-01-15 10:30:01 INFO ✅ API connection established
2024-01-15 10:30:15 INFO 🎬 Starting video analysis: https://instagram.com/reel/...
```

## 🧪 Testing

Run the test suite:
```bash
cd mcp-server
uv run pytest tests/ -v
```

## 📁 Project Structure

```
instagram-video-analyzer-mcp/
├── 📂 backend/                        # FastAPI backend server
│   ├── app/
│   │   ├── main.py                    # FastAPI application
│   │   ├── database.py                # Database configuration
│   │   ├── models/                    # SQLAlchemy models
│   │   └── services/                  # AI analysis services
│   ├── requirements.txt
│   └── .env                          # Environment variables
├── 📂 mcp-server/                     # MCP bridge server
│   ├── instagram_video_analyzer_mcp.py
│   ├── pyproject.toml
│   └── tests/
├── 📂 data/                          # Storage directories
│   ├── videos/                       # Downloaded Instagram videos
│   ├── results/                      # Analysis results
│   └── temp/                         # Temporary processing files
├── 📂 docs/                          # Documentation
├── 📂 frontend/                      # Optional React frontend
├── 📂 vibekanban-templates/          # Automation workflows
├── 📄 README.md                      # This file
├── 📄 INSTALLATION_GUIDE.md          # Setup instructions
├── 📄 TECHNICAL_DOCUMENTATION.md     # Technical details
└── 📄 LICENSE                        # MIT License
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Documentation

- **📖 [Installation Guide](INSTALLATION_GUIDE.md)** - Complete setup instructions
- **🔧 [Technical Documentation](TECHNICAL_DOCUMENTATION.md)** - Architecture and API details
- **🎯 [Usage Examples](README.md#usage-examples)** - Common use cases
- **🐛 [Troubleshooting](TECHNICAL_DOCUMENTATION.md#troubleshooting)** - Common issues and solutions

## 🆘 Support

- **🐛 Issues**: [GitHub Issues](https://github.com/Morfeu333/instagram-video-analyzer-mcp/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/Morfeu333/instagram-video-analyzer-mcp/discussions)
- **📧 Contact**: Create an issue for support requests

## 🎉 Acknowledgments

- Built with [FastMCP](https://github.com/modelcontextprotocol/python-sdk)
- Powered by Google Gemini AI
- Instagram content processing via Instaloader

---

**Made with ❤️ for the AI community**
