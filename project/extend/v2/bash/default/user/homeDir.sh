#!/usr/bin/env bash

userHomeDir() {
  case "$(wex system/os)" in
    "linux")
      echo /home/
      ;;
    "windows")
      echo C:\Users\
      ;;
  esac
}