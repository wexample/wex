#!/usr/bin/env python3
"""Main entry point for the application."""

if __name__ == "__main__":
    from src.common.wex import Wex

    Wex(entrypoint_path=__file__).exec()
