#!/usr/bin/env bash

gitTagRemoveAll() {
  git tag | xargs git tag -d
}