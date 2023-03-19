#!/usr/bin/env bash

_wexLog "Running custom app scripts"

wex app::app/exec -c="bash /var/www/html/cli/install"

