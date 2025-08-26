#!/usr/bin/env python3
"""
Simple video transcriber using Gemini API directly.
"""

import os
import sys
import time
import json
import asyncio
from pathlib import Path
from datetime import datetime

# Try to import required modules
try:
    import requests
    print("✅ requests module available")
except ImportError:
    print("❌ requests module not found. Installing...")
    os.system("pip install requests")
    import requests

# API Configuration
GEMINI_API_KEY = "AIzaSyDtBbilIcTPVv466TjIjB0JPuIz8rPnDl0"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"

def find_mp4_files():
    """Find all MP4 files in AI-Videos folder."""
    videos_folder = Path("AI-Videos")
    if not videos_folder.exists():
        print(f"❌ Folder not found: {videos_folder}")
        return []
    
    mp4_files = list(videos_folder.glob("*.mp4"))
    print(f"Found {len(mp4_files)} MP4 files:")
    for file in mp4_files:
        size_mb = file.stat().st_size / (1024 * 1024)
        print(f"  - {file.name} ({size_mb:.2f} MB)")
    
    return mp4_files

def upload_file_to_gemini(file_path):
    """Upload file to Gemini Files API."""
    print(f"📤 Uploading {file_path.name}...")
    
    # Upload endpoint
    upload_url = f"https://generativelanguage.googleapis.com/upload/v1beta/files?key={GEMINI_API_KEY}"
    
    # Prepare file data
    with open(file_path, 'rb') as f:
        files = {
            'file': (file_path.name, f, 'video/mp4')
        }
        
        metadata = {
            'file': {
                'display_name': file_path.name
            }
        }
        
        data = {
            'metadata': json.dumps(metadata)
        }
        
        try:
            response = requests.post(upload_url, files=files, data=data)
            response.raise_for_status()
            
            file_info = response.json()
            file_uri = file_info.get('file', {}).get('uri')
            
            if file_uri:
                print(f"✅ Upload successful: {file_path.name}")
                return file_uri
            else:
                print(f"❌ Upload failed: {file_path.name}")
                return None
                
        except Exception as e:
            print(f"❌ Upload error for {file_path.name}: {e}")
            return None

def transcribe_with_gemini(file_uri, video_name):
    """Transcribe video using Gemini API."""
    print(f"🎤 Transcribing {video_name}...")
    
    headers = {
        'Content-Type': 'application/json',
    }
    
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
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "file_data": {
                            "mime_type": "video/mp4",
                            "file_uri": file_uri
                        }
                    }
                ]
            }
        ]
    }
    
    try:
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        if 'candidates' in result and len(result['candidates']) > 0:
            transcription = result['candidates'][0]['content']['parts'][0]['text']
            print(f"✅ Transcription complete: {video_name}")
            return {
                'success': True,
                'transcription': transcription,
                'video_name': video_name
            }
        else:
            print(f"❌ No transcription returned for {video_name}")
            return {
                'success': False,
                'error': 'No transcription returned',
                'video_name': video_name
            }
            
    except Exception as e:
        print(f"❌ Transcription error for {video_name}: {e}")
        return {
            'success': False,
            'error': str(e),
            'video_name': video_name
        }

def create_markdown_file(transcription_data, video_path):
    """Create markdown file with transcription."""
    video_stem = video_path.stem
    output_filename = f"{video_stem}_transcription.md"
    output_path = video_path.parent / output_filename
    
    if not transcription_data['success']:
        content = f"""# Transcription Error - {video_stem}

## Video Information
- **File**: {video_path.name}
- **Size**: {video_path.stat().st_size / (1024*1024):.2f} MB
- **Processing Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Error
{transcription_data['error']}
"""
    else:
        content = f"""# Video Transcription - {video_stem}

## Video Information
- **File**: {video_path.name}
- **Size**: {video_path.stat().st_size / (1024*1024):.2f} MB
- **Processing Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Transcription with Timestamps

{transcription_data['transcription']}

---

*Generated using Gemini Video Understanding API*
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"💾 Saved: {output_filename}")
    return str(output_path)

def process_video(video_path):
    """Process a single video."""
    print(f"\n📹 Processing: {video_path.name}")
    start_time = time.time()
    
    try:
        # Upload video
        file_uri = upload_file_to_gemini(video_path)
        if not file_uri:
            return {
                'success': False,
                'error': 'Upload failed',
                'video_path': str(video_path),
                'processing_time': time.time() - start_time
            }
        
        # Wait a moment for processing
        time.sleep(2)
        
        # Transcribe
        transcription_data = transcribe_with_gemini(file_uri, video_path.name)
        
        # Create markdown file
        output_path = create_markdown_file(transcription_data, video_path)
        
        processing_time = time.time() - start_time
        
        return {
            'success': transcription_data['success'],
            'video_path': str(video_path),
            'output_path': output_path if transcription_data['success'] else None,
            'processing_time': processing_time,
            'error': transcription_data.get('error')
        }
        
    except Exception as e:
        processing_time = time.time() - start_time
        print(f"❌ Failed to process {video_path.name}: {e}")
        
        return {
            'success': False,
            'video_path': str(video_path),
            'output_path': None,
            'processing_time': processing_time,
            'error': str(e)
        }

def main():
    """Main function."""
    print("🎥 Video Transcription with Gemini Video Understanding")
    print("=" * 60)
    
    # Check API key
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_api_key_here":
        print("❌ Please configure your Gemini API key")
        return
    
    # Find MP4 files
    mp4_files = find_mp4_files()
    if not mp4_files:
        print("❌ No MP4 files found!")
        return
    
    print(f"\n🎬 Starting transcription of {len(mp4_files)} videos...")
    print("=" * 60)
    
    results = []
    successful = 0
    
    for i, video_path in enumerate(mp4_files, 1):
        print(f"\n[{i}/{len(mp4_files)}] Processing {video_path.name}")
        
        result = process_video(video_path)
        results.append(result)
        
        if result['success']:
            successful += 1
            print(f"✅ Success! ({successful}/{len(mp4_files)} completed)")
        else:
            print(f"❌ Failed! Error: {result['error']}")
        
        print(f"⏱️  Processing time: {result['processing_time']:.2f} seconds")
        
        # Wait between videos to avoid rate limits
        if i < len(mp4_files):
            print("⏳ Waiting 5 seconds before next video...")
            time.sleep(5)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TRANSCRIPTION SUMMARY")
    print("=" * 60)
    print(f"✅ Successful: {successful}/{len(results)}")
    print(f"❌ Failed: {len(results) - successful}/{len(results)}")
    
    if successful > 0:
        successful_results = [r for r in results if r['success']]
        total_time = sum(r['processing_time'] for r in successful_results)
        avg_time = total_time / len(successful_results)
        print(f"⏱️  Average processing time: {avg_time:.2f} seconds")
        print(f"⏱️  Total processing time: {total_time:.2f} seconds")
        
        print(f"\n📁 Generated transcription files:")
        for result in successful_results:
            video_name = Path(result['video_path']).name
            output_name = Path(result['output_path']).name
            print(f"   {video_name} → {output_name}")
    
    failed_results = [r for r in results if not r['success']]
    if failed_results:
        print(f"\n❌ Failed videos:")
        for result in failed_results:
            video_name = Path(result['video_path']).name
            print(f"   {video_name}: {result['error']}")
    
    print(f"\n🎉 Transcription complete! Check the AI-Videos folder for *_transcription.md files.")

if __name__ == "__main__":
    main()
