"""File output handling and summary generation.

Creates timestamped output directories and writes extracted text files.
Generates extraction summary logs.
"""

from pathlib import Path
from datetime import datetime

from .exceptions import WriteError


def create_timestamped_dir(base_dir: Path) -> Path:
    """Create timestamped output directory with _VIDEO-PROMPT suffix.

    Args:
        base_dir: Base output directory

    Returns:
        Path to created timestamped directory

    Raises:
        WriteError: If directory creation fails
    """
    # Format: YYMMDD_HHMMSS_VIDEO-PROMPT
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    output_dir = base_dir / f"{timestamp}_VIDEO-PROMPT"

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir
    except Exception as e:
        raise WriteError(
            f"Cannot create output directory: {output_dir}\nError: {str(e)}\n"
            f"Resolution: Check write permissions for USER-FILES/05.OUTPUT/"
        ) from e


def write_text_file(content: str, output_path: Path) -> None:
    """Write content to text file with UTF-8 encoding.

    Args:
        content: Text content to write
        output_path: Path to output file

    Raises:
        WriteError: If file write fails
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        raise WriteError(
            f"Cannot write file: {output_path}\nError: {str(e)}\n"
            f"Resolution: Check write permissions and disk space"
        ) from e


def write_extracted_files(blocks: list[tuple[str, str]], output_dir: Path) -> list[Path]:
    """Write code blocks to text files using filenames from markdown.

    Args:
        blocks: List of (filename, content) tuples
        output_dir: Directory to write files to

    Returns:
        List of created file paths

    Raises:
        WriteError: If any file write fails
    """
    created_files = []

    for filename, content in blocks:
        output_path = output_dir / filename
        write_text_file(content, output_path)
        created_files.append(output_path)

    return created_files


def generate_summary_content(md_file: Path, blocks: list[tuple[str, str]], output_dir: Path) -> str:
    """Generate markdown summary content.

    Args:
        md_file: Source markdown file
        blocks: List of (filename, content) tuples
        output_dir: Output directory path

    Returns:
        Formatted markdown summary
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dir_name = output_dir.name

    summary = f"""# Extraction Summary

**Processed File:** {md_file.name}
**Extraction Time:** {timestamp}
**Output Directory:** 05.OUTPUT/{dir_name}/

## Results

- **Total Code Blocks Found:** {len(blocks)}
- **Files Created:** {len(blocks)}
- **Status:** SUCCESS

## File List

"""

    # Add numbered list of created files with their actual filenames
    for i, (filename, _) in enumerate(blocks, start=1):
        summary += f"{i}. {filename}\n"

    summary += "\n---\nExtraction completed successfully.\n"

    return summary


def write_summary_log(md_file: Path, blocks: list[tuple[str, str]], output_dir: Path) -> None:
    """Write extraction summary to markdown file.

    Args:
        md_file: Source markdown file
        blocks: List of (filename, content) tuples
        output_dir: Output directory path

    Raises:
        WriteError: If summary write fails
    """
    summary_content = generate_summary_content(md_file, blocks, output_dir)
    summary_path = output_dir / "extraction_summary.md"
    write_text_file(summary_content, summary_path)
