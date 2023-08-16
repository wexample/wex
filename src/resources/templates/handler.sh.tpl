#!/bin/bash

# Source to handler if exists.
if [ -f "{handler_path}" ]; then
    . "{handler_path}"
fi
