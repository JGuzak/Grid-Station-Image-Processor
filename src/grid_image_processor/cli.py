"""
Grid Image Processor CLI

Command-line interface for batch processing Grid interface screenshots.
"""

import click
import os
import sys
from typing import Tuple

from .processor import GridImageProcessor


@click.command()
@click.option(
    '--input-dir', '-i',
    default='images',
    help='Input directory containing PNG images to process',
    type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.option(
    '--output-dir', '-o',
    default='images/processed',
    help='Output directory for processed images',
    type=click.Path(file_okay=False, dir_okay=True)
)
@click.option(
    '--width', '-w',
    default=670,
    help='Target width for output images',
    type=int
)
@click.option(
    '--height', '-h',
    default=366,
    help='Target height for output images',
    type=int
)
@click.option(
    '--bracket-offset',
    default=2,
    help='Pixels to crop inside brackets to exclude black lines',
    type=int
)
@click.option(
    '--quiet', '-q',
    is_flag=True,
    help='Suppress output messages'
)
@click.version_option(version='1.0.0', prog_name='grid-process')
def main(input_dir: str, output_dir: str, width: int, height: int, bracket_offset: int, quiet: bool):
    """
    Grid Image Processor - Batch process Monome Grid interface screenshots.
    
    This tool crops Grid interface screenshots to their bracket intersections
    and resizes them to standard dimensions, excluding the black bracket lines.
    
    Examples:
    
        # Process images in 'images' directory to 'images/processed'
        grid-process
        
        # Process with custom directories
        grid-process -i screenshots -o processed_screenshots
        
        # Process with custom dimensions
        grid-process --width 800 --height 450
        
        # Process quietly (no output)
        grid-process --quiet
    """
    if not quiet:
        click.echo("Grid Interface Image Processor")
        click.echo("=" * 40)
    
    # Validate input directory
    if not os.path.exists(input_dir):
        click.echo(f"Error: Input directory '{input_dir}' not found!", err=True)
        sys.exit(1)
    
    # Initialize processor
    target_size = (width, height)
    processor = GridImageProcessor(target_size=target_size, bracket_offset=bracket_offset)
    
    # Process images
    try:
        successful, failed = processor.batch_process(
            input_dir=input_dir,
            output_dir=output_dir,
            verbose=not quiet
        )
        
        if not quiet:
            if successful > 0:
                click.echo(f"\n✓ Successfully processed {successful} images")
            if failed > 0:
                click.echo(f"✗ Failed to process {failed} images", err=True)
        
        # Exit with error code if any failures
        if failed > 0:
            sys.exit(1)
            
    except KeyboardInterrupt:
        click.echo("\nProcessing interrupted by user", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@click.command()
@click.argument('input_file', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('output_file', type=click.Path(file_okay=True, dir_okay=False))
@click.option(
    '--width', '-w',
    default=670,
    help='Target width for output image',
    type=int
)
@click.option(
    '--height', '-h',
    default=366,
    help='Target height for output image',
    type=int
)
@click.option(
    '--bracket-offset',
    default=2,
    help='Pixels to crop inside brackets to exclude black lines',
    type=int
)
@click.option(
    '--quiet', '-q',
    is_flag=True,
    help='Suppress output messages'
)
def process_single(input_file: str, output_file: str, width: int, height: int, bracket_offset: int, quiet: bool):
    """
    Process a single Grid interface screenshot.
    
    INPUT_FILE: Path to the input PNG image
    OUTPUT_FILE: Path for the processed output image
    
    Example:
        grid-process-single screenshot.png processed.png
    """
    target_size = (width, height)
    processor = GridImageProcessor(target_size=target_size, bracket_offset=bracket_offset)
    
    try:
        success = processor.process_image(
            input_path=input_file,
            output_path=output_file,
            verbose=not quiet
        )
        
        if success:
            if not quiet:
                click.echo(f"✓ Successfully processed {input_file}")
        else:
            click.echo(f"✗ Failed to process {input_file}", err=True)
            sys.exit(1)
            
    except KeyboardInterrupt:
        click.echo("\nProcessing interrupted by user", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


# Add the single file processor as a separate command
@click.group()
def cli():
    """Grid Image Processor CLI Tools"""
    pass


cli.add_command(main, name='batch')
cli.add_command(process_single, name='single')


if __name__ == '__main__':
    main()
