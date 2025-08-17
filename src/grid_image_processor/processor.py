"""
Grid Image Processor Core Module

Contains the main image processing logic for cropping Grid interface screenshots
to bracket intersections and resizing to standard dimensions.
"""

from PIL import Image
import os
from typing import Tuple, Optional


class GridImageProcessor:
    """Main processor class for Grid interface screenshots."""

    def __init__(self, target_size: Tuple[int, int] = (670, 366), bracket_offset: int = 2):
        """
        Initialize the processor.

        Args:
            target_size: Target dimensions for output images (width, height)
            bracket_offset: Pixels to crop inside brackets to exclude black lines
        """
        self.target_size = target_size
        self.bracket_offset = bracket_offset

    def find_bracket_intersections(self, img: Image.Image) -> Tuple[int, int, int, int]:
        """Find the bracket intersection corners for precise cropping."""
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        width, height = img.size

        # Find bracket corners by looking for black pixels (brackets)
        # and determining the rectangular frame they create
        top_left = None
        for y in range(min(50, height)):
            for x in range(min(50, width)):
                r, g, b, a = img.getpixel((x, y))
                if r == 0 and g == 0 and b == 0:
                    top_left = (x, y)
                    break
            if top_left:
                break

        bottom_right = None
        for y in range(height-1, max(height-50, 0), -1):
            for x in range(width-1, max(width-50, 0), -1):
                r, g, b, a = img.getpixel((x, y))
                if r == 0 and g == 0 and b == 0:
                    bottom_right = (x, y)
                    break
            if bottom_right:
                break

        top_right = None
        for y in range(min(50, height)):
            for x in range(width-1, max(width-50, 0), -1):
                r, g, b, a = img.getpixel((x, y))
                if r == 0 and g == 0 and b == 0:
                    top_right = (x, y)
                    break
            if top_right:
                break

        bottom_left = None
        for y in range(height-1, max(height-50, 0), -1):
            for x in range(min(50, width)):
                r, g, b, a = img.getpixel((x, y))
                if r == 0 and g == 0 and b == 0:
                    bottom_left = (x, y)
                    break
            if bottom_left:
                break
        
        if top_left and bottom_right:
            offset = self.bracket_offset
            left = top_left[0] + offset
            top = top_left[1] + offset
            right = bottom_right[0] - offset
            bottom = bottom_right[1] - offset

            if top_right:
                right = max(right, top_right[0] - offset)
                top = min(top, top_right[1] + offset)
            if bottom_left:
                left = min(left, bottom_left[0] + offset)
                bottom = max(bottom, bottom_left[1] - offset)

            if right > left and bottom > top:
                return (left, top, right, bottom)
            else:
                print(f"  Warning: Bracket offset too large, using fallback method")
                return self._find_content_bounds_fallback(img)

        return self._find_content_bounds_fallback(img)
    
    def _find_content_bounds_fallback(self, img: Image.Image) -> Tuple[int, int, int, int]:
        """Fallback method: Find the bounding box of non-white content."""
        width, height = img.size
        left, top, right, bottom = width, height, 0, 0

        for y in range(height):
            for x in range(width):
                r, g, b, a = img.getpixel((x, y))
                if not (r > 250 and g > 250 and b > 250):
                    left = min(left, x)
                    right = max(right, x)
                    top = min(top, y)
                    bottom = max(bottom, y)
        
        return (left, top, right, bottom)
    
    def process_image(self, input_path: str, output_path: str, verbose: bool = True) -> bool:
        """
        Process a single image: crop to bracket intersections and resize.
        
        Args:
            input_path: Path to input image
            output_path: Path for output image
            verbose: Whether to print processing information
            
        Returns:
            True if successful, False otherwise
        """
        try:
            img = Image.open(input_path)
            if verbose:
                print(f"Processing {os.path.basename(input_path)} ({img.size})")

            bounds = self.find_bracket_intersections(img)
            left, top, right, bottom = bounds

            cropped = img.crop((left, top, right + 1, bottom + 1))
            if verbose:
                print(f"  Cropped to: {cropped.size}")

            resized = cropped.resize(self.target_size, Image.Resampling.LANCZOS)
            if verbose:
                print(f"  Resized to: {resized.size}")

            if resized.mode == 'RGBA':
                background = Image.new('RGB', resized.size, (255, 255, 255))
                background.paste(resized, mask=resized.split()[-1])
                resized = background

            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            resized.save(output_path, 'PNG', optimize=True)
            if verbose:
                print(f"  Saved: {output_path}")
            return True

        except Exception as e:
            if verbose:
                print(f"Error processing {input_path}: {e}")
            return False

    def batch_process(self, input_dir: str, output_dir: str, verbose: bool = True) -> Tuple[int, int]:
        """
        Batch process all PNG images in the input directory.

        Args:
            input_dir: Directory containing input images
            output_dir: Directory for output images
            verbose: Whether to print processing information

        Returns:
            Tuple of (successful_count, failed_count)
        """
        os.makedirs(output_dir, exist_ok=True)

        png_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.png')]

        if not png_files:
            if verbose:
                print(f"No PNG files found in {input_dir}")
            return (0, 0)

        if verbose:
            print(f"Found {len(png_files)} PNG files to process")
            print(f"Target size: {self.target_size[0]}x{self.target_size[1]}")
            print("=" * 50)

        successful = 0
        failed = 0

        for png_file in png_files:
            input_path = os.path.join(input_dir, png_file)
            output_path = os.path.join(output_dir, png_file)

            if self.process_image(input_path, output_path, verbose):
                successful += 1
            else:
                failed += 1

            if verbose:
                print()

        if verbose:
            print("=" * 50)
            print(f"Processing complete!")
            print(f"Successful: {successful}")
            print(f"Failed: {failed}")
            print(f"Processed images saved to: {output_dir}")

        return (successful, failed)
