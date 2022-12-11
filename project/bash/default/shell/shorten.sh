#!/usr/bin/env bash

shellShortenArgs() {
  _DESCRIPTION='Returns a command to execute manually to keep only the folder name instead of full absolute path in your shell prompt'
}

shellShorten() {
  # Unable te execute it from here
  echo PS1=\'\\u:\\W\\$ \'
}