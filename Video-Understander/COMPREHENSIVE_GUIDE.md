# 🎥 Video-Understander: Complete Usage Guide

## 📋 Table of Contents
1. [Installation & Setup](#installation--setup)
2. [Quick Start](#quick-start)
3. [CLI Usage](#cli-usage)
4. [MCP Server](#mcp-server)
5. [Python API](#python-api)
6. [Instagram Video Processing](#instagram-video-processing)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11+ (recommended)
- FFmpeg installed on system
- Google Gemini API key

### Step 1: Install Dependencies
```bash
cd Video-Understander
pip install -r requirements.txt
```

### Step 2: Configure Environment
Your API key is already configured in `config/.env`:
```env
GEMINI_API_KEY=AIzaSyDtBbilIcTPVv466TjIjB0JPuIz8rPnDl0
```

### Step 3: Verify Installation
```bash
python main.py info
```

---

## ⚡ Quick Start

### Analyze a YouTube Video
```bash
python main.py analyze-url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --type transcription --format markdown
```

### Process Instagram Videos (Your Use Case!)
```bash
python main.py batch-instagram \
  "https://www.instagram.com/reel/DNI-L5Eicg2/" \
  "https://www.instagram.com/reel/DNGZeTnChuH/" \
  "https://www.instagram.com/reel/DM25RH8iL3B/" \
  --output-dir "AI-Transcrips" \
  --type comprehensive
```

### Ask Questions About Video
```bash
python main.py ask "path/to/video.mp4" "What is the main topic discussed?"
```

---

## 💻 CLI Usage

### Available Commands

#### 1. `analyze-url` - Analyze Video from URL
```bash
python main.py analyze-url <URL> [OPTIONS]

Options:
  --type, -t          Analysis type [comprehensive|transcription|summary|visual_description]
  --output, -o        Output file path
  --format, -f        Output format [json|markdown]
  --sampling-rate     Frame sampling rate (FPS)
  --start            Start time in seconds
  --end              End time in seconds
```

**Examples:**
```bash
# Comprehensive analysis
python main.py analyze-url "https://youtube.com/watch?v=abc123" --type comprehensive

# Transcription with timestamps
python main.py analyze-url "https://instagram.com/reel/abc123" --type transcription --format markdown

# Analyze specific segment
python main.py analyze-url "https://youtube.com/watch?v=abc123" --start 30 --end 120
```

#### 2. `analyze-file` - Analyze Local Video
```bash
python main.py analyze-file <VIDEO_PATH> [OPTIONS]

Options:
  --type, -t          Analysis type
  --output, -o        Output file path
  --format, -f        Output format [json|markdown]
```

**Examples:**
```bash
# Analyze local file
python main.py analyze-file "videos/my_video.mp4" --type transcription

# Save results to specific file
python main.py analyze-file "video.mp4" --output "results/analysis.json"
```

#### 3. `ask` - Ask Questions About Video
```bash
python main.py ask <VIDEO_PATH> <QUESTION> [OPTIONS]

Options:
  --context          Additional context for the question
```

**Examples:**
```bash
# Simple question
python main.py ask "video.mp4" "What products are mentioned?"

# Question with context
python main.py ask "video.mp4" "How many people appear?" --context "This is a marketing video"
```

#### 4. `batch-instagram` - Process Multiple Instagram Videos
```bash
python main.py batch-instagram <URL1> <URL2> ... [OPTIONS]

Options:
  --output-dir, -d    Output directory (default: AI-Transcrips)
  --type, -t          Analysis type
```

**Example:**
```bash
python main.py batch-instagram \
  "https://www.instagram.com/reel/DNI-L5Eicg2/" \
  "https://www.instagram.com/reel/DNGZeTnChuH/" \
  --output-dir "My-Transcripts" \
  --type comprehensive
```

#### 5. `start-mcp` - Start MCP Server
```bash
python main.py start-mcp
```

#### 6. `info` - System Information
```bash
python main.py info
```

---

## 🔌 MCP Server

### Starting the Server
```bash
python main.py start-mcp
```

### Available MCP Tools

1. **analyze_video_from_url** - Download and analyze video from URL
2. **analyze_video_file** - Analyze local video file
3. **transcribe_video** - Get transcription with timestamps
4. **ask_video_question** - Ask specific questions about video
5. **summarize_video** - Generate video summary
6. **extract_scenes** - Extract specific scenes/moments
7. **batch_analyze** - Process multiple videos
8. **get_video_info** - Get basic video metadata
9. **list_supported_formats** - Show capabilities
10. **get_system_status** - System information

### MCP Tool Examples

```json
{
  "tool": "analyze_video_from_url",
  "arguments": {
    "url": "https://www.instagram.com/reel/DNI-L5Eicg2/",
    "analysis_type": "comprehensive",
    "sampling_rate": 1
  }
}
```

```json
{
  "tool": "transcribe_video",
  "arguments": {
    "video_path": "https://youtube.com/watch?v=abc123",
    "include_timestamps": true,
    "language": "en"
  }
}
```

---

## 🐍 Python API

### Basic Usage
```python
import asyncio
from src.video_analyzer import VideoAnalyzer
from src.file_manager import FileManager

async def main():
    analyzer = VideoAnalyzer()
    file_manager = FileManager()
    
    # Analyze video
    result = await analyzer.analyze_video_url(
        url="https://www.instagram.com/reel/DNI-L5Eicg2/",
        analysis_type="comprehensive"
    )
    
    # Save results
    await file_manager.save_analysis_result(result.__dict__)
    
    print(f"Analysis completed in {result.processing_time:.2f} seconds")

asyncio.run(main())
```

### Advanced Usage
```python
import asyncio
from src.video_analyzer import VideoAnalyzer

async def advanced_analysis():
    analyzer = VideoAnalyzer()
    
    # Transcribe with timestamps
    transcription = await analyzer.transcribe_video(
        video_path="video.mp4",
        include_timestamps=True,
        language="en"
    )
    
    # Ask questions
    answer = await analyzer.ask_video_question(
        video_path="video.mp4",
        question="What is the main topic?",
        context="Educational content"
    )
    
    # Analyze specific segment
    result = await analyzer.analyze_video_file(
        video_path="video.mp4",
        analysis_type="visual_description",
        sampling_rate=2,
        start_offset=30,
        end_offset=120
    )
    
    return transcription, answer, result

asyncio.run(advanced_analysis())
```

---

## 📱 Instagram Video Processing

### Your Specific Use Case

To process your Instagram videos exactly as requested:

```bash
python main.py batch-instagram \
  "https://www.instagram.com/reel/DNI-L5Eicg2/" \
  "https://www.instagram.com/reel/DNGZeTnChuH/" \
  "https://www.instagram.com/reel/DM25RH8iL3B/" \
  "https://www.instagram.com/reel/DMDoy3ZCXIf/" \
  "https://www.instagram.com/reel/DLaW8G0iGa8/" \
  "https://www.instagram.com/reel/DM5dVMzsdJk/" \
  "https://www.instagram.com/reel/DMVweC6pIcX/" \
  "https://www.instagram.com/reel/DNcbYyzO1H5/" \
  "https://www.instagram.com/reel/DNQwBzGIARV/" \
  --output-dir "AI-Transcrips" \
  --type comprehensive
```

### Output Format
Each video will generate a markdown file like:
```
AI-Transcrips/
├── nathanhodgson.ai_DNI-L5Eicg2.md
├── nathanhodgson.ai_DNGZeTnChuH.md
├── nathanhodgson.ai_DM25RH8iL3B.md
└── ...
```

### Markdown File Structure
```markdown
# Video Analysis - nathanhodgson.ai_DNI-L5Eicg2

## Video Information
- **Profile**: nathanhodgson.ai
- **Video Code**: DNI-L5Eicg2
- **URL**: https://www.instagram.com/reel/DNI-L5Eicg2/
- **Duration**: 00:30
- **Views**: 1,843
- **Likes**: 1,843

## Description
Comment 'RIONA' to get this free AI social media agent...

## Transcription with Timestamps
**[00:05]** Meet Riona, an open-source AI that can handle...
**[00:15]** Setup is simple: Just connect your accounts...
**[00:25]** This isn't just another bot—it's an AI that...

## Analysis Metadata
- **Analysis Date**: 2024-08-18 16:30:00
- **Processing Time**: 45.2 seconds
- **Analysis Type**: comprehensive
```

---

## 🔧 Advanced Features

### Custom Prompts
```python
custom_prompt = """
Analyze this video and provide:
1. Detailed transcription with timestamps
2. Key topics discussed
3. Any products or services mentioned
4. Target audience analysis
5. Engagement strategies used
"""

result = await analyzer.analyze_video_url(
    url="https://instagram.com/reel/abc123",
    custom_prompt=custom_prompt
)
```

### Batch Processing
```python
urls = [
    "https://instagram.com/reel/1",
    "https://instagram.com/reel/2",
    "https://instagram.com/reel/3"
]

results = []
for url in urls:
    result = await analyzer.analyze_video_url(url)
    results.append(result)
```

### Video Trimming
```python
# Analyze only first 60 seconds
result = await analyzer.analyze_video_file(
    video_path="long_video.mp4",
    start_offset=0,
    end_offset=60
)
```

### High-Quality Sampling
```python
# Analyze at 2 FPS for detailed visual analysis
result = await analyzer.analyze_video_file(
    video_path="video.mp4",
    analysis_type="visual_description",
    sampling_rate=2
)
```

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. "Module not found" errors
```bash
# Ensure you're in the correct directory
cd Video-Understander

# Install dependencies
pip install -r requirements.txt
```

#### 2. FFmpeg not found
```bash
# Windows (using chocolatey)
choco install ffmpeg

# Or download from https://ffmpeg.org/
```

#### 3. Instagram download fails
```bash
# Try with yt-dlp directly
yt-dlp "https://www.instagram.com/reel/DNI-L5Eicg2/"
```

#### 4. Gemini API errors
- Check your API key in `config/.env`
- Verify API quota and billing
- Check network connectivity

#### 5. Large video files
```python
# For videos > 2GB, use video trimming
result = await analyzer.analyze_video_file(
    video_path="large_video.mp4",
    end_offset=1800  # First 30 minutes
)
```

### Performance Tips

1. **Use appropriate sampling rates**
   - 1 FPS for transcription
   - 2-5 FPS for detailed visual analysis

2. **Trim long videos**
   - Focus on key segments
   - Use start/end offsets

3. **Batch processing**
   - Process multiple videos efficiently
   - Use async operations

### Getting Help

1. Check logs in `logs/video_understander.log`
2. Use verbose mode: `python main.py --verbose`
3. Test with simple videos first
4. Verify all dependencies are installed

---

## 🎯 Summary

You now have a complete video analysis system with:

✅ **Full Gemini Video Understanding Integration**
✅ **Instagram/YouTube/TikTok Support**
✅ **Transcription with Timestamps**
✅ **MCP Server with 10 Tools**
✅ **CLI Interface**
✅ **Python API**
✅ **Batch Processing**
✅ **Markdown Output**

**Ready to process your Instagram videos!** 🚀
