"""File validation and discovery logic.

Validates markdown files exist, are readable, non-empty, and contain code blocks.
Uses natsort for natural file ordering.
"""

from pathlib import Path
from natsort import natsorted

from .exceptions import (
    NoMarkdownFilesError,
    FileReadError,
    EmptyFileError,
    NoCodeBlocksError,
)
from .markdown_parser import parse_and_extract


def discover_first_markdown_file(input_dir: Path) -> Path:
    """Find first markdown file in input directory (natural sort).

    Args:
        input_dir: Directory to search for markdown files

    Returns:
        Path to first markdown file

    Raises:
        NoMarkdownFilesError: If no .md files found
    """
    md_files = list(input_dir.glob("*.md"))

    if not md_files:
        raise NoMarkdownFilesError(
            f"No markdown files found in {input_dir}\n"
            f"Resolution: Place at least one .md file in USER-FILES/04.INPUT/"
        )

    # Natural sort and return first
    sorted_files = natsorted(md_files)
    return sorted_files[0]


def validate_file_exists(file_path: Path) -> None:
    """Verify file exists.

    Args:
        file_path: Path to validate

    Raises:
        FileReadError: If file does not exist
    """
    if not file_path.exists():
        raise FileReadError(
            f"File does not exist: {file_path}\n"
            f"Resolution: Verify file path is correct"
        )


def validate_file_readable(file_path: Path) -> None:
    """Verify file has read permissions.

    Args:
        file_path: Path to validate

    Raises:
        FileReadError: If file cannot be read
    """
    if not file_path.is_file():
        raise FileReadError(
            f"Not a file: {file_path}\n" f"Resolution: Provide a valid file path"
        )

    try:
        with open(file_path, "r") as f:
            f.read(1)  # Try reading one character
    except PermissionError as e:
        raise FileReadError(
            f"Cannot read file (permission denied): {file_path}\n"
            f"Resolution: Check file permissions"
        ) from e
    except Exception as e:
        raise FileReadError(
            f"Cannot read file: {file_path}\nError: {str(e)}\n"
            f"Resolution: Verify file is accessible"
        ) from e


def validate_file_non_empty(file_path: Path) -> None:
    """Verify file is not empty.

    Args:
        file_path: Path to validate

    Raises:
        EmptyFileError: If file size is 0
    """
    if file_path.stat().st_size == 0:
        raise EmptyFileError(
            f"Markdown file is empty: {file_path.name}\n"
            f"Resolution: Add content to the file"
        )


def validate_has_code_blocks(blocks: list[tuple[str, str]]) -> None:
    """Verify at least one code block exists.

    Args:
        blocks: List of (filename, content) tuples

    Raises:
        NoCodeBlocksError: If no code blocks found
    """
    if len(blocks) == 0:
        raise NoCodeBlocksError(
            "No fenced code blocks found in markdown file\n"
            "Resolution: Verify file contains ``` fenced code blocks"
        )


def validate_and_extract(input_dir: Path) -> tuple[Path, list[tuple[str, str]]]:
    """Run all validations and extract code blocks with filenames.

    Main validation orchestration function.

    Args:
        input_dir: Input directory to process

    Returns:
        Tuple of (markdown file path, list of (filename, content) tuples)

    Raises:
        NoMarkdownFilesError: If no markdown files found
        FileReadError: If file cannot be read
        EmptyFileError: If file is empty
        NoCodeBlocksError: If no code blocks found
        Other extraction errors from markdown_parser
    """
    # Discover markdown file
    md_file = discover_first_markdown_file(input_dir)

    # Validate file
    validate_file_exists(md_file)
    validate_file_readable(md_file)
    validate_file_non_empty(md_file)

    # Parse and extract code blocks (also validates blocks)
    code_blocks = parse_and_extract(md_file)

    # Validate we have code blocks
    validate_has_code_blocks(code_blocks)

    return md_file, code_blocks
