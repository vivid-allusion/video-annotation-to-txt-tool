# Video Annotation to Text Extraction Tool

A minimalist Python tool that extracts text blocks from markdown using a `**filename.txt:**` prefix convention and saves them as individual text files. Built for processing video annotation prompt reviews.

## Overview

This tool processes markdown files containing video prompts formatted with the `**filename.txt:** \`\`\` \`\`\`` pattern, extracting each block into a text file named after its markdown-specified filename.

## Features

- **Filename-Driven Extraction**: Output filenames come directly from `**name.txt:**` prefixes in the source markdown, not auto-numbered placeholders
- **Regex-Based Parsing**: Uses pattern `r"^\*\*([^\s\*]+\.txt):\*\*\s*$\s*^```[^\n]*$\s*^(.*?)^```"` targeting the `**name.txt:**` prefix convention
- **Exact Preservation**: Maintains exact content including whitespace and line endings
- **Timestamped Output**: Generates output directories in `YYMMDD_HHMMSS_VIDEO-PROMPT` format
- **Fail-Fast Design**: Stops immediately with clear error messages on any issue
- **UTF-8 Only**: Exclusive UTF-8 encoding, no auto-detection or fallback
- **Malformed Detection**: Validates code blocks for unclosed fences and markdown syntax leakage

## Expected Input Format

The source markdown must follow the `**filename.txt:**` convention:

```markdown
## Shot 1

**shot1_prompt.txt:**
```text
A person walking through a forest path, camera follows behind, dolly zoom effect
```

## Shot 2

**shot2_prompt.txt:**
```text
Establishing shot of a futuristic city skyline at sunset, flying cars, neon lights
```
```

Each code block must be preceded by a `**name.txt:**` line — this determines the output filename.

## Installation

```bash
# Navigate to project directory
cd video-annotation-to-txt-tool

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

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
   ```

3. **Review the output** in `USER-FILES/05.OUTPUT/{YYMMDD_HHMMSS_VIDEO-PROMPT}/`:
   - Files named after the `**name.txt:**` conventions in the source markdown
   - `extraction_summary.md` (summary log with source file and block count)

## Project Structure

```
video-annotation-to-txt-tool/
├── src/                        # Source code modules
│   ├── exceptions.py          # Custom exception hierarchy (exit codes 1-9)
│   ├── logger.py              # Loguru logging configuration
│   ├── markdown_parser.py     # Regex-based extraction with **name.txt:** pattern
│   ├── validator.py           # File validation and discovery
│   ├── file_handler.py        # Output file writing
│   └── main.py                # Main workflow orchestration
├── USER-FILES/
│   ├── 04.INPUT/              # Place .md files here (read-only)
│   └── 05.OUTPUT/             # Timestamped extraction results
├── run.py                      # Wrapper script for venv activation
└── requirements.txt            # Dependencies (loguru, natsort; mistune listed but unused)
```

## Requirements

- Python 3.8+
- Dependencies:
  - `loguru==0.7.2` — Structured logging
  - `natsort==8.4.0` — Natural file sorting
  - `mistune==3.0.2` — Listed in requirements.txt but no longer used by the tool

## Design Philosophy

This tool follows strict minimalist principles:
- **Single purpose**: Extract text blocks from markdown using the `**name.txt:**` convention
- **Fail fast**: Stop immediately on errors with clear messages
- **No modification**: Input files never moved or modified
- **No configuration**: All behavior hardcoded for simplicity
- **UTF-8 exclusive**: No encoding auto-detection
- **Regex parsing**: Simple pattern matching over complex AST parsing

## Exit Codes

The tool uses specific exit codes for different error conditions:

- **0**: Success — all text blocks extracted
- **1**: No markdown files found in INPUT directory
- **2**: File read error (permissions, missing file)
- **3**: Empty file error
- **4**: No matching `**name.txt:**` blocks found in markdown
- **5**: Parse error (malformed blocks detected)
- **6**: Empty code block found
- **7**: Nested code blocks (unsupported)
- **8**: UTF-8 encoding error
- **9**: Write error (output directory issues)

