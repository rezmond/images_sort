# images_sort

Sort images by year and season.

## Project Overview

The `images_sort` project is a Python-based image and media file sorting application that organizes files by year and season. It scans source directories for media files (images and videos), extracts date information from file metadata or filenames, and moves them to a destination directory organized by year and season. The main goal of this application is to simplify the organization of large collections of images and videos, making them easier to manage and access, especially to help to elliminate duplicates of files even after multiple moves.

The application has to work as fast as possible. To achive this we have to use any needed alhorythm to improve the app's performance. To make it more efficient, we need to implement an algorithm that can handle large datasets efficiently.


## Architecture

The application follows an MVC (Model-View-Controller) architectural pattern with:
- **Model**: Handles business logic and data operations using dependency injection
- **View**: Console-based output for user interaction and progress reporting. It also planned to support graphical user interface (GUI, Tkinter) in future versions.
- **Controller**: Coordinates between the model and view

## Key Features

- Scans source directories for media files (images and videos)
- Extracts date information from file metadata (EXIF for images, or filename patterns) only for service usage
- Handles scenarios where EXIF data is missing by parsing filename patterns
- Moves files to destination organized by year and season
- Provides detailed progress reporting during scan and move operations
- Supports various image formats and video formats
- Command-line interface with various options for different operations. And it's planned to support GUI mode using Tkinter.

## Implementation Details

### Core Components

1. **Scanner**: Identifies media files in a directory and determines their date information
2. **Date Extractor**: Extracts datetime information from file metadata (EXIF for images, or filename patterns)
3. **Mover**: Handles the actual moving/copying of files to destination paths
4. **MoveMap**: Determines destination paths based on extracted dates (organizes by year and season, or custom criteria in future versions)
5. **Presenters**: Format media information for different file types

### Architecture

- Uses `dependency-injector` for managing dependencies
- Implements an `Either` monad pattern for handling operations that can fail
- Follows a layered architecture with clear separation of concerns
- Utilizes type checking with `typeguard`
- Supports EXIF data extraction for images using `exifread`
- Uses `click` for command-line argument parsing

## Building and Running

To run the application:
```bash
python3 start <src> <dst>
```

Where:
- `<src>` is the source directory path
- `<dst>` is the destination directory path

### Command Options
* `-s, --scan`: Start the scan process only
* `-r, --report`: Create a report after moving files (requires -m parameter)
* `-m, --move`: Scan and then move files
* `-v, --verbose`: Set verbosity level (higher number = more detail)

Run tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov="./src" --cov-report=html
```

## Directory Structure

```
/app
├── start.py                    # Entry point
├── containers.py               # Dependency injection configuration
├── src/
│   ├── core/
│   │   ├── scanner/            # File scanning and date extraction logic
│   │   ├── mover/              # File moving logic
│   │   ├── date_extractor/     # Date extraction logic
│   │   └── fs/                 # File system operations
│   ├── mvc/
│   │   ├── controllers/        # Controller implementations
│   │   ├── model/              # Model logic
│   │   └── views/              # View logic
│   ├── system_interfaces/      # File system operations interface
│   ├── use_cases/              # Business logic for presenters and map
│   └── utils/                  # Utility functions
├── tests/                      # Test files
├── requirements.txt            # Project dependencies
└── README.md
```

## Dependencies

The project uses the following key dependencies:
- `exifread==2.1.2` - For EXIF data processing in images
- `pytest==6.2.5` - Testing framework
- `pytest-cov==2.10.1` - Code coverage reporting
- `typeguard==2.2.2` - Type checking
- `python-dateutil==2.8.1` - Date parsing
- `dependency-injector==4.41.0` - Dependency injection
- `click==8.0.0` - Command-line interface
- `PyMonad==2.4.0` - Functional programming tools

## Usage Pattern

The application processes files in a three-step approach:
1. Scan the source folder for media files
2. Determine destination paths using date information
3. Move files to their appropriate destination folders organized by year and season

## Supported File Formats

- Images: JPEG, PNG (with EXIF date parsing)
- Video files (parsed via filename patterns)

## Date Extraction Logic

The application extracts dates in the following priority order:
1. EXIF data for images (using exifread library)
2. Filename patterns for images, such as:
   - "20200429_*.jpg"
   - "IMG-20220316-WA0000"
   - "PXL_20220910_153412777.MP.jpg"

## Season Mapping

Images are organized by seasons (based on month):
- Winter (begin): January, February
- Spring: March, April, May
- Summer: June, July, August
- Autumn: September, October, November
- Winter (end): December

## Testing

The project uses pytest for testing and includes comprehensive test coverage for all major components. Tests are organized in the `tests/` directory following the same structure as `src/`.
