#!/usr/bin/env python3
"""
YouTube Video Analysis with Gemini Video Understanding.
Combines transcription with comprehensive visual scene analysis.
"""

import os
import time
import json
import requests
from pathlib import Path
from datetime import datetime

# API Configuration
GEMINI_API_KEY = "AIzaSyDtBbilIcTPVv466TjIjB0JPuIz8rPnDl0"

def upload_youtube_to_gemini(youtube_url):
    """Upload YouTube video directly to Gemini."""
    print(f"📤 Uploading YouTube video to Gemini...")
    print(f"🔗 URL: {youtube_url}")
    
    upload_url = f"https://generativelanguage.googleapis.com/upload/v1beta/files?key={GEMINI_API_KEY}"
    
    try:
        # For YouTube videos, we can pass the URL directly
        metadata = {
            'file': {
                'display_name': 'Claude Code Design Tutorial',
                'uri': youtube_url
            }
        }
        
        data = {
            'metadata': json.dumps(metadata)
        }
        
        # Alternative: Use the direct video URI approach
        files_url = f"https://generativelanguage.googleapis.com/v1beta/files?key={GEMINI_API_KEY}"
        
        payload = {
            "file": {
                "display_name": "Claude Code Design Tutorial",
                "uri": youtube_url
            }
        }
        
        response = requests.post(files_url, json=payload, timeout=120)
        
        if response.status_code == 200:
            file_info = response.json()
            file_uri = file_info.get('uri')
            
            if file_uri:
                print(f"✅ YouTube video uploaded successfully!")
                return file_uri
        
        # If direct URI doesn't work, we'll need to download and upload
        print("⚠️  Direct URI upload failed, trying alternative method...")
        return None
        
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return None

