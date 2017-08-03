#!/usr/bin/env bash

fileTextAppend() {
  sed -i "\$a${1}" ${2}
}
