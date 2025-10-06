"""Custom exceptions for video annotation extraction tool.

Each exception has a specific exit code for clear error handling.
Exit codes 1-9 represent different failure scenarios.
"""


class ExtractionError(Exception):
    """Base exception for all extraction errors."""

    exit_code: int = 1

    def __init__(self, message: str):
        """Initialize exception with error message.

        Args:
            message: Error description
        """
        super().__init__(message)
        self.message = message


class NoMarkdownFilesError(ExtractionError):
    """Raised when no markdown files found in input directory."""

    exit_code = 1


class FileReadError(ExtractionError):
    """Raised when file cannot be read."""

    exit_code = 2


class EmptyFileError(ExtractionError):
    """Raised when markdown file is empty."""

    exit_code = 3


class NoCodeBlocksError(ExtractionError):
    """Raised when no fenced code blocks found in markdown."""

    exit_code = 4


class ParseError(ExtractionError):
    """Raised when markdown parsing fails."""

    exit_code = 5


class EmptyCodeBlockError(ExtractionError):
    """Raised when code block contains only whitespace."""

    exit_code = 6


class NestedCodeBlockError(ExtractionError):
    """Raised when nested code blocks detected (unsupported)."""

    exit_code = 7


class EncodingError(ExtractionError):
    """Raised when UTF-8 encoding/decoding fails."""

    exit_code = 8


class WriteError(ExtractionError):
    """Raised when output file cannot be written."""

    exit_code = 9
