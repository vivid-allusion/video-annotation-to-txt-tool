"""Markdown parsing and code block extraction.

Uses regex to extract fenced code blocks from markdown.
Validates blocks for empty content and nested patterns.
"""

from pathlib import Path
import re

from .exceptions import (
    EncodingError,
    ParseError,
    EmptyCodeBlockError,
    NestedCodeBlockError,
)


def parse_markdown(file_path: Path) -> str:
    """Read markdown file with UTF-8 encoding.

    Args:
        file_path: Path to markdown file

    Returns:
        Markdown content as string

    Raises:
        EncodingError: If UTF-8 decoding fails
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError as e:
        raise EncodingError(
            f"UTF-8 decoding failed for {file_path.name}: {str(e)}"
        ) from e


def extract_code_blocks(markdown_content: str) -> list[tuple[str, str]]:
    """Extract fenced code blocks with their filenames from markdown.

    Looks for patterns like:
    **filename.txt:**
    ```text
    content
    ```

    Args:
        markdown_content: Markdown text to parse

    Returns:
        List of tuples (filename, content)

    Raises:
        ParseError: If markdown parsing fails or filename not found
    """
    try:
        # Pattern to match: **filename.txt:** on its own line, followed by code block
        # [^\s\*]+ ensures we only match filename characters (not spaces or asterisks)
        # \.txt matches the .txt extension literally
        pattern = r"^\*\*([^\s\*]+\.txt):\*\*\s*$\s*^```[^\n]*$\s*^(.*?)^```"
        matches = re.findall(pattern, markdown_content, re.MULTILINE | re.DOTALL)
        
        if not matches:
            raise ParseError(
                "No filename patterns found in markdown.\n"
                "Expected pattern: **filename.txt:**\\n```\\ncontent\\n```"
            )
        
        # Return list of (filename, content) tuples with trailing newlines stripped
        return [(filename, content.rstrip("\n")) for filename, content in matches]
    except ParseError:
        raise
    except Exception as e:
        raise ParseError(f"Markdown parsing failed: {str(e)}") from e


def detect_empty_blocks(blocks: list[tuple[str, str]]) -> None:
    """Check for empty or whitespace-only code blocks.

    Args:
        blocks: List of (filename, content) tuples

    Raises:
        EmptyCodeBlockError: If any block is empty or whitespace
    """
    for i, (filename, content) in enumerate(blocks, 1):
        if not content.strip():
            raise EmptyCodeBlockError(
                f"Empty code block found at position {i} ({filename})\n"
                f"Resolution: Remove empty code block or add content"
            )


def detect_nested_blocks(blocks: list[tuple[str, str]]) -> None:
    """Check for nested code block patterns (unsupported).

    Args:
        blocks: List of (filename, content) tuples

    Raises:
        NestedCodeBlockError: If nested blocks detected
    """
    for i, (filename, content) in enumerate(blocks, 1):
        if "```" in content:
            raise NestedCodeBlockError(
                f"Nested code block detected at position {i} ({filename})\n"
                f"Resolution: Remove nested code blocks (unsupported pattern)"
            )


def detect_malformed_blocks(blocks: list[tuple[str, str]]) -> None:
    """Check for malformed code blocks with markdown structure inside.

    Detects blocks that contain markdown syntax indicating an unclosed
    code block that captured content beyond its intended boundary.

    Args:
        blocks: List of (filename, content) tuples

    Raises:
        ParseError: If malformed blocks detected
    """
    for i, (filename, content) in enumerate(blocks, 1):
        # Check for markdown structure that shouldn't be in code blocks
        suspicious_patterns = [
            "<!---",  # HTML comments
            "## ",  # Markdown headers
            "| ---",  # Table separators
            "**line_",  # The specific bold pattern from this file
        ]

        for pattern in suspicious_patterns:
            if pattern in content:
                raise ParseError(
                    f"Malformed code block at position {i} ({filename})\n"
                    f"Block contains markdown syntax: '{pattern}'\n"
                    f"This indicates an unclosed code block in the source file\n"
                    f"Resolution: Check that all ``` opening fences have matching closing ``` fences"
                )


def parse_and_extract(file_path: Path) -> list[tuple[str, str]]:
    """Parse markdown and extract validated code blocks with filenames.

    Main orchestration function that runs all parsing steps.

    Args:
        file_path: Path to markdown file

    Returns:
        List of (filename, content) tuples

    Raises:
        EncodingError: If UTF-8 decoding fails
        ParseError: If markdown parsing fails
        EmptyCodeBlockError: If empty blocks found
        NestedCodeBlockError: If nested blocks detected
    """
    # Read and parse markdown
    content = parse_markdown(file_path)
    blocks = extract_code_blocks(content)

    # Validate blocks
    detect_empty_blocks(blocks)
    detect_nested_blocks(blocks)
    detect_malformed_blocks(blocks)

    return blocks