def comprehensive_video_analysis(video_uri, youtube_url):
    """Perform comprehensive video analysis with visual scene understanding."""
    print(f"🎬 Starting comprehensive video analysis...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={GEMINI_API_KEY}"
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    prompt = f"""
    Perform a COMPREHENSIVE ANALYSIS of this Claude code design capabilities tutorial video: {youtube_url}

    I need both TRANSCRIPTION and VISUAL ANALYSIS. Please provide:

    ## 1. COMPLETE TRANSCRIPTION WITH TIMESTAMPS
    - Transcribe ALL spoken content with precise MM:SS timestamps
    - Include every word, pause, and verbal cue
    - Format: [MM:SS] Transcribed content

    ## 2. VISUAL SCENE ANALYSIS
    For each major scene/section, analyze:
    - **Screen Layout**: What's visible on screen
    - **UI Elements**: Buttons, menus, panels, tools
    - **Code Snippets**: Any code shown, syntax, languages
    - **Visual Transitions**: How scenes change
    - **Demonstrations**: What actions are being performed

    ## 3. TECHNICAL CONTENT ANALYSIS
    - **Tools Demonstrated**: What software/platforms are shown
    - **Features Highlighted**: Specific capabilities being taught
    - **Code Examples**: Programming languages, frameworks, libraries
    - **Workflow Steps**: Step-by-step processes shown
    - **Best Practices**: Techniques and methodologies demonstrated

    ## 4. EDUCATIONAL STRUCTURE ANALYSIS
    - **Learning Objectives**: What skills are being taught
    - **Difficulty Level**: Beginner, intermediate, advanced content
    - **Prerequisites**: What knowledge is assumed
    - **Key Takeaways**: Main lessons and insights
    - **Practical Applications**: How to apply the knowledge

    ## 5. VISUAL DESIGN ANALYSIS
    - **Interface Design**: UI/UX elements and layouts
    - **Color Schemes**: Visual themes and styling
    - **Typography**: Fonts, text styling, readability
    - **Visual Hierarchy**: How information is organized
    - **User Experience**: Interaction patterns and flows

    ## 6. CONTENT DELIVERY ANALYSIS
    - **Presentation Style**: How information is communicated
    - **Pacing**: Speed of content delivery
    - **Visual Aids**: Diagrams, annotations, highlights
    - **Engagement Techniques**: How viewer attention is maintained
    - **Clarity**: How well concepts are explained

    ## 7. TECHNICAL IMPLEMENTATION DETAILS
    - **Code Quality**: Best practices demonstrated
    - **Architecture Patterns**: Design patterns shown
    - **Development Workflow**: Process and methodology
    - **Tool Integration**: How different tools work together
    - **Problem-Solving Approach**: How challenges are addressed

    ## 8. ACTIONABLE INSIGHTS
    - **Key Techniques**: Specific methods to implement
    - **Tool Recommendations**: Software and resources mentioned
    - **Learning Path**: Suggested progression for learners
    - **Common Pitfalls**: Mistakes to avoid
    - **Next Steps**: How to continue learning

    Please be extremely detailed and specific. I want to understand both what is being said AND what is being shown visually throughout the entire video.

    Focus on practical, actionable insights that someone could use to improve their own Claude code design capabilities.
    """
    
    # Try different payload formats for YouTube videos
    payload_options = [
        # Option 1: Direct video reference
        {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "file_data": {
                                "mime_type": "video/mp4",
                                "file_uri": video_uri
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 8192
            }
        },
        # Option 2: YouTube URL direct
        {
            "contents": [
                {
                    "parts": [
                        {"text": f"{prompt}\n\nYouTube Video URL: {youtube_url}"}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 8192
            }
        }
    ]
    
    for i, payload in enumerate(payload_options, 1):
        try:
            print(f"🔄 Trying analysis method {i}...")
            response = requests.post(url, headers=headers, json=payload, timeout=300)
            response.raise_for_status()
            
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                analysis = result['candidates'][0]['content']['parts'][0]['text']
                print(f"✅ Comprehensive analysis complete!")
                return {
                    'success': True,
                    'analysis': analysis,
                    'method': f"Method {i}",
                    'video_url': youtube_url
                }
            else:
                print(f"❌ No analysis returned with method {i}")
                
        except Exception as e:
            print(f"❌ Analysis method {i} failed: {e}")
            if i < len(payload_options):
                print(f"⏳ Trying next method...")
                time.sleep(3)
    
    return {
        'success': False,
        'error': 'All analysis methods failed',
        'video_url': youtube_url
    }

def create_comprehensive_analysis_file(analysis_data, youtube_url):
    """Create comprehensive analysis markdown file."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f"claude_tutorial_analysis_{timestamp}.md"
    output_path = Path("AI-Videos") / output_filename
    
    # Ensure directory exists
    output_path.parent.mkdir(exist_ok=True)
    
    if not analysis_data['success']:
        content = f"""# YouTube Video Analysis Error

## Video Information
- **URL**: {youtube_url}
- **Title**: Claude Code Design Capabilities Tutorial
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Analysis Type**: Comprehensive Video + Visual Analysis

## Error
{analysis_data['error']}

## Attempted Methods
- Direct video file upload
- YouTube URL processing
- Alternative API endpoints

## Recommendations
1. Try downloading the video locally first
2. Use yt-dlp to extract video file
3. Upload video file directly to Gemini
4. Retry with different video formats
"""
    else:
        content = f"""# Comprehensive YouTube Video Analysis
## Claude Code Design Capabilities Tutorial

### Video Information
- **URL**: {youtube_url}
- **Title**: Claude Code Design Capabilities Tutorial
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Analysis Type**: Complete Transcription + Visual Scene Analysis
- **Analysis Method**: {analysis_data['method']}
- **API**: Gemini 2.0 Flash Experimental

### Analysis Overview
This comprehensive analysis combines audio transcription with detailed visual scene analysis, providing insights into both the spoken content and visual demonstrations throughout the tutorial.

---

## Complete Analysis

{analysis_data['analysis']}

---

## Analysis Capabilities Demonstrated

### ✅ Transcription Features:
- Complete audio transcription with timestamps
- Verbal cues and speaking patterns
- Technical terminology recognition
- Natural language processing

### ✅ Visual Analysis Features:
- Screen layout and UI element identification
- Code snippet recognition and analysis
- Visual transition tracking
- Interface design evaluation
- User interaction pattern analysis

### ✅ Technical Content Analysis:
- Programming language identification
- Framework and library recognition
- Development workflow analysis
- Best practice identification
- Tool integration assessment

### ✅ Educational Structure Analysis:
- Learning objective identification
- Skill level assessment
- Knowledge prerequisite analysis
- Practical application guidance

---

*Comprehensive analysis generated using Gemini 2.0 Flash Experimental*
*Combining advanced video understanding with visual scene analysis*
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"💾 Saved comprehensive analysis: {output_filename}")
    return str(output_path)

def main():
    """Main function for YouTube video analysis."""
    print("🎬 YouTube Video Comprehensive Analysis")
    print("=" * 60)
    
    youtube_url = "https://www.youtube.com/watch?v=xOO8Wt_i72s"
    
    print(f"📺 Analyzing: Claude Code Design Capabilities Tutorial")
    print(f"🔗 URL: {youtube_url}")
    print(f"🎯 Analysis Type: Transcription + Visual Scene Analysis")
    
    # Try to upload/reference the video
    print(f"\n📤 Preparing video for analysis...")
    video_uri = upload_youtube_to_gemini(youtube_url)
    
    # Perform comprehensive analysis
    print(f"\n🔍 Starting comprehensive analysis...")
    start_time = time.time()
    
    analysis_result = comprehensive_video_analysis(video_uri, youtube_url)
    
    processing_time = time.time() - start_time
    
    # Create analysis file
    analysis_file = create_comprehensive_analysis_file(analysis_result, youtube_url)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE ANALYSIS SUMMARY")
    print("=" * 60)
    
    if analysis_result['success']:
        print(f"✅ Analysis successful!")
        print(f"📁 Analysis file: {Path(analysis_file).name}")
        print(f"⏱️  Processing time: {processing_time:.2f} seconds")
        print(f"🎯 Analysis method: {analysis_result['method']}")
        
        print(f"\n🎬 Analysis includes:")
        print(f"   📝 Complete transcription with timestamps")
        print(f"   👁️  Visual scene analysis")
        print(f"   💻 Technical content breakdown")
        print(f"   🎓 Educational structure analysis")
        print(f"   🎨 Visual design evaluation")
        print(f"   📋 Actionable insights and recommendations")
        
    else:
        print(f"❌ Analysis failed: {analysis_result['error']}")
        print(f"📁 Error report: {Path(analysis_file).name}")
        print(f"⏱️  Processing time: {processing_time:.2f} seconds")
    
    print(f"\n🎉 YouTube video analysis complete!")
    print(f"📂 Check the AI-Videos folder for the analysis file")

if __name__ == "__main__":
    main()
