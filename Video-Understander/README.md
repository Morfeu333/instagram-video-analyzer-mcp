# Video-Understander

A comprehensive video analysis application powered by Google's Gemini Video Understanding API with full MCP (Model Context Protocol) support.

## 🎥 Features

### Core Video Analysis
- **Video Transcription**: Audio-to-text with precise timestamps (MM:SS format)
- **Visual Description**: Frame-by-frame analysis with customizable sampling rates
- **Question Answering**: Ask specific questions about video content
- **Scene Understanding**: Automatic video segmentation and description
- **Batch Processing**: Analyze up to 10 videos simultaneously
- **Multi-format Support**: mp4, mpeg, mov, avi, flv, mkv, webm

### Video Sources
- **YouTube URLs**: Direct processing of YouTube videos
- **Local Files**: Upload and analyze local video files
- **Instagram/TikTok**: Download and analyze social media videos
- **Streaming URLs**: Process videos from various streaming platforms

### Advanced Capabilities
- **Custom Sampling**: Adjustable frame rate analysis (default 1 FPS)
- **Video Trimming**: Analyze specific segments with start/end offsets
- **Large File Support**: Handle videos up to 2GB and 2 hours duration
- **Context Awareness**: 2M token context window for comprehensive analysis

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Environment Setup
```bash
# Copy environment template
cp config/.env.template config/.env

# Add your Gemini API key
GEMINI_API_KEY=your_api_key_here
```

### Basic Usage
```python
from src.video_analyzer import VideoAnalyzer

analyzer = VideoAnalyzer()

# Analyze YouTube video
result = analyzer.analyze_video_url("https://youtube.com/watch?v=...")

# Analyze local file
result = analyzer.analyze_video_file("path/to/video.mp4")

# Get transcription with timestamps
transcription = analyzer.transcribe_video("video.mp4")
```

### MCP Server
```bash
# Start MCP server
python src/mcp_server.py

# Available MCP functions:
# - analyze_video_from_url
# - analyze_video_file
# - transcribe_video
# - ask_video_question
# - summarize_video
# - extract_scenes
# - batch_analyze
# - get_video_info
```

## 📁 Project Structure

```
Video-Understander/
├── src/
│   ├── __init__.py
│   ├── video_analyzer.py      # Core Gemini integration
│   ├── video_downloader.py    # Download from various sources
│   ├── mcp_server.py          # MCP protocol server
│   ├── file_manager.py        # File handling and storage
│   └── utils/
│       ├── __init__.py
│       ├── gemini_client.py   # Gemini API client
│       ├── video_processor.py # Video processing utilities
│       └── validators.py      # Input validation
├── tests/
├── docs/
├── examples/
├── config/
│   ├── .env.template
│   └── settings.py
├── requirements.txt
└── README.md
```

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key
- `MAX_VIDEO_SIZE`: Maximum video file size (default: 2GB)
- `MAX_VIDEO_DURATION`: Maximum video duration (default: 2 hours)
- `DEFAULT_SAMPLING_RATE`: Default frame sampling rate (default: 1 FPS)
- `STORAGE_PATH`: Path for temporary video storage

### API Limits
- **File Size**: Up to 2GB per video
- **Duration**: Up to 2 hours (standard) or 6 hours (low resolution)
- **Batch Size**: Up to 10 videos simultaneously
- **Context**: 2M tokens per analysis

## 📖 Documentation

See the `docs/` directory for detailed documentation:
- [API Reference](docs/api_reference.md)
- [MCP Integration](docs/mcp_integration.md)
- [Video Processing](docs/video_processing.md)
- [Examples](examples/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.
