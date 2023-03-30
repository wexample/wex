#!/usr/bin/env bash

APP_NAME='wex'
VERSION='5.0.0~beta.3'
PATH_ROOT="$(realpath "$(dirname "$(dirname "${BASH_SOURCE[0]}")")")/"

echo "Build changelog"
python3 "${PATH_ROOT}scripts/1.build.py" -n "${APP_NAME}" -v "${VERSION}"
