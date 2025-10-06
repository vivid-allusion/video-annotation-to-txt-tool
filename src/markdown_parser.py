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


def extract_code_blocks(markdown_content: str) -> list[str]:
    """Extract fenced code blocks from markdown using regex.

    Args:
        markdown_content: Markdown text to parse

    Returns:
        List of code block contents

    Raises:
        ParseError: If markdown parsing fails
    """
    try:
        # Regex pattern for fenced code blocks (with or without language)
        # Matches: ```lang\ncontent\n``` or ```\ncontent\n```
        pattern = r"^```[^\n]*\n(.*?)^```"
        matches = re.findall(pattern, markdown_content, re.MULTILINE | re.DOTALL)
        # Strip trailing newline from each match (preserve internal newlines)
        return [m.rstrip("\n") for m in matches]
    except Exception as e:
        raise ParseError(f"Markdown parsing failed: {str(e)}") from e


def detect_empty_blocks(blocks: list[str]) -> None:
    """Check for empty or whitespace-only code blocks.

    Args:
        blocks: List of code block contents

    Raises:
        EmptyCodeBlockError: If any block is empty or whitespace
    """
    for i, block in enumerate(blocks, 1):
        if not block.strip():
            raise EmptyCodeBlockError(
                f"Empty code block found at position {i}\n"
                f"Resolution: Remove empty code block or add content"
            )


def detect_nested_blocks(blocks: list[str]) -> None:
    """Check for nested code block patterns (unsupported).

    Args:
        blocks: List of code block contents

    Raises:
        NestedCodeBlockError: If nested blocks detected
    """
    for i, block in enumerate(blocks, 1):
        if "```" in block:
            raise NestedCodeBlockError(
                f"Nested code block detected at position {i}\n"
                f"Resolution: Remove nested code blocks (unsupported pattern)"
            )


def detect_malformed_blocks(blocks: list[str]) -> None:
    """Check for malformed code blocks with markdown structure inside.

    Detects blocks that contain markdown syntax indicating an unclosed
    code block that captured content beyond its intended boundary.

    Args:
        blocks: List of code block contents

    Raises:
        ParseError: If malformed blocks detected
    """
    for i, block in enumerate(blocks, 1):
        # Check for markdown structure that shouldn't be in code blocks
        suspicious_patterns = [
            "<!---",  # HTML comments
            "## ",  # Markdown headers
            "| ---",  # Table separators
            "**line_",  # The specific bold pattern from this file
        ]

        for pattern in suspicious_patterns:
            if pattern in block:
                raise ParseError(
                    f"Malformed code block at position {i}\n"
                    f"Block contains markdown syntax: '{pattern}'\n"
                    f"This indicates an unclosed code block in the source file\n"
                    f"Resolution: Check that all ``` opening fences have matching closing ``` fences"
                )


def parse_and_extract(file_path: Path) -> list[str]:
    """Parse markdown and extract validated code blocks.

    Main orchestration function that runs all parsing steps.

    Args:
        file_path: Path to markdown file

    Returns:
        List of validated code block contents

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
