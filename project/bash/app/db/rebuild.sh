#!/usr/bin/env bash

dbRebuildArgs() {
  _DESCRIPTION="Recreate a fresh database instance, and feed it with base fixtures if available"
}

dbRebuild() {
  wex hook/exec -c=dbRebuild
}