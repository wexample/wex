#!/usr/bin/env bash

userHomeDir() {
  case "$(wex system/osName)" in
    "linux")
      echo /home/
      ;;
    "windows")
      echo C:\Users\
      ;;
  esac
}