#!/usr/bin/env bash

# The given file for completion is cached,
# so we use a different file to be able
# to live edit it during script creation.
_wex_autocomplete() {
  . /opt/wex/project/bash/autocomplete.sh
}

complete -o nospace -F _wex_autocomplete wex