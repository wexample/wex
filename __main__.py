#!/usr/bin/env python3
"""Main entry point for the application."""

from src.core.Kernel import Kernel
import sys

if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg is None:
        print('Please use the "bash ./cli/wex" file to run wex script.')
        sys.exit(1)

    Kernel(
        __file__,
        arg
    ).call()
