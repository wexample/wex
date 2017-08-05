#!/usr/bin/env bash

fileTextRemoveLastLine() {
  sed -i '$ d' ${1}
}
