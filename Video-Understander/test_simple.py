#!/usr/bin/env python3
"""
Simple test script for Video-Understander core functionality.
"""

import asyncio
import sys
import json
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

try:
    from src.video_analyzer import VideoAnalyzer
    from src.file_manager import FileManager
    from config.settings import settings
    print("✅ All imports successful!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


async def test_gemini_connection():
    """Test Gemini API connection."""
    print("\n🔍 Testing Gemini API connection...")
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.gemini_api_key)
        
        # Test with a simple text prompt
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content("Say 'Hello from Gemini!'")
        
        print(f"✅ Gemini API working: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return False


async def test_video_info():
    """Test getting video info from URL."""
    print("\n📹 Testing video info extraction...")
    
    try:
        from src.video_downloader import VideoDownloader
        downloader = VideoDownloader()
        
        # Test with a simple YouTube video
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        info = await downloader.get_video_info(test_url)
        
        if 'error' not in info:
            print(f"✅ Video info extracted: {info.get('title', 'Unknown')}")
            return True
        else:
            print(f"❌ Video info error: {info['error']}")
            return False
    except Exception as e:
        print(f"❌ Video info error: {e}")
        return False


async def test_instagram_video():
    """Test Instagram video analysis."""
    print("\n📱 Testing Instagram video analysis...")
    
    try:
        analyzer = VideoAnalyzer()
        
        # Test with your Instagram video
        url = "https://www.instagram.com/reel/DNI-L5Eicg2/"
        
        print(f"Analyzing: {url}")
        result = await analyzer.analyze_video_url(
            url=url,
            analysis_type="comprehensive"
        )
        
        if result.error:
            print(f"❌ Analysis error: {result.error}")
            return False
        else:
            print(f"✅ Analysis successful!")
            print(f"   Processing time: {result.processing_time:.2f} seconds")
            print(f"   Result preview: {str(result.result)[:200]}...")
            
            # Save result
            file_manager = FileManager()
            output_path = await file_manager.save_analysis_result(
                result=result.__dict__,
                filename="instagram_test_result.json"
            )
            print(f"   Saved to: {output_path}")
            
            return True
            
    except Exception as e:
        print(f"❌ Instagram analysis error: {e}")
        return False


async def test_markdown_generation():
    """Test markdown file generation."""
    print("\n📝 Testing markdown generation...")
    
    try:
        file_manager = FileManager()
        
        # Sample data
        transcription_data = {
            "content": "This is a test transcription with timestamps.",
            "transcription": [
                {"timestamp": "00:05", "text": "Hello and welcome to this video"},
                {"timestamp": "00:15", "text": "Today we'll be discussing AI technology"},
                {"timestamp": "00:25", "text": "Thank you for watching"}
            ],
            "analysis_type": "comprehensive",
            "processing_time": 30.5
        }
        
        video_info = {
            "profile": "test_profile",
            "video_code": "TEST123",
            "url": "https://example.com/test",
            "title": "Test Video",
            "description": "This is a test video for markdown generation",
            "duration": "00:30",
            "upload_date": "2024-08-18",
            "view_count": "1,000",
            "like_count": "100"
        }
        
        markdown_path = await file_manager.save_transcription_markdown(
            transcription_data=transcription_data,
            video_info=video_info,
            output_path="test_output.md"
        )
        
        print(f"✅ Markdown generated: {markdown_path}")
        
        # Read and display first few lines
        with open(markdown_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:10]
            print("   Preview:")
            for line in lines:
                print(f"   {line.strip()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Markdown generation error: {e}")
        return False


async def main():
    """Run all tests."""
    print("🎥 Video-Understander Test Suite")
    print("=" * 50)
    
    tests = [
        ("Gemini API Connection", test_gemini_connection),
        ("Video Info Extraction", test_video_info),
        ("Instagram Video Analysis", test_instagram_video),
        ("Markdown Generation", test_markdown_generation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            success = await test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} - {test_name}")
        if success:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Video-Understander is ready to use!")
        print("\nTo process your Instagram videos, run:")
        print("python main.py batch-instagram \\")
        print('  "https://www.instagram.com/reel/DNI-L5Eicg2/" \\')
        print('  "https://www.instagram.com/reel/DNGZeTnChuH/" \\')
        print('  --output-dir "AI-Transcrips"')
    else:
        print(f"\n⚠️  {len(results) - passed} tests failed. Check the errors above.")


if __name__ == "__main__":
    asyncio.run(main())
