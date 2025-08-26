#!/usr/bin/env python3
"""
Batch process the remaining 4 videos using Gemini 2.0 in a single request.
"""

import os
import time
import json
import requests
from pathlib import Path
from datetime import datetime

# API Configuration
GEMINI_API_KEY = "AIzaSyDtBbilIcTPVv466TjIjB0JPuIz8rPnDl0"

# Remaining videos to process
REMAINING_VIDEOS = [
    "brodyautomates_DNcbYyzO1H5.mp4",
    "nathanhodgson.ai_DLaW8G0iGa8.mp4", 
    "nathanhodgson.ai_DM25RH8iL3B.mp4",
    "pbiloai_DMVweC6pIcX.mp4"
]

def upload_file_to_gemini(file_path):
    """Upload file to Gemini Files API."""
    print(f"📤 Uploading {file_path.name}...")
    
    upload_url = f"https://generativelanguage.googleapis.com/upload/v1beta/files?key={GEMINI_API_KEY}"
    
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
            
            response = requests.post(upload_url, files=files, data=data, timeout=120)
            response.raise_for_status()
            
            file_info = response.json()
            file_uri = file_info.get('file', {}).get('uri')
            
            if file_uri:
                print(f"✅ Upload successful: {file_path.name}")
                return {
                    'uri': file_uri,
                    'name': file_path.name,
                    'path': file_path
                }
            else:
                print(f"❌ Upload failed: {file_path.name}")
                return None
                
    except Exception as e:
        print(f"❌ Upload error for {file_path.name}: {e}")
        return None

