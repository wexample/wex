#!/usr/bin/env python3
"""Main entry point for the application."""

from src.core.Kernel import Kernel

if __name__ == '__main__':
    Kernel(
        entrypoint_path=__file__,
    ).call()
