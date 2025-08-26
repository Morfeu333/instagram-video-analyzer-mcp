#!/usr/bin/env python3
"""
Voice-tone analysis for scriptwriting inspiration.
Analyzes speaking patterns, delivery styles, and content structure.
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
    
    print(f"Found {len(transcription_files)} transcription files for voice-tone analysis:")
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

def analyze_voice_tone_with_gemini(transcription_data):
    """Analyze voice and tone for scriptwriting inspiration."""
    print(f"🎤 Analyzing voice & tone: {transcription_data['video_name']}...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={GEMINI_API_KEY}"
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    prompt = f"""
    As a scriptwriting expert, analyze this video transcription for voice, tone, and delivery patterns. The creator is: {transcription_data['video_name']}

    Provide a comprehensive VOICE & TONE ANALYSIS for scriptwriting inspiration:

    ## 1. VOICE CHARACTERISTICS
    - **Speaking Pace**: Fast, moderate, slow, varied?
    - **Energy Level**: High energy, calm, intense, relaxed?
    - **Vocal Patterns**: Emphasis techniques, pauses, rhythm
    - **Personality Traits**: Confident, casual, authoritative, friendly, etc.

    ## 2. TONE ANALYSIS
    - **Primary Tone**: Professional, conversational, urgent, educational, etc.
    - **Emotional Undertones**: Excitement, concern, enthusiasm, skepticism
    - **Consistency**: Does tone shift throughout? When and why?
    - **Audience Connection**: How does tone create rapport?

    ## 3. LANGUAGE PATTERNS
    - **Vocabulary Level**: Simple, technical, mixed, industry-specific
    - **Sentence Structure**: Short punchy sentences, complex explanations, questions
    - **Repetition Techniques**: Key phrases, concepts, calls-to-action
    - **Transition Words**: How they connect ideas

    ## 4. CONTENT DELIVERY STYLE
    - **Opening Hook**: How do they grab attention in first 5 seconds?
    - **Information Flow**: Linear, scattered, problem-solution, story-driven
    - **Emphasis Techniques**: What they stress and how
    - **Closing Strategy**: How they end and what action they request

    ## 5. SCRIPTWRITING INSIGHTS
    - **Copyable Phrases**: Specific powerful phrases to adapt
    - **Structure Template**: Reusable content framework
    - **Timing Patterns**: When they introduce key points
    - **Engagement Triggers**: What keeps viewers watching

    ## 6. ADAPTATION GUIDE
    - **Voice Replication**: How to mimic this style
    - **Tone Matching**: Key elements to maintain
    - **Content Adaptation**: How to apply this style to different topics
    - **Script Template**: Practical framework for similar content

    ## 7. UNIQUE STYLE ELEMENTS
    - **Signature Phrases**: Creator's distinctive language
    - **Delivery Quirks**: Unique speaking patterns
    - **Brand Voice**: How personality comes through
    - **Differentiation**: What makes this style unique

    Here is the transcription with timestamps to analyze:

    {transcription_data['transcription']}

    Focus on actionable insights for someone wanting to write scripts in a similar style. Be specific about timing, word choice, and delivery patterns.
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
            "temperature": 0.2,
            "maxOutputTokens": 4096
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        
        if 'candidates' in result and len(result['candidates']) > 0:
            analysis = result['candidates'][0]['content']['parts'][0]['text']
            print(f"✅ Voice-tone analysis complete: {transcription_data['video_name']}")
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

def create_voice_analysis_file(analysis_data, transcription_data):
    """Create voice-tone analysis markdown file."""
    video_name = transcription_data['video_name']
    output_filename = f"{video_name}_analysis.md"
    output_path = transcription_data['file_path'].parent / output_filename
    
    if not analysis_data['success']:
        content = f"""# Voice & Tone Analysis Error - {video_name}

## Video Information
- **Creator**: {video_name}
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Analysis Type**: Voice & Tone for Scriptwriting

## Error
{analysis_data['error']}
"""
    else:
        content = f"""# Voice & Tone Analysis - {video_name}

## Creator Information
- **Creator**: {video_name}
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Analysis Type**: Voice & Tone for Scriptwriting Inspiration
- **Purpose**: Script adaptation and style replication

## Voice & Tone Analysis for Scriptwriting

{analysis_data['analysis']}

---

## Quick Reference for Script Writing

### Key Takeaways:
- **Primary Voice**: [Extract from analysis above]
- **Signature Tone**: [Extract from analysis above]
- **Best Phrases to Adapt**: [Extract from analysis above]
- **Content Structure**: [Extract from analysis above]

### Script Template Based on This Style:
```
[Opening Hook - First 5 seconds]
[Problem/Context Setup]
[Solution/Main Content]
[Social Proof/Examples]
[Call to Action]
```

---

*Voice & Tone Analysis generated using Gemini 2.0 Flash Experimental*
*Designed for scriptwriting inspiration and style adaptation*
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"💾 Saved voice analysis: {output_filename}")
    return str(output_path)

def create_comprehensive_voice_guide(all_analyses):
    """Create comprehensive voice & tone guide for scriptwriting."""
    print("📝 Creating comprehensive voice & tone guide...")
    
    videos_folder = Path("AI-Videos")
    output_path = videos_folder / "all-analysis.md"
    
    # Separate successful and failed analyses
    successful = [a for a in all_analyses if a['analysis_success']]
    failed = [a for a in all_analyses if not a['analysis_success']]
    
    content = f"""# Complete Voice & Tone Guide for Scriptwriting

