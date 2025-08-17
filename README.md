# Grid Station Image Processor

A CLI tool for batch processing Monome Grid interface screenshots from [Grid Station](https://tyleretters.github.io/GridStation/). This tool automatically detects bracket intersections in images, crops to exclude the black bracket lines, and resizes to standardized dimensions.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone or download this repository
2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - **Windows**

      ```
      .venv\Scripts\activate
      pip install -e .
      ```

   - **macOS/Linux**

      ```
      source .venv/bin/activate
      pip install -e .
      ```

## CLI Options

- `-i, --input-dir`: Input directory containing PNG images (default: `images`)
- `-o, --output-dir`: Output directory for processed images (default: `images/processed`)
- `-w, --width`: Target width for output images (default: `670`)
- `-h, --height`: Target height for output images (default: `366`)
- `--bracket-offset`: Pixels to crop inside brackets (default: `2`)
- `-q, --quiet`: Suppress output messages
- `--version`: Show version information
- `--help`: Show help message

## Usage

Process all PNG images in the `images` directory:

```bash
grid-process -i input_folder -o output_folder --width 670 --height 366
```

## How It Works

1. **Bracket Detection**: Scans images for black pixels that form the Grid interface brackets
2. **Corner Finding**: Identifies the intersection points where brackets meet
3. **Smart Cropping**: Crops inside the brackets with configurable offset to exclude black lines
4. **Standardization**: Resizes all images to consistent dimensions
5. **Optimization**: Saves as optimized PNG files

## License

MIT License - Feel free to use and modify as needed.
