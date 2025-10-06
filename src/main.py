"""Main entry point for video annotation text extraction tool.

Extracts fenced code blocks from markdown files and saves as numbered text files.
"""

import sys
from pathlib import Path

from .exceptions import ExtractionError
from .logger import log_error, log_success, log_info
from .validator import validate_and_extract
from .file_handler import (
    create_timestamped_dir,
    write_extracted_files,
    write_summary_log,
)

# Constants
INPUT_DIR = Path("USER-FILES/04.INPUT")
OUTPUT_DIR = Path("USER-FILES/05.OUTPUT")


def main() -> int:
    """Main extraction workflow.

    Returns:
        Exit code (0 for success, 1-9 for various errors)
    """
    try:
        # Step 1: Discover and validate markdown file
        log_info("Discovering markdown file...")
        md_file, code_blocks = validate_and_extract(INPUT_DIR)
        log_info(f"Found: {md_file.name}")

        # Step 2: Validate code blocks found
        log_info(f"Found {len(code_blocks)} fenced code blocks")

        # Step 3: Create timestamped output directory
        log_info("Creating output directory...")
        output_dir = create_timestamped_dir(OUTPUT_DIR)
        log_info(f"Output: {output_dir}")

        # Step 4: Write extracted files
        log_info("Extracting code blocks...")
        write_extracted_files(code_blocks, output_dir)

        # Step 5: Write summary log
        write_summary_log(md_file, code_blocks, output_dir)

        # Step 6: Success
        log_success("Extracted code blocks successfully", len(code_blocks))
        log_info(f"Summary: {output_dir / 'extraction_summary.md'}")

        return 0

    except ExtractionError as e:
        log_error(e)
        return e.exit_code

    except Exception as e:
        # Unexpected error
        log_info(f"Unexpected error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
