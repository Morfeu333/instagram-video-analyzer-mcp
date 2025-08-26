#!/usr/bin/env python3
"""
Retry failed video transcriptions with better error handling.
"""

import os
import time
import json
import requests
from pathlib import Path
from datetime import datetime

# API Configuration
GEMINI_API_KEY = "AIzaSyDtBbilIcTPVv466TjIjB0JPuIz8rPnDl0"

# Failed videos from previous run
FAILED_VIDEOS = [
    "brodyautomates_DNcbYyzO1H5.mp4",
    "nathanhodgson.ai_DLaW8G0iGa8.mp4", 
    "nathanhodgson.ai_DM25RH8iL3B.mp4",
    "pbiloai_DMVweC6pIcX.mp4"
]

def upload_file_to_gemini(file_path):
    """Upload file to Gemini Files API with retry logic."""
    print(f"📤 Uploading {file_path.name}...")
    
    upload_url = f"https://generativelanguage.googleapis.com/upload/v1beta/files?key={GEMINI_API_KEY}"
    
    for attempt in range(3):  # 3 attempts
        try:
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
                
                response = requests.post(upload_url, files=files, data=data, timeout=60)
                response.raise_for_status()
                
                file_info = response.json()
                file_uri = file_info.get('file', {}).get('uri')
                
                if file_uri:
                    print(f"✅ Upload successful: {file_path.name}")
                    return file_uri
                    
        except Exception as e:
            print(f"❌ Upload attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                print(f"⏳ Waiting 10 seconds before retry...")
                time.sleep(10)
    
    return None

def transcribe_with_gemini_stable(file_uri, video_name):
    """Transcribe using stable Gemini model."""
    print(f"🎤 Transcribing {video_name} with stable model...")
    
    # Use the stable model instead of experimental
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    prompt = """
    Please provide a detailed transcription of this video with precise timestamps.
    
    Format the output as follows:
    1. Include timestamps in MM:SS format for each segment
    2. Transcribe all spoken content accurately
    3. Note any important visual elements or text shown
    4. Format each line as: [MM:SS] Transcribed text
    
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
    
    for attempt in range(3):  # 3 attempts
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=120)
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
                
        except Exception as e:
            print(f"❌ Transcription attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                print(f"⏳ Waiting 15 seconds before retry...")
                time.sleep(15)
    
    return {
        'success': False,
        'error': 'All transcription attempts failed',
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

*Generated using Gemini Video Understanding API (Stable Model)*
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"💾 Saved: {output_filename}")
    return str(output_path)

def process_video(video_path):
    """Process a single video with retry logic."""
    print(f"\n📹 Retrying: {video_path.name}")
    start_time = time.time()
    
    try:
        # Upload video with retry
        file_uri = upload_file_to_gemini(video_path)
        if not file_uri:
            return {
                'success': False,
                'error': 'Upload failed after retries',
                'video_path': str(video_path),
                'processing_time': time.time() - start_time
            }
        
        # Wait for processing
        print("⏳ Waiting for file processing...")
        time.sleep(5)
        
        # Transcribe with stable model
        transcription_data = transcribe_with_gemini_stable(file_uri, video_path.name)
        
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
    """Main function to retry failed videos."""
    print("🔄 Retrying Failed Video Transcriptions")
    print("=" * 50)
    
    videos_folder = Path("AI-Videos")
    
    if not videos_folder.exists():
        print(f"❌ AI-Videos folder not found!")
        return
    
    # Find failed video files
    failed_paths = []
    for video_name in FAILED_VIDEOS:
        video_path = videos_folder / video_name
        if video_path.exists():
            failed_paths.append(video_path)
            print(f"Found: {video_name}")
        else:
            print(f"Not found: {video_name}")
    
    if not failed_paths:
        print("❌ No failed videos found to retry!")
        return
    
    print(f"\n🔄 Retrying {len(failed_paths)} failed videos with stable model...")
    print("=" * 50)
    
    results = []
    successful = 0
    
    for i, video_path in enumerate(failed_paths, 1):
        print(f"\n[{i}/{len(failed_paths)}] Retrying {video_path.name}")
        
        result = process_video(video_path)
        results.append(result)
        
        if result['success']:
            successful += 1
            print(f"✅ Success! ({successful}/{len(failed_paths)} completed)")
        else:
            print(f"❌ Still failed! Error: {result['error']}")
        
        print(f"⏱️  Processing time: {result['processing_time']:.2f} seconds")
        
        # Wait between videos
        if i < len(failed_paths):
            print("⏳ Waiting 10 seconds before next video...")
            time.sleep(10)
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 RETRY SUMMARY")
    print("=" * 50)
    print(f"✅ Now successful: {successful}/{len(results)}")
    print(f"❌ Still failed: {len(results) - successful}/{len(results)}")
    
    if successful > 0:
        successful_results = [r for r in results if r['success']]
        print(f"\n📁 Newly generated transcription files:")
        for result in successful_results:
            video_name = Path(result['video_path']).name
            output_name = Path(result['output_path']).name
            print(f"   {video_name} → {output_name}")
    
    still_failed = [r for r in results if not r['success']]
    if still_failed:
        print(f"\n❌ Still failed videos:")
        for result in still_failed:
            video_name = Path(result['video_path']).name
            print(f"   {video_name}: {result['error']}")
    
    print(f"\n🎉 Retry complete!")

if __name__ == "__main__":
    main()