def batch_transcribe_with_gemini2(uploaded_files):
    """Batch transcribe all videos using Gemini 2.0."""
    print(f"🎤 Batch transcribing {len(uploaded_files)} videos with Gemini 2.0...")
    
    # Use Gemini 2.0 Flash Experimental
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={GEMINI_API_KEY}"
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    # Create parts for all videos
    parts = []
    
    # Add instruction
    instruction = f"""
    I'm providing you with {len(uploaded_files)} video files. Please transcribe each video separately with precise timestamps.

    For each video, provide:
    1. Video filename as a header
    2. Detailed transcription with timestamps in MM:SS format
    3. Each line formatted as: [MM:SS] Transcribed text
    4. Capture all spoken content accurately
    5. Note any important visual elements or text shown

    Format your response like this:

    ## VIDEO 1: [filename]
    [00:00] Transcribed content...
    [00:05] More content...

    ## VIDEO 2: [filename]
    [00:00] Transcribed content...

    And so on for all videos.

    Here are the {len(uploaded_files)} videos to transcribe:
    """
    
    parts.append({"text": instruction})
    
    # Add each video file
    for i, file_info in enumerate(uploaded_files, 1):
        parts.append({
            "text": f"\nVIDEO {i}: {file_info['name']}"
        })
        parts.append({
            "file_data": {
                "mime_type": "video/mp4",
                "file_uri": file_info['uri']
            }
        })
    
    payload = {
        "contents": [
            {
                "parts": parts
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 8192
        }
    }
    
    try:
        print("🚀 Sending batch request to Gemini 2.0...")
        response = requests.post(url, headers=headers, json=payload, timeout=300)
        response.raise_for_status()
        
        result = response.json()
        
        if 'candidates' in result and len(result['candidates']) > 0:
            transcription = result['candidates'][0]['content']['parts'][0]['text']
            print(f"✅ Batch transcription complete!")
            return {
                'success': True,
                'transcription': transcription,
                'video_count': len(uploaded_files)
            }
        else:
            print(f"❌ No transcription returned")
            return {
                'success': False,
                'error': 'No transcription returned'
            }
            
    except Exception as e:
        print(f"❌ Batch transcription error: {e}")
        return {
            'success': False,
            'error': str(e)
        }

def parse_and_save_transcriptions(batch_result, uploaded_files):
    """Parse batch transcription and save individual markdown files."""
    if not batch_result['success']:
        print(f"❌ Cannot parse failed transcription: {batch_result['error']}")
        return []
    
    transcription_text = batch_result['transcription']
    print(f"📝 Parsing batch transcription...")
    
    # Split by video headers
    video_sections = []
    lines = transcription_text.split('\n')
    current_video = None
    current_content = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('## VIDEO') and ':' in line:
            # Save previous video if exists
            if current_video and current_content:
                video_sections.append({
                    'header': current_video,
                    'content': '\n'.join(current_content)
                })
            
            # Start new video
            current_video = line
            current_content = []
        elif current_video and line:
            current_content.append(line)
    
    # Save last video
    if current_video and current_content:
        video_sections.append({
            'header': current_video,
            'content': '\n'.join(current_content)
        })
    
    print(f"📊 Found {len(video_sections)} video transcriptions")
    
    # Save individual files
    saved_files = []
    
    for section in video_sections:
        # Extract filename from header
        header = section['header']
        filename = None
        
        # Try to match with uploaded files
        for file_info in uploaded_files:
            if file_info['name'] in header:
                filename = file_info['name']
                video_path = file_info['path']
                break
        
        if not filename:
            print(f"⚠️  Could not match section to file: {header}")
            continue
        
        # Create markdown file
        video_stem = video_path.stem
        output_filename = f"{video_stem}_transcription.md"
        output_path = video_path.parent / output_filename
        
        content = f"""# Video Transcription - {video_stem}

## Video Information
- **File**: {video_path.name}
- **Size**: {video_path.stat().st_size / (1024*1024):.2f} MB
- **Processing Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Transcription with Timestamps

{section['content']}

---

*Generated using Gemini 2.0 Flash Experimental (Batch Processing)*
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"💾 Saved: {output_filename}")
        saved_files.append(str(output_path))
    
    return saved_files

def main():
    """Main function to batch process remaining videos."""
    print("🎬 Batch Processing Remaining Videos with Gemini 2.0")
    print("=" * 60)
    
    videos_folder = Path("AI-Videos")
    
    if not videos_folder.exists():
        print(f"❌ AI-Videos folder not found!")
        return
    
    # Find remaining video files
    remaining_paths = []
    for video_name in REMAINING_VIDEOS:
        video_path = videos_folder / video_name
        if video_path.exists():
            remaining_paths.append(video_path)
            size_mb = video_path.stat().st_size / (1024 * 1024)
            print(f"Found: {video_name} ({size_mb:.2f} MB)")
        else:
            print(f"Not found: {video_name}")
    
    if not remaining_paths:
        print("❌ No remaining videos found!")
        return
    
    print(f"\n📤 Uploading {len(remaining_paths)} videos...")
    print("=" * 60)
    
    # Upload all videos
    uploaded_files = []
    total_size = 0
    
    for video_path in remaining_paths:
        file_info = upload_file_to_gemini(video_path)
        if file_info:
            uploaded_files.append(file_info)
            total_size += video_path.stat().st_size / (1024 * 1024)
        else:
            print(f"❌ Failed to upload {video_path.name}")
    
    if not uploaded_files:
        print("❌ No videos uploaded successfully!")
        return
    
    print(f"\n✅ Successfully uploaded {len(uploaded_files)}/{len(remaining_paths)} videos")
    print(f"📊 Total size: {total_size:.2f} MB")
    
    # Wait for processing
    print("\n⏳ Waiting 10 seconds for file processing...")
    time.sleep(10)
    
    # Batch transcribe
    print("\n🎤 Starting batch transcription...")
    print("=" * 60)
    
    start_time = time.time()
    batch_result = batch_transcribe_with_gemini2(uploaded_files)
    processing_time = time.time() - start_time
    
    if batch_result['success']:
        print(f"✅ Batch transcription completed in {processing_time:.2f} seconds!")
        
        # Parse and save individual files
        saved_files = parse_and_save_transcriptions(batch_result, uploaded_files)
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 BATCH PROCESSING SUMMARY")
        print("=" * 60)
        print(f"✅ Videos processed: {len(uploaded_files)}")
        print(f"💾 Files saved: {len(saved_files)}")
        print(f"⏱️  Total processing time: {processing_time:.2f} seconds")
        print(f"⚡ Average time per video: {processing_time/len(uploaded_files):.2f} seconds")
        
        if saved_files:
            print(f"\n📁 Generated transcription files:")
            for file_path in saved_files:
                filename = Path(file_path).name
                print(f"   ✅ {filename}")
        
        print(f"\n🎉 All remaining videos processed successfully!")
        print(f"📂 Check the AI-Videos folder for the new *_transcription.md files")
        
    else:
        print(f"❌ Batch transcription failed: {batch_result['error']}")
        print(f"⏱️  Processing time: {processing_time:.2f} seconds")

if __name__ == "__main__":
    main()
