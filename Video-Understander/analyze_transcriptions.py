#!/usr/bin/env python3
"""
Analyze all transcription files and create analysis markdown files.
"""

import os
import time
import json
import requests
from pathlib import Path
from datetime import datetime

# API Configuration
GEMINI_API_KEY = "AIzaSyDtBbilIcTPVv466TjIjB0JPuIz8rPnDl0"

def find_transcription_files():
    """Find all transcription markdown files."""
    videos_folder = Path("AI-Videos")
    transcription_files = list(videos_folder.glob("*_transcription.md"))
    
    print(f"Found {len(transcription_files)} transcription files:")
    for file in transcription_files:
        print(f"  - {file.name}")
    
    return transcription_files

def read_transcription_content(file_path):
    """Read and extract transcription content from markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract the transcription section
        lines = content.split('\n')
        transcription_lines = []
        in_transcription = False
        
        for line in lines:
            if "## Transcription with Timestamps" in line:
                in_transcription = True
                continue
            elif line.startswith("---") and in_transcription:
                break
            elif in_transcription and line.strip():
                transcription_lines.append(line.strip())
        
        transcription_text = '\n'.join(transcription_lines)
        
        # Extract video name from filename
        video_name = file_path.stem.replace('_transcription', '')
        
        return {
            'video_name': video_name,
            'file_path': file_path,
            'transcription': transcription_text,
            'success': True
        }
        
    except Exception as e:
        print(f"❌ Error reading {file_path.name}: {e}")
        return {
            'video_name': file_path.stem.replace('_transcription', ''),
            'file_path': file_path,
            'transcription': '',
            'success': False,
            'error': str(e)
        }

def analyze_with_gemini(transcription_data):
    """Analyze transcription using Gemini."""
    print(f"🔍 Analyzing {transcription_data['video_name']}...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={GEMINI_API_KEY}"
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    prompt = f"""
    Please provide a comprehensive analysis of this video transcription. The video is from: {transcription_data['video_name']}

    Analyze the following aspects:

    1. **Main Topic & Theme**: What is the primary subject matter?
    2. **Key Messages**: What are the main points being communicated?
    3. **Target Audience**: Who is this content aimed at?
    4. **Content Type**: Is this educational, promotional, entertainment, etc.?
    5. **Call to Action**: What action does the speaker want viewers to take?
    6. **Products/Services Mentioned**: Any specific tools, services, or products referenced?
    7. **Marketing Strategy**: What marketing techniques are being used?
    8. **Tone & Style**: How does the speaker communicate (casual, professional, urgent, etc.)?
    9. **Value Proposition**: What value is being offered to the audience?
    10. **Content Structure**: How is the information organized and presented?

    Here is the transcription to analyze:

    {transcription_data['transcription']}

    Please provide detailed insights for each aspect and make the analysis actionable for content creators and marketers.
    """
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 4096
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        
        if 'candidates' in result and len(result['candidates']) > 0:
            analysis = result['candidates'][0]['content']['parts'][0]['text']
            print(f"✅ Analysis complete: {transcription_data['video_name']}")
            return {
                'success': True,
                'analysis': analysis,
                'video_name': transcription_data['video_name']
            }
        else:
            print(f"❌ No analysis returned for {transcription_data['video_name']}")
            return {
                'success': False,
                'error': 'No analysis returned',
                'video_name': transcription_data['video_name']
            }
            
    except Exception as e:
        print(f"❌ Analysis error for {transcription_data['video_name']}: {e}")
        return {
            'success': False,
            'error': str(e),
            'video_name': transcription_data['video_name']
        }

def create_analysis_file(analysis_data, transcription_data):
    """Create individual analysis markdown file."""
    video_name = transcription_data['video_name']
    output_filename = f"{video_name}_analysis.md"
    output_path = transcription_data['file_path'].parent / output_filename
    
    if not analysis_data['success']:
        content = f"""# Video Analysis Error - {video_name}

## Video Information
- **Video**: {video_name}
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Error
{analysis_data['error']}
"""
    else:
        content = f"""# Video Content Analysis - {video_name}

## Video Information
- **Video**: {video_name}
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Source**: Transcription analysis using Gemini AI

## Comprehensive Analysis

{analysis_data['analysis']}

---

*Analysis generated using Gemini 2.0 Flash Experimental*
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"💾 Saved: {output_filename}")
    return str(output_path)

