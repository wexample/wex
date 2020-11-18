#!/usr/bin/env bash

# Gives the cumulative disk usage of all non-hidden directories.
dirSpace() {

  du -sh -- * | sort -h
}
