#!/usr/bin/env bash

gitGraph() {
  git log --graph --decorate --pretty=oneline --abbrev-commit --all
}