#!/usr/bin/env bash

# Load parent entry point.
bash /docker-entrypoint-ubuntu17.sh

service apache2 restart

/bin/bash
