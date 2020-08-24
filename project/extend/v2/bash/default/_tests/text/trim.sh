#!/usr/bin/env bash

textTrimTest() {
  local text=$(wex string/trim -s="    YAY!!    ")
  wexTestAssertEqual ${text} "YAY!!"
}
