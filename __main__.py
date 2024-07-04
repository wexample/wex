#!/usr/bin/env python3
"""Main entry point for the application."""

from wexample_wex_core.core.Kernel import Kernel

if __name__ == '__main__':
    Kernel(
        entrypoint_path=__file__,
    ).call()
