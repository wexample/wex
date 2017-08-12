#!/usr/bin/env bash

textDiff() {
  diff <(echo "${1}") <(echo "${2}")
}
