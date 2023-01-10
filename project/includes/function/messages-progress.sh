#!/usr/bin/env bash

_wexLog() {
  wex prompt/progress -p="${WEX_PROGRESS_CURRENT_PERCENTAGE}" -s="${1}" -nl
}

_wexMessage() {
  wex prompt/progress -p="${WEX_PROGRESS_CURRENT_PERCENTAGE}" -s="${1}" -nl
}
