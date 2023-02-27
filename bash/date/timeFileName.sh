#!/usr/bin/env bash

dateTimeFileNameArgs() {
  _DESCRIPTION="Create a time string for file names like backups"
}

dateTimeFileName() {
  # Return date time without ":" char.
  date +%Y-%m-%dT%H-%M-%S
}
