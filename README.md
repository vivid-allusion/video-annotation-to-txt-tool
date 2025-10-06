# Video Annotation to Text Extraction Tool

A minimalist Python tool that extracts fenced code blocks from markdown files and saves them as individual text files. Built for processing video annotation prompt reviews.

## Overview

This tool processes markdown files containing video prompts wrapped in fenced code blocks (` ``` `), extracting each block into sequentially numbered text files for further processing or analysis.

## Features

- **Simple Extraction**: Extracts all fenced code blocks from the first markdown file (alphabetically)
- **Sequential Naming**: Creates `video_prompt_1.txt`, `video_prompt_2.txt`, etc. (unpadded counters)
- **Exact Preservation**: Maintains exact content including whitespace and line endings
- **Timestamped Output**: Generates output directories in `YYMMDD_HHMMSS` format
- **Fail-Fast Design**: Stops immediately with clear error messages on any issue
- **UTF-8 Only**: Exclusive UTF-8 encoding, no auto-detection or fallback
- **Malformed Detection**: Validates code blocks for unclosed fences and markdown syntax leakage

## Installation

```bash
# Navigate to project directory
cd video_annotation_to_txt_tool

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

1. **Place markdown file** in the input directory:
   ```bash
   cp your_file.md USER-FILES/04.INPUT/
   ```

2. **Run the extraction tool**:
   ```bash
   python run.py
   # Alternative: python3 -m src.main
   ```

3. **Review the output** in `USER-FILES/05.OUTPUT/{timestamp}/`:
   - `video_prompt_1.txt`, `video_prompt_2.txt`, ... (extracted code blocks)
   - `extraction_summary.md` (summary log with source file and block count)

## Project Structure

```
video_annotation_to_txt_tool/
├── src/                        # Source code modules
│   ├── exceptions.py          # Custom exception hierarchy (exit codes 1-9)
│   ├── logger.py              # Loguru logging configuration
│   ├── markdown_parser.py     # Regex-based code block extraction
│   ├── validator.py           # File validation and discovery
│   ├── file_handler.py        # Output file writing
│   └── main.py                # Main workflow orchestration
├── USER-FILES/
│   ├── 04.INPUT/              # Place .md files here (read-only)
│   └── 05.OUTPUT/             # Timestamped extraction results
├── run.py                      # Wrapper script for venv activation
└── requirements.txt            # Dependencies (mistune, loguru, natsort)
```

## Requirements

- Python 3.8+
- Dependencies:
  - `mistune==3.0.2` - Markdown parsing support
  - `loguru==0.7.2` - Structured logging
  - `natsort==8.4.0` - Natural file sorting

## Design Philosophy

This tool follows strict minimalist principles:
- **Single purpose**: Extract code blocks from markdown
- **Fail fast**: Stop immediately on errors with clear messages
- **No modification**: Input files never moved or modified
- **No configuration**: All behavior hardcoded for simplicity
- **UTF-8 exclusive**: No encoding auto-detection
- **Regex parsing**: Simple pattern matching over complex AST parsing
- **Unpadded counters**: Natural numbering (1, 2, 3) not zero-padded (001, 002, 003)

## Exit Codes

The tool uses specific exit codes for different error conditions:

- **0**: Success - all code blocks extracted
- **1**: No markdown files found in INPUT directory
- **2**: File read error (permissions, missing file)
- **3**: Empty file error
- **4**: No code blocks found in markdown
- **5**: Parse error (malformed code blocks detected)
- **6**: Empty code block found
- **7**: Nested code blocks (unsupported)
- **8**: UTF-8 encoding error
- **9**: Write error (output directory issues)

## Example Output

```
2025-10-05 16:09:10 | INFO | Discovering markdown file...
2025-10-05 16:09:10 | INFO | Found: Video_Prompt_Review_251005_071715.md
2025-10-05 16:09:10 | INFO | Found 46 fenced code blocks
2025-10-05 16:09:10 | INFO | Creating output directory...
2025-10-05 16:09:10 | INFO | Output: USER-FILES/05.OUTPUT/251005_160910
2025-10-05 16:09:10 | INFO | Extracting code blocks...
2025-10-05 16:09:10 | SUCCESS | Extracted code blocks successfully: 46
2025-10-05 16:09:10 | INFO | Summary: USER-FILES/05.OUTPUT/251005_160910/extraction_summary.md
```

## Behavior Details

### Input Processing
- Processes **only the first** markdown file alphabetically in `USER-FILES/04.INPUT/`
- Input files remain in `04.INPUT/` permanently (never moved or modified)
- Natural sorting ensures consistent file selection

### Code Block Extraction
- Detects fenced code blocks using regex pattern: ` ^```[^\n]*\n(.*?)^``` `
- Strips trailing newlines while preserving internal content exactly
- Detects malformed blocks (unclosed fences) via markdown syntax pattern matching
- Fails fast if markdown structure (HTML comments, headers, tables) appears in extracted content

### Output Generation
- Creates timestamped directory: `USER-FILES/05.OUTPUT/YYMMDD_HHMMSS/`
- Writes files: `video_prompt_1.txt`, `video_prompt_2.txt`, ... (unpadded)
- Generates summary: `extraction_summary.md` with source file and block count

## Error Handling

The tool will exit immediately if:
- No `.md` files exist in `USER-FILES/04.INPUT/`
- Markdown file is empty or unreadable
- No fenced code blocks found
- Code blocks contain markdown syntax (indicates unclosed fence)
- Any code block is empty or contains only whitespace
- Nested code blocks detected (` ``` ` inside ` ``` `)
- File is not UTF-8 encoded
- Output directory cannot be created

## Troubleshooting

### No markdown files found (Exit Code 1)
**Issue**: `USER-FILES/04.INPUT/` is empty or contains no `.md` files

**Solution**: Place at least one markdown file in the input directory

### Malformed code block detected (Exit Code 5)
**Issue**: Code block missing closing ` ``` ` fence

**Solution**: Check source markdown file - ensure all opening ` ``` ` have matching closing ` ``` `

### UTF-8 encoding error (Exit Code 8)
**Issue**: Markdown file not UTF-8 encoded

**Solution**: Convert file to UTF-8 encoding before processing

## Code Quality

- **Total lines**: 627 lines across 7 files
- **File size**: All files < 400 lines (max: 153 lines)
- **Function size**: All functions < 50 lines (max: 46 lines)
- **Type hints**: All function signatures typed
- **Docstrings**: All public functions documented
- **Formatting**: Black formatted
- **Linting**: Ruff compliant
- **Testing**: Manual testing verified (exit codes 0-9)

## Limitations

- Processes only the first markdown file (alphabetically)
- UTF-8 encoding only - no auto-detection or fallback
- No support for nested code blocks
- No configuration file (all behavior hardcoded)
- No automatic cleanup or archiving of input files

## License

Personal tool - no license required.

## Author

Developed as a personal tool for video annotation processing.
