#!/usr/bin/env bash

textTrimTest() {
  local text=$(${WEX_DIR_V3_CMD} string/trim -s="    YAY!!    ")
  wexTestAssertEqual ${text} "YAY!!"
}