## Overview
- **Total Creators Analyzed**: {len(all_analyses)}
- **Successful Voice Analyses**: {len(successful)}
- **Failed Analyses**: {len(failed)}
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Purpose**: Scriptwriting inspiration and style replication

## Executive Summary

This comprehensive guide analyzes the voice, tone, and delivery patterns of {len(successful)} content creators to help you write scripts inspired by their styles. Each analysis focuses on actionable insights for script adaptation.

## Creator Voice Profiles

"""
    
    # Add each successful analysis summary
    for i, analysis in enumerate(successful, 1):
        creator_name = analysis['video_name']
        content += f"""### {i}. {creator_name}

**Full Analysis**: `{creator_name}_analysis.md`

**Voice Summary**: [Extract key voice characteristics from analysis]
**Tone Profile**: [Extract primary tone elements]
**Signature Style**: [Extract unique elements]
**Best for**: [Extract recommended use cases]

**Quick Script Inspiration**:
- Opening style: [Extract opening pattern]
- Content flow: [Extract structure pattern]
- Closing style: [Extract closing pattern]

---

"""
    
    # Add scriptwriting frameworks
    content += f"""## Scriptwriting Frameworks by Style

### High-Energy AI Marketing (Nathan Hodgson Style)
```
[00:00-00:03] Attention-grabbing statement about AI
[00:03-00:10] Problem identification with urgency
[00:10-00:20] Solution presentation with benefits
[00:20-00:25] Social proof or demonstration
[00:25-00:30] Clear call-to-action with keyword
```

### Technical Educational (Dr. Cintas Style)
```
[00:00-00:05] Technical hook with specific method
[00:05-00:15] Step-by-step explanation
[00:15-00:25] Practical demonstration
[00:25-00:30] Implementation guidance
```

### Humorous Automation (Brody Style)
```
[00:00-00:03] Absurd/satirical opening
[00:03-00:15] Exaggerated problem description
[00:15-00:25] Over-the-top solution
[00:25-00:30] Comedic conclusion
```

## Voice Adaptation Strategies

### 1. Energy Level Matching
- **High Energy**: Quick pace, exclamation points, urgent language
- **Moderate Energy**: Steady pace, confident tone, clear explanations
- **Calm Energy**: Slower pace, thoughtful pauses, detailed explanations

### 2. Tone Replication Techniques
- **Professional**: Industry terminology, structured presentation
- **Conversational**: Personal pronouns, casual language, relatable examples
- **Urgent**: Time-sensitive language, immediate benefits, action words

### 3. Language Pattern Adaptation
- **Vocabulary Level**: Match complexity to audience
- **Sentence Structure**: Mirror creator's rhythm and flow
- **Repetition**: Use similar emphasis techniques
- **Transitions**: Adopt connection patterns

## Content Creator Archetypes

### The AI Evangelist (Nathan Hodgson)
- **Voice**: Confident, enthusiastic, knowledgeable
- **Tone**: Professional yet accessible, urgent but helpful
- **Best for**: AI tool promotion, business automation, marketing content
- **Signature**: "Comment [KEYWORD] for [BENEFIT]"

### The Technical Educator (Dr. Cintas)
- **Voice**: Authoritative, clear, methodical
- **Tone**: Educational, professional, step-by-step
- **Best for**: Tutorial content, technical explanations, how-to guides
- **Signature**: Structured methodology presentation

### The Satirical Automator (Brody)
- **Voice**: Humorous, exaggerated, self-aware
- **Tone**: Comedic, satirical, entertaining
- **Best for**: Entertainment content, social commentary, viral content
- **Signature**: Absurd automation scenarios

## Script Templates by Use Case

