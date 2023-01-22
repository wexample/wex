#!/usr/bin/env bash

_wexMessage() {
  wex prompt/progress -p="${WEX_PROGRESS_CURRENT_PERCENTAGE}" -s="${1}" -nl
}
