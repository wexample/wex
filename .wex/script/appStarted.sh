#!/usr/bin/env bash

_wexLog "Running custom app scripts"

wex app::app/exec -c="cd /var/www/html && pip install -r requirements.txt"
wex app::app/exec -c="bash /var/www/html/install"

