#!/usr/bin/env python3
"""
Main CLI interface for Video-Understander.
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.video_analyzer import VideoAnalyzer
from src.file_manager import FileManager
from src.video_downloader import VideoDownloader
from config.settings import settings

console = Console()


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def cli(verbose):
    """Video-Understander: Comprehensive video analysis using Gemini AI."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format=settings.log_format,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(settings.log_file)
        ]
    )


@cli.command()
@click.argument('url')
@click.option('--type', '-t', 'analysis_type', 
              type=click.Choice(['comprehensive', 'transcription', 'summary', 'visual_description']),
              default='comprehensive', help='Type of analysis to perform')
@click.option('--output', '-o', help='Output file path')
@click.option('--format', '-f', 'output_format',
              type=click.Choice(['json', 'markdown']),
              default='json', help='Output format')
@click.option('--sampling-rate', type=int, help='Frame sampling rate (FPS)')
@click.option('--start', type=int, help='Start time in seconds')
@click.option('--end', type=int, help='End time in seconds')
def analyze_url(url, analysis_type, output, output_format, sampling_rate, start, end):
    """Analyze video from URL."""
    asyncio.run(_analyze_url(url, analysis_type, output, output_format, sampling_rate, start, end))


async def _analyze_url(url, analysis_type, output, output_format, sampling_rate, start, end):
    """Async implementation of analyze_url."""
    console.print(f"[bold blue]Analyzing video from URL:[/bold blue] {url}")
    
    analyzer = VideoAnalyzer()
    file_manager = FileManager()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Analyzing video...", total=None)
        
        try:
            result = await analyzer.analyze_video_url(
                url=url,
                analysis_type=analysis_type,
                sampling_rate=sampling_rate,
                start_offset=start,
                end_offset=end
            )
            
            progress.update(task, description="Analysis complete!")
            
            # Display results
            console.print(f"[green]✓[/green] Analysis completed in {result.processing_time:.2f} seconds")
            
            if result.error:
                console.print(f"[red]Error:[/red] {result.error}")
                return
            
            # Save results
            if output:
                if output_format == 'markdown' and analysis_type == 'transcription':
                    # Save as markdown for transcription
                    video_info = {
                        'profile': 'unknown',
                        'video_code': result.video_id,
                        'url': url,
                        'title': 'Video Analysis',
                        'description': result.result.get('content', ''),
                        'duration': 'Unknown',
                        'upload_date': 'Unknown',
                        'view_count': 'Unknown',
                        'like_count': 'Unknown'
                    }
                    
                    output_path = await file_manager.save_transcription_markdown(
                        transcription_data=result.result,
                        video_info=video_info,
                        output_path=output
                    )
                else:
                    # Save as JSON
                    result_dict = {
                        'video_id': result.video_id,
                        'video_path': result.video_path,
                        'analysis_type': result.analysis_type,
                        'result': result.result,
                        'metadata': result.metadata,
                        'timestamp': result.timestamp,
                        'processing_time': result.processing_time
                    }
                    
                    output_path = await file_manager.save_analysis_result(
                        result=result_dict,
                        filename=output
                    )
                
                console.print(f"[green]✓[/green] Results saved to: {output_path}")
            else:
                # Display results in console
                console.print("\n[bold]Analysis Results:[/bold]")
                console.print(json.dumps(result.result, indent=2))
                
        except Exception as e:
            progress.update(task, description="Analysis failed!")
            console.print(f"[red]✗[/red] Error: {str(e)}")


@cli.command()
@click.argument('video_path')
@click.option('--type', '-t', 'analysis_type',
              type=click.Choice(['comprehensive', 'transcription', 'summary', 'visual_description']),
              default='comprehensive', help='Type of analysis to perform')
@click.option('--output', '-o', help='Output file path')
@click.option('--format', '-f', 'output_format',
              type=click.Choice(['json', 'markdown']),
              default='json', help='Output format')
def analyze_file(video_path, analysis_type, output, output_format):
    """Analyze local video file."""
    asyncio.run(_analyze_file(video_path, analysis_type, output, output_format))


async def _analyze_file(video_path, analysis_type, output, output_format):
    """Async implementation of analyze_file."""
    console.print(f"[bold blue]Analyzing video file:[/bold blue] {video_path}")
    
    analyzer = VideoAnalyzer()
    file_manager = FileManager()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Analyzing video...", total=None)
        
        try:
            result = await analyzer.analyze_video_file(
                video_path=video_path,
                analysis_type=analysis_type
            )
            
            progress.update(task, description="Analysis complete!")
            
            console.print(f"[green]✓[/green] Analysis completed in {result.processing_time:.2f} seconds")
            
            if result.error:
                console.print(f"[red]Error:[/red] {result.error}")
                return
            
            # Save or display results (similar to analyze_url)
            if output:
                result_dict = {
                    'video_id': result.video_id,
                    'video_path': result.video_path,
                    'analysis_type': result.analysis_type,
                    'result': result.result,
                    'metadata': result.metadata,
                    'timestamp': result.timestamp,
                    'processing_time': result.processing_time
                }
                
                output_path = await file_manager.save_analysis_result(
                    result=result_dict,
                    filename=output
                )
                
                console.print(f"[green]✓[/green] Results saved to: {output_path}")
            else:
                console.print("\n[bold]Analysis Results:[/bold]")
                console.print(json.dumps(result.result, indent=2))
                
        except Exception as e:
            progress.update(task, description="Analysis failed!")
            console.print(f"[red]✗[/red] Error: {str(e)}")


