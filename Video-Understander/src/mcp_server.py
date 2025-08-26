"""
MCP (Model Context Protocol) server for Video-Understander.
Provides external access to video analysis capabilities.
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent
)

from config.settings import settings
from .video_analyzer import VideoAnalyzer
from .video_downloader import VideoDownloader
from .file_manager import FileManager


class VideoUnderstanderMCPServer:
    """MCP Server for Video-Understander capabilities."""
    
    def __init__(self):
        """Initialize the MCP server."""
        self.logger = logging.getLogger(__name__)
        self.video_analyzer = VideoAnalyzer()
        self.video_downloader = VideoDownloader()
        self.file_manager = FileManager()
        
        # Initialize MCP server
        self.server = Server("video-understander")
        self._register_tools()
        
        self.logger.info("VideoUnderstanderMCPServer initialized")
    
    def _register_tools(self):
        """Register all available MCP tools."""
        
        @self.server.list_tools()
        async def list_tools() -> ListToolsResult:
            """List all available tools."""
            return ListToolsResult(
                tools=[
                    Tool(
                        name="analyze_video_from_url",
                        description="Download and analyze video from URL (YouTube, Instagram, TikTok, etc.)",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "url": {
                                    "type": "string",
                                    "description": "Video URL to analyze"
                                },
                                "analysis_type": {
                                    "type": "string",
                                    "enum": ["comprehensive", "transcription", "summary", "visual_description", "question_answering"],
                                    "default": "comprehensive",
                                    "description": "Type of analysis to perform"
                                },
                                "custom_prompt": {
                                    "type": "string",
                                    "description": "Custom analysis prompt (optional)"
                                },
                                "sampling_rate": {
                                    "type": "integer",
                                    "description": "Frame sampling rate in FPS (optional)"
                                },
                                "start_offset": {
                                    "type": "integer",
                                    "description": "Start time in seconds (optional)"
                                },
                                "end_offset": {
                                    "type": "integer",
                                    "description": "End time in seconds (optional)"
                                }
                            },
                            "required": ["url"]
                        }
                    ),
                    Tool(
                        name="analyze_video_file",
                        description="Analyze local video file",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "video_path": {
                                    "type": "string",
                                    "description": "Path to local video file"
                                },
                                "analysis_type": {
                                    "type": "string",
                                    "enum": ["comprehensive", "transcription", "summary", "visual_description", "question_answering"],
                                    "default": "comprehensive",
                                    "description": "Type of analysis to perform"
                                },
                                "custom_prompt": {
                                    "type": "string",
                                    "description": "Custom analysis prompt (optional)"
                                },
                                "sampling_rate": {
                                    "type": "integer",
                                    "description": "Frame sampling rate in FPS (optional)"
                                },
                                "start_offset": {
                                    "type": "integer",
                                    "description": "Start time in seconds (optional)"
                                },
                                "end_offset": {
                                    "type": "integer",
                                    "description": "End time in seconds (optional)"
                                }
                            },
                            "required": ["video_path"]
                        }
                    ),
                    Tool(
                        name="transcribe_video",
                        description="Get video transcription with timestamps",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "video_path": {
                                    "type": "string",
                                    "description": "Path to video file or URL"
                                },
                                "include_timestamps": {
                                    "type": "boolean",
                                    "default": True,
                                    "description": "Include timestamp information"
                                },
                                "language": {
                                    "type": "string",
                                    "description": "Target language for transcription (optional)"
                                }
                            },
                            "required": ["video_path"]
                        }
                    ),
                    Tool(
                        name="ask_video_question",
                        description="Ask specific question about video content",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "video_path": {
                                    "type": "string",
                                    "description": "Path to video file or URL"
                                },
                                "question": {
                                    "type": "string",
                                    "description": "Question to ask about the video"
                                },
                                "context": {
                                    "type": "string",
                                    "description": "Additional context for the question (optional)"
                                }
                            },
                            "required": ["video_path", "question"]
                        }
                    ),
                    Tool(
                        name="summarize_video",
                        description="Generate video summary",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "video_path": {
                                    "type": "string",
                                    "description": "Path to video file or URL"
                                },
                                "summary_type": {
                                    "type": "string",
                                    "enum": ["brief", "detailed", "bullet_points", "chapters"],
                                    "default": "detailed",
                                    "description": "Type of summary to generate"
                                },
                                "max_length": {
                                    "type": "integer",
                                    "description": "Maximum summary length in words (optional)"
                                }
                            },
                            "required": ["video_path"]
                        }
                    ),
                    Tool(
                        name="extract_scenes",
                        description="Extract specific scenes or moments from video",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "video_path": {
                                    "type": "string",
                                    "description": "Path to video file or URL"
                                },
                                "scene_criteria": {
                                    "type": "string",
                                    "description": "Criteria for scene extraction (e.g., 'action scenes', 'dialogue', 'specific objects')"
                                },
                                "max_scenes": {
                                    "type": "integer",
                                    "default": 10,
                                    "description": "Maximum number of scenes to extract"
                                }
                            },
                            "required": ["video_path", "scene_criteria"]
                        }
                    ),
                    Tool(
                        name="batch_analyze",
                        description="Analyze multiple videos in batch",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "video_inputs": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "List of video paths or URLs"
                                },
                                "analysis_type": {
                                    "type": "string",
                                    "enum": ["comprehensive", "transcription", "summary", "visual_description"],
                                    "default": "comprehensive",
                                    "description": "Type of analysis to perform on all videos"
                                },
                                "custom_prompts": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "Custom prompts for each video (optional)"
                                }
                            },
                            "required": ["video_inputs"]
                        }
                    ),
                    Tool(
                        name="get_video_info",
                        description="Get basic video metadata and information",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "video_path": {
                                    "type": "string",
                                    "description": "Path to video file or URL"
                                }
                            },
                            "required": ["video_path"]
                        }
                    ),
                    Tool(
                        name="list_supported_formats",
                        description="List supported video formats and capabilities",
                        inputSchema={
                            "type": "object",
                            "properties": {}
                        }
                    ),
                    Tool(
                        name="get_system_status",
                        description="Get system status and configuration",
                        inputSchema={
                            "type": "object",
                            "properties": {}
                        }
                    )
                ]
            )
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Handle tool calls."""
            try:
                self.logger.info(f"Calling tool: {name} with arguments: {arguments}")
                
                if name == "analyze_video_from_url":
                    result = await self._analyze_video_from_url(**arguments)
                elif name == "analyze_video_file":
                    result = await self._analyze_video_file(**arguments)
                elif name == "transcribe_video":
                    result = await self._transcribe_video(**arguments)
                elif name == "ask_video_question":
                    result = await self._ask_video_question(**arguments)
                elif name == "summarize_video":
                    result = await self._summarize_video(**arguments)
                elif name == "extract_scenes":
                    result = await self._extract_scenes(**arguments)
                elif name == "batch_analyze":
                    result = await self._batch_analyze(**arguments)
                elif name == "get_video_info":
                    result = await self._get_video_info(**arguments)
                elif name == "list_supported_formats":
                    result = await self._list_supported_formats()
                elif name == "get_system_status":
                    result = await self._get_system_status()
                else:
                    raise ValueError(f"Unknown tool: {name}")
                
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(result, indent=2))]
                )
                
            except Exception as e:
                self.logger.error(f"Error calling tool {name}: {str(e)}")
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))],
                    isError=True
                )
    
    async def _analyze_video_from_url(self, **kwargs) -> Dict[str, Any]:
        """Analyze video from URL."""
        result = await self.video_analyzer.analyze_video_url(**kwargs)
        return self._format_analysis_result(result)
    
    async def _analyze_video_file(self, **kwargs) -> Dict[str, Any]:
        """Analyze local video file."""
        result = await self.video_analyzer.analyze_video_file(**kwargs)
        return self._format_analysis_result(result)
    
    async def _transcribe_video(self, video_path: str, **kwargs) -> Dict[str, Any]:
        """Transcribe video."""
        if self._is_url(video_path):
            # Download first
            local_path = await self.video_downloader.download_video(video_path)
            result = await self.video_analyzer.transcribe_video(local_path, **kwargs)
        else:
            result = await self.video_analyzer.transcribe_video(video_path, **kwargs)
        
        return {"transcription_result": result}
    
    async def _ask_video_question(self, video_path: str, **kwargs) -> Dict[str, Any]:
        """Ask question about video."""
        if self._is_url(video_path):
            local_path = await self.video_downloader.download_video(video_path)
            result = await self.video_analyzer.ask_video_question(local_path, **kwargs)
        else:
            result = await self.video_analyzer.ask_video_question(video_path, **kwargs)
        
        return {"answer": result}
    
    def _format_analysis_result(self, result) -> Dict[str, Any]:
        """Format analysis result for MCP response."""
        return {
            "video_id": result.video_id,
            "video_path": result.video_path,
            "analysis_type": result.analysis_type,
            "result": result.result,
            "metadata": result.metadata,
            "timestamp": result.timestamp,
            "processing_time": result.processing_time,
            "error": result.error
        }
    
    def _is_url(self, path: str) -> bool:
        """Check if path is a URL."""
        return path.startswith(('http://', 'https://'))
    
    async def run(self):
        """Run the MCP server."""
        self.logger.info(f"Starting Video-Understander MCP server on {settings.mcp_host}:{settings.mcp_port}")
        
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="video-understander",
                    server_version="1.0.0",
                    capabilities={}
                )
            )


async def main():
    """Main entry point for MCP server."""
    logging.basicConfig(
        level=getattr(logging, settings.mcp_log_level),
        format=settings.log_format
    )
    
    server = VideoUnderstanderMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
