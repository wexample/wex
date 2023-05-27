#!/usr/bin/env python3
"""Main entry point for the application."""

from src.core.Kernel import Kernel
import sys

if __name__ == '__main__':
    Kernel(
        __file__,
        sys.argv[1]
    ).call()
