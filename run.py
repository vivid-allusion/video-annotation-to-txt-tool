#!/usr/bin/env python3
"""Wrapper script to activate venv and run main entry point.

This script checks for a virtual environment and runs the extraction tool.
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Activate venv if needed and run src.main."""
    venv_python = Path(__file__).parent / "venv" / "bin" / "python"

    if venv_python.exists():
        # Run with venv python
        result = subprocess.run(
            [str(venv_python), "-m", "src.main"], cwd=Path(__file__).parent
        )
        sys.exit(result.returncode)
    else:
        # Run with system python
        result = subprocess.run(
            [sys.executable, "-m", "src.main"], cwd=Path(__file__).parent
        )
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()