## Example Output

```
2025-10-05 16:09:10 | INFO | Discovering markdown file...
2025-10-05 16:09:10 | INFO | Found: Video_Prompt_Review_251005_071715.md
2025-10-05 16:09:10 | INFO | Found 46 matching blocks
2025-10-05 16:09:10 | INFO | Creating output directory...
2025-10-05 16:09:10 | INFO | Output: USER-FILES/05.OUTPUT/251005_160910_VIDEO-PROMPT
2025-10-05 16:09:10 | INFO | Extracting text blocks...
2025-10-05 16:09:10 | SUCCESS | Extracted text blocks successfully: 46
2025-10-05 16:09:10 | INFO | Summary: USER-FILES/05.OUTPUT/251005_160910_VIDEO-PROMPT/extraction_summary.md
```

Output text files are named per the `**filename.txt:**` conventions from the source markdown — e.g., `shot1_prompt.txt`, `shot2_prompt.txt`, etc.

## Behavior Details

### Input Processing
- Processes **only the first** markdown file alphabetically in `USER-FILES/04.INPUT/`
- Input files remain in `04.INPUT/` permanently (never moved or modified)
- Natural sorting ensures consistent file selection

### Text Block Extraction
- Detects blocks using regex pattern: `r"^\*\*([^\s\*]+\.txt):\*\*\s*$\s*^```[^\n]*$\s*^(.*?)^```"`
- Required format: `**filename.txt:**` on its own line, followed by a fenced code block
- Strips trailing newlines while preserving internal content exactly
- Detects malformed blocks (unclosed fences) via markdown syntax pattern matching
- Fails fast if markdown structure (HTML comments, headers, tables) appears in extracted content

### Output Generation
- Creates timestamped directory: `USER-FILES/05.OUTPUT/YYMMDD_HHMMSS_VIDEO-PROMPT/`
- Writes files using the filenames from the `**name.txt:**` patterns in the source markdown
- Generates summary: `extraction_summary.md` with source file and block list

## Error Handling

The tool will exit immediately if:
- No `.md` files exist in `USER-FILES/04.INPUT/`
- Markdown file is empty or unreadable
- No `**name.txt:**` pattern matches found
- Code blocks contain markdown syntax (indicates unclosed fence)
- Any code block is empty or contains only whitespace
- Nested code blocks detected
- File is not UTF-8 encoded
- Output directory cannot be created

## Troubleshooting

### No markdown files found (Exit Code 1)
**Issue**: `USER-FILES/04.INPUT/` is empty or contains no `.md` files

**Solution**: Place at least one markdown file in the input directory

### Malformed code block detected (Exit Code 5)
**Issue**: Code block missing closing ` ``` ` fence

**Solution**: Check source markdown file — ensure all `**name.txt:**` lines have matching fenced code blocks

### UTF-8 encoding error (Exit Code 8)
**Issue**: Markdown file not UTF-8 encoded

**Solution**: Convert file to UTF-8 encoding before processing

## Code Quality

- **Total lines**: 660 lines across 8 files
- **File size**: All files < 200 lines (max: 169 lines)
- **Function size**: All functions < 50 lines
- **Type hints**: All function signatures typed
- **Docstrings**: All public functions documented
- **Formatting**: Black formatted
- **Linting**: Ruff compliant

## Limitations

- Processes only the first markdown file (alphabetically)
- Requires `**filename.txt:**` prefix convention in source markdown
- UTF-8 encoding only — no auto-detection or fallback
- No support for nested code blocks
- No configuration file (all behavior hardcoded)
- No automatic cleanup or archiving of input files

## License

Personal tool — no license required.

## Author

Developed as a personal tool for video annotation processing.
