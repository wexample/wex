#!/usr/bin/env bash

. /opt/wex/.wex/.env

if [ "${APP_ENV}" == "local" ]; then
  COLOR="\033[0;32m"
elif [ "${APP_ENV}" == "dev" ]; then
  COLOR="\033[0;33m"
else
  COLOR="\033[0;31m"
fi

PS1="\[${COLOR}\][${APP_ENV^^}]\[\033[0m\] \\u:\\W\\$ "

# The given file for completion is cached,
# so we use a different file to be able
# to live edit it during script creation.
_wexAutocomplete() {
  . /opt/wex/bash/autocomplete.sh
}

complete -o nospace -F _wexAutocomplete wex