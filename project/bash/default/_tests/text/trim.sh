#!/usr/bin/env bash

textTrimTest() {
  local text=$(wex text/trim -t="    YAY!!    ")
  wexTestAssertEqual ${text} "YAY!!"
}