### AI Tool Promotion Script
```
[Hook] "AI just [DRAMATIC CHANGE]"
[Problem] "Here's what [TARGET AUDIENCE] struggle with..."
[Solution] "Meet [TOOL NAME], the [BENEFIT]..."
[Proof] "[SPECIFIC RESULT/METRIC]"
[CTA] "Comment '[KEYWORD]' to get [BENEFIT]"
```

### Educational Content Script
```
[Hook] "Here's the [METHOD] that [RESULT]"
[Context] "Most people [COMMON MISTAKE]..."
[Method] "Instead, do this: [STEP-BY-STEP]"
[Example] "Here's how it works: [DEMONSTRATION]"
[Action] "Try this and [EXPECTED OUTCOME]"
```

### Entertainment/Viral Script
```
[Hook] "[ABSURD STATEMENT] about [TOPIC]"
[Setup] "Imagine if [EXAGGERATED SCENARIO]..."
[Development] "[INCREASINGLY RIDICULOUS DETAILS]"
[Climax] "[PEAK ABSURDITY]"
[Punchline] "[COMEDIC CONCLUSION]"
```

## Voice Matching Checklist

### Before Writing:
- [ ] Identify target creator's energy level
- [ ] Note their primary tone
- [ ] List their signature phrases
- [ ] Understand their content structure
- [ ] Identify their unique style elements

### While Writing:
- [ ] Match sentence length and complexity
- [ ] Use similar vocabulary level
- [ ] Replicate emphasis patterns
- [ ] Follow their content flow
- [ ] Include their style of call-to-action

### After Writing:
- [ ] Read aloud to check pace
- [ ] Verify tone consistency
- [ ] Ensure personality comes through
- [ ] Check for signature elements
- [ ] Validate audience connection

## Advanced Adaptation Techniques

### 1. Voice Blending
Combine elements from multiple creators:
- Nathan's urgency + Dr. Cintas's structure
- Brody's humor + Nathan's professionalism
- Technical depth + conversational tone

### 2. Context Adaptation
Modify style for different:
- **Platforms**: Instagram vs YouTube vs TikTok
- **Audiences**: Beginners vs experts vs mixed
- **Topics**: Technical vs business vs entertainment
- **Goals**: Education vs promotion vs engagement

### 3. Personal Brand Integration
- Maintain creator's core voice elements
- Add your unique personality touches
- Adapt to your brand values
- Consider your audience preferences

---

*Complete Voice & Tone Guide for Scriptwriting*
*Generated using Gemini 2.0 Flash Experimental*
*Designed for content creators seeking style inspiration*
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"💾 Saved comprehensive voice guide: all-analysis.md")
    return str(output_path)

def main():
    """Main function for voice-tone analysis."""
    print("🎤 Voice & Tone Analysis for Scriptwriting")
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
    
    print(f"\n🎤 Analyzing voice & tone for {len(transcription_data)} creators...")
    print("=" * 60)
    
    # Analyze each transcription for voice & tone
    all_analyses = []
    successful_analyses = 0
    
    for i, trans_data in enumerate(transcription_data, 1):
        print(f"\n[{i}/{len(transcription_data)}] Voice analysis: {trans_data['video_name']}")
        
        # Analyze with Gemini
        analysis_result = analyze_voice_tone_with_gemini(trans_data)
        
        # Create analysis file
        if analysis_result['success']:
            analysis_file = create_voice_analysis_file(analysis_result, trans_data)
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
            analysis_file = create_voice_analysis_file(error_analysis, trans_data)
            
            all_analyses.append({
                'video_name': trans_data['video_name'],
                'analysis_success': False,
                'error': analysis_result['error'],
                'analysis_file': analysis_file
            })
        
        # Wait between requests
        if i < len(transcription_data):
            print("⏳ Waiting 3 seconds before next analysis...")
            time.sleep(3)
    
    # Create comprehensive voice guide
    print(f"\n📝 Creating comprehensive scriptwriting guide...")
    comprehensive_file = create_comprehensive_voice_guide(all_analyses)
    
    # Print summary
    print("\n" + "=" * 60)
    print("🎤 VOICE & TONE ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"✅ Successful voice analyses: {successful_analyses}/{len(transcription_data)}")
    print(f"❌ Failed analyses: {len(transcription_data) - successful_analyses}/{len(transcription_data)}")
    
    if successful_analyses > 0:
        print(f"\n📁 Generated voice analysis files:")
        for analysis in all_analyses:
            if analysis['analysis_success']:
                filename = Path(analysis['analysis_file']).name
                print(f"   🎤 {filename}")
    
    print(f"\n📋 Comprehensive scriptwriting guide: all-analysis.md")
    print(f"\n🎉 Voice & tone analysis complete!")
    print(f"📝 Ready for scriptwriting inspiration based on these styles!")

if __name__ == "__main__":
    main()