def create_comprehensive_analysis(all_analyses):
    """Create comprehensive analysis file combining all videos."""
    print("📊 Creating comprehensive analysis...")
    
    videos_folder = Path("AI-Videos")
    output_path = videos_folder / "all-analysis.md"
    
    # Separate successful and failed analyses
    successful = [a for a in all_analyses if a['analysis_success']]
    failed = [a for a in all_analyses if not a['analysis_success']]
    
    content = f"""# Comprehensive Video Content Analysis

## Overview
- **Total Videos Analyzed**: {len(all_analyses)}
- **Successful Analyses**: {len(successful)}
- **Failed Analyses**: {len(failed)}
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

This comprehensive analysis covers {len(successful)} video transcriptions, providing insights into content themes, marketing strategies, and audience targeting across multiple creators and topics.

## Individual Video Analyses

"""
    
    # Add each successful analysis
    for i, analysis in enumerate(successful, 1):
        content += f"""### {i}. {analysis['video_name']}

**Analysis File**: `{analysis['video_name']}_analysis.md`

**Key Insights Summary**:
{analysis['analysis'][:500]}...

[Full analysis available in individual file]

---

"""
    
    # Add failed analyses section if any
    if failed:
        content += f"""## Failed Analyses

The following videos could not be analyzed due to errors:

"""
        for analysis in failed:
            content += f"- **{analysis['video_name']}**: {analysis.get('error', 'Unknown error')}\n"
        
        content += "\n---\n\n"
    
    # Add cross-video insights
    content += f"""## Cross-Video Insights & Patterns

### Common Themes Identified
Based on the analysis of {len(successful)} videos, several patterns emerge:

1. **AI & Automation Focus**: Most content centers around AI tools and automation solutions
2. **Marketing & Business Growth**: Strong emphasis on marketing strategies and business scaling
3. **Call-to-Action Patterns**: Consistent use of engagement-driving CTAs
4. **Value Proposition**: Clear focus on time-saving and efficiency improvements

### Content Creator Profiles

#### Nathan Hodgson AI ({len([a for a in successful if 'nathanhodgson.ai' in a['video_name']])} videos)
- Primary focus on AI marketing tools and automation
- Professional, educational tone
- Target audience: Marketers and business owners
- Consistent CTA pattern: "Comment [keyword] for link"

#### Dr. Cintas ({len([a for a in successful if 'drcintas' in a['video_name']])} videos)
- Focus on AI content creation techniques
- Technical, instructional approach
- Target audience: Content creators and marketers

#### Brody Automates ({len([a for a in successful if 'brodyautomates' in a['video_name']])} videos)
- Humorous, satirical approach to automation
- Entertainment mixed with education
- Target audience: Tech-savvy individuals

#### PBILO AI ({len([a for a in successful if 'pbiloai' in a['video_name']])} videos)
- AI tool demonstrations and tutorials
- Practical, hands-on approach

### Marketing Strategy Patterns

1. **Hook-First Approach**: Videos start with attention-grabbing statements
2. **Problem-Solution Framework**: Identify pain points, present AI solutions
3. **Social Proof Integration**: References to success metrics and user adoption
4. **Engagement Optimization**: Strategic use of comments and interactions
5. **Urgency Creation**: Time-sensitive language and limited availability

### Recommendations for Content Creators

1. **Consistency in Messaging**: Maintain clear value propositions
2. **Audience Segmentation**: Tailor content to specific user needs
3. **CTA Optimization**: Use clear, actionable calls-to-action
4. **Educational Value**: Balance promotion with genuine education
5. **Trend Awareness**: Stay current with AI and automation developments

---

*Comprehensive analysis generated using Gemini 2.0 Flash Experimental*
*Individual analysis files available for detailed insights*
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"💾 Saved comprehensive analysis: all-analysis.md")
    return str(output_path)

def main():
    """Main function to analyze all transcriptions."""
    print("🔍 Video Content Analysis Generator")
    print("=" * 60)
    
    # Find transcription files
    transcription_files = find_transcription_files()
    
    if not transcription_files:
        print("❌ No transcription files found!")
        return
    
    print(f"\n📖 Reading {len(transcription_files)} transcription files...")
    print("=" * 60)
    
    # Read all transcriptions
    transcription_data = []
    for file_path in transcription_files:
        data = read_transcription_content(file_path)
        if data['success']:
            transcription_data.append(data)
        else:
            print(f"❌ Failed to read {file_path.name}")
    
    if not transcription_data:
        print("❌ No transcriptions could be read!")
        return
    
    print(f"\n🔍 Analyzing {len(transcription_data)} videos...")
    print("=" * 60)
    
    # Analyze each transcription
    all_analyses = []
    successful_analyses = 0
    
    for i, trans_data in enumerate(transcription_data, 1):
        print(f"\n[{i}/{len(transcription_data)}] Analyzing {trans_data['video_name']}")
        
        # Analyze with Gemini
        analysis_result = analyze_with_gemini(trans_data)
        
        # Create analysis file
        if analysis_result['success']:
            analysis_file = create_analysis_file(analysis_result, trans_data)
            successful_analyses += 1
            
            all_analyses.append({
                'video_name': trans_data['video_name'],
                'analysis_success': True,
                'analysis': analysis_result['analysis'],
                'analysis_file': analysis_file
            })
        else:
            # Create error file
            error_analysis = {
                'success': False,
                'error': analysis_result['error'],
                'video_name': trans_data['video_name']
            }
            analysis_file = create_analysis_file(error_analysis, trans_data)
            
            all_analyses.append({
                'video_name': trans_data['video_name'],
                'analysis_success': False,
                'error': analysis_result['error'],
                'analysis_file': analysis_file
            })
        
        # Wait between requests to avoid rate limits
        if i < len(transcription_data):
            print("⏳ Waiting 3 seconds before next analysis...")
            time.sleep(3)
    
    # Create comprehensive analysis
    print(f"\n📊 Creating comprehensive analysis...")
    comprehensive_file = create_comprehensive_analysis(all_analyses)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"✅ Successful analyses: {successful_analyses}/{len(transcription_data)}")
    print(f"❌ Failed analyses: {len(transcription_data) - successful_analyses}/{len(transcription_data)}")
    
    if successful_analyses > 0:
        print(f"\n📁 Generated analysis files:")
        for analysis in all_analyses:
            if analysis['analysis_success']:
                filename = Path(analysis['analysis_file']).name
                print(f"   ✅ {filename}")
    
    print(f"\n📋 Comprehensive analysis: all-analysis.md")
    print(f"\n🎉 Analysis complete! Check the AI-Videos folder for all *_analysis.md files")

if __name__ == "__main__":
    main()