@cli.command()
@click.argument('video_path')
@click.argument('question')
@click.option('--context', help='Additional context for the question')
def ask(video_path, question, context):
    """Ask a question about video content."""
    asyncio.run(_ask(video_path, question, context))


async def _ask(video_path, question, context):
    """Async implementation of ask."""
    console.print(f"[bold blue]Asking question about:[/bold blue] {video_path}")
    console.print(f"[bold]Question:[/bold] {question}")
    
    analyzer = VideoAnalyzer()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Processing question...", total=None)
        
        try:
            answer = await analyzer.ask_video_question(
                video_path=video_path,
                question=question,
                context=context
            )
            
            progress.update(task, description="Question answered!")
            
            console.print(f"\n[bold green]Answer:[/bold green]")
            console.print(answer.get('content', str(answer)))
            
        except Exception as e:
            progress.update(task, description="Question failed!")
            console.print(f"[red]✗[/red] Error: {str(e)}")


@cli.command()
@click.argument('urls', nargs=-1, required=True)
@click.option('--output-dir', '-d', default='AI-Transcrips', help='Output directory')
@click.option('--type', '-t', 'analysis_type',
              type=click.Choice(['comprehensive', 'transcription', 'summary']),
              default='comprehensive', help='Type of analysis to perform')
def batch_instagram(urls, output_dir, analysis_type):
    """Batch process Instagram videos (like the user requested)."""
    asyncio.run(_batch_instagram(urls, output_dir, analysis_type))


async def _batch_instagram(urls, output_dir, analysis_type):
    """Async implementation of batch_instagram."""
    console.print(f"[bold blue]Processing {len(urls)} Instagram videos[/bold blue]")
    
    analyzer = VideoAnalyzer()
    file_manager = FileManager()
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    results = []
    
    with Progress(console=console) as progress:
        main_task = progress.add_task("Processing videos...", total=len(urls))
        
        for i, url in enumerate(urls):
            progress.update(main_task, description=f"Processing video {i+1}/{len(urls)}")
            
            try:
                # Extract video code
                video_code = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
                
                # Analyze video
                result = await analyzer.analyze_video_url(
                    url=url,
                    analysis_type=analysis_type
                )
                
                if result.error:
                    console.print(f"[red]✗[/red] Error processing {url}: {result.error}")
                    continue
                
                # Extract profile name (simplified - would need better extraction)
                profile = "profile"  # This should be extracted from the analysis
                
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
                
                # Save markdown
                output_file = output_path / f"{profile}_{video_code}.md"
                markdown_path = await file_manager.save_transcription_markdown(
                    transcription_data=result.result,
                    video_info=video_info,
                    output_path=output_file
                )
                
                results.append({
                    'url': url,
                    'markdown_path': markdown_path,
                    'success': True
                })
                
                console.print(f"[green]✓[/green] Saved: {markdown_path}")
                
            except Exception as e:
                console.print(f"[red]✗[/red] Error processing {url}: {str(e)}")
                results.append({
                    'url': url,
                    'error': str(e),
                    'success': False
                })
            
            progress.advance(main_task)
    
    # Summary
    successful = len([r for r in results if r.get('success', False)])
    console.print(f"\n[bold green]Completed:[/bold green] {successful}/{len(urls)} videos processed successfully")


@cli.command()
def start_mcp():
    """Start the MCP server."""
    console.print("[bold blue]Starting Video-Understander MCP Server...[/bold blue]")
    
    try:
        from src.mcp_server import main as mcp_main
        asyncio.run(mcp_main())
    except KeyboardInterrupt:
        console.print("\n[yellow]MCP Server stopped[/yellow]")
    except Exception as e:
        console.print(f"[red]Error starting MCP server:[/red] {str(e)}")


@cli.command()
def info():
    """Show system information and configuration."""
    table = Table(title="Video-Understander Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Gemini Model", settings.gemini_model)
    table.add_row("Max Video Size", f"{settings.max_video_size / (1024*1024):.0f} MB")
    table.add_row("Max Duration", f"{settings.max_video_duration / 3600:.1f} hours")
    table.add_row("Batch Size", str(settings.batch_size))
    table.add_row("Storage Path", settings.storage_path)
    table.add_row("Results Path", settings.results_path)
    
    console.print(table)


if __name__ == '__main__':
    cli()
