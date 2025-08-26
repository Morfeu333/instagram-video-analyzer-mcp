"""
Basic usage examples for Video-Understander.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from video_analyzer import VideoAnalyzer
from file_manager import FileManager


async def example_analyze_youtube_video():
    """Example: Analyze YouTube video."""
    print("=== Analyzing YouTube Video ===")
    
    analyzer = VideoAnalyzer()
    
    # Analyze a YouTube video
    result = await analyzer.analyze_video_url(
        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        analysis_type="comprehensive"
    )
    
    print(f"Video ID: {result.video_id}")
    print(f"Processing time: {result.processing_time:.2f} seconds")
    print(f"Analysis result: {result.result}")
    
    return result


async def example_transcribe_video():
    """Example: Transcribe video with timestamps."""
    print("\n=== Transcribing Video ===")
    
    analyzer = VideoAnalyzer()
    
    # Transcribe a video
    transcription = await analyzer.transcribe_video(
        video_path="path/to/your/video.mp4",  # Replace with actual path
        include_timestamps=True,
        language="en"
    )
    
    print("Transcription:")
    for item in transcription.get('transcription', []):
        print(f"[{item['timestamp']}] {item['text']}")
    
    return transcription


async def example_ask_video_question():
    """Example: Ask question about video."""
    print("\n=== Asking Video Question ===")
    
    analyzer = VideoAnalyzer()
    
    # Ask a question about the video
    answer = await analyzer.ask_video_question(
        video_path="path/to/your/video.mp4",  # Replace with actual path
        question="What is the main topic of this video?",
        context="This is an educational video"
    )
    
    print(f"Answer: {answer}")
    
    return answer


async def example_batch_analysis():
    """Example: Batch analyze multiple videos."""
    print("\n=== Batch Analysis ===")
    
    analyzer = VideoAnalyzer()
    
    # List of video URLs or paths
    video_urls = [
        "https://www.youtube.com/watch?v=example1",
        "https://www.youtube.com/watch?v=example2",
        # Add more URLs
    ]
    
    # Analyze all videos
    results = []
    for url in video_urls:
        try:
            result = await analyzer.analyze_video_url(
                url=url,
                analysis_type="summary"
            )
            results.append(result)
            print(f"Analyzed: {url}")
        except Exception as e:
            print(f"Error analyzing {url}: {str(e)}")
    
    print(f"Completed batch analysis of {len(results)} videos")
    return results


async def example_save_transcription_markdown():
    """Example: Save transcription as markdown."""
    print("\n=== Saving Transcription as Markdown ===")
    
    analyzer = VideoAnalyzer()
    file_manager = FileManager()
    
    # Analyze video
    result = await analyzer.analyze_video_url(
        url="https://www.instagram.com/reel/DNI-L5Eicg2/",
        analysis_type="comprehensive"
    )
    
    # Prepare video info
    video_info = {
        'profile': 'nathanhodgson.ai',
        'video_code': 'DNI-L5Eicg2',
        'url': 'https://www.instagram.com/reel/DNI-L5Eicg2/',
        'title': 'AI Social Media Agent',
        'description': result.result.get('content', ''),
        'duration': '00:30',
        'upload_date': '2024-08-09',
        'view_count': '1,843',
        'like_count': '1,843'
    }
    
    # Save as markdown
    markdown_path = await file_manager.save_transcription_markdown(
        transcription_data=result.result,
        video_info=video_info
    )
    
    print(f"Transcription saved to: {markdown_path}")
    return markdown_path


async def example_instagram_videos_batch():
    """Example: Process Instagram videos like the user requested."""
    print("\n=== Processing Instagram Videos ===")
    
    analyzer = VideoAnalyzer()
    file_manager = FileManager()
    
    # Instagram video URLs
    instagram_urls = [
        "https://www.instagram.com/reel/DNI-L5Eicg2/",
        "https://www.instagram.com/reel/DNGZeTnChuH/",
        "https://www.instagram.com/reel/DM25RH8iL3B/",
        "https://www.instagram.com/reel/DMDoy3ZCXIf/",
        "https://www.instagram.com/reel/DLaW8G0iGa8/",
        "https://www.instagram.com/reel/DM5dVMzsdJk/",
        "https://www.instagram.com/reel/DMVweC6pIcX/",
        "https://www.instagram.com/reel/DNcbYyzO1H5/",
        "https://www.instagram.com/reel/DNQwBzGIARV/"
    ]
    
    # Create AI-Transcrips directory
    output_dir = Path("AI-Transcrips")
    output_dir.mkdir(exist_ok=True)
    
    results = []
    
    for url in instagram_urls:
        try:
            print(f"Processing: {url}")
            
            # Extract video code from URL
            video_code = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
            
            # Analyze video
            result = await analyzer.analyze_video_url(
                url=url,
                analysis_type="comprehensive"
            )
            
            # Extract profile name (would need to be extracted from analysis)
            profile = "profile_name"  # This would come from the analysis
            
            # Prepare video info
            video_info = {
                'profile': profile,
                'video_code': video_code,
                'url': url,
                'title': f'Video {video_code}',
                'description': result.result.get('content', ''),
                'duration': 'Unknown',
                'upload_date': 'Unknown',
                'view_count': 'Unknown',
                'like_count': 'Unknown'
            }
            
            # Save transcription markdown
            output_path = output_dir / f"{profile}_{video_code}.md"
            markdown_path = await file_manager.save_transcription_markdown(
                transcription_data=result.result,
                video_info=video_info,
                output_path=output_path
            )
            
            results.append({
                'url': url,
                'result': result,
                'markdown_path': markdown_path
            })
            
            print(f"Saved: {markdown_path}")
            
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
    
    print(f"Completed processing {len(results)} Instagram videos")
    return results


async def main():
    """Run all examples."""
    print("Video-Understander Examples")
    print("=" * 50)
    
    try:
        # Run examples
        await example_analyze_youtube_video()
        await example_transcribe_video()
        await example_ask_video_question()
        await example_batch_analysis()
        await example_save_transcription_markdown()
        await example_instagram_videos_batch()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
