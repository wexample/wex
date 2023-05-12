#!/usr/bin/env python3
"""Main entry point for the daemon."""

from src.core.WebhookHttpServer import WebhookHttpServer
from src.core.WebhookHandler import WebhookHandler
import sys
import os
import unittest

if __name__ == "__main__":
    entrypoint_path = os.path.dirname(__file__)

    if len(sys.argv) > 1:
        # Run command line parsing.
        if sys.argv[1].startswith('http://'):
            WebhookHandler(entrypoint_path).parse_url_and_execute(sys.argv[1])

        # Search for unit tests.
        elif sys.argv[1] == 'test':
            test_loader = unittest.TestLoader()
            test_suite = test_loader.discover(
                os.path.join(entrypoint_path, 'tests'),
                pattern='*TestCase.py',
            )

            unittest.TextTestRunner().run(test_suite)
    else:
        # Run daemon server.
        WebhookHttpServer(entrypoint_path, 4242)
