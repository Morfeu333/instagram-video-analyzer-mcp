#!/usr/bin/env python3
"""
Transcribe all MP4 videos in AI-Videos folder using Gemini Video Understanding.
Generates markdown files with transcriptions and timestamps.
"""

import asyncio
import os
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config/.env')

# Configure Gemini
GEMINI_API_KEY = "AIzaSyDtBbilIcTPVv466TjIjB0JPuIz8rPnDl0"
genai.configure(api_key=GEMINI_API_KEY)

class VideoTranscriber:
    """Transcribe videos using Gemini Video Understanding."""
    
    def __init__(self):
        """Initialize the transcriber."""
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.videos_folder = Path("AI-Videos")
        self.processed_count = 0
        self.total_videos = 0
        
    def find_mp4_files(self) -> List[Path]:
        """Find all MP4 files in the AI-Videos folder."""
        mp4_files = list(self.videos_folder.glob("*.mp4"))
        print(f"Found {len(mp4_files)} MP4 files:")
        for file in mp4_files:
            print(f"  - {file.name}")
        return mp4_files
    
    async def upload_video_file(self, video_path: Path) -> Any:
        """Upload video file to Gemini."""
        print(f"📤 Uploading {video_path.name}...")
        
        try:
            # Upload file
            video_file = genai.upload_file(
                path=str(video_path),
                display_name=video_path.name
            )
            
            # Wait for processing
            while video_file.state.name == "PROCESSING":
                print(f"   Processing {video_path.name}...")
                await asyncio.sleep(2)
                video_file = genai.get_file(video_file.name)
            
            if video_file.state.name == "FAILED":
                raise Exception(f"Video processing failed: {video_file.state}")
            
            print(f"✅ Upload complete: {video_path.name}")
            return video_file
            
        except Exception as e:
            print(f"❌ Upload error for {video_path.name}: {e}")
            raise
    
    async def transcribe_video(self, video_file: Any, video_name: str) -> Dict[str, Any]:
        """Transcribe video using Gemini."""
        print(f"🎤 Transcribing {video_name}...")
        
        prompt = """
        Please provide a detailed transcription of this video with precise timestamps.
        
        Format the output as follows:
        1. Include timestamps in MM:SS format for each segment
        2. Transcribe all spoken content accurately
        3. Note any important visual elements or text shown
        4. Include any background music or sound effects mentioned
        5. Format each line as: [MM:SS] Transcribed text
        
        Be very precise with the timestamps and capture all spoken content.
        """
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                [prompt, video_file],
                stream=False
            )
            
            print(f"✅ Transcription complete: {video_name}")
            return {
                'transcription': response.text,
                'video_name': video_name,
                'timestamp': datetime.now().isoformat(),
                'success': True
            }
            
        except Exception as e:
            print(f"❌ Transcription error for {video_name}: {e}")
            return {
                'error': str(e),
                'video_name': video_name,
                'timestamp': datetime.now().isoformat(),
                'success': False
            }
    
    def create_markdown_file(self, transcription_data: Dict[str, Any], video_path: Path) -> str:
        """Create markdown file with transcription."""
        # Generate output filename
        video_stem = video_path.stem  # filename without extension
        output_filename = f"{video_stem}_transcription.md"
        output_path = self.videos_folder / output_filename
        
        if not transcription_data['success']:
            # Create error file
            content = f"""# Transcription Error - {video_stem}

## Video Information
- **File**: {video_path.name}
- **Size**: {video_path.stat().st_size / (1024*1024):.2f} MB
- **Processing Date**: {transcription_data['timestamp']}

## Error
{transcription_data['error']}
"""
        else:
            # Create successful transcription file
            content = f"""# Video Transcription - {video_stem}

## Video Information
- **File**: {video_path.name}
- **Size**: {video_path.stat().st_size / (1024*1024):.2f} MB
- **Processing Date**: {transcription_data['timestamp']}

## Transcription with Timestamps

{transcription_data['transcription']}

---

*Generated using Gemini Video Understanding API*
"""
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"💾 Saved: {output_filename}")
        return str(output_path)
    
    async def process_single_video(self, video_path: Path) -> Dict[str, Any]:
        """Process a single video file."""
        start_time = time.time()
        
        try:
            # Upload video
            video_file = await self.upload_video_file(video_path)
            
            # Transcribe
            transcription_data = await self.transcribe_video(video_file, video_path.name)
            
            # Create markdown file
            output_path = self.create_markdown_file(transcription_data, video_path)
            
            # Clean up uploaded file
            try:
                genai.delete_file(video_file.name)
                print(f"🗑️  Cleaned up uploaded file for {video_path.name}")
            except:
                pass  # Ignore cleanup errors
            
            processing_time = time.time() - start_time
            
            return {
                'video_path': str(video_path),
                'output_path': output_path,
                'success': transcription_data['success'],
                'processing_time': processing_time,
                'error': transcription_data.get('error')
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"❌ Failed to process {video_path.name}: {e}")
            
            return {
                'video_path': str(video_path),
                'output_path': None,
                'success': False,
                'processing_time': processing_time,
                'error': str(e)
            }
    
    async def process_all_videos(self) -> List[Dict[str, Any]]:
        """Process all MP4 videos in the folder."""
        mp4_files = self.find_mp4_files()
        
        if not mp4_files:
            print("❌ No MP4 files found in AI-Videos folder!")
            return []
        
        self.total_videos = len(mp4_files)
        results = []
        
        print(f"\n🎬 Starting transcription of {self.total_videos} videos...")
        print("=" * 60)
        
        for i, video_path in enumerate(mp4_files, 1):
            print(f"\n📹 Processing video {i}/{self.total_videos}: {video_path.name}")
            
            result = await self.process_single_video(video_path)
            results.append(result)
            
            if result['success']:
                self.processed_count += 1
                print(f"✅ Success! ({self.processed_count}/{self.total_videos} completed)")
            else:
                print(f"❌ Failed! Error: {result['error']}")
            
            print(f"⏱️  Processing time: {result['processing_time']:.2f} seconds")
            
            # Small delay between videos to avoid rate limits
            if i < len(mp4_files):
                print("⏳ Waiting 3 seconds before next video...")
                await asyncio.sleep(3)
        
        return results
    
    def print_summary(self, results: List[Dict[str, Any]]):
        """Print processing summary."""
        print("\n" + "=" * 60)
        print("📊 TRANSCRIPTION SUMMARY")
        print("=" * 60)
        
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        print(f"✅ Successful: {len(successful)}/{len(results)}")
        print(f"❌ Failed: {len(failed)}/{len(results)}")
        
        if successful:
            total_time = sum(r['processing_time'] for r in successful)
            avg_time = total_time / len(successful)
            print(f"⏱️  Average processing time: {avg_time:.2f} seconds")
            print(f"⏱️  Total processing time: {total_time:.2f} seconds")
            
            print(f"\n📁 Generated transcription files:")
            for result in successful:
                video_name = Path(result['video_path']).name
                output_name = Path(result['output_path']).name
                print(f"   {video_name} → {output_name}")
        
        if failed:
            print(f"\n❌ Failed videos:")
            for result in failed:
                video_name = Path(result['video_path']).name
                print(f"   {video_name}: {result['error']}")
        
        print(f"\n🎉 Transcription complete! Check the AI-Videos folder for *_transcription.md files.")


async def main():
    """Main function."""
    print("🎥 Video Transcription with Gemini Video Understanding")
    print("=" * 60)
    
    transcriber = VideoTranscriber()
    
    # Check if API key is configured
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_api_key_here":
        print("❌ Please configure your Gemini API key in config/.env")
        return
    
    # Check if videos folder exists
    if not transcriber.videos_folder.exists():
        print(f"❌ AI-Videos folder not found: {transcriber.videos_folder}")
        return
    
    try:
        # Process all videos
        results = await transcriber.process_all_videos()
        
        # Print summary
        transcriber.print_summary(results)
        
    except KeyboardInterrupt:
        print("\n⚠️  Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
