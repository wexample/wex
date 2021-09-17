#!/usr/bin/env bash
# Return "true" if wex script are properly installed.

# Test if wex hi command runs.
[ $(wex hi | xargs) = "hi!" ] && echo "true" || echo "false"
