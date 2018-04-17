#!/usr/bin/env bash

gitCurrentTag() {
  git describe --abbrev=0 --tags
}
