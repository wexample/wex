#!/usr/bin/env python3
"""Main entry point for the demon."""

from src.core.WebhookHttpServer import WebhookHttpServer
from src.core.WebhookHandler import WebhookHandler
import sys
import os

if __name__ == "__main__":
    entrypoint_path = os.path.dirname(__file__)

    if len(sys.argv) > 1 and sys.argv[1].startswith("http://"):
        WebhookHandler(entrypoint_path).parse_url_and_execute(sys.argv[1])
    else:
        WebhookHttpServer(entrypoint_path, 4242)
